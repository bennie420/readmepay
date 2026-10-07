"""
Tests for Maintainer Multi-Repo Auto-Claim, Selective Toggle, and Payout Management.
"""

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.models.repository import Repository
from tests.conftest import create_test_repository, create_test_ad


def test_auth_user_unauthenticated(client: TestClient):
    """Unauthenticated call to /api/auth/github/user returns authenticated=False."""
    resp = client.get("/api/auth/github/user")
    assert resp.status_code == 200
    data = resp.json()
    assert data["authenticated"] is False
    assert data["username"] is None
    assert data["repos"] == []


def test_auth_user_authenticated_summary_and_repos(client: TestClient, db_session: Session):
    """Authenticated maintainer gets complete summary and repo portfolio."""
    r1 = create_test_repository(db_session, owner="alice", name="cool-lib", claimed=True, maintainer_handle="alice")
    r2 = create_test_repository(db_session, owner="alice", name="docs-tool", claimed=False)
    
    # Simulate session cookie
    client.cookies.set("readmepay_user", "alice")
    resp = client.get("/api/auth/github/user")
    assert resp.status_code == 200
    data = resp.json()
    assert data["authenticated"] is True
    assert data["username"] == "alice"
    assert "summary" in data
    assert data["summary"]["total_repos"] == 2
    assert data["summary"]["claimed_repos_count"] == 1
    assert len(data["repos"]) == 2


def test_toggle_claim_status(client: TestClient, db_session: Session):
    """Maintainer can toggle claiming on/off for their repository."""
    repo = create_test_repository(db_session, owner="alice", name="toggle-repo", claimed=True, maintainer_handle="alice")

    client.cookies.set("readmepay_user", "alice")
    
    # 1. Pause monetization (unclaim)
    resp = client.post("/api/maintainers/toggle-claim", json={"repo_id": repo.id, "claimed": False})
    assert resp.status_code == 200
    assert resp.json()["claimed"] is False
    db_session.refresh(repo)
    assert repo.claimed is False

    # 2. Re-enable monetization (claim)
    resp = client.post("/api/maintainers/toggle-claim", json={"repo_id": repo.id, "claimed": True})
    assert resp.status_code == 200
    assert resp.json()["claimed"] is True
    db_session.refresh(repo)
    assert repo.claimed is True


def test_toggle_claim_forbidden_for_other_users(client: TestClient, db_session: Session):
    """Users cannot toggle repositories they do not own."""
    repo = create_test_repository(db_session, owner="bob", name="secret-repo", claimed=True, maintainer_handle="bob")

    client.cookies.set("readmepay_user", "mallory")
    resp = client.post("/api/maintainers/toggle-claim", json={"repo_id": repo.id, "claimed": False})
    assert resp.status_code == 403


def test_update_payout_for_all_repos(client: TestClient, db_session: Session):
    """Maintainer can update payout address across all their repositories."""
    r1 = create_test_repository(db_session, owner="charlie", name="repo-a", claimed=True, maintainer_handle="charlie")
    r2 = create_test_repository(db_session, owner="charlie", name="repo-b", claimed=True, maintainer_handle="charlie")

    client.cookies.set("readmepay_user", "charlie")
    resp = client.post("/api/maintainers/update-payout", json={"payout_address": "payout@charlie.org"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["updated_repositories"] >= 2

    db_session.refresh(r1)
    db_session.refresh(r2)
    assert r1.payout_address == "payout@charlie.org"
    assert r2.payout_address == "payout@charlie.org"


def test_sponsor_side_positioning_banner_and_shield(client: TestClient, db_session: Session):
    """Verify sponsor_pos parameter works for both banner and shield layouts."""
    repo = create_test_repository(db_session, owner="pos-test", name="position-repo")
    ad = create_test_ad(db_session, sponsor_name="SpeedyAd")

    # Banner left
    resp_banner_left = client.get(f"/badge/{repo.owner}/{repo.name}.svg?sponsor_pos=left")
    assert resp_banner_left.status_code == 200
    assert "SpeedyAd" in resp_banner_left.text
    # Left banner puts ad card at x="8"
    assert 'x="8"' in resp_banner_left.text

    # Banner right
    resp_banner_right = client.get(f"/badge/{repo.owner}/{repo.name}.svg?sponsor_pos=right")
    assert resp_banner_right.status_code == 200
    assert 'x="256"' in resp_banner_right.text

    # Shield left
    resp_shield_left = client.get(f"/badge/{repo.owner}/{repo.name}.svg?style=shield&sponsor_pos=left")
    assert resp_shield_left.status_code == 200
    assert "SpeedyAd" in resp_shield_left.text

    # Shield right
    resp_shield_right = client.get(f"/badge/{repo.owner}/{repo.name}.svg?style=shield&sponsor_pos=right")
    assert resp_shield_right.status_code == 200
    assert "SpeedyAd" in resp_shield_right.text
