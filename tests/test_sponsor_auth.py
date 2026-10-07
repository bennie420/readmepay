"""
Tests for Sponsor Authentication, Session Inspection, and Dashboard Data Isolation.
"""

from decimal import Decimal
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.models.ad import Ad
from tests.conftest import create_test_ad


def test_sponsor_user_unauthenticated(client: TestClient):
    """Unauthenticated call to /api/auth/sponsor/user returns authenticated=False."""
    resp = client.get("/api/auth/sponsor/user")
    assert resp.status_code == 200
    data = resp.json()
    assert data["authenticated"] is False
    assert data["sponsor_name"] is None
    assert data["campaigns"] == []
    assert data["summary"] is None


def test_sponsor_login_and_user_session(client: TestClient, db_session: Session):
    """Sponsor can sign in by brand name and inspect their campaigns and KPIs."""
    # Create test ads for Supabase and another sponsor
    ad1 = create_test_ad(
        db_session,
        sponsor_name="Supabase",
        headline="Serverless Postgres Database",
        total_budget=Decimal("500.00"),
        remaining_budget=Decimal("350.00"),
    )
    ad2 = create_test_ad(
        db_session,
        sponsor_name="Supabase",
        headline="Auth & Storage for Developers",
        total_budget=Decimal("200.00"),
        remaining_budget=Decimal("200.00"),
    )
    other_ad = create_test_ad(
        db_session,
        sponsor_name="OtherBrand",
        headline="Unrelated product",
        total_budget=Decimal("100.00"),
        remaining_budget=Decimal("100.00"),
    )

    # 1. Sign in as Supabase
    login_resp = client.post("/api/auth/sponsor/login", json={"sponsor_name": "Supabase"})
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert login_data["authenticated"] is True
    assert login_data["sponsor_name"] == "Supabase"
    assert login_data["campaigns_count"] == 2

    # 2. Inspect sponsor session
    user_resp = client.get("/api/auth/sponsor/user")
    assert user_resp.status_code == 200
    user_data = user_resp.json()
    assert user_data["authenticated"] is True
    assert user_data["sponsor_name"] == "Supabase"
    assert user_data["campaigns_count"] == 2
    assert len(user_data["campaigns"]) == 2
    assert user_data["summary"]["total_campaigns"] == 2
    assert user_data["summary"]["total_budget"] == 700.0
    assert user_data["summary"]["remaining_budget"] == 550.0
    assert user_data["summary"]["total_spent"] == 150.0

    # 3. Sign out
    logout_resp = client.post("/api/auth/sponsor/logout")
    assert logout_resp.status_code == 200
    assert logout_resp.json()["authenticated"] is False

    # 4. Verify unauthenticated after logout
    verify_resp = client.get("/api/auth/sponsor/user")
    assert verify_resp.status_code == 200
    assert verify_resp.json()["authenticated"] is False


def test_sponsor_github_sso_session(client: TestClient, db_session: Session):
    """Sponsor authenticated via GitHub SSO can inspect their financial campaigns and KPIs."""
    create_test_ad(
        db_session,
        sponsor_name="Datadog",
        headline="Cloud monitoring & security platform",
        total_budget=Decimal("1000.00"),
        remaining_budget=Decimal("800.00"),
    )

    # Set GitHub SSO session cookies
    client.cookies.set("readmepay_sponsor_user", "datadog-admin", domain="testserver.local")
    client.cookies.set("readmepay_sponsor_name", "Datadog", domain="testserver.local")
    client.cookies.set("readmepay_sponsor_avatar", "https://avatars.githubusercontent.com/u/datadog", domain="testserver.local")

    resp = client.get("/api/auth/sponsor/user")
    assert resp.status_code == 200
    data = resp.json()
    assert data["authenticated"] is True
    assert data["github_user"] == "datadog-admin"
    assert data["sponsor_name"] == "Datadog"
    assert data["avatar_url"] == "https://avatars.githubusercontent.com/u/datadog"
    assert data["campaigns_count"] == 1
    assert data["summary"]["total_budget"] == 1000.0
    assert data["summary"]["remaining_budget"] == 800.0

    # Logout clears all sponsor cookies
    logout_resp = client.post("/api/auth/sponsor/logout")
    assert logout_resp.status_code == 200
    assert logout_resp.json()["authenticated"] is False

    # Check unauthenticated
    after_resp = client.get("/api/auth/sponsor/user")
    assert after_resp.status_code == 200
    assert after_resp.json()["authenticated"] is False


def test_edit_sponsor_campaign(client: TestClient, db_session: Session):
    """Sponsor can edit headline, CTA, click_url, target_language, and is_active on their campaigns."""
    ad = create_test_ad(
        db_session,
        sponsor_name="Neon",
        headline="Old Headline",
        cta_text="Old CTA",
        click_url="https://neon.tech/old",
        target_language="Rust",
    )

    # 1. Edit as unauthenticated or matching sponsor
    client.cookies.set("readmepay_sponsor_name", "Neon", domain="testserver.local")

    update_payload = {
        "headline": "Serverless Postgres with Instant Autoscaling",
        "call_to_action": "Start Free DB",
        "click_url": "https://neon.tech/new",
        "target_language": "General",
        "is_active": True,
        "cost_per_click": 0.75,
    }

    resp = client.put(f"/api/inventory/ads/{ad.id}", json=update_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["headline"] == "Serverless Postgres with Instant Autoscaling"
    assert data["call_to_action"] == "Start Free DB"
    assert data["click_url"] == "https://neon.tech/new"
    assert data["target_language"] == "General"
    assert data["cost_per_click"] == 0.75

    # 2. Unauthorized edit attempt by another sponsor
    client.cookies.set("readmepay_sponsor_name", "Supabase", domain="testserver.local")
    forbidden_resp = client.put(f"/api/inventory/ads/{ad.id}", json={"headline": "Malicious Change"})
    assert forbidden_resp.status_code == 403


