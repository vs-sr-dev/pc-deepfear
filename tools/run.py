"""Run Deep Fear on saturnkit's runtime: to play it, or headless, and report what it did.

    python tools/run.py --play [--disc 2] [-- saturn args...]    # a window, the keyboard and a gamepad
    python tools/run.py [--vblanks N] [--trace] [--report] [--input SCRIPT] [-- saturn args...]

--play opens the window (keys in saturnkit/runtime/host.cpp: arrows, Enter
START, Z X C = A B C, A S D = X Y Z, Q W = L R; F12 saves the picture, F11
fullscreen) with no pad script and no end. Without it the run is headless:
it boots the disc (iso/*(Disc N).cue) into the recompiled program
(build/recomp-build, from `python tools/recomp.py --build`), with the pad
script that reaches the first room: START on the title, START on New
Game, START to skip the opening movie. The run is deterministic (virtual
time), so the same script always gets to the same place.

--report prints the hardware log of the run (build/run/hw-log.txt) as
Markdown tables, registers named by saturnkit.hw.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
from collections import defaultdict

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
BUILD = os.path.join(ROOT, "build", "recomp-build")
OUT = os.path.join(ROOT, "build", "run")
MSYS = r"C:\msys64\mingw64\bin"

# VBlanks (60 Hz): the title takes START from about 1000; New Game; the opening movie (from about 1850)
ROOM_SCRIPT = "1100:START,1108:,1250:START,1258:,2300:START,2308:"


def report(path):
    from saturnkit import hw
    regs, areas = [], []
    for line in open(path):
        p = line.split()
        if p[0] == "reg":
            regs.append((p[1], int(p[2]), int(p[3], 16), int(p[4])))
        elif p[0] == "area":
            areas.append((p[1], " ".join(p[2:-3]), int(p[-3], 16), int(p[-2], 16), int(p[-1])))
    blocks = defaultdict(list)
    for rw, size, a, n in regs:
        name = hw.name(a) or "?"
        blocks[name.split(".")[0] if "." in name else name].append((a, name, rw, size, n))
    print("| Block | Register | Address | Access | Count |")
    print("|---|---|---|---|---|")
    for block in sorted(blocks):
        for a, name, rw, size, n in sorted(blocks[block]):
            reg = name.split(".", 1)[1] if "." in name else "-"
            print("| %s | %s | 0x%08X | %s%d | %s |" % (block, reg, a, rw, size * 8, format(n, ",").replace(",", " ")))
    print()
    print("| Area | Access | Lowest | Highest | Count |")
    print("|---|---|---|---|---|")
    for rw, name, lo, hi, n in sorted(areas, key=lambda x: (x[1], x[0])):
        print("| %s | %s | 0x%08X | 0x%08X | %s |" % (name, rw, lo, hi, format(n, ",").replace(",", " ")))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--play", action="store_true", help="a window, no pad script, no end")
    ap.add_argument("--disc", type=int, default=1, choices=(1, 2))
    ap.add_argument("--vblanks", type=int, default=3000)
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--report", action="store_true", help="print the hardware log as Markdown, do not run")
    ap.add_argument("--input", default=None, help="pad script (default: the one that reaches the first room)")
    ap.add_argument("rest", nargs="*", help="more arguments for the saturn executable")
    a = ap.parse_args()
    if a.report:
        report(os.path.join(OUT, "hw-log.txt"))
        return
    cue = glob.glob(os.path.join(ROOT, "iso", "*(Disc %d).cue" % a.disc))
    if not cue:
        sys.exit("no disc %d .cue in iso/" % a.disc)
    os.makedirs(OUT, exist_ok=True)
    env = dict(os.environ, PATH=MSYS + os.pathsep + os.environ["PATH"])
    exe = shutil.which("saturn", path=BUILD) or os.path.join(BUILD, "saturn.exe")
    cmd = [exe, "--cue", cue[0], "--out", OUT]
    if a.play:
        if a.input is not None:
            cmd += ["--input", a.input]
    else:
        cmd += ["--headless", "--vblanks", str(a.vblanks), "--input", a.input if a.input is not None else ROOM_SCRIPT]
    if a.trace:
        cmd.append("--trace")
    sys.exit(subprocess.run(cmd + a.rest, env=env).returncode)


if __name__ == "__main__":
    main()
