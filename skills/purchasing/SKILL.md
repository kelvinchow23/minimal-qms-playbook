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
1. Ask how many units the build is for, what is already on hand (inventory, spares from
   an earlier build), and whether anything else should go on the same supplier reqs (other
   projects, side projects, stock). For an exact part (A01 Purchasing "exact part"), check that the stock is
   that exact part; for "any matching part", that it matches the description.
2. Write the stock to `builds/B00n/stock.csv` (`pn,qty_on_hand`, in pieces) and run the tool
   with it, writing everything for the order into the build's folder:

   ```
   python tools/requisition.py <product>/02_design/build_document/bom.csv <TOP-PN> <units> \
       --build B00n --stock <product>/builds/B00n/stock.csv --out <product>/builds/B00n/ \
       --plan <product>/builds/B00n/parts_plan.csv --sheet <product>/builds/B00n/order_sheet.md \
       [--extra <product>/builds/B00n/extras.csv]
   ```

   **Extras** are lines that are not for this build but ride on the same req (one req per
   supplier). `extras.csv` has `pn,qty,for`, e.g. `ECM-0005,2,inventory`. Add a part you will
   buy again to the OTS library first (`new_pn.py`), with its supplier part number and price
   read from the supplier's page; a true one-off may leave `pn` blank and give description,
   supplier, supplier_pn, unit_price, pack_qty, currency and link. Extras are ordered as
   listed; the order sheet shows what each line is for and the total per purpose. When the
   order is recorded, only this product's lines go in its `purchasing/purchases.csv`: pass the
   parts plan to `record_order.py` (`--plan builds/B00n/parts_plan.csv`).

3. **The human reviews the order sheet** (`builds/B00n/order_sheet.md`): how many purchase reqs
   to send (one per supplier), each req's lines, quantities, prices and totals (also in CAD),
   the parts taken from stock (marked where they must be the exact part), the parts made in
   house, and a short checklist. Report every warning on it (missing or old prices, unknown
   PNs); do not guess a missing value. Change the stock or the quantity and rerun until the
   human agrees with the sheet.

## Making the purchase reqs

1. Each req section on the order sheet names its upload file (`builds/B00n/<supplier>-<date>.csv`,
   one per supplier, for the "order" lines only). That file is what the organization's
   purchase-req step reads (organization add-on: Airtable).
2. Make one req per section, only after the human has approved the order sheet. An agent never
   places an order.

## Where the files go (product repo)

| File | Where | When |
|---|---|---|
| **Order sheet to review** (reqs, lines, totals, stock, checklist) | `builds/B00n/order_sheet.md` | when the order is decided |
| Parts plan, stock count and extras for a build | `builds/B00n/parts_plan.csv`, `stock.csv`, `extras.csv` | when the order is decided |
| Upload file per supplier (draft until the req is made) | `builds/B00n/<supplier>-<date>.csv` | when the order is decided |
| Order file as submitted | `purchasing/requisitions/<order_ref>.csv` | after ordering (`record_order.py`) |
| One line per item ordered | `purchasing/purchases.csv` | after ordering (`record_order.py`) |
| Approved suppliers | `purchasing/suppliers.csv` | before a supplier's first order |

## Recording the order

1. Ask the human for the order reference (requisition or PO number) and the actual order date.
2. Record it in the product repo, on a branch:

   ```
   python tools/record_order.py <product>/builds/B00n/<supplier>-<date>.csv <Supplier> "<order_ref>" <product> \
       --plan <product>/builds/B00n/parts_plan.csv [--date YYYY-MM-DD]
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
