"""
Sponsor Authentication and Campaign Management Router (app/routers/sponsor_auth.py).

Provides:
- POST /api/auth/sponsor/login: Sign in sponsor by company/brand name and set session cookie.
- GET /api/auth/sponsor/user: Fetch current sponsor profile, KPI summary, and active campaigns.
- POST /api/auth/sponsor/logout: Clear sponsor session cookie.
- GET /api/auth/sponsor/logout: Clear sponsor session cookie and redirect to sponsor portal.
"""

from __future__ import annotations

import logging
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ad import Ad

logger = logging.getLogger("router_sponsor_auth")

router = APIRouter(prefix="/api/auth/sponsor", tags=["Sponsor Authentication"])


class SponsorLoginRequest(BaseModel):
    sponsor_name: str = Field(..., min_length=1, max_length=255, description="Company or brand name")


@router.post("/login", summary="Sign in sponsor by brand name")
async def sponsor_login(
    payload: SponsorLoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    Authenticate a sponsor by their company/brand name.
    Sets 'readmepay_sponsor' session cookie and returns campaign summary.
    """
    clean_name = payload.sponsor_name.strip()
    if not clean_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company or brand name is required.",
        )

    # Count campaigns associated with this sponsor
    existing_campaigns = (
        db.query(Ad)
        .filter(func.lower(Ad.sponsor_name) == clean_name.lower())
        .all()
    )

    resp = JSONResponse(content={
        "authenticated": True,
        "sponsor_name": clean_name,
        "campaigns_count": len(existing_campaigns),
        "message": f"Signed in as sponsor '{clean_name}'.",
    })

    resp.set_cookie(
        key="readmepay_sponsor",
        value=clean_name,
        httponly=False,
        max_age=86400 * 30,  # 30 days
        samesite="lax",
    )

    logger.info("Sponsor '%s' signed in (%d campaigns)", clean_name, len(existing_campaigns))
    return resp


@router.get("/user", summary="Get current sponsor profile and campaigns")
async def get_current_sponsor(request: Request, db: Session = Depends(get_db)):
    """
    Check currently authenticated sponsor session and return their campaigns and KPIs.
    """
    sponsor_name = request.cookies.get("readmepay_sponsor")
    if not sponsor_name:
        return {
            "authenticated": False,
            "sponsor_name": None,
            "campaigns_count": 0,
            "campaigns": [],
            "summary": None,
        }

    ads = (
        db.query(Ad)
        .filter(func.lower(Ad.sponsor_name) == sponsor_name.lower())
        .order_by(Ad.id.desc())
        .all()
    )

    items = []
    total_budget = Decimal("0.00")
    remaining_budget = Decimal("0.00")
    total_clicks = 0
    total_impressions = 0

    for a in ads:
        clicks_cnt = len(a.clicks) if hasattr(a, "clicks") and a.clicks else 0
        impr_cnt = len(a.impressions) if hasattr(a, "impressions") and a.impressions else 0
        total_b = a.total_budget if getattr(a, "total_budget", None) is not None else a.remaining_budget
        rem_b = a.remaining_budget
        spent = max(Decimal("0.00"), total_b - rem_b)

        total_budget += total_b
        remaining_budget += rem_b
        total_clicks += clicks_cnt
        total_impressions += impr_cnt

        items.append({
            "id": a.id,
            "sponsor_name": a.sponsor_name,
            "headline": a.headline,
            "cta_text": a.cta_text,
            "click_url": a.click_url,
            "target_language": a.target_language or "general",
            "target_repo_id": a.target_repo_id,
            "cpc": float(a.cpc),
            "remaining_budget": float(rem_b),
            "total_budget": float(total_b),
            "spent": float(spent),
            "clicks_count": clicks_cnt,
            "impressions_count": impr_cnt,
            "ctr": round((clicks_cnt / impr_cnt * 100), 1) if impr_cnt > 0 else 0.0,
            "is_active": a.is_active,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        })

    avg_ctr = round((total_clicks / total_impressions * 100), 1) if total_impressions > 0 else 0.0
    total_spent = max(Decimal("0.00"), total_budget - remaining_budget)

    return {
        "authenticated": True,
        "sponsor_name": sponsor_name,
        "campaigns_count": len(items),
        "campaigns": items,
        "summary": {
            "total_campaigns": len(items),
            "total_budget": float(total_budget),
            "remaining_budget": float(remaining_budget),
            "total_spent": float(total_spent),
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "avg_ctr": avg_ctr,
        },
    }


@router.post("/logout", summary="Sign out sponsor (POST)")
async def sponsor_logout():
    """Clear sponsor session cookie."""
    resp = JSONResponse(content={"authenticated": False, "message": "Signed out successfully."})
    resp.delete_cookie(key="readmepay_sponsor")
    return resp


@router.get("/logout", summary="Sign out sponsor (GET redirect)")
async def sponsor_logout_get(request: Request):
    """Clear sponsor session cookie and redirect to sponsor portal."""
    base_url = str(request.base_url).rstrip("/")
    redirect = RedirectResponse(url=f"{base_url}/sponsors", status_code=status.HTTP_302_FOUND)
    redirect.delete_cookie(key="readmepay_sponsor")
    return redirect
