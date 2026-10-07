"""
Badge Compilation Service (app/services/badge_service.py).

Compiles dynamic SVG badges via Jinja2 with strict XML autoescaping,
performs XML syntax validation via xml.etree.ElementTree, formats numbers,
computes cryptographic SHA-256 ETags, and renders honest error badges.
"""

from __future__ import annotations

import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import jinja2

# Locate app/templates directory
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def should_autoescape(template_name: str | None) -> bool:
    """Strictly autoescape XML/SVG entities for all templates (.svg, .xml, .j2, .svg.j2)."""
    if not template_name:
        return True
    lower = template_name.lower()
    return (
        lower.endswith(".svg")
        or lower.endswith(".xml")
        or lower.endswith(".html")
        or lower.endswith(".j2")
        or ".svg." in lower
        or ".xml." in lower
    )


# Configure Jinja2 environment with strict XML/SVG/HTML autoescape to prevent XSS and XML injection
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
    autoescape=should_autoescape,
    trim_blocks=True,
    lstrip_blocks=True,
)

# Canonical GitHub programming language color mappings
LANGUAGE_COLORS: dict[str, str] = {
    "python": "#3572A5",
    "typescript": "#3178c6",
    "javascript": "#f1e05a",
    "rust": "#dea584",
    "go": "#00ADD8",
    "c++": "#f34b7d",
    "c": "#555555",
    "c#": "#178600",
    "ruby": "#701516",
    "java": "#b07219",
    "php": "#4F5D95",
    "swift": "#F05138",
    "kotlin": "#A97BFF",
    "shell": "#89e051",
    "html": "#e34c26",
    "css": "#563d7c",
    "haskell": "#5e5086",
    "scala": "#c22d40",
    "elixir": "#6e4a7e",
    "clojure": "#db5855",
    "dart": "#00B4AB",
    "lua": "#000080",
    "r": "#198CE7",
    "julia": "#a270ba",
}

DEFAULT_LANGUAGE_COLOR = "#8b949e"


def get_language_color(language: str | None) -> str:
    """Resolve GitHub official hex color for programming language (case-insensitive)."""
    if not language:
        return DEFAULT_LANGUAGE_COLOR
    normalized = language.strip().lower()
    return LANGUAGE_COLORS.get(normalized, DEFAULT_LANGUAGE_COLOR)


def format_stars(stars: int) -> str:
    """
    Format GitHub star count into compact human-readable string.
    Examples:
      0 -> '0'
      950 -> '950'
      1200 -> '1.2k'
      51000 -> '51k'
      68000 -> '68k'
      102800 -> '102.8k'
      1500000 -> '1.5M'
    """
    if not isinstance(stars, (int, float)) or stars < 0:
        return "0"
    stars_int = int(stars)
    if stars_int >= 1_000_000:
        val = stars_int / 1_000_000
        return f"{int(val)}M" if val.is_integer() else f"{val:.1f}M"
    elif stars_int >= 1_000:
        val = stars_int / 1_000
        return f"{int(val)}k" if val.is_integer() else f"{val:.1f}k"
    else:
        return str(stars_int)


def truncate_text(text: str | None, length: int = 30, suffix: str = "...") -> str:
    """Safely truncate text to a maximum length while preserving clean rendering."""
    if not text:
        return ""
    text_str = str(text).strip()
    if len(text_str) <= length:
        return text_str
    cutoff = max(0, length - len(suffix))
    return text_str[:cutoff].rstrip() + suffix


def sanitize_url(url: str | None) -> str:
    """
    Sanitize hyperlink URL against dangerous schemes like javascript: or data:.
    Allows http://, https://, and relative paths.
    """
    if not url:
        return "#"
    clean = str(url).strip()
    lower = clean.lower()
    if lower.startswith("javascript:") or lower.startswith("data:") or lower.startswith("vbscript:"):
        return "#"
    return clean


def get_ci_colors(ci_status: str | None) -> tuple[str, str]:
    """Return (bg_color, text_color) tuple for CI/CD badge pill."""
    if not ci_status:
        return ("#30363d", "#8b949e")
    lower = ci_status.lower()
    if any(w in lower for w in ["fail", "error"]):
        return ("#da3633", "#ffffff")
    elif any(w in lower for w in ["run", "pending", "build"]):
        return ("#9e6a03", "#ffffff")
    elif any(w in lower for w in ["pass", "success"]):
        return ("#238636", "#ffffff")
    else:
        return ("#30363d", "#c9d1d9")


# Register custom filters into Jinja environment
jinja_env.filters["format_stars"] = format_stars
jinja_env.filters["truncate_text"] = truncate_text
jinja_env.filters["sanitize_url"] = sanitize_url
jinja_env.filters["lang_color"] = get_language_color


def validate_svg_xml(svg_text: str) -> ET.Element:
    """
    Strictly validate that the rendered SVG string is syntactically well-formed XML
    with a root <svg> element.

    Raises:
        ValueError: If XML parsing fails or root tag is not svg.
    """
    if not svg_text or not svg_text.strip():
        raise ValueError("Rendered SVG content cannot be empty.")
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:
        raise ValueError(f"Rendered SVG failed XML syntax validation: {exc}") from exc
    tag = root.tag.lower()
    if not tag.endswith("svg"):
        raise ValueError(f"Root XML element must be <svg>, received <{root.tag}>")
    return root


def compute_svg_etag(svg_content: str) -> str:
    """
    Compute a cryptographic SHA-256 HTTP entity tag (ETag) for caching and 304 validation.
    Returns standard RFC 7232 quoted hexadecimal string: '"<sha256-hex>"'.
    """
    digest = hashlib.sha256(svg_content.encode("utf-8")).hexdigest()
    return f'"{digest}"'


THEMES = {
    "dark": {
        "card_bg_0": "#111620", "card_bg_1": "#0b0e14",
        "ad_bg_0": "#161e2b", "ad_bg_1": "#0e141e",
        "border": "#30363d", "border_accent": "#58a6ff",
        "text_title": "#58a6ff", "text_meta": "#e6edf3",
        "text_headline": "#f0f6fc", "text_sponsor": "#ffffff",
        "shield_left": "#161b22", "shield_right": "#0d1117", "shield_border": "#30363d",
        "btn_bg_0": "#238636", "btn_bg_1": "#2ea043", "btn_text": "#ffffff",
        "accent": "#58a6ff", "glow": "#2ea043"
    },
    "cyberpunk": {
        "card_bg_0": "#0f051d", "card_bg_1": "#05020a",
        "ad_bg_0": "#20093b", "ad_bg_1": "#120524",
        "border": "#f43f5e", "border_accent": "#00f0ff",
        "text_title": "#00f0ff", "text_meta": "#fde047",
        "text_headline": "#f43f5e", "text_sponsor": "#00f0ff",
        "shield_left": "#1f0438", "shield_right": "#0a0114", "shield_border": "#00f0ff",
        "btn_bg_0": "#ec4899", "btn_bg_1": "#d946ef", "btn_text": "#ffffff",
        "accent": "#00f0ff", "glow": "#ec4899"
    },
    "emerald": {
        "card_bg_0": "#062319", "card_bg_1": "#02120d",
        "ad_bg_0": "#0b3b2b", "ad_bg_1": "#06241a",
        "border": "#10b981", "border_accent": "#34d399",
        "text_title": "#34d399", "text_meta": "#a7f3d0",
        "text_headline": "#6ee7b7", "text_sponsor": "#34d399",
        "shield_left": "#06281d", "shield_right": "#03140e", "shield_border": "#10b981",
        "btn_bg_0": "#059669", "btn_bg_1": "#10b981", "btn_text": "#ffffff",
        "accent": "#10b981", "glow": "#10b981"
    },
    "light": {
        "card_bg_0": "#ffffff", "card_bg_1": "#f6f8fa",
        "ad_bg_0": "#f6f8fa", "ad_bg_1": "#ffffff",
        "border": "#d0d7de", "border_accent": "#0969da",
        "text_title": "#0969da", "text_meta": "#24292f",
        "text_headline": "#1f2328", "text_sponsor": "#0969da",
        "shield_left": "#f6f8fa", "shield_right": "#ffffff", "shield_border": "#d0d7de",
        "btn_bg_0": "#2da44e", "btn_bg_1": "#2c974b", "btn_text": "#ffffff",
        "accent": "#0969da", "glow": "#2da44e"
    },
    "linear": {
        "card_bg_0": "#08090d", "card_bg_1": "#030407",
        "ad_bg_0": "#13111c", "ad_bg_1": "#0b0a12",
        "border": "#2e2640", "border_accent": "#a78bfa",
        "text_title": "#a78bfa", "text_meta": "#e2e8f0",
        "text_headline": "#f3f4f6", "text_sponsor": "#c084fc",
        "shield_left": "#100e17", "shield_right": "#07060a", "shield_border": "#7c3aed",
        "btn_bg_0": "#7c3aed", "btn_bg_1": "#9333ea", "btn_text": "#ffffff",
        "accent": "#a855f7", "glow": "#a855f7"
    },
    "dracula": {
        "card_bg_0": "#21222c", "card_bg_1": "#282a36",
        "ad_bg_0": "#282a36", "ad_bg_1": "#1e1f29",
        "border": "#6272a4", "border_accent": "#bd93f9",
        "text_title": "#8be9fd", "text_meta": "#f8f8f2",
        "text_headline": "#f1fa8c", "text_sponsor": "#ff79c6",
        "shield_left": "#282a36", "shield_right": "#1e1f29", "shield_border": "#bd93f9",
        "btn_bg_0": "#bd93f9", "btn_bg_1": "#ff79c6", "btn_text": "#282a36",
        "accent": "#50fa7b", "glow": "#bd93f9"
    },
    "nord": {
        "card_bg_0": "#242933", "card_bg_1": "#2e3440",
        "ad_bg_0": "#2e3440", "ad_bg_1": "#3b4252",
        "border": "#4c566a", "border_accent": "#88c0d0",
        "text_title": "#88c0d0", "text_meta": "#eceff4",
        "text_headline": "#e5e9f0", "text_sponsor": "#81a1c1",
        "shield_left": "#2e3440", "shield_right": "#3b4252", "shield_border": "#88c0d0",
        "btn_bg_0": "#5e81ac", "btn_bg_1": "#81a1c1", "btn_text": "#eceff4",
        "accent": "#88c0d0", "glow": "#88c0d0"
    },
    "monokai": {
        "card_bg_0": "#1e1f1c", "card_bg_1": "#272822",
        "ad_bg_0": "#272822", "ad_bg_1": "#1e1f1c",
        "border": "#75715e", "border_accent": "#66d9ef",
        "text_title": "#66d9ef", "text_meta": "#f8f8f2",
        "text_headline": "#a6e22e", "text_sponsor": "#fd971f",
        "shield_left": "#272822", "shield_right": "#1e1f1c", "shield_border": "#a6e22e",
        "btn_bg_0": "#f92672", "btn_bg_1": "#e6db74", "btn_text": "#1e1f1c",
        "accent": "#fd971f", "glow": "#f92672"
    },
    "synthwave": {
        "card_bg_0": "#1a102f", "card_bg_1": "#2b1055",
        "ad_bg_0": "#2b1055", "ad_bg_1": "#1a102f",
        "border": "#ff71ce", "border_accent": "#01cdfe",
        "text_title": "#01cdfe", "text_meta": "#fffb96",
        "text_headline": "#ff71ce", "text_sponsor": "#05ffa1",
        "shield_left": "#241442", "shield_right": "#130924", "shield_border": "#ff71ce",
        "btn_bg_0": "#b967ff", "btn_bg_1": "#ff71ce", "btn_text": "#ffffff",
        "accent": "#05ffa1", "glow": "#ff71ce"
    }
}

# Theme aliases
THEMES["purple"] = THEMES["linear"]
THEMES["sunset"] = THEMES["synthwave"]
THEMES["neon"] = THEMES["cyberpunk"]
THEMES["brutalist"] = THEMES["linear"]

# Style to Template mappings
STYLE_TEMPLATES = {
    "shield": "shield.svg.j2",
    "linear": "badge_linear.svg.j2",
    "brutalist": "badge_linear.svg.j2",
    "neon": "badge_linear.svg.j2",
    "spotlight": "badge_spotlight.svg.j2",
    "pill": "badge_spotlight.svg.j2",
    "dual-pill": "badge_spotlight.svg.j2",
    "compact": "badge_compact.svg.j2",
    "micro": "badge_compact.svg.j2",
    "minimal": "badge_compact.svg.j2",
    "glass": "badge.svg.j2",
    "github": "badge.svg.j2",
    "banner": "badge.svg.j2",
    "backer": "badge_backer.svg.j2",
    "supporter": "badge_backer.svg.j2",
    "sponsor": "badge_backer.svg.j2",
    "powered": "badge_backer.svg.j2",
    "partner": "badge_backer.svg.j2",
    "goal": "badge_goal.svg.j2",
}


def build_badge_svg(
    repo_name: str,
    stars: int,
    language: str | None = None,
    ci_status: str | None = None,
    ad: Any | None = None,
    click_url: str | None = None,
    owner: str | None = None,
    style: str = "banner",
    theme: str = "dark",
    marquee: bool = False,
    sponsor_position: str = "right",
    hide_stars: bool = False,
    hide_ci: bool = False,
) -> str:
    """
    Compile dynamic SVG badge string matching PROJECT.md interface contract.

    Args:
        repo_name: Repository name (e.g. 'flask' or 'requests')
        stars: Live star count (e.g. 68000)
        language: Primary programming language (e.g. 'Python')
        ci_status: CI/CD status ('passing', 'failing', or None)
        ad: Matched Ad model instance, dict, or None
        click_url: Direct click-redirect URL (e.g. '/click/1/1')
        owner: Optional repository owner (e.g. 'pallets')
        style: Badge layout style ('banner', 'linear', 'spotlight', 'compact', 'shield')
        theme: Color theme ('dark', 'cyberpunk', 'emerald', 'light', 'linear', 'dracula', 'nord', 'monokai', 'synthwave')
        marquee: Enable marquee ticker animation on badge (default False on banner, True on shield)
        sponsor_position: 'right' (default) or 'left' for layout
        hide_stars: Whether to hide the star counter
        hide_ci: Whether to hide CI/CD status pill

    Returns:
        Valid XML SVG string.
    """
    norm_style = style.strip().lower() if style else "banner"
    template_name = STYLE_TEMPLATES.get(norm_style, "badge.svg.j2")
    template = jinja_env.get_template(template_name)

    has_ad = ad is not None
    sponsor_name = ""
    headline = ""
    cta_text = "Learn More"

    if has_ad:
        if isinstance(ad, dict):
            sponsor_name = ad.get("sponsor_name", "") or ""
            headline = ad.get("headline", "") or ""
            cta_text = ad.get("call_to_action") or ad.get("cta_text") or "Learn More"
            raw_click_url = click_url or ad.get("click_url", "#")
        else:
            sponsor_name = getattr(ad, "sponsor_name", "") or ""
            headline = getattr(ad, "headline", "") or ""
            cta_text = (
                getattr(ad, "call_to_action", None)
                or getattr(ad, "cta_text", None)
                or "Learn More"
            )
            raw_click_url = click_url or getattr(ad, "click_url", "#")
    else:
        raw_click_url = click_url or "/onboard"

    effective_click_url = sanitize_url(raw_click_url)
    ci_bg_color, ci_text_color = get_ci_colors(ci_status)
    palette = THEMES.get(theme.lower(), THEMES["dark"])

    # For marquee animation in shield, if marquee is disabled or text is short, we can flag it
    should_marquee = marquee is not False and marquee != "0" and marquee != "false"

    rendered = template.render(
        repo_name=repo_name,
        formatted_stars=format_stars(stars),
        language=language.strip() if language and language.strip() else None,
        lang_color=get_language_color(language),
        ci_status=ci_status.strip() if ci_status and ci_status.strip() and not hide_ci else None,
        ci_bg_color=ci_bg_color,
        ci_text_color=ci_text_color,
        has_ad=has_ad,
        owner=owner,
        sponsor_name=sponsor_name,
        headline=headline,
        cta_text=cta_text,
        click_url=effective_click_url,
        theme=theme.lower(),
        palette=palette,
        marquee=should_marquee,
        sponsor_position=sponsor_position.lower(),
        hide_stars=hide_stars,
        hide_ci=hide_ci,
    )

    # Strictly validate XML syntax before returning
    validate_svg_xml(rendered)
    return rendered


def build_error_svg(
    error_title: str | None = None,
    error_message: str | None = None,
    error_code: int | None = None,
    title: str | None = None,
    message: str | None = None,
    status_code: int | None = None,
) -> str:
    """
    Compile honest transparent error SVG badge for non-existent repositories,
    rate limits, or upstream failures. Strictly zero synthetic personas or mock figures.

    Args:
        error_title / title: Human-readable error heading
        error_message / message: Transparent diagnostic explanation
        error_code / status_code: HTTP status code (404, 429, 500, etc.)

    Returns:
        Valid XML SVG string.
    """
    eff_title = error_title or title or "Repository Not Found"
    eff_message = error_message or message or "The requested repository could not be located or verified."
    eff_code = error_code or status_code or 404

    template = jinja_env.get_template("error.svg.j2")
    rendered = template.render(
        error_title=eff_title,
        error_message=eff_message,
        error_code=eff_code,
    )
    validate_svg_xml(rendered)
    return rendered


def compile_and_validate_badge(
    repo_name: str,
    stars: int,
    language: str | None = None,
    ci_status: str | None = None,
    ad: Any | None = None,
    click_url: str | None = None,
    owner: str | None = None,
    style: str = "banner",
    theme: str = "dark",
    marquee: bool = True,
    sponsor_position: str = "right",
    hide_stars: bool = False,
    hide_ci: bool = False,
) -> tuple[str, str]:
    """
    Convenience method compiling badge SVG and computing its SHA-256 ETag.

    Returns:
        Tuple of (svg_content, etag)
    """
    svg_content = build_badge_svg(
        repo_name=repo_name,
        stars=stars,
        language=language,
        ci_status=ci_status,
        ad=ad,
        click_url=click_url,
        owner=owner,
        style=style,
        theme=theme,
        marquee=marquee,
        sponsor_position=sponsor_position,
        hide_stars=hide_stars,
        hide_ci=hide_ci,
    )
    etag = compute_svg_etag(svg_content)
    return svg_content, etag
