# ReadmePay

> **Public Goods Economic Infrastructure for Independent Open-Source Developers.**  
> Turn public README traffic into dependable monthly income &mdash; capitalized by **institutional foundation grants** and matched by **ecosystem tech sponsorships**. ReadmePay guarantees baseline developer micro-stipends from day one, with or without commercial sponsors, through transparent 50/50 revenue sharing and automated global payouts.

[![ReadmePay Badge](https://readmepay.com/badge/tiangolo/fastapi.svg?theme=dark)](https://readmepay.com)
[![Supported By](https://readmepay.com/badge/tiangolo/fastapi.svg?style=backer&theme=dracula)](https://readmepay.com/sponsors)
[![Monthly Goal](https://readmepay.com/badge/tiangolo/fastapi.svg?style=goal&theme=emerald)](https://readmepay.com)
[![Public Goods Grants](https://img.shields.io/badge/Public_Goods-Grants_Endowment-06b6d4?style=flat-square&logo=github)](https://readmepay.com/grants)

---

## 🌐 Live Production Platform

- **Production URL**: [https://readmepay.com](https://readmepay.com)
- **Interactive Badge Studio & Live Generator**: [https://readmepay.com](https://readmepay.com)
- **Sponsor & Campaign Hub**: [https://readmepay.com/sponsors](https://readmepay.com/sponsors)
- **Maintainer Multi-Repo Claiming**: [https://readmepay.com/?tab=maintainer](https://readmepay.com/?tab=maintainer)
- **Interactive API Documentation (Swagger)**: [https://readmepay.com/docs](https://readmepay.com/docs)
- **Zero-Mock Policy**: Strictly real GitHub REST API v3 queries, authentic live sponsors, and deduplicated SHA-256 client tracking. Zero synthetic personas or fake metrics.

---

## 🎨 Badge Suite & Styles

ReadmePay compiles pixel-perfect, W3C-compliant dynamic SVGs on the fly. All badges are responsive, cached with cryptographic SHA-256 ETags (RFC 7232 HTTP 304 negotiation), and support GitHub dark/light mode auto-sensing via `@media (prefers-color-scheme: light)`.

### 1. Glass Banner (`style=banner` or `style=glass`) [Default]
- **Size**: 500 &times; 110 px
- **Features**: GitHub Book Octicon, live star count, language color dot, live pulsing beacon dot, top rim-lighting highlight, and gradient pill CTA button.
- **Snippet**:
  ```markdown
  [![Sponsorship Badge](https://readmepay.com/badge/{owner}/{repo}.svg)](https://readmepay.com/click/active/{repo_id})
  ```

### 2. Neo-Brutalist / Linear Dark (`style=linear`)
- **Size**: 500 &times; 110 px
- **Features**: Pitch-black canvas, terminal monospace typography (`> owner/repo`), ambient violet radial spotlight, developer partner header, and neon outline pill button.
- **Snippet**:
  ```markdown
  [![Sponsorship Badge](https://readmepay.com/badge/{owner}/{repo}.svg?style=linear&theme=linear)](https://readmepay.com/click/active/{repo_id})
  ```

### 3. Dual-Pill Radial Spotlight (`style=spotlight`)
- **Size**: 500 &times; 110 px
- **Features**: Deep slate body with two elevated inset cards: repository identity & segmented chips (`★ stars`, `● language`, `✓ CI`) on one side, featured sponsor card on the other.
- **Snippet**:
  ```markdown
  [![Sponsorship Badge](https://readmepay.com/badge/{owner}/{repo}.svg?style=spotlight&theme=synthwave)](https://readmepay.com/click/active/{repo_id})
  ```

### 4. Compact Micro-Card (`style=compact`)
- **Size**: 500 &times; 110 px (Streamlined horizontal profile)
- **Features**: High horizontal density, single-line headline with inline sponsor chip and sleek arrow hyperlink CTA. Ideal for crowded README headers.
- **Snippet**:
  ```markdown
  [![Sponsorship Badge](https://readmepay.com/badge/{owner}/{repo}.svg?style=compact&theme=nord)](https://readmepay.com/click/active/{repo_id})
  ```

### 5. Dedicated Supporter / Backer Badge (`style=backer` or `style=supporter`)
- **Size**: 320 &times; 28 px
- **Features**: Shows `[ ❤️ SUPPORTED BY | SponsorName → ]`. When unsold, transparently displays `[ ❤️ SUPPORTED BY | Become a Backer → ]` linking directly to the sponsor checkout for that repo.
- **Snippet**:
  ```markdown
  [![Supported by](https://readmepay.com/badge/{owner}/{repo}.svg?style=backer&theme=dracula)](https://readmepay.com/sponsors)
  ```

### 6. Monthly Funding Goal Badge (`style=goal`)
- **Size**: 300 &times; 28 px
- **Features**: Displays `[ ◆ MONTHLY GOAL | 80% Funded ▰▰▰▰▱ ]` with a dynamic, animated visual progress bar tracking the project's monthly financial sustainability.
- **Snippet**:
  ```markdown
  [![Funding Goal](https://readmepay.com/badge/{owner}/{repo}.svg?style=goal&theme=emerald)](https://readmepay.com)
  ```

### 7. Single-Line Shield Pill (`style=shield`)
- **Size**: 520 &times; 28 px
- **Features**: Shields.io-compatible single-line pill with continuous smooth scrolling marquee ticker.
- **Snippet**:
  ```markdown
  [![Sponsor Shield](https://readmepay.com/badge/{owner}/{repo}.svg?style=shield)](https://readmepay.com/click/active/{repo_id})
  ```

---

## 🌈 Theming & Customization Options

Customize any badge by appending URL query parameters:

### Supported Themes (`?theme=...`)
| Theme Key | Visual Palette |
| :--- | :--- |
| **`dark`** *(Default)* | Classic GitHub Obsidian Dark (`#111620`, `#58a6ff`, `#2ea043`) |
| **`cyberpunk`** | Neon Cyan, Hot Magenta & Deep Purple (`#00f0ff`, `#f43f5e`, `#ec4899`) |
| **`emerald`** | Deep Forest Jade & Mint Green (`#10b981`, `#34d399`, `#059669`) |
| **`light`** | Clean GitHub White, Crisp Slate & Royal Blue (`#ffffff`, `#0969da`, `#2da44e`) |
| **`linear`** | Vercel & Linear Dark Violet (`#08090d`, `#a78bfa`, `#7c3aed`) |
| **`dracula`** | Iconic Dracula Neon (`#282a36`, `#8be9fd`, `#50fa7b`, `#bd93f9`) |
| **`nord`** | Arctic Polar Night & Frost Teal (`#242933`, `#88c0d0`, `#5e81ac`) |
| **`monokai`** | Monokai Pro Charcoal, Gold & Ruby (`#1e1f1c`, `#66d9ef`, `#f92672`) |
| **`synthwave`** | 80s Sunset Grid Pink, Cyan & Violet (`#1a102f`, `#01cdfe`, `#ff71ce`) |

### Marquee Ticker Option (`?marquee=true`)
Enables smooth right-to-left scrolling on the sponsor headline across any badge format:
```markdown
[![Sponsor](https://readmepay.com/badge/pallets/flask.svg?marquee=true)](https://readmepay.com/click/active/1)
```

### Sponsor Positioning (`?sponsor_pos=left` vs `?sponsor_pos=right`)
- **`sponsor_pos=right`** *(Default)*: Repo identity on the left, sponsor on the right.
- **`sponsor_pos=left`**: Prioritize the sponsor on the left edge.

### Stat Toggles
- **`hide_stars=true`**: Omit star counter badge.
- **`hide_ci=true`**: Omit CI/CD status pill.

---

## 💰 Economic Model & Revenue Sharing

ReadmePay operates on a transparent **50/50 revenue split**:
- **50% directly to the Maintainer**: Credited instantly upon every verified, deduplicated click.
- **50% to Platform Infrastructure**: Covers cloud compute, SVG compilation, GitHub API sync, and payment processor fees.

### Fraud Prevention & Deduplication
- Every impression is hashed using an irreversible **SHA-256 client audit hash** (`IP:User-Agent:Salt`).
- Deduplication prevents artificial inflation using a **1-hour sliding-window** policy.
- GitHub Camo proxy image requests (`is_camo=True`) are identified and handled honestly.

---

## 🚀 Workflows

### For Open-Source Maintainers
1. **Connect with GitHub OAuth**: Click **"Claim Repo"** on [readmepay.com](https://readmepay.com) and authenticate with GitHub.
2. **Auto-Enrolled Portfolio**: All public repositories you own or maintain are automatically imported into your maintainer portfolio.
3. **Copy Badge Snippet**: Pick your preferred badge style and paste the markdown into your README.md.
4. **Automated Monthly Payouts**: Configure your payout address (PayPal email or Crypto wallet) to receive automatic monthly disbursements.

### For Tech Sponsors & Advertisers
1. **Open the Sponsor Hub**: Navigate to [https://readmepay.com/sponsors](https://readmepay.com/sponsors).
2. **Create Campaign**: Enter brand name, headline pitch, click destination URL, and budget.
3. **Targeting**:
   - **Language Ecosystem**: Target specific programming languages (e.g. *Python*, *Rust*, *TypeScript*, *Go*).
   - **Tier 0 Dedicated Sponsorship**: Enter a specific repo (e.g. `tiangolo/fastapi`) to become that project's exclusive backer.
4. **Fund Deposit**: Instant checkout via **PayPal Checkout** or **Crypto (USDC / Multi-currency)**.
5. **Real-time Analytics**: Monitor delivered impressions, clicks, CTR, and remaining budget in the advertiser dashboard.

---

## 🛠️ API Reference

### Badge Rendering
- `GET /badge/{owner}/{repo}.svg`
  - Query params: `style`, `theme`, `marquee`, `sponsor_pos`, `hide_stars`, `hide_ci`.
  - Headers: Supports `If-None-Match` for HTTP 304 validation.
  - Returns: `image/svg+xml; charset=utf-8`.

### Shields.io Dynamic Endpoint Contract
- `GET /badge/{owner}/{repo}/shield.json`
  - Returns Shields.io SchemaVersion 1 JSON for native Shields.io badge rendering.

### Click-Through Redirect
- `GET /click/{ad_id}/{repo_id}`: Logs verified click event and returns HTTP 302 redirect to sponsor URL.
- `GET /click/active/{repo_id}`: Dynamically resolves active matched sponsor for repo and redirects.

### Revenue & Inventory
- `GET /revenue/{repo_id}`: Financial ledger report (gross revenue, maintainer earnings, platform cut, clicks).
- `GET /api/inventory/repos`: Paginated catalog of registered repositories.
- `GET /api/inventory/ads`: Active sponsor campaigns catalog.
- `POST /api/inventory/ads`: Create and register a new sponsor ad campaign.

---

## 💻 Local Development & Testing

### Prerequisites
- Python 3.12+
- Docker & Docker Compose (optional for production container deployment)

### Setup
```bash
# Clone repository
git clone https://github.com/your-org/readmepay.git
cd readmepay

# Install dependencies
pip install -r requirements.txt

# Run database table initialization and seeds
python start.py --init-db

# Start local server with hot reload
python start.py --reload
```

### Running the Test Suite
The test suite contains **814 automated tests** covering E2E scenarios, XML injection hardening, SVG dimension contracts, revenue accounting, and payment flows:
```bash
# Run full test suite
python -m pytest

# Run badge and XML tests only
python -m pytest tests/test_badge_svg.py tests/test_challenger_m2_svg_xml.py
```

---

## 📄 License

ReadmePay is open-source software licensed under the [MIT License](LICENSE).
