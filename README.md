# minimal-qms-playbook

Work instructions for [minimalQMS](https://github.com/kelvinchow23/minimal-qms): how to do
the work the SOPs require in a specific tool. The SOPs say *what* must happen ("the MCAD
tool exports the BOM at release"). The playbook says *how* to do it in Fusion, Onshape or KiCad.

Each work instruction is a `SKILL.md`: plain Markdown that a person reads as an instruction
and an agent loads as a skill. One file serves both, so the two can't drift apart.

| Skill | Use it when |
|---|---|
| [fusion-cad](skills/fusion-cad/SKILL.md) | Modelling in Autodesk Fusion, and releasing a part or assembly from it |
| [onshape-cad](skills/onshape-cad/SKILL.md) | The same, in Onshape |
| [kicad-design](skills/kicad-design/SKILL.md) | Schematic and PCB design in KiCad, and releasing a board |
| [assembly-instructions](skills/assembly-instructions/SKILL.md) | Writing the assembly instruction for an in-house assembly (SOP-006) |
| [purchasing](skills/purchasing/SKILL.md) | Ordering parts for a build and recording the order (SOP-005) |
| [lab-drivers](skills/lab-drivers/SKILL.md) | Writing firmware or host drivers for lab devices and sensors |

## Public playbook, private add-ons

This repo is public and generic. Steps that belong to one organization (its purchasing
system, approval limits, accounts, internal contacts) go in a private repo,
`minimal-qms-playbook-private`, cloned beside this one. It mirrors the folders here and
holds only add-on files:

```
minimal-qms-playbook/skills/purchasing/SKILL.md                              public, generic
minimal-qms-playbook-private/skills/purchasing/purchasing-private-addon.md   private, additions only
```

Each public skill ends with an **Organization add-on** section telling the reader to check
for that file. The add-on holds only what differs. It never copies the public text, so a
fix to the public skill reaches every organization.

## Using the skills

- **Any agent:** a product repo's `AGENTS.md` points to `../minimal-qms-playbook/skills/`.
  The agent reads the relevant `SKILL.md` before starting that kind of work.
- **Agents that load skills from a folder** (e.g. Claude Code's `~/.claude/skills/` or a
  project's `.claude/skills/`): link or copy the skill folders there.
- **People:** read the `SKILL.md` directly.

## Changing a skill

Skills are revised through a PR, like the SOPs (see [AGENTS.md](AGENTS.md)). A skill must
not contradict an SOP. If the work requires a different rule, change the SOP in
`minimal-qms` first.

## Licence

MIT. See [LICENSE](LICENSE).
