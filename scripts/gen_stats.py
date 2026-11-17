#!/usr/bin/env python3
"""Self-hosted stats card for the profile README. No third-party render servers.
usage: gen_stats.py [--user 03xe] [--out assets/stats.svg] [--demo | --placeholder]
env:   GITHUB_TOKEN (or STATS_TOKEN, a PAT with read:user, to include private contribs)"""
import argparse, json, os, random, sys, urllib.request
from datetime import datetime, timezone, timedelta

QUERY = """query($u:String!){user(login:$u){followers{totalCount}
pullRequests{totalCount} issues{totalCount}
repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC,orderBy:{field:PUSHED_AT,direction:DESC}){
 totalCount nodes{stargazerCount languages(first:8,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}
contributionsCollection{totalCommitContributions restrictedContributionsCount
 contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}}}"""


def fetch(user, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"u": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    if "errors" in d or not d.get("data", {}).get("user"):
        raise SystemExit(f"graphql error: {d.get('errors')}")
    u = d["data"]["user"]
    cc = u["contributionsCollection"]
    langs = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    days = [x for w in cc["contributionCalendar"]["weeks"] for x in w["contributionDays"]]
    return dict(
        user=user, followers=u["followers"]["totalCount"], prs=u["pullRequests"]["totalCount"],
        issues=u["issues"]["totalCount"], repos=u["repositories"]["totalCount"],
        stars=sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        commits=cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        total=cc["contributionCalendar"]["totalContributions"], days=days, langs=langs)


def demo(user):
    random.seed(7)
    today = datetime.now(timezone.utc).date()
    days = []
    for i in range(371, -1, -1):
        d = today - timedelta(days=i)
        n = max(0, int(random.gauss(2.2, 3.2))) if random.random() > .35 else 0
        days.append({"date": d.isoformat(), "contributionCount": n})
    return dict(user=user, followers=12, prs=9, issues=4, repos=14, stars=37, commits=412,
                total=sum(x["contributionCount"] for x in days), days=days,
                langs={"C": 52000, "Python": 38000, "Assembly": 21000, "Rust": 14000, "Shell": 9000, "Lua": 6000})


def streaks(days):
    cur = best = run = 0
    counts = [x["contributionCount"] for x in days]
    for c in counts:
        run = run + 1 if c else 0
        best = max(best, run)
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:  # today may not be done yet
        i -= 1
    while i >= 0 and counts[i]:
        cur += 1
        i -= 1
    return cur, best


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;")


def render(d, pending=False):
    W, H = 900, 468
    F = "font-family=\"'Courier New',Courier,monospace\""
    v = (lambda x: "--") if pending else (lambda x: f"{x:,}")
    cur, best = (0, 0) if pending else streaks(d["days"])
    stamp = "AWAITING FIRST SYNC" if pending else "synced " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs><clipPath id="rc"><rect x="28" y="60" width="844" height="10"/></clipPath>'
         '<pattern id="gr" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#111"/></pattern>'
         '<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
         f'<g {F}><rect width="{W}" height="{H}" fill="#050505"/><rect width="{W}" height="{H}" fill="url(#gr)"/>'
         f'<path d="M18 2H882L898 18V{H-18}L882 {H-2}H18L2 {H-18}V18Z" fill="none" stroke="#3a3a3a" stroke-width="2"/>'
         '<rect x="28" y="24" width="8" height="30" fill="#d4d4d4"/>'
         '<text x="50" y="48" font-size="24" font-weight="700" fill="#f2f2f2" letter-spacing="3">STATS</text>'
         f'<text x="872" y="46" font-size="12" fill="#555" text-anchor="end" letter-spacing="2">// {esc(d["user"])} · {stamp}</text>'
         '<path d="M28 66H872" stroke="#1f1f1f"/><g clip-path="url(#rc)"><rect y="65" width="140" height="2" fill="url(#sw)"><animate attributeName="x" values="-140;900" dur="3.6s" repeatCount="indefinite"/></rect></g>']
    rows = [("STARS EARNED", d["stars"]), ("COMMITS / 12M", d["commits"]), ("PULL REQUESTS", d["prs"]),
            ("ISSUES", d["issues"]), ("PUBLIC REPOS", d["repos"]), ("FOLLOWERS", d["followers"])]
    for i, (k, val) in enumerate(rows):
        cx = 28 + (i // 3) * 290
        y = 100 + (i % 3) * 38
        o.append(f'<rect x="{cx}" y="{y-9}" width="6" height="6" fill="#d4d4d4"/><text x="{cx+18}" y="{y-2}" font-size="12" fill="#6e6e6e" letter-spacing="3">{k}</text>'
                 f'<text x="{cx+262}" y="{y+2}" font-size="20" font-weight="700" fill="#f2f2f2" text-anchor="end">{v(val)}</text><path d="M{cx} {y+12}H{cx+262}" stroke="#1a1a1a"/>')
    rx, ry, r = 745, 138, 46
    circ = 2 * 3.14159 * r
    frac = min(cur / 30, 1)
    o.append(f'<circle cx="{rx}" cy="{ry}" r="{r}" fill="none" stroke="#1f1f1f" stroke-width="6"/>'
             f'<circle cx="{rx}" cy="{ry}" r="{r}" fill="none" stroke="#f2f2f2" stroke-width="6" stroke-dasharray="{circ*frac:.1f} {circ:.1f}" transform="rotate(-90 {rx} {ry})"/>'
             f'<text x="{rx}" y="{ry+9}" font-size="28" font-weight="700" fill="#fff" text-anchor="middle">{"--" if pending else cur}</text>'
             f'<text x="{rx}" y="{ry+68}" font-size="11" fill="#6e6e6e" text-anchor="middle" letter-spacing="3">CURRENT STREAK</text>'
             f'<text x="{rx}" y="{ry+86}" font-size="11" fill="#8a8a8a" text-anchor="middle">best {"--" if pending else best} · total {v(d["total"])}</text>')
    o.append('<text x="28" y="248" font-size="12" fill="#6e6e6e" letter-spacing="3">TOP LANGUAGES</text><path d="M200 244H872" stroke="#1a1a1a"/>')
    tot = sum(d["langs"].values()) or 1
    top = sorted(d["langs"].items(), key=lambda kv: -kv[1])[:6]
    shades = ["#f2f2f2", "#cfcfcf", "#a8a8a8", "#818181", "#5c5c5c", "#3d3d3d"]
    topsum = sum(s for _, s in top) or 1
    x = 28
    for i, (n, s) in enumerate(top):
        w = 844 * s / topsum
        o.append(f'<rect x="{x:.1f}" y="260" width="{max(w-2,1):.1f}" height="10" fill="{shades[i]}"/>')
        x += w
        lx = 28 + (i % 3) * 290
        ly = 296 + (i // 3) * 22
        o.append(f'<rect x="{lx}" y="{ly-9}" width="8" height="8" fill="{shades[i]}"/><text x="{lx+16}" y="{ly}" font-size="12" fill="#cfcfcf">{esc(n)}</text>'
                 f'<text x="{lx+262}" y="{ly}" font-size="12" fill="#8a8a8a" text-anchor="end">{s*100/tot:.1f}%</text>')
    if not top:
        o.append('<rect x="28" y="260" width="844" height="10" fill="#101010"/><text x="28" y="296" font-size="12" fill="#555">-- no data yet --</text>')
    o.append('<text x="28" y="350" font-size="12" fill="#6e6e6e" letter-spacing="3">CONTRIBUTIONS</text><text x="872" y="350" font-size="11" fill="#444" text-anchor="end">last 52 weeks</text><path d="M160 346H700" stroke="#1a1a1a"/>')
    days = d["days"][-371:] if d["days"] else []
    mx = max([x["contributionCount"] for x in days] + [1])
    lv = ["#101010", "#2a2a2a", "#555", "#9a9a9a", "#f2f2f2"]
    n_cells = len(days) if days else 53 * 7
    for i in range(n_cells):
        c = days[i]["contributionCount"] if days else 0
        l = 0 if c == 0 else min(4, 1 + int(3 * (c - 1) / max(mx - 1, 1) + .5))
        o.append(f'<rect x="{28+(i//7)*15.5:.1f}" y="{366+(i%7)*11.5}" width="11" height="10" fill="{lv[l]}"/>')
    o.append('</g></svg>')
    return "".join(o)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="03xe")
    ap.add_argument("--out", default="assets/stats.svg")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--placeholder", action="store_true")
    a = ap.parse_args()
    if a.placeholder:
        svg = render(dict(user=a.user, followers=0, prs=0, issues=0, repos=0, stars=0, commits=0, total=0, days=[], langs={}), True)
    elif a.demo:
        svg = render(demo(a.user))
    else:
        tok = os.environ.get("STATS_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not tok:
            sys.exit("no GITHUB_TOKEN / STATS_TOKEN")
        svg = render(fetch(a.user, tok))
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(svg)
    print("wrote", a.out)
