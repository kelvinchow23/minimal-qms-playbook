"""Slice released STL files into a ready-to-print Bambu Studio 3MF (project + G-code), for one build.

Usage:
    python slice_bambu.py --printer P1S --out builds/B001/B001_print_P1S.3mf \\
        --part "make_files/LSN-0001_base_rev_A.stl:2" --part "make_files/LSN-0002_lid_rev_A.stl:2:flip"

--part STL:COUNT[:flip]   the released STL (from appendix A02), how many to print, and "flip" to
                          print it upside down (rotated 180 degrees about X, e.g. a lid with its
                          flat top on the bed). Repeat for each part.
--printer P1S | H2S       the printer (Bambu Lab, 0.4 mm nozzle). Profiles are Bambu's own system
                          presets: 0.20 mm Standard, Bambu PETG HF, Textured PEI plate.
--filament NAME           a Bambu system filament preset instead of PETG HF for that printer.

Everything lands on one plate (Bambu arranges it). The 3MF holds the plate's G-code, so it can be
sent to the printer as is, and the settings it was sliced with, so the print can be repeated.
Objects are named after the part (e.g. "LSN-0001 base rev A"), never after a local path.
Needs Bambu Studio installed. Standard-library Python only.
"""
import argparse
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile

STUDIO = r"C:\Program Files\Bambu Studio"
PROFILES = os.path.join(STUDIO, "resources", "profiles", "BBL")
PRINTERS = {
    "P1S": {"machine": "Bambu Lab P1S 0.4 nozzle", "process": "0.20mm Standard @BBL X1C",
            "filament": "Bambu PETG HF @BBL P1S 0.4 nozzle"},
    "H2S": {"machine": "Bambu Lab H2S 0.4 nozzle", "process": "0.20mm Standard @BBL H2S",
            "filament": "Bambu PETG HF @BBL H2S"},
}
PLATE = "Textured PEI Plate"   # PETG does not release from the cool plate


def find(kind, name):
    for dp, _, fs in os.walk(os.path.join(PROFILES, kind)):
        if name + ".json" in fs:
            return os.path.join(dp, name + ".json")
    sys.exit(f"Bambu preset not found: {kind}/{name}")


def flat(kind, name):
    """A system preset with its 'inherits' chain resolved (the CLI needs full settings)."""
    d = json.load(open(find(kind, name), encoding="utf-8"))
    base = flat(kind, d["inherits"]) if d.get("inherits") else {}
    base.update(d)
    base.pop("inherits", None)
    return base


def read_stl(path):
    b = open(path, "rb").read()
    if b[:5] == b"solid" and b"facet" in b[:400]:
        sys.exit(f"{path}: ASCII STL; export binary STL")
    n = struct.unpack("<I", b[80:84])[0]
    return [(list(struct.unpack("<12f", b[84 + i * 50:84 + i * 50 + 48])), b[84 + i * 50 + 48:84 + i * 50 + 50])
            for i in range(n)]


def write_stl(path, tris, header):
    out = bytearray(header.encode()[:80].ljust(80, b" ") + struct.pack("<I", len(tris)))
    for v, attr in tris:
        out += struct.pack("<12f", *v) + attr
    open(path, "wb").write(out)


def part_name(stl):
    # LSN-0001_base_rev_A.stl -> "LSN-0001 base rev A"
    return os.path.splitext(os.path.basename(stl))[0].replace("_", " ")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--printer", required=True, choices=sorted(PRINTERS))
    ap.add_argument("--part", action="append", required=True, metavar="STL:COUNT[:flip]")
    ap.add_argument("--out", required=True)
    ap.add_argument("--filament")
    args = ap.parse_args()

    presets = dict(PRINTERS[args.printer])
    if args.filament:
        presets["filament"] = args.filament
    work = tempfile.mkdtemp(prefix="slice_")
    try:
        files = {}
        for kind, name in presets.items():
            d = flat(kind, name)
            d["from"], d["name"] = "system", name
            if kind == "process":
                d["curr_bed_type"] = PLATE
            files[kind] = os.path.join(work, kind + ".json")
            json.dump(d, open(files[kind], "w", encoding="utf-8"), indent=1)

        models = []
        for spec in args.part:
            m = re.match(r"^(.+?\.stl)(?::(\d+))?(?::(flip))?$", spec, re.I)
            if not m:
                sys.exit(f"--part {spec!r}: expected STL:COUNT[:flip]")
            stl, count, flip = m.group(1), int(m.group(2) or 1), bool(m.group(3))
            name = part_name(stl) + (" (flipped)" if flip else "")
            local = os.path.join(work, name + ".stl")
            tris = read_stl(stl)
            if flip:
                zmin = 1e9
                for v, _ in tris:
                    for k in (0, 3, 6, 9):
                        v[k + 1], v[k + 2] = -v[k + 1], -v[k + 2]
                    zmin = min(zmin, v[5], v[8], v[11])
                for v, _ in tris:
                    for k in (5, 8, 11):
                        v[k] -= zmin
            write_stl(local, tris, name)
            models += [os.path.basename(local)] * count

        out_name = os.path.basename(args.out)
        cmd = [os.path.join(STUDIO, "bambu-studio.exe"), "--slice", "0", "--arrange", "1",
               "--load-settings", files["machine"] + ";" + files["process"],
               "--load-filaments", files["filament"], "--export-3mf", out_name, "--outputdir", work] + models
        subprocess.run(cmd, cwd=work, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=900)
        res = json.load(open(os.path.join(work, "result.json"), encoding="utf-8"))
        if res.get("return_code") != 0:
            sys.exit(f"Bambu Studio: {res.get('error_string')} (code {res.get('return_code')})")
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        shutil.copyfile(os.path.join(work, out_name), args.out)

        z = zipfile.ZipFile(args.out)
        info = z.read("Metadata/slice_info.config").decode()
        secs = re.search(r'key="prediction" value="(\d+)"', info)
        grams = re.search(r'key="weight" value="([\d.]+)"', info)
        print(f"wrote {args.out}: {args.printer}, {presets['process']}, {presets['filament']}, {PLATE}")
        print(f"  {len(models)} parts on 1 plate; about {int(secs.group(1)) / 3600:.1f} h, {grams.group(1)} g"
              if secs and grams else "  (no time/weight in slice info)")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
