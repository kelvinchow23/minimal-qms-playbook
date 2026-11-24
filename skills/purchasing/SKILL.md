---
name: purchasing
description: Order the parts for a build and record the order in the product repo (minimalQMS SOP-005), using the OTS library's requisition.py and record_order.py. Use when someone asks for order files for N units, says an order was placed, or records parts received.
metadata:
  rev: A
  status: draft
---

# Purchasing

Carries out SOP-005. The tools are in the `minimal-qms-ots-library` repo; run them from its root.
The organization's own ordering steps (its purchasing system, approvals, who places the
order) are in the organization add-on, not here.

## Before ordering

1. Every PN to be ordered is `released` (SOP-002 section 5). Prototype parts for design work
   are the exception; mark them `proto` in `notes`.
2. Every supplier is in `purchasing/suppliers.csv`. Add a new supplier before its first
   order, with a basis (SOP-005 section 3).
3. Prices have a date. Check any price older than 90 days.

## Making the order files

1. Generate one upload file per supplier from the BOM and the build quantity:

   ```
   python tools/requisition.py <product>/03_build_package/bom.csv <TOP-PN> <qty> --out out/
   ```

   Add `--stock stock.csv` to subtract stock on hand.
2. Report every warning to the human (missing or old prices, unknown PNs). Do not guess a
   missing value.
3. The human checks the files and places the order through the organization's system. An
   agent never places an order.

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
2. Inspect Class A lines (SOP-006) and record the result in `inspection`.
3. A failed inspection opens a nonconformance (SOP-008).

## Organization add-on

If the private playbook is cloned beside this repo, also read
`minimal-qms-playbook-private/skills/purchasing/purchasing-private-addon.md`. It says how the
organization places and approves orders, and where its order documents are kept. Where it
conflicts with this file, the add-on applies. Neither may conflict with an SOP.
