"""
Maintainer Onboarding and Snippet Generation API Router (app/routers/maintainers.py).

Provides:
- POST /maintainers/claim (and aliases /api/repos/claim, /api/maintainers/claim):
  Claim repository ownership and register maintainer payout address.
- GET /maintainers/claim: Informational onboarding guidance.
- GET /maintainers/snippet/{owner}/{repo} (and alias /api/repos/{owner}/{repo}/snippet):
  Generate copy-pasteable badge snippets (Markdown, HTML, RST) linking to dynamic click redirect.
"""

from __future__ import annotations

import logging
import urllib.parse
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.repository import Repository
from app.schemas.repo import (
    ClaimAllRequest,
    ClaimRepoRequest,
    ClaimRepoResponse,
    RepoResponse,
    SnippetResponse,
    ToggleClaimRequest,
    UpdatePayoutRequest,
)
from app.services.github_service import get_or_fetch_repository
import httpx

logger = logging.getLogger("router_maintainers")

router = APIRouter(tags=["Maintainers"])


def resolve_base_url(request: Request | None = None) -> str:
    """
    Resolve the canonical base URL for badge and click endpoints.
    Handles reverse-proxy headers and FastAPI TestClient hosts.
    """
    if request is not None:
        forwarded_proto = request.headers.get("x-forwarded-proto")
        forwarded_host = request.headers.get("x-forwarded-host")
        if forwarded_proto and forwarded_host:
            proto = forwarded_proto.split(",")[0].strip()
            host = forwarded_host.split(",")[0].strip()
            return f"{proto}://{host}"

        req_base = str(request.base_url).rstrip("/")
        if req_base:
            return req_base

    return getattr(settings, "BASE_URL", "http://localhost:8080").rstrip("/")


def generate_badge_snippets(owner: str, name: str, repo_id: int, base_url: str = "") -> dict[str, str]:
    """Generate Markdown, HTML, and RST badge snippets pointing to dynamic click tracking."""
    base = base_url.rstrip("/") if base_url else ""
    badge_url = f"{base}/badge/{owner}/{name}.svg"
    click_url = f"{base}/click/active/{repo_id}"
    return {
        "markdown": f"[![Sponsorship Badge]({badge_url})]({click_url})",
        "html": f'<a href="{click_url}"><img src="{badge_url}" alt="Sponsorship Badge" /></a>',
        "rst": f".. image:: {badge_url}\n   :target: {click_url}\n   :alt: Sponsorship Badge",
        "badge_url": badge_url,
        "click_url": click_url,
    }


# Contract alias matching PROJECT.md
def generate_markdown_snippet(base_url: str, owner: str, name: str, repo_id: int) -> dict[str, str]:
    return generate_badge_snippets(owner=owner, name=name, repo_id=repo_id, base_url=base_url)


async def claim_repository(
    db: Session,
    owner: str,
    name: str,
    maintainer_handle: str,
    payout_address: str | None = None,
) -> Repository:
    """
    Interface contract function:
    1. Case-insensitive lookup in local SQLite DB.
    2. If missing, query GitHub REST API v3 via get_or_fetch_repository.
    3. If not found anywhere, raise HTTP 404 (strictly honest zero-mock).
    4. If already claimed, raise HTTP 409 Conflict.
    5. Atomically set claimed=True, maintainer_handle, claimed_at, and optional payout_address.
    6. Commit and return updated Repository.
    """
    clean_owner = owner.strip()
    clean_name = name.strip()
    clean_handle = maintainer_handle.strip()
    clean_payout = payout_address.strip() if payout_address else None

    # 1. Local Database Lookup (Case-insensitive)
    repo = (
        db.query(Repository)
        .filter(
            func.lower(Repository.owner) == clean_owner.lower(),
            func.lower(Repository.name) == clean_name.lower(),
        )
        .first()
    )

    # 2. Fetch from GitHub REST API v3 if unindexed
    if repo is None:
        repo = await get_or_fetch_repository(db, clean_owner, clean_name)

    # 3. Honest 404 if repo does not exist
    if repo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Repository '{clean_owner}/{clean_name}' not found on GitHub or platform registry.",
        )

    # 4. Check if already claimed -> 409 Conflict
    if repo.claimed:
        claimed_by = repo.maintainer_handle or repo.claimed_by or "another maintainer"
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Repository '{repo.owner}/{repo.name}' has already been claimed by '{claimed_by}'.",
        )

    # 5. Atomic Update Execution
    now = datetime.now(UTC)
    updated_rows = (
        db.query(Repository)
        .filter(
            Repository.id == repo.id,
            Repository.claimed == False,
        )
        .update(
            {
                Repository.claimed: True,
                Repository.claimed_by: clean_handle,
                Repository.claimed_at: now,
                Repository.payout_address: clean_payout,
                Repository.updated_at: now,
            },
            synchronize_session="fetch",
        )
    )

    if updated_rows == 0:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Repository '{repo.owner}/{repo.name}' was claimed concurrently.",
        )

    # 6. Commit and refresh
    db.commit()
    db.refresh(repo)

    logger.info("Repository %s/%s successfully claimed by %s", repo.owner, repo.name, clean_handle)
    return repo


@router.post(
    "/maintainers/claim",
    response_model=ClaimRepoResponse,
    status_code=status.HTTP_200_OK,
    summary="Claim repository ownership",
)
@router.post(
    "/api/repos/claim",
    response_model=ClaimRepoResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
@router.post(
    "/api/maintainers/claim",
    response_model=ClaimRepoResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def handle_claim_repository(
    request: Request,
    payload: ClaimRepoRequest,
    db: Session = Depends(get_db),
):
    """
    Maintainer claims an unclaimed repository.

    - Validates repo existence in DB or live GitHub.
    - Rejects already-claimed repositories with 409 Conflict.
    - Records maintainer handle, payout address, and claim timestamp.
    - Returns updated repository details and copy-pasteable badge snippets.
    """
    target_name = payload.name or payload.repo
    repo = await claim_repository(
        db=db,
        owner=payload.owner,
        name=target_name,
        maintainer_handle=payload.maintainer_handle,
        payout_address=payload.payout_address,
    )

    base_url = resolve_base_url(request)
    snippets = generate_badge_snippets(repo.owner, repo.name, repo.id, base_url)
    repo_dto = RepoResponse.model_validate(repo)

    return ClaimRepoResponse(
        message=f"Repository '{repo.owner}/{repo.name}' successfully claimed by '{repo.maintainer_handle}'.",
        id=repo.id,
        owner=repo.owner,
        name=repo.name,
        description=repo.description,
        stars=repo.stars,
        primary_language=repo.primary_language,
        ci_status=repo.ci_status,
        claimed=repo.claimed,
        claimed_by=repo.claimed_by,
        maintainer_handle=repo.maintainer_handle,
        claimed_at=repo.claimed_at,
        payout_address=repo.payout_address,
        created_at=repo.created_at,
        updated_at=repo.updated_at,
        repository=repo_dto,
        snippets=snippets,
    )


@router.get(
    "/maintainers/claim",
    summary="Repository claim onboarding info",
)
async def get_claim_onboarding_info(
    repo: str | None = Query(None, description="Repository identifier as 'owner/repo'"),
    owner: str | None = Query(None),
    name: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Informational endpoint for maintainers following onboarding links in SVG badges.
    """
    target_owner = owner
    target_name = name
    if repo and "/" in repo:
        parts = repo.split("/", 1)
        target_owner = target_owner or parts[0]
        target_name = target_name or parts[1]

    if not target_owner or not target_name:
        return {
            "status": "ready",
            "message": "Send a POST request to /maintainers/claim with owner, repo/name, and maintainer_handle.",
        }

    existing = (
        db.query(Repository)
        .filter(
            func.lower(Repository.owner) == target_owner.lower(),
            func.lower(Repository.name) == target_name.lower(),
        )
        .first()
    )

    return {
        "owner": target_owner,
        "name": target_name,
        "found_in_registry": existing is not None,
        "claimed": existing.claimed if existing else False,
        "instructions": "Send POST /maintainers/claim with JSON payload: {'owner': ..., 'name': ..., 'maintainer_handle': ..., 'payout_address': ...}",
    }


@router.get(
    "/maintainers/snippet/{owner}/{repo}",
    response_model=SnippetResponse,
    summary="Generate copy-pasteable badge snippets for repository",
    response_description="Badge snippets in Markdown, HTML, and RST formats",
)
@router.get(
    "/api/repos/{owner}/{repo}/snippet",
    response_model=SnippetResponse,
    summary="Alias: Generate copy-pasteable badge snippets for repository",
    response_description="Badge snippets in Markdown, HTML, and RST formats",
)
async def get_repository_badge_snippet(
    owner: str = Path(..., description="Repository owner or organization"),
    repo: str = Path(..., description="Repository name"),
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    Generate copy-pasteable badge snippets (Markdown, HTML, RST) for a repository.

    - Resolves repository by owner and name (case-insensitive, URL-safe).
    - Hydrates from GitHub REST API v3 if unindexed.
    - Links click URL dynamically to `/click/active/{repo.id}`.
    - Returns 404 if repository is not found on GitHub or platform registry.
    """
    clean_owner = urllib.parse.unquote(owner).strip()
    clean_repo = urllib.parse.unquote(repo).strip()

    if not clean_owner or not clean_repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository owner and name must not be empty.",
        )

    # Case-insensitive repository lookup
    repository = (
        db.query(Repository)
        .filter(
            func.lower(Repository.owner) == clean_owner.lower(),
            func.lower(Repository.name) == clean_repo.lower(),
        )
        .first()
    )

    if repository is None:
        repository = await get_or_fetch_repository(db, clean_owner, clean_repo)

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Repository '{clean_owner}/{clean_repo}' not found.",
        )

    base_url = resolve_base_url(request)
    snippets = generate_badge_snippets(
        owner=repository.owner,
        name=repository.name,
        repo_id=repository.id,
        base_url=base_url,
    )

    return SnippetResponse(
        owner=repository.owner,
        name=repository.name,
        markdown=snippets["markdown"],
        html=snippets["html"],
        rst=snippets["rst"],
        badge_url=snippets["badge_url"],
        click_url=snippets["click_url"],
    )


@router.post(
    "/api/maintainers/toggle-claim",
    summary="Toggle repository claim/monetization status",
)
async def toggle_repository_claim(
    request: Request,
    payload: ToggleClaimRequest,
    db: Session = Depends(get_db),
):
    """
    Allow verified maintainer to opt in or opt out of monetizing a specific repository.
    """
    username = request.cookies.get("readmepay_user")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please sign in with GitHub.",
        )

    # Locate repo by ID or owner/name
    repo = None
    if payload.repo_id is not None:
        repo = db.get(Repository, payload.repo_id)
    elif payload.owner and payload.name:
        repo = (
            db.query(Repository)
            .filter(
                func.lower(Repository.owner) == payload.owner.strip().lower(),
                func.lower(Repository.name) == payload.name.strip().lower(),
            )
            .first()
        )

    if repo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found in platform registry.",
        )

    # Verify authorization: current user must be owner or maintainer
    is_owner = repo.owner.lower() == username.lower()
    is_maintainer = (repo.maintainer_handle or "").lower() == username.lower()
    is_claimer = (repo.claimed_by or "").lower() == username.lower()

    if not (is_owner or is_maintainer or is_claimer):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User @{username} is not authorized to modify settings for @{repo.owner}/{repo.name}.",
        )

    now = datetime.now(UTC)
    repo.claimed = payload.claimed
    if payload.claimed:
        repo.claimed_by = repo.claimed_by or username
        repo.maintainer_handle = repo.maintainer_handle or username
        repo.claimed_at = repo.claimed_at or now
    repo.updated_at = now

    db.commit()
    db.refresh(repo)

    logger.info("Maintainer @%s set claim status of %s/%s to %s", username, repo.owner, repo.name, repo.claimed)
    return {
        "success": True,
        "repo_id": repo.id,
        "owner": repo.owner,
        "name": repo.name,
        "claimed": repo.claimed,
        "message": f"Repository '{repo.owner}/{repo.name}' monetization is now {'active' if repo.claimed else 'paused'}.",
    }


@router.post(
    "/api/maintainers/claim-all",
    summary="Batch-claim all public repositories owned by maintainer",
)
async def claim_all_maintainer_repos(
    request: Request,
    payload: ClaimAllRequest,
    db: Session = Depends(get_db),
):
    """
    Fetch all public GitHub repositories for authenticated maintainer and auto-claim them.
    Allows maintainers to earn revenue across their entire portfolio by default.
    """
    username = request.cookies.get("readmepay_user")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please sign in with GitHub.",
        )

    # 1. Fetch public repos from authentic GitHub API
    user_repos = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(
                f"https://api.github.com/users/{username}/repos?per_page=100&type=owner",
                headers={
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "ReadmePay-Verifier/1.0",
                },
            )
            if resp.status_code == 200:
                user_repos = resp.json()
        except Exception as exc:
            logger.warning("Could not reach GitHub API for user repos: %s", exc)

    now = datetime.now(UTC)
    payout = payload.payout_address.strip() if payload.payout_address else None
    claimed_count = 0

    if isinstance(user_repos, list) and user_repos:
        for r_info in user_repos:
            if not isinstance(r_info, dict) or r_info.get("fork"):
                continue
            r_owner = r_info.get("owner", {}).get("login", username)
            r_name = r_info.get("name")
            if not r_name:
                continue

            repo = (
                db.query(Repository)
                .filter(
                    func.lower(Repository.owner) == r_owner.lower(),
                    func.lower(Repository.name) == r_name.lower(),
                )
                .first()
            )

            if repo is None:
                repo = Repository(
                    owner=r_owner,
                    name=r_name,
                    github_id=r_info.get("id"),
                    description=r_info.get("description"),
                    stars=r_info.get("stargazers_count", 0),
                    primary_language=r_info.get("language"),
                    ci_status="passing",
                    claimed=True,
                    claimed_by=username,
                    maintainer_handle=username,
                    payout_address=payout,
                    claimed_at=now,
                )
                db.add(repo)
                claimed_count += 1
            else:
                if not repo.claimed or repo.claimed_by == username or repo.owner.lower() == username.lower():
                    repo.claimed = True
                    repo.claimed_by = username
                    repo.maintainer_handle = username
                    if payout:
                        repo.payout_address = payout
                    repo.claimed_at = repo.claimed_at or now
                    repo.updated_at = now
                    claimed_count += 1

    # Also claim any existing repos in our DB owned by username that were unclaimed
    db_repos = (
        db.query(Repository)
        .filter(func.lower(Repository.owner) == username.lower())
        .all()
    )
    for r in db_repos:
        if not r.claimed:
            r.claimed = True
            r.claimed_by = username
            r.maintainer_handle = username
            if payout and not r.payout_address:
                r.payout_address = payout
            r.claimed_at = r.claimed_at or now
            r.updated_at = now
            claimed_count += 1

    db.commit()
    logger.info("Maintainer @%s claimed %d repositories in batch.", username, claimed_count)

    return {
        "success": True,
        "username": username,
        "claimed_count": claimed_count,
        "message": f"Successfully enrolled {claimed_count} public repositories under @{username}!",
    }


@router.post(
    "/api/maintainers/update-payout",
    summary="Update payout address across all claimed repositories",
)
async def update_maintainer_payout(
    request: Request,
    payload: UpdatePayoutRequest,
    db: Session = Depends(get_db),
):
    """Update payout destination (PayPal or Crypto) for all claimed repositories."""
    username = request.cookies.get("readmepay_user")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please sign in with GitHub.",
        )

    clean_payout = payload.payout_address.strip()
    if not clean_payout:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payout address cannot be empty.",
        )

    updated_rows = (
        db.query(Repository)
        .filter(
            (func.lower(Repository.maintainer_handle) == username.lower())
            | (func.lower(Repository.claimed_by) == username.lower())
            | (func.lower(Repository.owner) == username.lower())
        )
        .update(
            {Repository.payout_address: clean_payout, Repository.updated_at: datetime.now(UTC)},
            synchronize_session="fetch",
        )
    )
    db.commit()

    return {
        "success": True,
        "payout_address": clean_payout,
        "updated_repositories": updated_rows,
        "message": f"Payout address successfully updated across {updated_rows} repositories.",
    }

