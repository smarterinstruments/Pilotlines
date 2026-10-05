"""Build the EU Pilot Lines Monitor page from the Pillar I Monitor data.

Usage: python3 tools/build_pl.py <pillar1-monitor.html | data.json> [eu-pilot-lines-monitor.html]

Reads the shared monitor data (the <script type="application/json" id="monitor-data"> block of the
Pillar I Monitor page, or a data.json), keeps only what concerns the pilot lines, adds the
competence-centre access layer (aCCCess) and fills tools/pl_template.html. The result is the
editorial page; tools/publish.py wraps it for GitHub Pages.
"""
import json, sys, os, re

TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pl_template.html')
SRC = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else 'eu-pilot-lines-monitor.html'

raw = open(SRC, encoding='utf-8').read()
m = re.search(r'<script type="application/json" id="monitor-data">\n?(.*?)\n?</script>', raw, re.S)
d = json.loads((m.group(1) if m else raw).replace('<\\/', '</'))

lines = d['lines']
ring = lambda n: [l['name'] for l in lines if l['ring'] == n]
quant = [l for l in lines if l['sector'] == 'quant']

stats = [
    {"v": str(len(lines)), "l": "pilot lines", "s": f"{len(lines) - len(quant)} semiconductor, {len(quant)} quantum"},
    {"v": str(len(ring(1)) + len(ring(2))), "l": "take external users today",
     "s": "open access: " + ", ".join(ring(1)) + "; early access: " + ", ".join(ring(2))},
    {"v": str(len(ring(3))), "l": "preparing access", "s": ", ".join(ring(3)) + "; no public call yet"},
    {"v": str(len(ring(4))), "l": "in ramp-up", "s": "first grants started in 2026; access from 2027 or not yet dated"},
]

webinars = next(r for r in d['acc']['results'] if r['r'] == 'Technology Offers webinars')

skip = ('EuroCDP', 'Siemens', 'Chips Venture Forum', 'Blumorpho', 'survey', 'HCHiP', 'training catalogue')
seen, sources = set(), []
for name, url in d['sources']:
    if any(k.lower() in name.lower() for k in skip) or not url or url in seen:
        continue
    seen.add(url); sources.append([name, url])

out = {
    "meta": {**d['meta'],
             "lede": "Where the 11 pilot lines of the EU Chips Act stand on the road to open access, what they offer today, and how to reach them through the network of Chips Competence Centres. Updated weekly from the lines' own channels, CORDIS and the Chips JU."},
    "stats": stats,
    "sectors": d['sectors'],
    "rings": d['rings'],
    "lines": lines,
    "newsTypes": d['newsTypes'],
    "news": sorted([n for n in d['news'] if 'pl' in n['c']], key=lambda n: n['d'], reverse=True),
    "events": sorted([e for e in d['events'] if 'pl' in e['c']], key=lambda e: e['d']),
    "next": [x for x in d['overview']['next'] if x['c'] == 'pl'],
    "access": {
        "lede": "Every EU Member State and Norway has a Chips Competence Centre. Under the Chips Act the centres help companies, start-ups and researchers reach the pilot lines, and the aCCCess network action connects all 30 of them.",
        "ctas": [
            {"t": "Find your national centre", "p": "30 centres in 28 countries, each with a contact for pilot-line access.", "b": "Network", "u": "https://www.acccess.eu/network"},
            {"t": "Ask the Technology Advisor", "p": "Describe what you need; the advisor routes the request to the centres that work on that technology.", "b": "Technologies", "u": "https://www.acccess.eu/technologies"},
            {"t": "Check open calls", "p": "Active calls from pilot lines, the design platform, the centres and the Chips JU in one list.", "b": "Open calls", "u": "https://www.acccess.eu/open-calls"},
        ],
        "webinars": {"t": "Technology Offers webinars", "n": webinars['n'], "u": webinars['u']},
    },
    "models": d['models'],
    "legal": d['legal'],
    "feedback": {
        "banner": d['feedback']['banner'],
        "intro": "This page is an independent view of the EU Chips Act pilot lines, built to sit alongside the aCCCess network of competence centres. It reports what the lines publish. Tell us what is wrong, what is missing and what would make it useful.",
        "questions": [
            ["Accuracy", "Is your pilot line described correctly? What is missing or out of date?"],
            ["Readiness scale", "Do the four levels (open access running, early access, preparing access, ramp-up) describe readiness well? Which criteria should define each level?"],
            ["Indicators", "Which two or three indicators would help you most? For example external users, access requests and lead times, published price conditions, PDKs on the design platform, referrals from competence centres."],
            ["Competence centres", "Which centre helped you reach a pilot line? Which link between a line and a centre is missing here?"],
            ["Data contribution", "Would your pilot line send a short monthly status line?"],
            ["Home", "Should this page stay independent, or be hosted or endorsed by the aCCCess network or the Chips JU?"],
        ],
        "contactNote": "Short answers are enough; a correction can be one line. Please mention which pilot line or centre you refer to.",
        "email": d['feedback']['email'],
    },
    "sources": sources,
    "method": "Compiled from the pilot lines' websites and LinkedIn company pages, CORDIS, the Chips JU, aCCCess and the competence centres' channels, and partner press releases. Each weekly edition adds new items and changes only the facts they affect. Dates marked ≈ are derived from the relative age of a post.",
}

dump = lambda v: json.dumps(v, ensure_ascii=False)
parts = []
for i, (k, v) in enumerate(out.items()):
    end = ',' if i < len(out) - 1 else ''
    if isinstance(v, list):
        parts.append(f'  {dump(k)}: [\n' + ',\n'.join(f'    {dump(x)}' for x in v) + f'\n  ]{end}')
    else:
        parts.append(f'  {dump(k)}: {dump(v)}{end}')
body = ('{\n' + '\n'.join(parts) + '\n}').replace('</', '<\\/')
html = open(TPL, encoding='utf-8').read().replace('/*__DATA__*/', body)
open(OUT, 'w', encoding='utf-8').write(html)
print(OUT, len(html), 'news', len(out['news']), 'events', len(out['events']), 'sources', len(sources))
