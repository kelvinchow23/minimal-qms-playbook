---
name: fusion-cad
description: Model parts and assemblies in Autodesk Fusion to a consistent standard (symmetry, sketches, holes, 3D-print defaults, heat-set inserts, off-the-shelf models) so they map to minimalQMS part numbers, and release them (milestone, exports, BOM, parts.csv). Use when creating, changing or reviewing mechanical CAD in Fusion, or when a Fusion part or assembly is being released.
metadata:
  rev: C
  status: draft
---

# Fusion CAD

Carries out SOP-002 (part numbers, revisions) and SOP-004 (build package) for designs kept
in Autodesk Fusion. Parts are assumed to be 3D printed unless stated otherwise.

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

## Files and folders

1. Every custom part is its own Fusion design, inserted into the assembly as a reference (xref).
   Never model a custom part as a local component inside the assembly.
2. Name every design by its part number: custom parts `<PPP-NNNN> <short name>` (e.g.
   `PRX-0004 Lid`), assemblies `<PPP-A-NNNN> <short name>` (e.g. `PRX-A-0001 Microscope mount`).
   Before a PN is allocated, a descriptive name is fine.
3. Never put the revision in a name. Record it in the design's properties, together with the
   Part Number property set to the PN.
4. Project folder: the assembly and custom parts in the project root; off-the-shelf part
   files in a subfolder named `OTS parts`, and retired designs in a subfolder named `Obsolete`.
5. Keep one design per PN and revise it in place. Fusion's version history holds every
   version, a milestone marks each released revision (see Releasing), and assembly references
   point to specific versions. Do not keep `revA`, `WIP` or `vN` copies: copies break
   references and leave several files claiming one PN. The frozen copy of a released revision
   is its export in git, named with the revision (SOP-002 section 4).
6. Make a copy only when:
   - the change is not interchangeable: "Save as" a new design with its new PN (SOP-002
     section 4); or
   - you are exploring an idea that may be thrown away: copy to a scratch design named
     `scratch - <idea>`, with no PN. Bring the chosen geometry back into the PN design, then
     move the scratch design to `Obsolete`.
7. Never delete a design that has been released (milestoned for a gate or ECO). When it is
   retired, move it to `Obsolete` and prefix its name with `OBSOLETE`. PNs are never reused
   (SOP-002 section 3). A draft that was never released and has been replaced, e.g. a rough
   model swapped for an accurate one, may be deleted.
8. The latest version of a design is work in progress. Before a gate or ECO, check that the
   latest version is the one to be milestoned. Anyone who needs a released revision takes it
   from the release exports in git, or opens the milestone version, not the latest.

## Modelling practice

1. Work in millimetres. Put key dimensions in user parameters with descriptive names.
2. Make parts as symmetric as possible. Start the first sketch at the origin, and keep the part
   symmetric about the origin and the base planes.
3. One sketch per feature. Do not reuse one large sketch for an extrude plus holes and cutouts.
4. Sketch on existing body faces. Create a construction plane only where no suitable face exists.
5. Capture design intent with constraints rather than dimensions, and do not over-dimension.
   Where a datasheet gives a dimensioning scheme, follow it.
6. Hole patterns: dimension the hole-to-hole spacing in both directions on a construction
   rectangle, then locate the pattern's centre from one clear datum. Do not locate each hole
   from the part origin.
7. Model holes with the Hole feature, not extruded cuts.
8. End extents at a face ("to object") rather than at a fixed distance wherever possible, so
   edits do not break the model.
9. Put fillets and chamfers at the end of the timeline, unless that is not possible.
10. Name bodies, sketches and important features. Never leave `Body1` or `Sketch12` in a
    released design.
11. Save with a version description that says what changed.

## Printed parts

1. Two printed parts that mate have a clearance offset, driven by a user parameter.
2. Fasten printed parts with machine screws into heat-set inserts. No self-tapping screw holes.
3. Heat-set insert holes use the diameter in [heat-set-inserts.csv](heat-set-inserts.csv)
   exactly. The depth there is a minimum; go a few millimetres deeper where the part allows.
   The table is for the inserts listed in it; for any other insert, use its datasheet.
4. Blend heat-set bosses into the wall with fillets, not a thin tangent attachment.
5. A boss near the top of a printed wall is short, with a chamfered or cone-shaped underside,
   so it prints without supports.
6. Prefer flat-head (countersunk) screws over pan-head unless the function needs a pan head.
   Screws driven in from the underside of a part that must sit flat are always flat-head.
7. Choose part thicknesses and insert depths to suit screws already in the OTS library, and use
   those screws in the BOM.

## Off-the-shelf parts

1. Look up the OTS library (`minimal-qms-ots-library`) first, and prefer a part that is already
   in it. Treat every part in the library as available. This skill does not list parts.
2. Use the supplier's real STEP model wherever one exists (e.g. McMaster-Carr). For
   McMaster-Carr, download the non-threaded version.
3. If there is no STEP model, ask the human before modelling it. Build it only from a technical
   drawing or measurements the human provides.
4. Never guess the dimensions of an off-the-shelf part. Flag any geometry that is neither a
   supplier model nor measured as **unconfirmed**, in its component name and in the review
   package, until a human confirms it.
5. Name each OTS component `<CCC-NNNN> <short name>` and set its Part Number property.
   Allocate the PN first with the OTS library's `new_pn.py`.

## BOM

1. Every component has a PN before the BOM is exported.
2. Keep the BOM short: consolidate fasteners to one head type and length per size wherever
   reasonable, instead of mixing heads and lengths.
3. Group BOM views and drawing parts lists into off-the-shelf and custom parts. In `bom.csv`
   the PN format already separates them (`CCC-NNNN` vs `PPP-NNNN`).

## Releasing a part or assembly

Do this when the part goes on a released BOM (at G2, or through an ECO after G2). Names below
are the minimalQMS defaults (`minimal-qms` `docs/INTERFACES.md`, "Release file names"); if
the team has changed them there, use those instead.

1. Confirm the change is approved (SOP-003 review or SOP-001 ECO). Releasing is not approval.
2. Save the design. Mark that version as a milestone named `<PN> rev <X>`, with the gate or
   ECO in the version description (e.g. `G2 design freeze`). Update the revision property.
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

## Milestones at gates

When a gate is passed (G2, G3, G4), mark a milestone on the current version of every design
in the product: the top assembly, its sub-assemblies and every custom part. Name each
`<PN> rev <X>` with the gate in the version description, even if the design did not change.
The milestone list then shows which version of each design was approved at each gate.

## Agent notes

- Deliver models as editable Fusion timelines. Do not hand over code-first CAD (e.g. CadQuery,
  build123d) as the final model.
- The Fusion MCP server works only while Fusion is open. Inspect the design before changing it.
- The Fusion API uses **centimetres** and **radians**. Convert from millimetres and degrees.
- Build geometry in small steps (sketch → profile → feature) and check visually after each
  significant change.
- Never overwrite or delete a milestone version.

## Open questions

Not yet decided; raise them with the human when they come up:
- Fillets: several separate fillet features, or one feature with several radii? The aim is a
  model that does not break across iterations.

## Organization add-on

If the private playbook is cloned beside this repo, also read
`minimal-qms-playbook-private/skills/fusion-cad/fusion-cad-private-addon.md`. It adds local
conventions. Where it conflicts with this file, the add-on applies. Neither may conflict with
an SOP.
