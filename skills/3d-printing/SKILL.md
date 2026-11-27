---
name: 3d-printing
description: Prepare and record the 3D prints for a build (minimalQMS SOP-006): slice the released STL files into a ready-to-print Bambu Studio 3MF with slice_bambu.py, file it with the build, and record which printer, filament and file made the parts. Use when a build needs printed parts, or someone asks for a slicer file or plate.
metadata:
  rev: A
  status: draft
---

# 3D printing

Carries out the printed-part side of a build (SOP-006). The released make files (appendix A02)
are STLs with a print note ("PETG, any colour, standard print profile"); they say what to make,
not how one printer made it. The sliced 3MF is the record of how a build's parts were printed,
so a print can be repeated exactly.

## Equipment
A printer makes parts; it does not measure them, so it needs no calibration (ISO 9001 §7.1.5
covers measuring equipment). The printed parts are checked by the build's own checks. Record
which printer and filament made each part, so a bad batch can be traced.

## Slicing for a build
1. Use the released STLs from `02_design/build_document/make_files/` (the files in A02), never a
   working CAD export.
2. Slice one plate per build and printer with [slice_bambu.py](slice_bambu.py):

   ```
   python slice_bambu.py --printer P1S --out <product>/builds/B00n/B00n_print_P1S.3mf \
       --part "<make_files>/<PN>_base_rev_A.stl:2" --part "<make_files>/<PN>_lid_rev_A.stl:2:flip"
   ```

   - `:COUNT` is parts per plate (units in the build x quantity per unit).
   - `:flip` prints a part upside down: use it for a lid or cover with a flat top, so the flat
     face is on the bed and nothing needs supports.
   - Profiles are Bambu's own system presets (0.20 mm Standard, Bambu PETG HF, Textured PEI
     plate), so the file is reproducible on any Bambu Studio install. `--printer` is P1S or H2S
     (0.4 mm nozzle); make one file per printer the human might use and let them pick.
3. Check the plate thumbnail in the 3MF (`Metadata/plate_1.png`): every part on the plate, each
   the right way up. Report the print time and filament use the script prints.
4. The 3MF holds the G-code: the human sends it to the printer as it is.

## Recording
- File the 3MFs in the build's folder: `builds/B00n/B00n_print_<printer>.3mf` (Git LFS).
- When the parts are printed, record in `builds/B00n/build.yaml` which file was printed, on which
  printer, with which filament (brand, colour, lot if known), and the date.
- After a fix to a printed part (a new export in A02), slice again; the old 3MF stays with the
  build that used it.
