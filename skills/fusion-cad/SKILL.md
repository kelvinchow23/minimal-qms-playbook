---
name: fusion-cad
description: Model parts and assemblies in Autodesk Fusion so they map to minimalQMS part numbers, and release them (milestone, exports, BOM, parts.csv). Use when creating or changing mechanical CAD in Fusion, or when a Fusion part or assembly is being released.
metadata:
  rev: A
  status: draft
---

# Fusion CAD

Carries out SOP-002 (part numbers, revisions) and SOP-004 (build package) for designs kept
in Autodesk Fusion.

## Where things live

| Thing | Lives in | Not in |
|---|---|---|
| Geometry and its version history | Fusion | git |
| Part numbers, revisions, lifecycle | product repo `03_build_package/parts.csv` | Fusion properties or Fusion Manage |
| BOM | product repo `03_build_package/bom.csv` (exported at release) | Fusion only |
| Released files (STEP, STL/3MF, PDF) | product repo `03_build_package/mechanical/` | Fusion only |

Fusion versions (`v12`) are not revisions (`B`). A released revision points to one Fusion
version through the `source` column of `parts.csv`. Do not use Fusion's own lifecycle or
release features as the record; they would duplicate `parts.csv`.

## Modelling practice

1. Work in millimetres. Put key dimensions in user parameters with descriptive names.
2. One component per custom part. Name each component `<PN> <short name>`, e.g.
   `PRX-0004 Lid`, and set the component's Part Number property to the PN.
3. Name bodies, sketches and important features. Never leave `Body1` or `Sketch12` in a
   released design.
4. Parts shared between products are separate Fusion designs, inserted as linked
   components. Do not copy them.
5. OTS parts: insert the supplier's model (e.g. a McMaster-Carr STEP) as a component named
   `<CCC-NNNN> <short name>`. Allocate the PN first with the OTS library's `new_pn.py`.
6. A part with no PN yet may be named descriptively. It must have a PN before the BOM is exported.
7. Fully constrain sketches for released parts. Check for errors in the timeline before saving.
8. Save with a version description that says what changed.

## Releasing a part or assembly

Do this when the part goes on a released BOM (at G2, or through an ECO after G2). Names below
are the minimalQMS defaults (`minimal-qms` `docs/INTERFACES.md`, "Release file names"); if
the team has changed them there, use those instead.

1. Confirm the change is approved (SOP-003 review or SOP-001 ECO). Releasing is not approval.
2. Save the design. Mark that version as a milestone named `<PN> rev <X>`.
3. Update `parts.csv`: `rev`, `lifecycle`, and `source` = `Fusion: <project>/<design> v<n>`.
4. Export into `03_build_package/mechanical/`, named `<PN>_rev<X>_<short-name>.<ext>`:
   - STEP for every custom part and the top assembly;
   - STL or 3MF for printed parts;
   - PDF drawing where a dimension, tolerance or finish matters to the maker or inspector.
5. Export the BOM of each assembly. Use the drawing parts list or a script; an agent may
   read the assembly through the Fusion MCP server. Write the lines into `bom.csv`
   (`parent_pn, parent_rev, pn, qty, unit, refdes, source, notes`).
6. Compare `bom.csv` with the Fusion assembly. Every component has a PN, and quantities
   match. Report any difference; do not resolve it silently.
7. Commit the exports, `parts.csv` and `bom.csv` together, in one PR (SOP-001).

## Agent notes

- The Fusion MCP server works only while Fusion is open. Inspect the design before changing it.
- The Fusion API uses **centimetres** and **radians**. Convert from millimetres and degrees.
- Build geometry in small steps (sketch → profile → feature) and check visually after each
  significant change.
- Never overwrite or delete a milestone version.

## Organization add-on

If the private playbook is cloned beside this repo, also read
`minimal-qms-playbook-private/skills/fusion-cad/fusion-cad-private-addon.md`. It adds the
organization's own conventions (team hub, project folders). Where it conflicts with this
file, the add-on applies. Neither may conflict with an SOP.
