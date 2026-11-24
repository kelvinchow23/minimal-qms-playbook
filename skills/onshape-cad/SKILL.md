---
name: onshape-cad
description: Model parts and assemblies in Onshape so they map to minimalQMS part numbers, and release them (named version, exports, BOM, parts.csv). Use when creating or changing mechanical CAD in Onshape, or when an Onshape part or assembly is being released.
metadata:
  rev: A
  status: draft   # not yet used on a project; check each step on first use
---

# Onshape CAD

Carries out SOP-002 (part numbers, revisions) and SOP-004 (build package) for designs kept
in Onshape. Same rules as `fusion-cad`; only the tool steps differ.

## Where things live

| Thing | Lives in | Not in |
|---|---|---|
| Geometry and its version history | Onshape document | git |
| Part numbers, revisions, lifecycle | product repo `03_build_package/parts.csv` | Onshape properties or release management |
| BOM | product repo `03_build_package/bom.csv` (exported at release) | Onshape only |
| Released files (STEP, STL/3MF, PDF) | product repo `03_build_package/mechanical/` | Onshape only |

An Onshape version is not a revision. A released revision points to one named Onshape
version through the `source` column of `parts.csv`. Do not use Onshape release management
as the record; it would duplicate `parts.csv`.

## Modelling practice

1. Work in millimetres. Put key dimensions in variables or configuration inputs with
   descriptive names.
2. One part per custom PN. Name each part `<PN> <short name>` and set its Part number
   property to the PN. Leave Onshape's Revision and State properties empty.
3. Name sketches and important features.
4. Parts shared between products live in their own document and are inserted from a named
   version. Do not copy them.
5. OTS parts: insert the supplier's model, named `<CCC-NNNN> <short name>`, with the Part
   number property set. Allocate the PN first with the OTS library's `new_pn.py`.
6. Every part has a PN before the BOM is exported.

## Releasing a part or assembly

1. Confirm the change is approved (SOP-003 review or SOP-001 ECO). Releasing is not approval.
2. Create a version named `<PN> rev <X>`.
3. Update `parts.csv`: `rev`, `lifecycle`, and `source` = `Onshape: <document> / <version name>`.
4. Export into `03_build_package/mechanical/`, named `<PN>_rev<X>_<short-name>.<ext>`: STEP
   for custom parts and the top assembly, STL or 3MF for printed parts, PDF drawings where needed.
5. Export the assembly BOM table as CSV and write the lines into `bom.csv`.
6. Compare `bom.csv` with the assembly. Report any difference; do not resolve it silently.
7. Commit the exports, `parts.csv` and `bom.csv` together, in one PR (SOP-001).

## Organization add-on

If the private playbook is cloned beside this repo, also read
`minimal-qms-playbook-private/skills/onshape-cad/onshape-cad-private-addon.md`. Where it
conflicts with this file, the add-on applies. Neither may conflict with an SOP.
