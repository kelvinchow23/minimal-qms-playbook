---
name: assembly-instructions
description: Write or update the assembly instruction for an in-house assembly (minimalQMS SOP-006-A04) as a picture-led guide in the style of flat-pack furniture instructions, with short callout IDs from the BOM, CAD renders for every step, and a buildability check against the CAD model. Use when an assembly needs an instruction before its first build, or when its design changes.
metadata:
  rev: B
  status: draft
---

# Assembly instructions

Carries out SOP-006 for every in-house assembly (`PPP-A-NNNN` with `make: assemble`). The
template is SOP-006-A04. The file is `03_build_package/assembly/<PN>.md`, with its pictures in
`03_build_package/assembly/images/`, linked as in the template.

## Style: pictures first, little text

Write it like flat-pack furniture instructions: a builder should be able to follow the
pictures alone, and the text only adds what a picture cannot show (a temperature, an
orientation check).

1. **Callout IDs.** Give every BOM line a short callout: a class letter and a number, numbered
   within the class in the order the parts are first used.

   | Letter | Class | Examples |
   |---|---|---|
   | P | Printed and other custom parts | base, lid |
   | B | Bought parts | boards, modules, power supply, SD card |
   | F | Fasteners | screws, nuts, washers, standoffs |
   | H | Heat-set inserts | M2 insert |
   | W | Cables and wires | Qwiic cable, harnesses |
   | C | Wiring consumables | ferrules, crimps, heat-shrink |

   The callout goes in the `refdes` column of `bom.csv`, and the same callout is used in the
   parts gallery, every step, and every picture. The PN stays on the BOM; the steps use only
   the callout.
2. **Fastener labels** give the size, the length and the head: `M2×5 pan`, `M4×10 flat`,
   `M4 standoff 40`. Inserts give the thread: `M2`. Never just "screw".
3. **Parts gallery** first: one card per callout with a picture, the callout, the quantity
   and its label. Then a wiring section, if there are wires: one card per W with both ends,
   connectors and length.
4. **Each step** has:
   - a large step number and a short title (a few words);
   - a parts box: thumbnail, callout and quantity for each part used in this step;
   - a tools box, if the step needs a tool;
   - one CAD render, with a callout bubble and a leader line to every place a part goes;
   - a legend: one line per callout, quantity and an action of a few words ("press flush");
   - at most two short notes, for what the picture cannot show.
5. One colour per class, the same throughout the guide.

## Writing it

1. Start from the assembly's lines in `bom.csv`. Every part on the BOM appears in exactly
   one step, by callout and quantity.
2. Order the steps the way a person builds it: sub-assemblies first, then fasteners, then
   anything that blocks access to earlier work. Plug in a cable before the part that covers
   its connector.
3. One action per step, in the imperative ("Press the inserts flush.").
4. Add a setting wherever one matters: torque, temperature, orientation, glue cure time.
5. Add a check wherever a mistake is likely or hard to undo: orientation, polarity, cable
   routing, a part that cannot be reached later.
6. Render every step from the CAD, showing only the parts fitted so far, with the parts
   added in this step highlighted (Fusion: hide later components, or use the Animation
   workspace for exploded views; Onshape: exploded views). A photo of the real unit replaces
   a render after the first build, where it is clearer.
7. List tools, consumables and safety notes in "Before you start". Set-up tools (a computer, an
   SD card reader) count as tools.
8. Set `rev` to the assembly's revision, and `time_estimate` to a guess; correct it after the
   first build.

Keep the guide's data in one file (`steps.json`: callouts, steps, cables) and generate the
page and its PDF from it, so a change is made once.

## Checking it in the CAD model

An agent runs these checks against the CAD model before the instruction goes to review,
replaying the build step by step (show only the parts fitted so far), and reports every
failure:

1. **Order.** Each part is joined only to parts fitted in earlier steps.
2. **Insertion path.** Sweep each part from outside the assembly along its insertion direction.
   It must not hit anything already fitted.
3. **Tool access.** At every screw and insert, place a temporary tool envelope along its axis
   (screwdriver: shaft Ø4 × 100 mm, handle Ø25; insert tip: Ø6 × 80 mm). It must not hit
   anything already fitted.
4. **Connectors and openings.** Place a mating-plug envelope in front of every connector, and
   the card or plug path through every opening. It must not hit the housing or other parts.
5. **Cables.** Sketch each cable's route from connector to connector, through its notches and
   below the rims. The route plus plug allowance must fit the cable's length.
6. **Closing.** A final interference check with the cable and plug envelopes in place: lids
   and covers close.
7. **Instruction against BOM.** Every BOM line is in exactly one step, and quantities add up.
8. **Pictures.** Every step has a render from this replay.

These checks are only as good as the models: a connector on an unconfirmed OTS model is an
unconfirmed result. Hands, cable stiffness and awkward angles are not modelled; the first
build is still the final check, and what it finds goes in the build record.

## Review

1. Someone who did not write it builds a unit from it, or walks through it step by step
   against the CAD model.
2. Fix every step they had to ask about.
3. The instruction is approved with the BOM at G2 (SOP-004), or through an ECO after G2.

## When the design changes

The instruction carries the assembly's revision. A change to the assembly's BOM or build
order updates the instruction, its callouts and its pictures in the same PR (SOP-001).

## Organization add-on

If the private playbook is cloned beside this repo, also read
`minimal-qms-playbook-private/skills/assembly-instructions/assembly-instructions-private-addon.md`.
Where it conflicts with this file, the add-on applies. Neither may conflict with an SOP.
