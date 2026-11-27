---
name: purchasing
description: Order the parts for a build and record the order in the product repo (minimalQMS SOP-005), using the OTS library's requisition.py and record_order.py. Use when someone asks for order files for N units, says an order was placed, or records parts received.
metadata:
  rev: B
  status: draft
---

# Purchasing

Carries out SOP-005. The tools are in the `minimal-qms-ots-library` repo; run them from its root.
The organization's own ordering steps (its purchasing system, approvals, who places the
order) are in the organization add-on, not here.

## Before ordering

1. The build document is approved for build (G2) or released (SOP-002 section 5, SOP-005).
   Parts for design work before G2 are the exception; mark them `proto` in `notes`.
2. Every supplier is in `purchasing/suppliers.csv`. Add a new supplier before its first
   order, with a basis (SOP-005 section 3). Parts whose A01 Purchasing column says "any
   supplier" need no approved supplier.
3. Prices have a date. Check any price older than 90 days.

## Deciding what to order

The BOM (A01) is per unit. What to order is decided now, by the human, for one build:
1. Ask how many units the build is for, and what is already on hand (inventory, spares from
   an earlier build). For an exact part (A01 Purchasing "exact part"), check that the stock is
   that exact part; for "any matching part", that it matches the description.
2. Write the stock to a CSV (`pn,qty_on_hand`, in pieces) and run the tool with it. It prints
   the **parts plan**, one line per part: needed, on hand, to order, packs, and where it comes
   from (order, stock, or made in house):

   ```
   python tools/requisition.py <product>/02_design/build_document/bom.csv <TOP-PN> <units>        --stock stock.csv --plan <product>/builds/B00n/parts_plan.csv --out out/
   ```

3. Show the parts plan to the human and change the stock or the quantity until they agree
   with it. The plan goes in the build's folder (`builds/B00n/parts_plan.csv`), so the build
   record shows which parts came from stock.

## Making the order files

1. The same run writes one upload file per supplier, for the "order" lines only
   (`out/<supplier>-<date>.csv`). These are drafts: keep them out of the repo until ordered.
2. Report every warning to the human (missing or old prices, unknown PNs). Do not guess a
   missing value.
3. The human checks the files and places the order through the organization's system. An
   agent never places an order.

## Where the files go (product repo)

| File | Where | When |
|---|---|---|
| Parts plan for a build | `builds/B00n/parts_plan.csv` | when the order is decided |
| Order file as submitted | `purchasing/requisitions/<order_ref>.csv` | after ordering (`record_order.py`) |
| One line per item ordered | `purchasing/purchases.csv` | after ordering (`record_order.py`) |
| Approved suppliers | `purchasing/suppliers.csv` | before a supplier's first order |

## Recording the order

1. Ask the human for the order reference (requisition or PO number) and the actual order date.
2. Record it in the product repo, on a branch:

   ```
   python tools/record_order.py out/<supplier>-<date>.csv <Supplier> "<order_ref>" <product> [--date YYYY-MM-DD]
   ```

   It adds `P-nnnn` lines to `purchasing/purchases.csv` and stores the upload file in
   `purchasing/requisitions/`.
3. Open a PR with the new lines (SOP-001).

## Receiving

1. Fill in `received_date`, `received_qty` and the supplier lot or job number on each line.
2. Inspect the parts that have incoming checks in the build document (A03: critical parts only,
   SOP-006) and record the result in `inspection`.
3. A failed inspection opens a nonconformance (SOP-008).

## Organization add-on

If the private playbook is cloned beside this repo, also read
`minimal-qms-playbook-private/skills/purchasing/purchasing-private-addon.md`. It says how the
organization places and approves orders, and where its order documents are kept. Where it
conflicts with this file, the add-on applies. Neither may conflict with an SOP.
