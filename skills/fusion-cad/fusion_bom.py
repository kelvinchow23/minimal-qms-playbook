"""Read the BOM of the active Fusion assembly (run inside Fusion, e.g. Scripts and Add-Ins or an
agent through the Fusion MCP server). Prints `pn,qty,how` lines to compare with bom.csv.

Walks down through grouping components (local components with no bodies, e.g. "OTS parts" >
"Fasteners") and counts every referenced design it finds, ghost designs included. A referenced
design's own sub-components (a PCB's chips) are not counted. The PN is the component's Part
Number property; when that is not a PN (e.g. Fusion's timestamp default on an uploaded STEP),
the PN at the start of the referenced file's name is used, and the line says so. A local
component with bodies is reported as NO-PN: custom parts must be their own designs.
Only the PN at the start of the property counts (some uploaded models hold e.g.
`ECM-0004 Raspberry Pi Zero 2 W`). Last, it lists hidden components and bodies: Fusion
leaves them out of STEP and STL exports, so nothing may be hidden when a design is saved.
"""
import re

import adsk.core
import adsk.fusion

PN = re.compile(r"^([A-Z]{3}-(?:A-)?\d{4})")


def _parts(occurrences):
    for o in occurrences:
        if not o.isReferencedComponent and o.component.bRepBodies.count == 0:
            yield from _parts(o.childOccurrences)  # grouping component
        else:
            yield o


def run(_context: str):
    app = adsk.core.Application.get()
    root = adsk.fusion.Design.cast(app.activeProduct).rootComponent
    counts, how = {}, {}
    for o in _parts(root.occurrences):
        comp = o.component
        m = PN.match(comp.partNumber or "")
        pn, src = (m.group(1), "property") if m else (None, "")
        if not pn and o.isReferencedComponent:
            m = PN.match(comp.parentDesign.parentDocument.dataFile.name)
            pn, src = (m.group(1), "file name; Part Number property not set") if m else (None, "")
        pn = pn or "NO-PN " + comp.name
        counts[pn] = counts.get(pn, 0) + 1
        how[pn] = src
    print("pn,qty,how")
    for pn in sorted(counts):
        print(f"{pn},{counts[pn]},{how[pn]}")
    hidden = [o.fullPathName for o in root.allOccurrences if not o.isLightBulbOn]
    design = root.parentDesign
    hidden += [c.name + "/" + b.name for c in design.allComponents for b in c.bRepBodies if not b.isLightBulbOn]
    if hidden:
        print("HIDDEN (left out of STEP/STL exports): " + "; ".join(hidden))
