# ReadmePay System Architecture & Technical Specifications

ReadmePay is designed as high-throughput, fault-tolerant infrastructure providing economic empowerment to open-source software maintainers.

---

## 1. High-Level Architecture Diagram

```
+---------------------------------------------------------------------------------+
|                                 GITHUB.COM                                      |
|  - Developer README embeds: <img src="https://readmepay.com/badge/...svg">      |
|  - Maintainer OAuth Login: /api/auth/github/login                               |
+---------------------------------------+-----------------------------------------+
                                        |
                                        v
+---------------------------------------------------------------------------------+
|                       AZURE VM (vm-opensponsor)                                 |
|                       172.173.126.151 / Linux Ubuntu                            |
|                                                                                 |
|  +---------------------------------------------------------------------------+  |
|  |                       CADDY 2 REVERSE PROXY                               |  |
|  |   - Automated Let's Encrypt TLS (readmepay.com)                           |  |
|  |   - HTTP/2 & HTTP/3 termination                                           |  |
|  |   - Gzip & Zstd dynamic response compression                              |  |
|  +-------------------------------------+-------------------------------------+  |
|                                        |                                        |
|                                        v                                        |
|  +---------------------------------------------------------------------------+  |
|  |                       FASTAPI APPLICATION CONTAINER                       |  |
|  |                                                                           |  |
|  |   +--------------------------+       +---------------------------------+  |  |
|  |   |    Badge Rendering       |       |       Analytics Pipeline        |  |  |
|  |   |  - Jinja2 XML engine     |       |  - SHA-256 Client Audit Hash    |  |  |
|  |   |  - 7 SVG Templates       |       |  - 1-hour Sliding-Window Dedup  |  |  |
|  |   |  - 9 Color Themes        |       |  - Camo proxy transparency      |  |  |
|  |   +------------+-------------+       +----------------+----------------+  |  |
|  |                |                                      |                   |  |
|  |                v                                      v                   |  |
|  |   +--------------------------------------------------------------------+  |  |
|  |   |                    SQLAlchemy 2.0 ORM Engine                       |  |  |
|  |   |          SQLite 3 with Write-Ahead Logging (WAL mode)              |  |  |
|  |   |     PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;             |  |  |
|  |   +--------------------------------------------------------------------+  |  |
|  |                                                                           |  |
|  |   +--------------------------------------------------------------------+  |  |
|  |   |                     Billing & Payment Rails                        |  |  |
|  |   |    - PayPal Orders v2 API & Automated MassPay Batching             |  |  |
|  |   |    - NOWPayments Crypto Invoicing (USDC / SOL / BTC)               |  |  |
|  |   +--------------------------------------------------------------------+  |  |
|  +---------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------+
```

---

## 2. Core Architectural Pillars

### A. Zero-Mock Data Integrity
- **Authentic Metadata Only**: Live repository statistics (star count, primary programming language, CI/CD status) are retrieved directly from the GitHub REST API v3.
- **Fail-Transparent Boundary**: If a repository does not exist or API quotas fail, the system renders an honest 404 error SVG. It never injects synthetic repositories, fake fiduciaries, or mock numbers into production responses.
- **Strict Test Integrity**: Test suites do not short-circuit on `PYTEST_CURRENT_TEST`. All verification exercises production code paths.

### B. High-Concurrency SQLite Storage (WAL Mode)
- Configured with `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=5000;`.
- Allows concurrent read transactions while write operations execute independently without locking readers.
- `PRAGMA foreign_keys=ON;` enforces referential integrity across Repositories, Ads, Impressions, and Clicks.

### C. Anti-Fraud & Deduplication Pipeline
- **Irreversible SHA-256 Audit Hashing**:
  $$\text{ClientHash} = \text{SHA-256}(\text{ClientIP} \mathbin{\Vert} \text{UserAgent} \mathbin{\Vert} \text{SALT})$$
  Ensures user privacy while providing an auditable, persistent fingerprint.
- **Hourly Sliding Window**: Impressions matching `(repo_id, ad_id, client_hash)` within a 60-minute window are filtered to avoid artificial metric inflation.
- **GitHub Camo Proxy Awareness**: Detects GitHub's Camo caching proxy (`is_camo=True`) to handle cached image fetches without distorting maintainer analytics.

### D. Exact 50/50 Financial Ledger
- All revenue calculations use Python's `decimal.Decimal` module to prevent IEEE-754 floating-point inaccuracies.
- Every valid click decrements the sponsor's budget by $CPC$ and immediately splits the value:
  $$\text{MaintainerCut} = \frac{CPC}{2}, \quad \text{PlatformCut} = \frac{CPC}{2}$$
- Unclaimed repositories continue to accumulate maintainer earnings until claimed by their rightful GitHub owner.

---

## 3. Production Deployment Specification

- **Host**: Azure Ubuntu Linux VM `vm-opensponsor` (`172.173.126.151`).
- **Resource Group**: `rg-opensponsor-prod`.
- **Domain**: `https://readmepay.com`.
- **Reverse Proxy**: Caddy 2 container routing traffic to internal FastAPI Uvicorn service on port `8080`.
- **Continuous Sync**: [`fast_deploy.py`](file:///c:/Users/ben/Documents/antigravity/hopeful-bardeen/fast_deploy.py) performs batch SSH base64 file synchronization and container reloading without system downtime.
