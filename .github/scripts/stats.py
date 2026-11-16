#!/usr/bin/env python3
"""Render GitHub stats cards that match the profile theme.

Reads live data from the GitHub GraphQL API (public data only) and writes
dist/stats.svg and dist/languages.svg. Nothing is estimated or padded: if the
API call fails the script exits non-zero and the previous cards stay in place.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

LOGIN = os.environ.get("GH_LOGIN", "yasirmalik36")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = Path(os.environ.get("OUT_DIR", "dist"))
SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, monospace"

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      contributionCalendar { totalContributions }
      totalCommitContributions
      totalPullRequestContributions
    }
  }
}
"""


def fetch():
    if os.environ.get("STATS_FIXTURE"):
        return json.loads(Path(os.environ["STATS_FIXTURE"]).read_text())
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(f"GraphQL errors: {data['errors']}")
    return data["data"]["user"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def frame(w, h, title, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">'
        f"<title id=\"t\">{esc(title)}</title>"
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0A0A1F"/>'
        '<stop offset=".55" stop-color="#140B30"/><stop offset="1" stop-color="#05192A"/></linearGradient>'
        '<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A78BFA" stop-opacity=".55"/>'
        '<stop offset="1" stop-color="#22D3EE" stop-opacity=".35"/></linearGradient></defs>'
        f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="20" fill="url(#bg)" stroke="url(#edge)"/>'
        f"{body}</svg>\n"
    )


def stats_card(u):
    repos = u["repositories"]
    stars = sum(n["stargazerCount"] for n in repos["nodes"])
    cc = u["contributionsCollection"]
    rows = [
        ("Public repositories", repos["totalCount"], "#A78BFA"),
        ("Stars earned", stars, "#FBBF24"),
        ("Followers", u["followers"]["totalCount"], "#22D3EE"),
        ("Contributions (last year)", cc["contributionCalendar"]["totalContributions"], "#34D399"),
        ("Commits (last year)", cc["totalCommitContributions"], "#F0ABFC"),
        ("Pull requests (last year)", cc["totalPullRequestContributions"], "#60A5FA"),
    ]
    # Rows that are zero are left out rather than padded (repositories always shown).
    rows = [r for i, r in enumerate(rows) if i == 0 or r[1] > 0]
    body = [f'<text x="24" y="40" font-family="{SANS}" font-size="18" font-weight="700" fill="#F1F5F9">GitHub activity</text>',
            f'<text x="24" y="60" font-family="{MONO}" font-size="11" fill="#64748B">public data · refreshed daily</text>']
    for i, (label, val, col) in enumerate(rows):
        y = 92 + i * 30
        body.append(
            f'<circle cx="30" cy="{y-5}" r="4" fill="{col}"/>'
            f'<text x="44" y="{y}" font-family="{SANS}" font-size="14" fill="#A5B4CF">{esc(label)}</text>'
            f'<text x="466" y="{y}" text-anchor="end" font-family="{SANS}" font-size="16" font-weight="700" fill="{col}">{val:,}</text>'
        )
    return frame(490, 92 + len(rows) * 30 - 6, "GitHub activity for " + LOGIN, "".join(body))


def languages_card(u):
    totals = {}
    for n in u["repositories"]["nodes"]:
        for e in n["languages"]["edges"]:
            name, color = e["node"]["name"], e["node"]["color"] or "#94A3B8"
            t = totals.setdefault(name, [0, color])
            t[0] += e["size"]
    top = sorted(totals.items(), key=lambda kv: -kv[1][0])[:6]
    grand = sum(v[0] for _, v in top) or 1
    body = [f'<text x="24" y="40" font-family="{SANS}" font-size="18" font-weight="700" fill="#F1F5F9">Top languages</text>',
            f'<text x="24" y="60" font-family="{MONO}" font-size="11" fill="#64748B">by code size · public, non-fork repos</text>']
    x = 24.0
    bar_w = 442
    for name, (size, col) in top:
        w = bar_w * size / grand
        body.append(f'<rect x="{x:.1f}" y="76" width="{max(w,1):.1f}" height="10" fill="{col}"/>')
        x += w
    body.insert(2, '<clipPath id="c"><rect x="24" y="76" width="442" height="10" rx="5"/></clipPath>')
    bars = "".join(b for b in body if b.startswith("<rect"))
    body = [b for b in body if not b.startswith("<rect")] + [f'<g clip-path="url(#c)">{bars}</g>']
    for i, (name, (size, col)) in enumerate(top):
        r, c = divmod(i, 2)
        bx, by = 24 + c * 225, 116 + r * 28
        body.append(
            f'<circle cx="{bx+6}" cy="{by-5}" r="5" fill="{col}"/>'
            f'<text x="{bx+18}" y="{by}" font-family="{SANS}" font-size="14" fill="#A5B4CF">{esc(name)}</text>'
            f'<text x="{bx+205}" y="{by}" text-anchor="end" font-family="{MONO}" font-size="13" fill="#F1F5F9">{100*size/grand:.1f}%</text>'
        )
    return frame(490, 116 + 3 * 28 - 6, "Top languages for " + LOGIN, "".join(body))


def main():
    u = fetch()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "stats.svg").write_text(stats_card(u), encoding="utf-8")
    (OUT / "languages.svg").write_text(languages_card(u), encoding="utf-8")
    print("wrote", OUT / "stats.svg", OUT / "languages.svg")


if __name__ == "__main__":
    main()
