# ReadmePay Badge Visual & Theming Specification

ReadmePay features 7 distinct badge designs crafted specifically for open-source READMEs, documentation headers, and developer portfolios.

All badges are built with valid XML SVG, pure inline vector graphics, responsive scaling, and automatic dark/light theme adaptation via standard SVG CSS `@media (prefers-color-scheme: light)`.

---

## 1. Badge Styles Matrix

| Style Key | Canonical Dimensions | Best Suited For | Visual Highlights |
| :--- | :---: | :--- | :--- |
| **`banner`** / **`glass`** *(Default)* | `500 × 110 px` | README top hero banner | Glassmorphism, live pulsing beacon dot, top rim-light, pill CTA button. |
| **`linear`** | `500 × 110 px` | Minimalist / CLI tools | Neo-brutalist dark canvas, terminal typography (`> repo`), radial violet glow. |
| **`spotlight`** | `500 × 110 px` | High-traffic developer libraries | Dual inset cards: author identity with star chips, spotlighted sponsor. |
| **`compact`** | `500 × 110 px` | Dense README tables of contents | Streamlined single-row banner, inline sponsor pill, minimal footprint. |
| **`backer`** / **`supporter`** | `320 × 28 px` | Header badge cluster | Shows `[ ❤️ SUPPORTED BY | Sponsor → ]` or `[ Become a Backer → ]`. |
| **`goal`** | `300 × 28 px` | Crowdfunding & community goals | Shows `[ ◆ MONTHLY GOAL | 80% Funded ▰▰▰▰▱ ]` with animated progress fill. |
| **`shield`** | `520 × 28 px` | Shields.io badge rows | Standard 28px height with continuous smooth marquee ticker. |

---

## 2. Color Palettes & Themes

Every badge style supports all 9 developer palettes via `?theme=<name>`.

### Theme Palettes

#### 1. `dark` (Default)
- **Canvas / Background**: `#0d1117` &rarr; `#161b22`
- **Border**: `#30363d`
- **Primary Text**: `#f0f6fc`
- **Accent Color**: `#58a6ff` (GitHub Blue)
- **Success / Star**: `#2ea043`

#### 2. `cyberpunk`
- **Canvas / Background**: `#0d0221` &rarr; `#1a0933`
- **Border**: `#f43f5e`
- **Primary Text**: `#fdf4ff`
- **Accent Color**: `#00f0ff` (Neon Cyan)
- **Success / Star**: `#ff007f` (Hot Magenta)

#### 3. `emerald`
- **Canvas / Background**: `#062016` &rarr; `#0b3b29`
- **Border**: `#059669`
- **Primary Text**: `#ecfdf5`
- **Accent Color**: `#34d399` (Mint Green)
- **Success / Star**: `#10b981`

#### 4. `light`
- **Canvas / Background**: `#ffffff` &rarr; `#f6f8fa`
- **Border**: `#d0d7de`
- **Primary Text**: `#1f2328`
- **Accent Color**: `#0969da` (Royal Blue)
- **Success / Star**: `#1a7f37`

#### 5. `linear`
- **Canvas / Background**: `#08090d` &rarr; `#0f1117`
- **Border**: `#2e303e`
- **Primary Text**: `#f4f4f5`
- **Accent Color**: `#a78bfa` (Electric Violet)
- **Success / Star**: `#7c3aed`

#### 6. `dracula`
- **Canvas / Background**: `#282a36` &rarr; `#1e1f29`
- **Border**: `#6272a4`
- **Primary Text**: `#f8f8f2`
- **Accent Color**: `#bd93f9` (Dracula Purple)
- **Success / Star**: `#50fa7b` (Dracula Green)

#### 7. `nord`
- **Canvas / Background**: `#242933` &rarr; `#2e3440`
- **Border**: `#4c566a`
- **Primary Text**: `#eceff4`
- **Accent Color**: `#88c0d0` (Frost Cyan)
- **Success / Star**: `#a3be8c` (Aurora Green)

#### 8. `monokai`
- **Canvas / Background**: `#1e1f1c` &rarr; `#272822`
- **Border**: `#5c5855`
- **Primary Text**: `#f8f8f2`
- **Accent Color**: `#66d9ef` (Monokai Blue)
- **Success / Star**: `#a6e22e` (Monokai Green)

#### 9. `synthwave`
- **Canvas / Background**: `#1a102f` &rarr; `#2b1055`
- **Border**: `#ff71ce`
- **Primary Text**: `#fff1f2`
- **Accent Color**: `#01cdfe` (Neon Blue)
- **Success / Star**: `#ffe600` (Electric Yellow)

---

## 3. Query Parameter Controls

### `?marquee=true`
Activates an animated ticker on the sponsor headline across all banner formats. When enabled, long marketing headlines smoothly scroll right-to-left using native SVG `<animate>` elements.

### `?sponsor_pos=left` vs `?sponsor_pos=right`
- `right` *(default)*: Standard layout. Left card showcases the repository identity (`owner/repo`, star count, language dot); right card showcases the sponsor campaign.
- `left`: Sponsor-first layout. Puts the sponsor card on the left and the repository stats on the right.

### `?hide_stars=true`
Removes the star counter badge. Useful for newly launched projects or repositories with hidden metrics.

### `?hide_ci=true`
Removes the CI/CD passing pill.

---

## 4. Markdown Embedding Examples

### Banner Style (Default Dark)
```markdown
[![ReadmePay Badge](https://readmepay.com/badge/facebook/react.svg)](https://readmepay.com/click/active/10)
```

### Linear Dark Minimalist
```markdown
[![ReadmePay Badge](https://readmepay.com/badge/astral-sh/uv.svg?style=linear&theme=linear)](https://readmepay.com/click/active/10)
```

### Cyberpunk Dual-Pill Spotlight with Marquee
```markdown
[![ReadmePay Badge](https://readmepay.com/badge/tokio-rs/tokio.svg?style=spotlight&theme=cyberpunk&marquee=true)](https://readmepay.com/click/active/10)
```

### Dedicated Supporter Badge
```markdown
[![Supported By](https://readmepay.com/badge/facebook/react.svg?style=backer&theme=dracula)](https://readmepay.com/sponsors)
```

### Monthly Sustainability Goal Badge
```markdown
[![Monthly Goal](https://readmepay.com/badge/facebook/react.svg?style=goal&theme=emerald)](https://readmepay.com)
```

### Shields.io Marquee Pill
```markdown
[![Sponsor Shield](https://readmepay.com/badge/facebook/react.svg?style=shield)](https://readmepay.com/click/active/10)
```
