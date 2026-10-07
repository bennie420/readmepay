# Project: ReadmePay — Economic Empowerment Infrastructure for Independent Open-Source Developers

## Architecture Overview
- **Language & Framework**: Python 3.12, FastAPI, Uvicorn (production multi-worker ASGI).
- **Database & Storage**: SQLAlchemy 2.0 with SQLite (`sqlite:///./badge_platform.db` / `sqlite+aiosqlite:///./badge_platform.db`), WAL mode enabled (`PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;`), and foreign keys enforced (`PRAGMA foreign_keys=ON;`).
- **Template & Rendering**: Jinja2 with `select_autoescape(['xml', 'svg', 'html'])` compiling valid SVG XML with responsive `viewBox="0 0 500 110"` (and dedicated compact `300-520×28` dimensions for Backer, Goal, and Shield styles).
- **External Integration**: Async HTTPX client for authentic GitHub REST API v3 queries (`/repos/{owner}/{repo}` and `/actions/runs`), supported by 1-hour TTL in-memory caching and optional `GITHUB_TOKEN`.
- **Security & Integrity Policy**: Zero synthetic/mock fallback personas or statistics in production models, zero `PYTEST_CURRENT_TEST` test bypasses, irreversible SHA-256 client audit hashing (`IP:User-Agent:Salt`).
- **Financial Ledger**: Exact `Decimal` mathematics for 50/50 maintainer revenue share and sponsor budget depletion.
- **Payment & Settlement**: Dual-rail checkout with PayPal Orders v2 API and NOWPayments/Crypto (USDC/SOL/BTC) invoices; automated payout batch exports (PayPal MassPay & Crypto instructions).
- **Production Infrastructure**: Hosted on Azure VM `vm-opensponsor` (`172.173.126.151`) in `rg-opensponsor-prod` behind Caddy reverse proxy with automated Let's Encrypt TLS certificate provisioning for `https://readmepay.com`.

---

## Feature Inventory

| # | Feature | Description | Milestone | Source | Status |
|---|---------|-------------|-----------|--------|:------:|
| F1 | Dynamic SVG Badge Endpoint | `GET /badge/{owner}/{repo}.svg` compiling responsive SVG via Jinja2 with inline styling | M2 | ORIGINAL_REQUEST §R1 | COMPLETE |
| F2 | Real GitHub Metadata Query | Live queries for stars, language, CI/CD status with `Cache-Control: public, max-age=3600` | M2 | ORIGINAL_REQUEST §R1 | COMPLETE |
| F3 | Honest Error Handling | Non-existent repos return authentic 404 or error SVG; zero synthetic fallback personas | M2 | ORIGINAL_REQUEST §R1, Rules | COMPLETE |
| F4 | Language Matching & Fallback | Match sponsor campaigns by repo primary language, falling back to general sponsor | M2 | ORIGINAL_REQUEST §R1 | COMPLETE |
| F5 | Click-Through Redirect Endpoint | `GET /click/{ad_id}/{repo_id}` logging click, deducting budget, and 302 redirecting to sponsor URL | M3 | ORIGINAL_REQUEST §R2 | COMPLETE |
| F6 | Embedded SVG Hyperlink | Standard SVG `<a href="..." target="_blank">` element surrounding ad card in badge | M2 | ORIGINAL_REQUEST §R2 | COMPLETE |
| F7 | Impression Tracking & Dedup | Hourly sliding-window deduplication using SHA-256 client audit hash | M3 | ORIGINAL_REQUEST §R2 | COMPLETE |
| F8 | SQLAlchemy 2.0 Data Models | Repositories, Ads, Impressions, and Clicks with strict schema and indexes | M1 | ORIGINAL_REQUEST §R3 | COMPLETE |
| F9 | DB Table Init & Migrations | Table auto-creation on startup and migration support | M1 | ORIGINAL_REQUEST §R3 | COMPLETE |
| F10 | Top Repositories Seed Script | Discover and persist real top open-source repos using real GitHub Search API | M1 | ORIGINAL_REQUEST §R3 | COMPLETE |
| F11 | Maintainer Onboarding & Claiming | Claim repo endpoints with maintainer verification and conflict handling | M4 | ORIGINAL_REQUEST §R4 | COMPLETE |
| F12 | Snippet Generator | Copy-pasteable GitHub Markdown/HTML badge snippet generation | M4 | ORIGINAL_REQUEST §R4 | COMPLETE |
| F13 | 50/50 Revenue Share Reporting | Financial reporting endpoints reflecting exact 50/50 maintainer/platform split | M4 | ORIGINAL_REQUEST §R4 | COMPLETE |
| F14 | Automated Test Rig | Automated test suite verifying XML validity, ad matching, redirects, 404 handling | M5 | ORIGINAL_REQUEST §R5 | COMPLETE |
| F15 | Opaque-Box E2E Test Suite | Comprehensive 4-tier requirement-driven test suite publishing `TEST_READY.md` | M-E2E | Project Pattern | COMPLETE |
| F16 | Adversarial Hardening (Tier 5) | White-box stress-testing, edge cases, and security boundary verification | M5 | Project Pattern | COMPLETE |
| F17 | Multi-Style Badge Engine | 7 distinct styles: Glass Banner, Neo-Brutalist Linear, Dual-Pill Spotlight, Compact Micro-Card, Backer, Monthly Goal, Shields.io Pill | M6 | Extension | COMPLETE |
| F18 | 9-Palette Theme System | `dark`, `cyberpunk`, `emerald`, `light`, `linear`, `dracula`, `nord`, `monokai`, `synthwave` | M6 | Extension | COMPLETE |
| F19 | Right-to-Left Marquee Ticker | Optional smooth CSS/SVG `<animate>` marquee ticker (`?marquee=true`) | M6 | Extension | COMPLETE |
| F20 | Dynamic Sponsor Placement | Layout flipping (`?sponsor_pos=left` vs `?sponsor_pos=right`) | M6 | Extension | COMPLETE |
| F21 | GitHub OAuth Verification | Maintainer authentication via GitHub OAuth; admin permission checking | M7 | Extension | COMPLETE |
| F22 | Multi-Repo Portfolio Auto-Claim | Auto-discover all public repos owned by maintainer and bulk-claim on login | M7 | Extension | COMPLETE |
| F23 | Per-Repo Monetization Toggle | Allow maintainers to toggle sponsorship on/off per repository | M7 | Extension | COMPLETE |
| F24 | Sponsor Campaign Hub & Checkout | Self-serve campaign creation UI at `/sponsors` with language & repo targeting | M8 | Extension | COMPLETE |
| F25 | Multi-Gateway Payment Rails | PayPal Checkout Orders v2 API & NOWPayments Crypto (USDC/SOL/BTC) | M8 | Extension | COMPLETE |
| F26 | Automated Maintainer Payouts | Export batch payloads for PayPal MassPay & Crypto instructions; run automated payouts | M8 | Extension | COMPLETE |
| F27 | Azure Production VM Deployment | Automated provisioning and synchronization scripts (`azure-deploy.ps1`, `fast_deploy.py`) | M9 | Extension | COMPLETE |

---

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|:------:|
| M1 | Data Models & Seeding Engine | SQLAlchemy 2.0 schema (`Repository`, `Ad`, `Impression`, `Click`), WAL mode, client hash, real GitHub Search API seed script | none | DONE |
| M2 | Dynamic SVG Badge Engine | FastAPI `/badge/{owner}/{repo}.svg`, Jinja2 SVG template, live GitHub client, caching headers, language matching cascade, honest 404 | M1 | DONE |
| M3 | Click Tracking & Analytics Pipeline | FastAPI `/click/{ad_id}/{repo_id}`, 302 redirect, budget deduction, impression logging & deduplication, `/click/active/{repo_id}` | M1, M2 | DONE |
| M4 | Maintainer Onboarding & Revenue Sharing | Claiming endpoints, snippet generator, 50/50 revenue ledger and reporting endpoints | M1, M2, M3 | DONE |
| M-E2E | E2E Testing Track | Independent requirement-driven test suite (Tiers 1-4), harness, assertions, publishing `TEST_READY.md` | none | DONE |
| M5 | Final Milestone: E2E Test Pass & Hardening | Phase 1: 100% pass of E2E test suite (Tiers 1-4); Phase 2: Adversarial coverage hardening (Tier 5) | M1-M4, M-E2E | DONE |
| M6 | Design Overhaul & Multi-Style Suite | 7 badge templates, 9 color palettes, SVG marquee animations, sponsor positioning, Shields.io schema JSON endpoint | M2 | DONE |
| M7 | Maintainer Identity & Portfolio Claiming | GitHub OAuth flow, portfolio discovery, batch auto-claiming (`/api/maintainers/claim-all`), per-repo claim toggling | M4 | DONE |
| M8 | Sponsor Campaign Hub & Automated Payouts | `/sponsors` dashboard, self-serve PayPal/Crypto checkout, automated disbursement batching (`/api/billing/payouts/...`) | M3, M4 | DONE |
| M9 | Live Production Cloud Deployment | Azure VM deployment (`https://readmepay.com`), Caddy reverse proxy, fast deployment pipeline | All | DONE |

---

## Interface Contracts

### M1 ↔ M2 (Data Models ↔ Badge Engine)
- `get_or_fetch_repository(db: Session, owner: str, name: str) -> Optional[Repository]`
  - Returns `Repository` model instance or `None` if not found on GitHub.
- `match_ad_for_repository(db: Session, primary_language: Optional[str]) -> Optional[Ad]`
  - Matches active ad by language (case-insensitive) or falls back to general ad (`target_language IS NULL` or `'general'`) with `remaining_budget > 0`.
- `build_badge_svg(repo_name: str, stars: int, language: Optional[str], ci_status: Optional[str], ad: Optional[Ad], click_url: str, style: str = "banner", theme: str = "dark", marquee: bool = False, sponsor_pos: str = "right", hide_stars: bool = False, hide_ci: bool = False) -> str`
  - Returns strictly valid XML SVG string matching outer dimension specifications.

### M1/M2 ↔ M3 (Badge & Ad Data ↔ Click Tracking)
- `record_click(db: Session, ad_id: int, repo_id: int, client_ip: str, user_agent: str, referer: Optional[str]) -> Tuple[str, Click]`
  - Validates `ad_id` and `repo_id`, verifies budget, records `Click` with SHA-256 `client_hash`, deducts CPC from `ad.remaining_budget`, credits maintainer, and returns `(ad.click_url, click_instance)`.
- `record_impression(db: Session, ad_id: int, repo_id: int, client_ip: str, user_agent: str, is_camo: bool) -> Optional[Impression]`
  - Hourly sliding-window deduplication by `(repo_id, ad_id, client_hash)`.

### M4 ↔ M7 (Maintainer Onboarding & Identity)
- `claim_repository(db: Session, owner: str, name: str, maintainer_handle: str, payout_address: Optional[str]) -> Repository`
  - Validates ownership, ensures unclaimed, sets `claimed=True`.
- `claim_all_maintainer_repos(request: Request, payload: ClaimAllRequest, db: Session) -> Dict`
  - Discovers all public repos for authenticated maintainer from authentic GitHub API and enrolls them into the maintainer's portfolio.
- `generate_badge_snippets(base_url: str, owner: str, repo: str, repo_id: int) -> Dict[str, str]`
  - Returns markdown, html, and rst snippets linking to `/click/active/{repo_id}`.

### M8 (Billing & Payouts Engine)
- `create_paypal_order(campaign_data: Dict) -> Dict`
  - Creates PayPal v2 Checkout Order with intent `CAPTURE`.
- `capture_paypal_order(order_id: str, ad_id: int, db: Session) -> Dict`
  - Captures PayPal payment and credits active ad budget.
- `create_crypto_invoice(campaign_data: Dict) -> Dict`
  - Generates USDC/SOL/BTC payment invoice with deposit address and QR code.
- `execute_automated_payouts(db: Session) -> PayoutResult`
  - Computes net unpaid maintainer balances and generates PayPal MassPay & Crypto disbursement batches.

---

## Directory Layout

```
c:/Users/ben/Documents/antigravity/hopeful-bardeen/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app factory, routes inclusion, lifespan
│   ├── config.py            # Settings (PORT, DB_URL, GITHUB_CLIENT_ID, SALT)
│   ├── database.py          # SQLAlchemy engine, sessionmaker, WAL event listeners
│   ├── models/
│   │   ├── __init__.py
│   │   ├── repository.py    # Repository ORM model
│   │   ├── ad.py            # Ad ORM model
│   │   └── analytics.py     # Impression & Click ORM models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── repo.py
│   │   ├── ad.py
│   │   └── revenue.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── github_service.py   # GitHub REST API v3 async client + TTL cache
│   │   ├── badge_service.py    # Jinja2 SVG compiler, XML validator, 7 styles & 9 themes
│   │   ├── matching_service.py # Language matching & fallback engine
│   │   ├── tracking_service.py # Impression dedup, click logging, SHA-256 hash
│   │   └── revenue_service.py  # 50/50 revenue math & reporting
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # GitHub OAuth login, callback, session user
│   │   ├── badge.py         # GET /badge/{owner}/{repo}.svg & shield.json
│   │   ├── billing.py       # PayPal Checkout, Crypto invoices & automated payouts
│   │   ├── click.py         # GET /click/{ad_id}/{repo_id} & /click/active/{repo_id}
│   │   ├── inventory.py     # Repos & Ads catalogs, ad creation
│   │   ├── maintainers.py   # Claiming, claim-all, toggle-claim, snippet generation
│   │   └── revenue.py       # Revenue share reporting endpoints
│   └── templates/
│       ├── badge.svg.j2          # Style 1: Glass Banner (500x110)
│       ├── badge_linear.svg.j2   # Style 2: Neo-Brutalist Linear Dark (500x110)
│       ├── badge_spotlight.svg.j2# Style 3: Dual-Pill Radial Spotlight (500x110)
│       ├── badge_compact.svg.j2  # Style 4: Compact Micro-Card (500x110)
│       ├── badge_backer.svg.j2   # Style 5: Dedicated Supporter Pill (320x28)
│       ├── badge_goal.svg.j2     # Style 6: Monthly Funding Goal Pill (300x28)
│       ├── shield.svg.j2         # Style 7: Shields.io Marquee Pill (520x28)
│       ├── error.svg.j2          # Honest error SVG template
│       └── index.html            # Single Page Dashboard & Interactive Badge Studio
├── deploy/
│   ├── azure-deploy.ps1     # Azure VM provisioning and initial setup
│   ├── env.production.example
│   └── vps-setup.sh         # Caddy SSL and Docker container configuration
├── docs/
│   ├── API.md               # Complete REST API reference
│   ├── BADGES.md            # Badge visual styles & theming guide
│   └── ARCHITECTURE.md      # System architecture, deduplication, and payment rails
├── scripts/
│   ├── seed_top_repos.py    # Real GitHub Search API repository seeder
│   ├── seed_sample_ads.py   # Tech sponsor campaign seeder
│   └── run_verification_rig.py # Standalone E2E verification rig
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_badge_svg.py
│   ├── test_matching.py
│   ├── test_click_tracking.py
│   ├── test_onboarding.py
│   ├── test_revenue.py
│   ├── test_github_service.py
│   ├── test_maintainer_multirepo.py
│   ├── test_challenger_m2_svg_xml.py
│   └── e2e/
│       ├── test_tier1_features.py
│       ├── test_tier2_boundaries.py
│       ├── test_tier3_combinations.py
│       └── test_tier4_scenarios.py
├── fast_deploy.py           # One-shot batch sync to Azure VM vm-opensponsor
├── PROJECT.md
├── pytest.ini
└── README.md
```
