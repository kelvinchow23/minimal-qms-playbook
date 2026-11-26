---
name: lab-drivers
description: Write device drivers and sensor code for lab hardware with one serial protocol and proven sensor practices, so instruments built under minimalQMS talk to lab software the same way. Use when writing firmware or host code that talks to a lab device or reads a sensor.
metadata:
  rev: A
  status: draft
---

# Lab device drivers

Carries out SOP-004 section 9 (build package: software) for firmware and host drivers.

## Serial protocol

1. Serial at 230400 baud, 8N1.
2. Messages are JSON, one per line.
3. Every command gets a handshake: `ACK` on receipt, `BEGIN` when the action starts, `END`
   when it finishes, or an error. The host does not send the next command before `END`.
4. Publish drivers under the BSD licence unless the project says otherwise.

## Sensors

1. Sensirion I2C sensors (e.g. SEN5x, SGP4x, SHT4x): talk to them over raw I2C (e.g.
   `smbus2`) and check the CRC-8 on every word.
2. Enclosures change gas and humidity readings: an open sensor beats a printed enclosure for
   VOC and RH. When a sensor must be enclosed, vent it well, keep it away from heat sources, and
   verify readings against an open reference.

## Organization add-on

If the private playbook is cloned beside this repo, also read
`minimal-qms-playbook-private/skills/lab-drivers/lab-drivers-private-addon.md`. It adds local
conventions. Where it conflicts with this file, the add-on applies. Neither may conflict with
an SOP.
