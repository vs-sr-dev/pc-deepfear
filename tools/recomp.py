"""Recompile Deep Fear's program to C++ and check it.

    python tools/recomp.py [--build] [--test] [--no-vectors]

1. `python -m saturnkit.recomp`: `1ST.BIN` of each disc as its own module
   (DISC1, DISC2: the two differ in the disc number, an immediate in the
   code, so each is recognised by its own crc32), and saturnkit's
   instruction test, into build/recomp; report.txt there has the counts per
   module.
2. `python -m saturnkit.recomp.selftest`: the vectors of every function of
   disc 1's program that runs alone (on its stack, or on what its pointer
   arguments point at), and the named helpers, into build/recomp/selftest.
3. --build: CMake, Ninja and clang from MSYS2 into build/recomp-build.
4. --test: the self-test executable on every vectors file.

Run from the repository root, after both discs have been extracted
(build/extract/disc1, build/extract/disc2).
"""
import argparse
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
EXTRACT = os.path.join(ROOT, "build", "extract")
OUT = os.path.join(ROOT, "build", "recomp")
BUILD = os.path.join(ROOT, "build", "recomp-build")
NAMES = os.path.join(ROOT, "tools", "names-1st.tsv")
MSYS = r"C:\msys64\mingw64\bin"
BASE = 0x06004000

PROGRAMS = [("DISC1", "disc1"), ("DISC2", "disc2")]
# the named helpers the self-test always takes (tools/names-1st.tsv): the divisions, slMulFX
FUNCS = "0604338C,06044F50,0604CC74"


def spec(name, disc):
    return "%s=%s@%08X" % (name, os.path.join(EXTRACT, disc, "1ST.BIN"), BASE)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--no-vectors", action="store_true")
    a = ap.parse_args()
    from saturnkit.recomp.__main__ import generate, parse_spec
    from saturnkit.recomp import selftest
    t0 = time.time()
    generate([parse_spec(spec(n, d)) for n, d in PROGRAMS], OUT, optest=True)
    if not a.no_vectors:
        os.makedirs(os.path.join(OUT, "selftest"), exist_ok=True)
        selftest.main(["--out", os.path.join(OUT, "selftest", "disc1.txt"), "--image", spec("DISC1", "disc1"),
                       "--test", "DISC1", "--auto", "--funcs", FUNCS, "--names", NAMES])
    print("generated in %.0f s" % (time.time() - t0))
    env = dict(os.environ, PATH=MSYS + os.pathsep + os.environ["PATH"])
    tool = lambda x: shutil.which(x, path=env["PATH"])      # CreateProcess searches the parent's PATH
    if a.build:
        t = time.time()
        subprocess.run([tool("cmake"), "-S", OUT, "-B", BUILD, "-G", "Ninja", "-DCMAKE_CXX_COMPILER=clang++",
                        "-DCMAKE_C_COMPILER=clang"], env=env, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([tool("ninja"), "-C", BUILD], env=env, check=True)
        print("built in %.0f s" % (time.time() - t))
    if a.test:
        files = [os.path.join(OUT, "selftest", f) for f in ("optest.txt", "disc1.txt")]
        r = subprocess.run([os.path.join(BUILD, "selftest.exe")] + [f for f in files if os.path.exists(f)], env=env)
        sys.exit(r.returncode)


if __name__ == "__main__":
    main()
