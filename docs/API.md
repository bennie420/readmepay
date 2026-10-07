# ReadmePay REST API Specification

ReadmePay provides a high-performance REST and SVG rendering API engineered for reliability, zero-mock authenticity, and sub-millisecond badge delivery.

All endpoints are hosted at `https://readmepay.com`. Interactive OpenAPI Swagger documentation is available at `https://readmepay.com/docs`.

---

## 1. Badge Rendering & Embeds

### `GET /badge/{owner}/{repo}.svg`
Compiles and serves a dynamic, responsive W3C-compliant SVG badge for a GitHub repository.

#### URL Parameters
- `owner` *(string, required)*: GitHub organization or username (e.g., `tiangolo`, `pallets`).
- `repo` *(string, required)*: Repository name (e.g., `fastapi`, `flask`).

#### Query Parameters
| Parameter | Type | Default | Options | Description |
| :--- | :---: | :---: | :--- | :--- |
| `style` | string | `banner` | `banner`, `glass`, `linear`, `spotlight`, `compact`, `backer`, `supporter`, `goal`, `shield` | Visual template layout. |
| `theme` | string | `dark` | `dark`, `cyberpunk`, `emerald`, `light`, `linear`, `dracula`, `nord`, `monokai`, `synthwave` | Color palette. |
| `marquee` | boolean | `false` | `true`, `false` | Enables right-to-left marquee animation on sponsor text. |
| `sponsor_pos` | string | `right` | `left`, `right` | Horizontal position of the sponsor card on banner styles. |
| `hide_stars` | boolean | `false` | `true`, `false` | Omits the live GitHub star counter badge. |
| `hide_ci` | boolean | `false` | `true`, `false` | Omits the live GitHub Actions CI/CD status pill. |

#### HTTP Response
- **Status**: `200 OK`
- **Headers**:
  - `Content-Type: image/svg+xml; charset=utf-8`
  - `Cache-Control: public, max-age=3600`
  - `ETag: W/"<sha256-hash>"`
- **HTTP 304 Not Modified**: Honored when matching `If-None-Match` header is sent.
- **HTTP 404 Not Found**: If repository does not exist on GitHub, returns transparent error SVG:
  ```xml
  <svg width="500" height="110" ...>
    <text>404 Not Found</text>
    <text>The requested repository could not be found.</text>
  </svg>
  ```

---

### `GET /badge/{owner}/{repo}/shield.json`
Returns Shields.io SchemaVersion 1 endpoint data for embedding ReadmePay within custom Shields.io badges.

#### HTTP Response
```json
{
  "schemaVersion": 1,
  "label": "sponsor",
  "message": "Acme Cloud • Deploy Faster",
  "color": "58a6ff",
  "labelColor": "161b22",
  "style": "flat-square"
}
```

---

## 2. Click Redirection & Analytics

### `GET /click/{ad_id}/{repo_id}`
Verifies click authenticity, deducts CPC from sponsor balance, credits 50% to maintainer ledger, and issues an immediate HTTP 302 redirect.

#### URL Parameters
- `ad_id` *(integer, required)*: Unique database ID of the sponsor campaign.
- `repo_id` *(integer, required)*: Database ID of the repository where the badge was clicked.

#### Headers Captured for Fraud Prevention
- `X-Forwarded-For` / Client IP
- `User-Agent`
- `Referer`

#### HTTP Response
- **Status**: `302 Found`
- **Location**: Destination target URL configured by the sponsor (e.g., `https://sponsor.com?ref=readmepay`).

---

### `GET /click/active/{repo_id}`
Dynamic resolution endpoint. Looks up the currently active matched sponsor for the repository and redirects to `/click/{ad_id}/{repo_id}`.

#### HTTP Response
- **Status**: `302 Found` to active sponsor URL (or `https://readmepay.com` if no ad active).

---

## 3. GitHub OAuth Authentication

### `GET /api/auth/github/login`
Redirects the maintainer to the GitHub OAuth consent authorization screen.

#### Query Parameters
- `repo_owner` *(optional)*: Specific owner intent to claim.
- `repo_name` *(optional)*: Specific repository intent to claim.
- `payout_address` *(optional)*: Initial payout email or wallet.

---

### `GET /api/auth/github/callback`
Exchanges the GitHub OAuth code for an access token, confirms the maintainer's authentic identity, imports all owned repositories into their portfolio, sets a signed `readmepay_user` session cookie, and redirects to `/dashboard?auth=success`.

---

### `GET /api/auth/github/user`
Returns the currently authenticated maintainer's profile and claimed repositories.

#### HTTP Response
```json
{
  "authenticated": true,
  "user": {
    "login": "octocat",
    "id": 583231,
    "avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4",
    "name": "The Octocat",
    "public_repos": 8
  },
  "claimed_repos": [
    {
      "id": 14,
      "owner": "octocat",
      "name": "Hello-World",
      "claimed": true,
      "stars": 2400
    }
  ]
}
```

---

### `GET /api/auth/github/logout`
Clears session cookies and signs out maintainer.

---

## 4. Maintainer Repository Claiming & Snippets

### `POST /api/maintainers/claim-all`
Batch-claims all public GitHub repositories owned by the authenticated maintainer.

#### Request Body
```json
{
  "payout_address": "developer@example.com"
}
```

#### Response
```json
{
  "success": true,
  "claimed_count": 5,
  "updated_count": 0,
  "total_repos": 5,
  "repositories": [
    { "id": 1, "owner": "octocat", "name": "repo-one", "claimed": true },
    { "id": 2, "owner": "octocat", "name": "repo-two", "claimed": true }
  ]
}
```

---

### `POST /api/maintainers/toggle-claim`
Toggles monetization status for a specific repository.

#### Request Body
```json
{
  "repo_id": 14,
  "claimed": false
}
```

---

### `GET /maintainers/snippet/{owner}/{repo}`
Generates copy-pasteable badge markdown, HTML, and RST snippets.

#### Response
```json
{
  "owner": "tiangolo",
  "name": "fastapi",
  "markdown": "[![Sponsor](https://readmepay.com/badge/tiangolo/fastapi.svg)](https://readmepay.com/click/active/42)",
  "html": "<a href=\"https://readmepay.com/click/active/42\"><img src=\"https://readmepay.com/badge/tiangolo/fastapi.svg\" alt=\"Sponsor\" /></a>",
  "rst": ".. image:: https://readmepay.com/badge/tiangolo/fastapi.svg\n   :target: https://readmepay.com/click/active/42",
  "badge_url": "https://readmepay.com/badge/tiangolo/fastapi.svg",
  "click_url": "https://readmepay.com/click/active/42"
}
```

---

## 5. Financial Ledger & Revenue Share

### `GET /revenue/{repo_id}`
Returns the verified 50/50 revenue report for a repository.

#### Response
```json
{
  "repo_id": 42,
  "owner": "tiangolo",
  "name": "fastapi",
  "gross_revenue": "250.00",
  "maintainer_revenue": "125.00",
  "platform_revenue": "125.00",
  "total_clicks": 500,
  "total_impressions": 125000,
  "last_click_at": "2026-10-06T10:45:00Z"
}
```

---

## 6. Sponsor Campaigns & Billing

### `POST /api/inventory/ads`
Creates a new sponsor campaign.

#### Request Body
```json
{
  "sponsor_name": "Supabase",
  "headline": "The Open Source Firebase Alternative",
  "cta_text": "Start Free",
  "click_url": "https://supabase.com?ref=readmepay",
  "target_language": "TypeScript",
  "cost_per_click": "0.50",
  "initial_budget": "500.00"
}
```

---

### `POST /api/billing/paypal/create-order`
Creates a PayPal Checkout Order v2.

#### Request Body
```json
{
  "ad_id": 5,
  "amount": "250.00",
  "currency": "USD"
}
```

---

### `POST /api/billing/paypal/capture-order`
Captures approved PayPal payment and credits campaign budget.

#### Request Body
```json
{
  "order_id": "8XY1234567890",
  "ad_id": 5
}
```

---

### `POST /api/billing/crypto/create-invoice`
Generates a crypto deposit invoice (USDC, SOL, BTC, ETH).

#### Request Body
```json
{
  "ad_id": 5,
  "amount_usd": "250.00",
  "crypto_currency": "USDC"
}
```

---

### `GET /api/billing/payouts/summary`
Summarizes pending unpaid earnings across all maintainers grouped by payment rail (PayPal vs Crypto).

---

### `POST /api/billing/payouts/run-automated`
Executes automated maintainer disbursement batches.
