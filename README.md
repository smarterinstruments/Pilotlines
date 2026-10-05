# EU Pilot Lines Monitor (alpha)

Independent weekly view of the 11 pilot lines of the EU Chips Act (Chips for Europe Initiative): how far each line is on the road to open access, what it offers today, when external users get in, and how to reach the lines through the national Chips Competence Centres of the aCCCess network.

- Live page: https://smarterinstruments.github.io/pilotlines/
- Prepared by Stanislav Černý, Czech National Semiconductor Cluster, a partner in the aCCCess network action
- Feedback until 1 November 2026: cerny@semicz.eu
- Not an official publication of aCCCess, the Chips JU, the European Commission or the pilot lines.

The page uses the visual language of the aCCCess network (acccess.eu) and links to its sections, but is a separate site.

## Embedding

Add `?embed` to the URL to hide the page's own top bar and footer, so it can sit inside another site, for example as an iframe on acccess.eu. A section can be opened directly with an anchor (`#radar`, `#lines`, `#timeline`, `#access`, `#news`, `#events`).

```
<iframe src="https://smarterinstruments.github.io/pilotlines/?embed" style="width:100%;height:1600px;border:0" title="EU Pilot Lines Monitor"></iframe>
```

## Data

All data sit in one JSON block (`<script type="application/json" id="monitor-data">`) inside `index.html`; the page renders itself from it. Updates are published weekly after editorial review.

`tools/publish.py` wraps the editorial page for GitHub Pages:

```
python3 tools/publish.py eu-pilot-lines-monitor.html index.html
```
