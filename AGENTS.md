# AGENTS.md

Instructions for any AI agent working in this repo. `CLAUDE.md` imports this file.
This repo follows [minimalQMS](https://github.com/kelvinchow23/minimal-qms); its hard
rules apply here (never commit to `main`, never merge or approve, never backdate).

## What this repo is

Public work instructions, one `skills/<name>/SKILL.md` per topic. Each is both a work
instruction for people and a skill for agents.

## Related repos

The minimalQMS repos are cloned side by side in one parent folder. Agent sessions in
different repos do not share memory; they coordinate through these files. Local folder
names may differ from the GitHub names (e.g. `minimal-qms` may be cloned as `mini-qms-ai`).

| Repo | What to read there |
|---|---|
| `minimal-qms` | `docs/INTERFACES.md`: the authority on shared names, IDs, columns and the product repo layout. `sops/`: the procedures these skills carry out. |
| `minimal-qms-ots-library` | OTS parts, project codes, part number allocation and purchasing tools. |
| `minimal-qms-playbook` (this repo) | Public, generic work instructions. |
| `minimal-qms-playbook-private` | Private organization add-ons, one `<name>-private-addon.md` per skill. Not every user has it. |

## Rules for this repo

1. **A skill never contradicts an SOP.** Cite the SOP section it carries out, e.g. (SOP-002
   section 4). If a skill needs a different rule, the SOP changes first.
2. **Nothing organization-specific here.** No system names, account details, approval limits,
   people or prices. Those go in the private add-on.
3. **Frontmatter:** `name` and `description` (what the skill does and when to use it), plus
   `metadata` with `rev` and `status` (`draft` or `released`). Increment `rev` (A, B, C …)
   when the meaning of a step changes; typo fixes do not need a new revision.
4. **Every skill ends with an "Organization add-on" section** naming its add-on file.
5. **Keep skills short:** what to do and the checks, not tutorials on the tool.
6. **Use the shared names** from `minimal-qms/docs/INTERFACES.md` (PN formats, file paths, columns).
7. Commit format: `[skill-name] summary`, e.g. `[kicad-design] add DRC report step`, or
   `[PB] summary` for repo-wide changes.
8. **Canadian English spelling** in prose (organization, colour, centre, licence as the
   noun). Proper names and code identifiers stay as they are.
