---
name: fusion-cam
description: Set up Fusion CAM toolpaths for small GRBL routers (e.g. a hobby CNC with a trim-router spindle) so machined parts cut reliably the first time, including inlays. Use when creating or changing CAM setups, toolpaths or posts in Fusion for a GRBL machine.
metadata:
  rev: A
  status: draft
---

# Fusion CAM (GRBL routers)

Carries out SOP-004 section 9 (build package: files to make a part) for parts machined on a
small GRBL router. Machine-specific numbers (spindle, feeds that are proven, tool list) live in
the organization add-on.

## Setup

1. Post with the GRBL post processor. Post with arcs (G2/G3) and smoothing on; tolerance
   0.01 mm.
2. Prefer one tool per job: avoid tool changes where the part allows.
3. Retract height 3 mm, clearance height 5 mm, unless the fixture needs more.
4. One work coordinate system per job, at an easy-to-find stock corner (e.g. front-left top).
5. After any design change, switch to the Design workspace and back before regenerating: CAM
   otherwise keeps using the old geometry.

## Toolpaths

1. Rough with offset roughing (3D Pocket), not adaptive: adaptive produces long, dense code
   that runs for hours on GRBL.
2. Ramp into material (helix or ramp); never plunge straight down at cutting feed. Use a
   separate, slower plunge feed.
3. Finish chamfers and lead-ins with 3D Contour on the sloped faces, with a small stepdown.

## Inlays

1. Grow the pocket from the insert by a clearance per side, driven by a parameter.
2. Insert convex corners must have a radius of at least the cutter radius plus the clearance.
3. Add a small lead-in chamfer to the pocket.
4. Cut the insert slightly taller than the pocket is deep, so it stands proud and is planed flush.
5. Lay out insert and receiver side by side in one setup, separated by a gap parameter.

## Running the job

1. Re-zero Z on an uncut surface.
2. Restart an interrupted operation from its start, not mid-path.
3. Check that the collet grips the tool shank; sleeve adapters in an oversize collet can slip.

## Organization add-on

If the private playbook is cloned beside this repo, also read
`minimal-qms-playbook-private/skills/fusion-cam/fusion-cam-private-addon.md`. It adds the
organization's machines, spindle settings and proven feeds. Where it conflicts with this file,
the add-on applies. Neither may conflict with an SOP.
