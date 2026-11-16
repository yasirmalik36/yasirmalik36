#!/usr/bin/env python3
"""Generate the animated SVG artwork used in the profile README.

Run from the repo root:  python3 tools/build_assets.py
Logos come from Simple Icons (CC0) via tools/icons.json. Items without an
official Simple Icons logo are drawn as monogram tiles instead of fakes.
"""
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
ICONS = json.loads((ROOT / "tools" / "icons.json").read_text())

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'Courier New', monospace"
PURPLE, VIOLET, CYAN, BLUE = "#A78BFA", "#7C3AED", "#22D3EE", "#3B82F6"
INK, MUTED, FAINT = "#F1F5F9", "#A5B4CF", "#64748B"

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, title, css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-labelledby="t"><title id="t">{esc(title)}</title>'
        f"<style>{css}{REDUCED}</style>{body}</svg>\n"
    )


def bg_defs(uid="bg"):
    return (
        f'<linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#0A0A1F"/><stop offset=".55" stop-color="#140B30"/>'
        '<stop offset="1" stop-color="#05192A"/></linearGradient>'
        '<linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{PURPLE}"/><stop offset=".5" stop-color="#818CF8"/>'
        f'<stop offset="1" stop-color="{CYAN}"/></linearGradient>'
        '<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#A78BFA" stop-opacity=".55"/>'
        '<stop offset="1" stop-color="#22D3EE" stop-opacity=".35"/></linearGradient>'
    )


def stars(w, h, n, seed=7):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.choice([0.6, 0.8, 1, 1.2, 1.5])
        d = rnd.uniform(0, 5)
        out.append(f'<circle class="star" cx="{x:.1f}" cy="{y:.1f}" r="{r}" style="animation-delay:{d:.2f}s"/>')
    return "".join(out)


def lighten(hexs, amt=0.3):
    r, g, b = (int(hexs[i:i + 2], 16) for i in (0, 2, 4))
    return "%02X%02X%02X" % tuple(round(c + (255 - c) * amt) for c in (r, g, b))


def luminance(hexs):
    r, g, b = (int(hexs[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


# ---------------------------------------------------------------- mascot ---
def mascot(x, y, scale=1.0, wave=False):
    """'Byte' — a friendly little robot. Pure shapes, CSS-animated."""
    arm = (
        '<g class="wave" style="transform-origin:96px 92px">'
        '<rect x="92" y="62" width="10" height="34" rx="5" fill="#8B5CF6"/>'
        '<circle cx="97" cy="60" r="8" fill="#C4B5FD"/></g>'
        if wave
        else '<rect x="92" y="88" width="10" height="28" rx="5" fill="#8B5CF6"/>'
    )
    return (
        f'<g transform="translate({x} {y}) scale({scale})"><g class="float">'
        '<ellipse cx="60" cy="168" rx="38" ry="6" fill="#000" opacity=".35" class="shadow"/>'
        # antenna
        '<line x1="60" y1="10" x2="60" y2="28" stroke="#C4B5FD" stroke-width="3" stroke-linecap="round"/>'
        f'<circle class="bulb" cx="60" cy="8" r="6" fill="{CYAN}"/>'
        # head
        '<rect x="18" y="26" width="84" height="66" rx="22" fill="url(#botBody)" stroke="#C4B5FD" stroke-opacity=".6"/>'
        '<rect x="28" y="38" width="64" height="42" rx="14" fill="#0B1024"/>'
        f'<g class="blink" style="transform-origin:60px 56px"><circle cx="46" cy="56" r="6" fill="{CYAN}"/>'
        f'<circle cx="74" cy="56" r="6" fill="{CYAN}"/></g>'
        '<path d="M50 68 Q60 75 70 68" stroke="#F0ABFC" stroke-width="3" fill="none" stroke-linecap="round"/>'
        '<circle cx="36" cy="68" r="4" fill="#F472B6" opacity=".5"/><circle cx="84" cy="68" r="4" fill="#F472B6" opacity=".5"/>'
        # body + arms
        '<rect x="30" y="96" width="60" height="50" rx="16" fill="url(#botBody)" stroke="#C4B5FD" stroke-opacity=".5"/>'
        '<rect x="18" y="100" width="10" height="28" rx="5" fill="#8B5CF6"/>'
        f"{arm}"
        # laptop
        '<rect x="34" y="112" width="52" height="30" rx="4" fill="#1E1B4B" stroke="#818CF8"/>'
        f'<text x="60" y="132" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{CYAN}" font-weight="700">&lt;/&gt;</text>'
        '<rect x="44" y="146" width="10" height="16" rx="4" fill="#6D28D9"/><rect x="66" y="146" width="10" height="16" rx="4" fill="#6D28D9"/>'
        "</g></g>"
    )


MASCOT_DEFS = (
    '<linearGradient id="botBody" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#A78BFA"/><stop offset="1" stop-color="#6D28D9"/></linearGradient>'
)
MASCOT_CSS = (
    ".float{animation:float 4s ease-in-out infinite}"
    "@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}"
    ".blink{animation:blink 5s infinite}"
    "@keyframes blink{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}"
    ".bulb{animation:bulb 2s ease-in-out infinite}"
    "@keyframes bulb{0%,100%{opacity:.5}50%{opacity:1}}"
    ".wave{animation:wave 2.4s ease-in-out infinite}"
    "@keyframes wave{0%,60%,100%{transform:rotate(0)}70%{transform:rotate(-18deg)}80%{transform:rotate(12deg)}90%{transform:rotate(-12deg)}}"
)
STAR_CSS = (
    ".star{fill:#E0E7FF;animation:tw 4s ease-in-out infinite}"
    "@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}"
)


# ------------------------------------------------------------------ hero ---
def hero():
    W, H = 1000, 420
    phrases = [
        "Enterprise .NET 10 & ASP.NET Core APIs",
        "Angular 20 apps with Signals & NgRx",
        "LLM, RAG & agentic AI workflows",
        "Payment switches at 1M+ tx / day",
        "Saudi CIT & Zakat automation @ Deloitte",
    ]
    n, slot = len(phrases), 3.6
    dur = n * slot
    clips, texts = [], []
    for i, p in enumerate(phrases):
        wpx = len(p) * 11.5 + 6
        a, b, c, d = (i * slot) / dur, (i * slot + 1.3) / dur, (i * slot + slot - 0.35) / dur, ((i + 1) * slot) / dur
        kt = sorted({0.0, a, b, c, d, 1.0})
        vals = {0.0: 0, a: 0, b: wpx, c: wpx, d: 0, 1.0: 0}
        clips.append(
            f'<clipPath id="tc{i}"><rect x="76" y="230" height="32" width="0">'
            f'<animate attributeName="width" dur="{dur}s" repeatCount="indefinite" '
            f'keyTimes="{";".join(f"{k:.4f}" for k in kt)}" values="{";".join(f"{vals[k]:.0f}" for k in kt)}"/>'
            "</rect></clipPath>"
        )
        texts.append(
            f'<text clip-path="url(#tc{i})" x="78" y="252" font-family="{MONO}" font-size="19" fill="{CYAN}">{esc(p)}</text>'
        )
    chips = [("5+ years", PURPLE), ("1M+ tx / day", CYAN), ("99.9% uptime", "#34D399"), ("LLM · RAG · Agents", "#F0ABFC")]
    cx, chip_svg = 60, []
    for label, col in chips:
        w = len(label) * 8.2 + 28
        chip_svg.append(
            f'<g transform="translate({cx} 292)"><rect width="{w:.0f}" height="30" rx="15" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-opacity=".55"/>'
            f'<text x="{w/2:.0f}" y="20" text-anchor="middle" font-family="{SANS}" font-size="13.5" font-weight="600" fill="{col}">{esc(label)}</text></g>'
        )
        cx += w + 10
    body = (
        f"<defs>{bg_defs()}{MASCOT_DEFS}"
        '<radialGradient id="g1" cx=".2" cy=".2" r=".6"><stop offset="0" stop-color="#7C3AED" stop-opacity=".45"/><stop offset="1" stop-color="#7C3AED" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="g2" cx=".85" cy=".8" r=".55"><stop offset="0" stop-color="#06B6D4" stop-opacity=".35"/><stop offset="1" stop-color="#06B6D4" stop-opacity="0"/></radialGradient>'
        '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#A78BFA" stroke-opacity=".06"/></pattern>'
        + "".join(clips) + "</defs>"
        + ''
        f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>'
        f'<rect width="{W}" height="{H}" rx="24" fill="url(#grid)"/>'
        f'<rect class="glow" width="{W}" height="{H}" rx="24" fill="url(#g1)"/>'
        f'<rect class="glow2" width="{W}" height="{H}" rx="24" fill="url(#g2)"/>'
        f"{stars(W, H, 46)}"
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="24" fill="none" stroke="url(#edge)"/>'
        # status pill
        '<g transform="translate(60 48)"><rect width="282" height="30" rx="15" fill="#22C55E" fill-opacity=".08" stroke="#22C55E" stroke-opacity=".45"/>'
        '<circle class="pulse" cx="18" cy="15" r="5" fill="#22C55E"/>'
        f'<text x="32" y="20" font-family="{SANS}" font-size="13.5" font-weight="600" fill="#86EFAC">Senior Consultant @ Deloitte · Remote</text></g>'
        f'<text x="60" y="124" font-family="{SANS}" font-size="24" fill="{MUTED}">Hi there, I\'m</text>'
        f'<text x="58" y="182" font-family="{SANS}" font-size="58" font-weight="800" fill="url(#brand)" letter-spacing="-1">Yasir Mehmood</text>'
        f'<text x="60" y="214" font-family="{SANS}" font-size="20" font-weight="600" fill="{INK}">Full-Stack (.NET &amp; Angular) &amp; AI Engineer</text>'
        f'<text x="60" y="252" font-family="{MONO}" font-size="19" fill="{FAINT}">&gt;</text>'
        + "".join(texts)
        + "".join(chip_svg)
        + f'<text x="60" y="364" font-family="{SANS}" font-size="14" fill="{FAINT}">Islamabad, Pakistan  ·  fintech · healthcare · tax tech · AI</text>'
        # mascot + bubble
        + '<g transform="translate(700 70)"><g class="bubble">'
        '<rect x="0" y="0" width="230" height="52" rx="16" fill="#1E1B4B" stroke="#818CF8" stroke-opacity=".6"/>'
        '<path d="M150 52 L162 68 L170 52Z" fill="#1E1B4B" stroke="#818CF8" stroke-opacity=".6"/>'
        '<rect x="148" y="48" width="24" height="6" fill="#1E1B4B"/>'
        f'<text x="115" y="22" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{MUTED}">Byte says:</text>'
        f'<text x="115" y="41" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{INK}">Hello, world!</text></g></g>'
        + mascot(745, 150, 1.45, wave=True)
    )
    css = (
        STAR_CSS
        + MASCOT_CSS
        + ".glow{animation:gl 8s ease-in-out infinite}.glow2{animation:gl 8s ease-in-out infinite reverse}"
        "@keyframes gl{0%,100%{opacity:.7}50%{opacity:1}}"
        ".pulse{animation:pu 1.8s ease-in-out infinite}@keyframes pu{0%,100%{opacity:1}50%{opacity:.3}}"
        ".bubble{animation:float 4s ease-in-out infinite;animation-delay:-1s}"
    )
    return svg(W, H, body, "Yasir Mehmood — Senior Consultant, Full-Stack .NET & Angular and AI Engineer", css)


# --------------------------------------------------------------- divider ---
def divider():
    W, H = 1000, 18
    body = (
        '<defs><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#A78BFA" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#A78BFA"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
        f'<rect y="8" width="{W}" height="2" fill="url(#l)"/>'
        '<rect class="sh" y="7" width="140" height="4" rx="2" fill="url(#s)"/>'
        f'<circle cx="{W/2}" cy="9" r="4" fill="#22D3EE"/><circle cx="{W/2}" cy="9" r="8" fill="none" stroke="#22D3EE" stroke-opacity=".4"/>'
    )
    css = ".sh{animation:sh 5s linear infinite}@keyframes sh{0%{transform:translateX(-160px)}100%{transform:translateX(1000px)}}"
    return svg(W, H, body, "section divider", css)


# ----------------------------------------------------------- tech cards ---
def tile(item, x, y):
    key, label = item
    size = 52
    if key.startswith("mono:"):
        _, txt, col = key.split(":")
        col = col.lstrip("#")
        inner = (
            f'<text x="{size/2}" y="{size/2+5.5}" text-anchor="middle" font-family="{SANS}" '
            f'font-size="{16 if len(txt) <= 3 else 12.5}" font-weight="800" fill="#{col if luminance(col) > .25 else "E2E8F0"}">{esc(txt)}</text>'
        )
        base = col
    else:
        ic = ICONS[key]
        base = ic["hex"]
        fill = "#" + lighten(base, 0.25) if luminance(base) > 0.22 else "#E2E8F0"
        inner = f'<g transform="translate(13 13) scale(1.083)"><path d="{ic["path"]}" fill="{fill}"/></g>'
    return (
        f'<g transform="translate({x} {y})" class="tile">'
        f'<rect width="{size}" height="{size}" rx="14" fill="#{base}" fill-opacity=".14" stroke="#{base if luminance(base) > .22 else "94A3B8"}" stroke-opacity=".45"/>'
        f"{inner}"
        f'<text x="{size/2}" y="{size+17}" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{MUTED}">{esc(label)}</text></g>'
    )


def tech_card(title, emoji_path, items, accent):
    W = 490
    per_row = 6
    rows = math.ceil(len(items) / per_row)
    H = 74 + rows * 86 + 8
    tiles = []
    gap = (W - 48 - per_row * 52) / (per_row - 1)
    for i, it in enumerate(items):
        r, c = divmod(i, per_row)
        tiles.append(tile(it, 24 + c * (52 + gap), 70 + r * 86))
    body = (
        f"<defs>{bg_defs()}</defs>"
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="url(#bg)" stroke="url(#edge)"/>'
        f'<rect x="24" y="22" width="30" height="30" rx="9" fill="{accent}" fill-opacity=".15" stroke="{accent}" stroke-opacity=".6"/>'
        f'<path d="{emoji_path}" transform="translate(30 28)" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<text x="66" y="43" font-family="{SANS}" font-size="18" font-weight="700" fill="{INK}">{esc(title)}</text>'
        f'<rect class="bar" x="66" y="52" width="60" height="3" rx="1.5" fill="{accent}"/>'
        + "".join(tiles)
    )
    css = ".bar{animation:bar 3s ease-in-out infinite}@keyframes bar{0%,100%{width:60px;opacity:.6}50%{width:120px;opacity:1}}"
    return svg(W, H, body, f"{title}: " + ", ".join(l for _, l in items), css)


# lucide-style 18px glyphs
G_SERVER = "M2 2h14v5H2zM2 11h14v5H2zM5 4.5h.01M5 13.5h.01"
G_LAYOUT = "M2 2h14v14H2zM2 7h14M7 7v9"
G_SPARK = "M9 1l2 5 5 2-5 2-2 5-2-5-5-2 5-2z"
G_CLOUD = "M5 15h8a4 4 0 0 0 0-8 5 5 0 0 0-9.6 1.5A3.3 3.3 0 0 0 5 15z"
G_DB = "M9 2c4 0 7 1.3 7 3s-3 3-7 3-7-1.3-7-3 3-3 7-3zM2 5v8c0 1.7 3 3 7 3s7-1.3 7-3V5M2 9c0 1.7 3 3 7 3s7-1.3 7-3"
G_SHIELD = "M9 1l7 3v5c0 4-3 7-7 8-4-1-7-4-7-8V4zM6 9l2 2 4-4"

CARDS = {
    "stack-backend": ("Backend Engineering", G_SERVER, PURPLE, [
        ("dotnet", ".NET 10 / 8"), ("mono:C#:#9B4F96", "C#"), ("mono:ASP:#7C6CF2", "ASP.NET Core"),
        ("mono:EF:#8B5CF6", "EF Core"), ("mono:SR:#6D8BFF", "SignalR"), ("mono:gRPC:#3FA9B5", "gRPC"),
        ("rabbitmq", "RabbitMQ"), ("mono:MT:#2BB3A3", "MassTransit"), ("mono:CQRS:#A78BFA", "CQRS"),
        ("mono:OBX:#F59E0B", "Outbox"), ("mono:AOT:#60A5FA", "Native AOT"), ("swagger", "OpenAPI"),
    ]),
    "stack-frontend": ("Frontend Engineering", G_LAYOUT, CYAN, [
        ("mono:NG:#E23237", "Angular 20"), ("mono:SIG:#F472B6", "Signals"), ("typescript", "TypeScript"),
        ("reactivex", "RxJS"), ("ngrx", "NgRx"), ("materialdesign", "Material"),
        ("react", "React"), ("nextdotjs", "Next.js"), ("tailwindcss", "Tailwind"),
    ]),
    "stack-ai": ("Python & Generative AI", G_SPARK, "#F0ABFC", [
        ("python", "Python"), ("fastapi", "FastAPI"), ("flask", "Flask"), ("openai", "OpenAI"),
        ("anthropic", "Claude"), ("googlegemini", "Gemini"), ("mono:AOAI:#0EA5E9", "Azure OpenAI"),
        ("langchain", "LangChain"), ("mono:FAISS:#3B82F6", "FAISS"), ("mono:PC:#22C55E", "Pinecone"),
        ("mono:RAG:#A78BFA", "RAG"), ("mono:MCP:#F97316", "MCP / Agents"),
    ]),
    "stack-cloud": ("Cloud & DevOps", G_CLOUD, BLUE, [
        ("mono:Az:#0EA5E9", "Azure"), ("mono:AKS:#3B82F6", "AKS"), ("amazonwebservices", "AWS"),
        ("docker", "Docker"), ("kubernetes", "Kubernetes"), ("helm", "Helm"),
        ("githubactions", "GH Actions"), ("mono:ADO:#2563EB", "Azure DevOps"), ("mono:KV:#38BDF8", "Key Vault"),
    ]),
    "stack-data": ("Databases & Testing", G_DB, "#34D399", [
        ("mono:SQL:#EF4444", "SQL Server"), ("postgresql", "PostgreSQL"), ("mysql", "MySQL"),
        ("redis", "Redis"), ("mono:xU:#8B5CF6", "xUnit"), ("mono:MS:#A78BFA", "MSTest"),
        ("jest", "Jest"), ("pytest", "Pytest"), ("mono:Q:#F59E0B", "Query tuning"),
    ]),
    "stack-security": ("Security & Enterprise", G_SHIELD, "#FBBF24", [
        ("mono:SSO:#F59E0B", "SSO"), ("jsonwebtokens", "OAuth2 / JWT"), ("mono:RBAC:#FB923C", "RBAC"),
        ("mono:PCI:#22C55E", "PCI-DSS"), ("mono:HIPAA:#38BDF8", "HIPAA"), ("mono:KYC:#E879F9", "AML / KYC"),
        ("odoo", "Odoo 19"), ("mono:ZKT:#14B8A6", "CIT / Zakat"), ("mono:SD:#A78BFA", "System design"),
    ]),
}


# ---------------------------------------------------------------- impact ---
def impact():
    W, H = 1000, 300
    m = [
        ("1M+", "daily interbank transactions", "1LINK Payment Switch · AKSA-SDS", 1.0, PURPLE),
        ("99.9%", "uptime on a PCI-DSS switch", "RabbitMQ · MassTransit · Outbox", 1.0, CYAN),
        ("10K+", "retailers on real-time dashboards", "Jazz Retailer Portal · 60% faster", 1.0, "#34D399"),
        ("~30%", "fewer AML false positives", "Fraud detection across 5+ banks", 1.0, "#F0ABFC"),
        ("35%", "fewer support tickets via RAG", "100K+ chunks · +30% CSAT · Markitech.AI", 1.0, "#FBBF24"),
        ("<200ms", "clinical alerts in a HIPAA EHR", "SignalR + Redis · MTBC CareCloud", 1.0, BLUE),
    ]
    cards = []
    cw, ch = 300, 116
    for i, (v, l, src, frac, col) in enumerate(m):
        r, c = divmod(i, 3)
        x, y = 30 + c * (cw + 20), 40 + r * (ch + 16)
        cards.append(
            f'<g transform="translate({x} {y})">'
            f'<rect width="{cw}" height="{ch}" rx="16" fill="#FFFFFF" fill-opacity=".035" stroke="{col}" stroke-opacity=".35"/>'
            f'<text x="20" y="46" font-family="{SANS}" font-size="34" font-weight="800" fill="{col}">{esc(v)}</text>'
            f'<text x="20" y="70" font-family="{SANS}" font-size="14" font-weight="600" fill="{INK}">{esc(l)}</text>'
            f'<text x="20" y="90" font-family="{SANS}" font-size="11.5" fill="{FAINT}">{esc(src)}</text>'
            f'<rect x="20" y="100" width="{cw-40}" height="4" rx="2" fill="#fff" fill-opacity=".06"/>'
            f'<rect x="20" y="100" width="0" height="4" rx="2" fill="{col}">'
            f'<animate attributeName="width" from="0" to="{(cw-40)*frac:.0f}" dur="1.6s" begin="{.2+i*.15:.2f}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>'
            "</g>"
        )
    body = (
        f"<defs>{bg_defs()}</defs>"
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="url(#bg)" stroke="url(#edge)"/>'
        f'<text x="30" y="26" font-family="{MONO}" font-size="12" fill="{FAINT}">// production impact — from professional work (code is confidential)</text>'
        + "".join(cards)
    )
    return svg(W, H, body, "Impact: 1M+ daily transactions, 99.9% uptime, 10K+ retailers, ~30% fewer AML false positives, 35% fewer support tickets, sub-200ms clinical alerts")


# -------------------------------------------------------------- timeline ---
def timeline():
    W, H = 1000, 360
    x0, x1 = 210, 960
    start, end = 2021.5, 2027.1  # Jul 2021 .. ~Feb 2027

    def X(year, month):
        t = year + (month - 1) / 12
        return x0 + (t - start) / (end - start) * (x1 - x0)

    roles = [
        ("Deloitte", "Senior Consultant · BPS", (2026, 10), None, "Oct 2026 – Present", "Saudi CIT & Zakat · Odoo 19 ↔ .NET · AI workflows", CYAN),
        ("AKSA-SDS", "Senior Software Engineer", (2024, 4), (2026, 10), "Apr 2024 – Oct 2026", "1LINK switch · Jazz Retailer Portal · AML", PURPLE),
        ("MTBC CareCloud", "Software Engineer", (2021, 11), (2024, 4), "Nov 2021 – Apr 2024", "HIPAA Web EHR · SignalR alerts · SQL tuning", "#34D399"),
        ("Markitech.AI", "Python & AI Solutions Eng.", (2021, 9), (2023, 3), "Sep 2021 – Mar 2023 · remote", "RAG chatbot · AI agents · face recognition", "#F0ABFC"),
    ]
    parts = []
    for yr in range(2022, 2028):
        gx = X(yr, 1)
        if gx <= x1:
            parts.append(f'<line x1="{gx:.1f}" y1="44" x2="{gx:.1f}" y2="{H-34}" stroke="#fff" stroke-opacity=".06"/>'
                         f'<text x="{gx:.1f}" y="{H-14}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{FAINT}">{yr}</text>')
    for i, (co, role, s, e, dates, hl, col) in enumerate(roles):
        y = 56 + i * 68
        sx = X(*s)
        ex = X(2026, 11) + 18 if e is None else X(*e)
        bar_w = max(ex - sx, 26)
        parts.append(
            f'<text x="30" y="{y+16}" font-family="{SANS}" font-size="16" font-weight="700" fill="{INK}">{esc(co)}</text>'
            f'<text x="30" y="{y+35}" font-family="{SANS}" font-size="12" fill="{MUTED}">{esc(role)}</text>'
            f'<rect x="{sx:.1f}" y="{y}" width="0" height="22" rx="11" fill="{col}" fill-opacity=".85">'
            f'<animate attributeName="width" from="0" to="{bar_w:.1f}" dur="1.2s" begin="{.2+i*.2:.1f}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>'
        )
        if e is None:
            anchor, label_x = "end", sx - 14
            parts[-1] = parts[-1].replace(f'y="{y+40}"', f'y="{y+40}"')
            ty1, ty2 = y + 9, y + 25
        else:
            anchor, label_x, ty1, ty2 = "start", sx, y + 40, y + 56
        parts.append(
            f'<text x="{label_x:.1f}" y="{ty1}" text-anchor="{anchor}" font-family="{MONO}" font-size="11.5" fill="{col}">{esc(dates)}</text>'
            f'<text x="{label_x:.1f}" y="{ty2}" text-anchor="{anchor}" font-family="{SANS}" font-size="12" fill="{FAINT}">{esc(hl)}</text>'
        )
        if e is None:
            parts.append(f'<circle class="now" cx="{sx+bar_w:.1f}" cy="{y+11}" r="7" fill="{col}"/>')
    body = (
        f"<defs>{bg_defs()}</defs>"
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="url(#bg)" stroke="url(#edge)"/>'
        f'<text x="30" y="30" font-family="{MONO}" font-size="12" fill="{FAINT}">// career timeline — Markitech.AI was a concurrent remote role</text>'
        + "".join(parts)
    )
    css = ".now{animation:now 1.6s ease-in-out infinite}@keyframes now{0%,100%{opacity:1}50%{opacity:.35}}"
    return svg(W, H, body, "Career timeline: Deloitte (Oct 2026–present), AKSA-SDS (Apr 2024–Oct 2026), MTBC CareCloud (Nov 2021–Apr 2024), Markitech.AI (Sep 2021–Mar 2023, remote, concurrent)", css)


# -------------------------------------------------------------- projects ---
def project_card(title, tagline, lines, chips, accent, glyph):
    W, H = 490, 236
    chip_svg, cx = [], 24
    for c in chips:
        w = len(c) * 7.3 + 20
        if cx + w > W - 20:
            break
        chip_svg.append(f'<g transform="translate({cx:.0f} 170)"><rect width="{w:.0f}" height="24" rx="12" fill="{accent}" fill-opacity=".1" stroke="{accent}" stroke-opacity=".45"/>'
                        f'<text x="{w/2:.0f}" y="16.5" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{accent}">{esc(c)}</text></g>')
        cx += w + 8
    text_lines = "".join(
        f'<text x="24" y="{110+i*20}" font-family="{SANS}" font-size="13" fill="{MUTED}">• {esc(l)}</text>' for i, l in enumerate(lines)
    )
    body = (
        f"<defs>{bg_defs()}</defs>"
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="url(#bg)" stroke="url(#edge)"/>'
        f'<rect x="24" y="24" width="40" height="40" rx="12" fill="{accent}" fill-opacity=".14" stroke="{accent}" stroke-opacity=".6"/>'
        f'<path d="{glyph}" transform="translate(35 35)" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<text x="78" y="42" font-family="{SANS}" font-size="19" font-weight="800" fill="{INK}">{esc(title)}</text>'
        f'<text x="78" y="61" font-family="{SANS}" font-size="12.5" fill="{FAINT}">{esc(tagline)}</text>'
        f'<line x1="24" y1="84" x2="{W-24}" y2="84" stroke="#fff" stroke-opacity=".07"/>'
        + text_lines + "".join(chip_svg)
        + f'<text x="{W-24}" y="218" text-anchor="end" font-family="{SANS}" font-size="12.5" font-weight="700" fill="{accent}" class="go">View repository →</text>'
    )
    css = ".go{animation:go 2.4s ease-in-out infinite}@keyframes go{0%,100%{opacity:.7}50%{opacity:1}}"
    return svg(W, H, body, f"{title} — {tagline}", css)


PROJECTS = {
    "project-payment-switch": ("Payment Switch API", "Interbank routing reference build · .NET 8", [
        "Clean Architecture + CQRS with MediatR",
        "Idempotency keys & domain-enforced state machine",
        "Domain events, Swagger, Docker, xUnit tests",
    ], [".NET 8", "MediatR", "CQRS", "Docker", "xUnit"], PURPLE, "M2 5h14v9H2zM2 8h14M5 11h3"),
    "project-rag-chatbot": ("RAG Chatbot", "Grounded answers with citations · FastAPI", [
        "PDF / DOCX / TXT ingestion, chunking & embeddings",
        "FAISS semantic search + GPT-4o generation",
        "Multi-turn sessions, source scores, pytest suite",
    ], ["Python", "FastAPI", "LangChain", "FAISS", "OpenAI"], "#F0ABFC", "M3 3h12v9H8l-4 3v-3H3z"),
    "project-smart-employee-portal": ("Smart Employee Portal", "HR & biometric attendance · 3 services", [
        "Angular 17 UI with webcam attendance capture",
        ".NET 8 API: JWT auth, employees, attendance",
        "FastAPI face service: ArcFace + FAISS, liveness",
    ], ["Angular 17", ".NET 8", "FastAPI", "DeepFace", "SQL Server"], CYAN, "M9 2a3 3 0 1 1 0 6 3 3 0 0 1 0-6zM3 16c0-3 2.7-5 6-5s6 2 6 5"),
    "project-ems": ("Employee Management System", "SaaS-style HRMS · Blazor Server", [
        "Dashboards, employees, leave, performance, reports",
        "MudBlazor UI with light / dark themes",
        "EF Core-ready services, FluentValidation",
    ], [".NET 8", "Blazor", "MudBlazor", "EF Core", "AutoMapper"], "#34D399", "M2 2h6v6H2zM10 2h6v6h-6zM2 10h6v6H2zM10 10h6v6h-6z"),
}


# ---------------------------------------------------------------- footer ---
def footer():
    W, H = 1000, 230
    body = (
        f"<defs>{bg_defs()}{MASCOT_DEFS}</defs>"
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="url(#bg)" stroke="url(#edge)"/>'
        f"{stars(W, H, 30, seed=3)}"
        + mascot(70, 28, 1.05, wave=True)
        + f'<text x="230" y="92" font-family="{SANS}" font-size="34" font-weight="800" fill="url(#brand)">Let\'s build something amazing</text>'
        f'<text x="230" y="126" font-family="{SANS}" font-size="16" fill="{MUTED}">Open to senior engineering, AI and consulting conversations — remote-friendly.</text>'
        f'<text x="230" y="160" font-family="{MONO}" font-size="14" fill="{CYAN}">await yasir.connect({{ via: ["LinkedIn", "email", "portfolio"] }});</text>'
        f'<rect class="cursor" x="785" y="148" width="9" height="16" fill="{CYAN}"/>'
    )
    css = STAR_CSS + MASCOT_CSS + ".cursor{animation:cur 1s steps(1) infinite}@keyframes cur{50%{opacity:0}}"
    return svg(W, H, body, "Let's build something amazing — connect with Yasir Mehmood", css)


def main():
    OUT.mkdir(exist_ok=True)
    files = {"hero.svg": hero(), "divider.svg": divider(), "impact.svg": impact(), "timeline.svg": timeline(), "footer.svg": footer()}
    for name, (t, g, a, items) in CARDS.items():
        files[f"{name}.svg"] = tech_card(t, g, items, a)
    for name, args in PROJECTS.items():
        files[f"{name}.svg"] = project_card(*args)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"{name:38s} {len(content)/1024:6.1f} KB")


if __name__ == "__main__":
    main()
