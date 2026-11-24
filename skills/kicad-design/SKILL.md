---
name: kicad-design
description: Design schematics and PCBs in KiCad so every component maps to a minimalQMS part number, and release a board (ERC/DRC, fabrication and assembly outputs, BOM, parts.csv, tag). Use when creating or changing a KiCad design, or when a board is being released for fabrication.
metadata:
  rev: A
  status: draft
---

# KiCad design

Carries out SOP-002 (part numbers, revisions) and SOP-004 (build package) for boards
designed in KiCad. Commands use `kicad-cli` (KiCad 8 or later).

## Part numbers for a board

| Item | PN | `make` in parts.csv |
|---|---|---|
| Bare PCB | `PPP-NNNN` | `fab` |
| Assembled PCB (by the fabricator or in-house) | `PPP-A-NNNN` | `fab` or `assemble` |
| Each component on it | OTS `CCC-NNNN` | (OTS library) |

The assembled board's BOM lists the bare PCB and every component, with reference designators.

## Design practice

1. The native `.kicad_sch` and `.kicad_pcb` files are the design. Do not regenerate them
   from scripts once they have been edited by hand.
2. Give every symbol a `PN` field holding its OTS part number. Mark parts that are not
   fitted with KiCad's DNP attribute.
3. Fill in the title block: board name, PN, revision letter and date.
4. Put the PN and revision on the silkscreen, e.g. `PRX-0002 rev B`.
5. Keep library tables in the project folder, so the project opens the same on any computer.
6. Run ERC and DRC before every review and before release. Explain every remaining
   exclusion in the review package.

## Releasing a board

Names below are the minimalQMS defaults (`minimal-qms` `docs/INTERFACES.md`, "Release file
names"); if the team has changed them there, use those instead.

1. Confirm the change is approved (SOP-003 review or SOP-001 ECO). Releasing is not approval.
2. Run the checks and save the reports:
   - `kicad-cli sch erc --output erc.rpt <project>.kicad_sch`
   - `kicad-cli pcb drc --output drc.rpt <project>.kicad_pcb`
3. Create the output folder `03_build_package/electronics/<PN>_rev<X>_<short-name>/` and export:
   - Gerbers and drill files (`kicad-cli pcb export gerbers`, `kicad-cli pcb export drill`);
   - pick-and-place file (`kicad-cli pcb export pos`) for assembled boards;
   - BOM with PN, quantity and reference designators (`kicad-cli sch export bom`);
   - schematic PDF (`kicad-cli sch export pdf`) and STEP (`kicad-cli pcb export step`);
   - the ERC and DRC reports.
4. Apply any fabricator-specific changes (e.g. component rotation offsets) only to the exported
   files, never to the native footprints.
5. Write the BOM lines into `bom.csv`, with `refdes` filled in.
6. Update `parts.csv`: `rev`, `lifecycle`, and `source` = `KiCad: <path>/<project>.kicad_pro
   (tag <PN>-rev<X>)`, e.g. `KiCad: electronics/driver/driver.kicad_pro (tag PRX-0002-revB)`.
7. Commit the outputs, `parts.csv` and `bom.csv` together, in one PR (SOP-001). After it is
   merged, tag the merge commit with the name in `source`.
8. Never overwrite a released output folder. A new revision gets a new folder.

## Organization add-on

If the private playbook is cloned beside this repo, also read
`minimal-qms-playbook-private/skills/kicad-design/kicad-design-private-addon.md`. It adds the
organization's own conventions (preferred fabricator settings, shared libraries). Where it
conflicts with this file, the add-on applies. Neither may conflict with an SOP.
