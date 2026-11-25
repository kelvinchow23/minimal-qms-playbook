"""Read the BOM of the active Fusion assembly (run inside Fusion, e.g. Scripts and Add-Ins or an
agent through the Fusion MCP server). Prints `pn,qty,how` lines to compare with bom.csv.

Counts every component one level below the assembly's grouping components (e.g. "Custom parts",
"OTS parts"), or below the root when there are none. Sub-components of an imported model (a
PCB's chips) are not counted. The PN is the component's Part Number property; when that is not a
PN (e.g. Fusion's timestamp default on an uploaded STEP), the PN at the start of the referenced
file's name is used, and the line says so.
"""
import re

import adsk.core
import adsk.fusion

PN = re.compile(r"^([A-Z]{3}-(?:A-)?\d{4})")


def run(_context: str):
    app = adsk.core.Application.get()
    root = adsk.fusion.Design.cast(app.activeProduct).rootComponent
    groups = [o for o in root.occurrences if not o.isReferencedComponent and o.childOccurrences.count]
    parts = [c for g in groups for c in g.childOccurrences] + [o for o in root.occurrences if o.isReferencedComponent]
    counts, how = {}, {}
    for o in parts:
        comp = o.component
        pn, src = (comp.partNumber, "property") if PN.match(comp.partNumber or "") else (None, "")
        if not pn and o.isReferencedComponent:
            m = PN.match(comp.parentDesign.parentDocument.dataFile.name)
            pn, src = (m.group(1), "file name; Part Number property not set") if m else (None, "")
        pn = pn or "NO-PN " + comp.name
        counts[pn] = counts.get(pn, 0) + 1
        how[pn] = src
    print("pn,qty,how")
    for pn in sorted(counts):
        print(f"{pn},{counts[pn]},{how[pn]}")
