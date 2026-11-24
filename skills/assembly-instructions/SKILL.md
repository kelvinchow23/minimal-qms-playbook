---
name: assembly-instructions
description: Write or update the assembly instruction for an in-house assembly (minimalQMS SOP-006-A04), with pictures from CAD and a check at each step where mistakes are likely. Use when an assembly needs an instruction before its first build, or when its design changes.
metadata:
  rev: A
  status: draft
---

# Assembly instructions

Carries out SOP-006 for every in-house assembly (`PPP-A-NNNN` with `make: assemble`). The
template is SOP-006-A04. The file is `03_build_package/assembly/<PN>.md`, with its pictures in
`03_build_package/assembly/images/`, linked as in the template.

## Writing it

1. Start from the assembly's lines in `bom.csv`. Every part on the BOM appears in exactly
   one step, by PN and quantity.
2. Order the steps the way a person builds it: sub-assemblies first, then fasteners,
   then anything that blocks access to earlier work.
3. Write one action per step, in the imperative ("Press the insert into the lid.").
4. Add a setting wherever one matters: torque, temperature, orientation, glue cure time.
5. Add a check wherever a mistake is likely or hard to undo: orientation, polarity, cable
   routing, a part that cannot be reached later.
6. Add a picture to each step that is not obvious from the text. Use CAD:
   - an exploded or partly assembled view for each step (Fusion: Animation workspace;
     Onshape: exploded views);
   - arrows or highlights for the part being added;
   - a photo of the real unit replaces the render after the first build, where it is clearer.
7. List tools, consumables and safety notes in "Before you start".
8. Set `rev` to the assembly's revision, and `time_estimate` to a guess; correct it after
   the first build.

## Checking it

1. Someone who did not write it builds a unit from it, or walks through it step by step
   against the CAD model.
2. Fix every step they had to ask about.
3. The instruction is approved with the BOM at G2 (SOP-004), or through an ECO after G2.

## When the design changes

The instruction carries the assembly's revision. A change to the assembly's BOM or build
order updates the instruction in the same PR (SOP-001).

## Organization add-on

If the private playbook is cloned beside this repo, also read
`minimal-qms-playbook-private/skills/assembly-instructions/assembly-instructions-private-addon.md`.
Where it conflicts with this file, the add-on applies. Neither may conflict with an SOP.
