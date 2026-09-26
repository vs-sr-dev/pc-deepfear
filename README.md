# pc-deepfear

Toward a native PC port of **Deep Fear** (Sega Saturn, 1998, System Sacom
/ Sega), the survival horror set in an underwater naval base, in the
manner of the first Resident Evil games: pre-rendered rooms, 3D
characters, fixed cameras, and more than an hour of movies over two
discs. It was released only on the Saturn and never re-released. The
goal is the game running natively on PC: without slowdown, at the speed it
was made for, with instant loading, and sharper where the hardware allows
it.

This repository documents the discs, their formats and their code, and
grows the tooling for the port. It is the second port built on
**saturnkit**, the game-agnostic toolkit for Saturn reverse engineering
that grew out of [pc-virtualhydlide](https://github.com/vs-sr-dev/pc-virtualhydlide);
Deep Fear is where saturnkit meets SGL and GCC's code for the first time.
saturnkit is taken here as a submodule: clone with `--recursive`, or run
`git submodule update --init`.

## BYOA — Bring Your Own Assets

This repository contains **documentation and tools only**. No game data, no
executables, no assets. You need your own original discs. The work is done
on the European release, MK-81804 (V1.001, 1998-07-13), two discs, as
Redump-style .cue/.bin sets in `iso/`.

## Layout

    docs/            disc, format and code analysis, and the plan
    tools/           Deep Fear-specific data and tools: names-1st.tsv, recomp.py, run.py, oracle.py
    saturnkit/       game-agnostic Saturn toolkit (submodule)
    iso/, build/     your discs and everything derived from them (ignored by git)

## Tools

The Python tools need only Python 3.8+ and no dependencies. Building the
recompiled C++ needs CMake, Ninja, clang and SDL3 (MSYS2's mingw64, found at
`C:\msys64\mingw64\bin`). The oracle needs RetroArch with the Beetle
Saturn core. Run from the repository root.

```sh
D1="iso/Deep Fear (Europe) (Disc 1).cue"
D2="iso/Deep Fear (Europe) (Disc 2).cue"

# the discs: IP.BIN, the ISO 9660 volume, the tracks; extract them
python -m saturnkit.disc "$D1" --info
python -m saturnkit.disc "$D1" --list
python -m saturnkit.disc "$D1" --extract build/extract/disc1
python -m saturnkit.disc "$D2" --extract build/extract/disc2
python -m saturnkit.disc "$D1" --audio build/audio/disc1

# the code: where the program loads, a function, who builds an address
EXE=build/extract/disc1/1ST.BIN
python -m saturnkit.sh2 $EXE --find-base
python -m saturnkit.sh2 $EXE --base 06004000 --at 0603B784 --count 60   # slInitSystem
python -m saturnkit.sh2 $EXE --base 06004000 --refs 25FE0080:25FE0090   # the SCU DSP
python -m saturnkit.hw 25FE0080 06000250

# functions and code/data; the SCU DSP's program (the ADX decoder)
python -m saturnkit.recomp.discover $EXE --base 06004000 --report
python -m saturnkit.scudsp $EXE --base 06004000 --at 0605AB94 --count 204

# both discs' programs to C++, built with clang (MSYS2) and checked against the interpreter
python tools/recomp.py --build --test

# run it on saturnkit's runtime: headless with the pad script (to the title, the
# attract movie, New Game), pictures at chosen VBlanks, the CD block's commands
python tools/run.py -- --shot 600,1500
python tools/run.py -- --trace
python tools/run.py --play                 # a window, the keyboard or a gamepad

# the oracle: Beetle Saturn in RetroArch, pressed and photographed from here
python tools/oracle.py --at 36:START,39:START,60:START,66:shot    # to the first room
python tools/oracle.py --disc 2 --at 30:shot
```

## Status

Session 1: the survey. Two discs that differ only in their movies and
one byte of the program; a single program, `1ST.BIN`, compiled with GCC
on SGL, paced by SGL at 25 frames a second on a European Saturn at best;
the SCU DSP in use; the sound all ADX through Sega's driver; the formats
read at a glance and nothing compressed; Beetle Saturn driven to the
first room. Static recompilation looks simpler than Virtual Hydlide's (one
program instead of fifteen), with new work for saturnkit: GCC's switches,
the SCU DSP, SGL's timing, two discs (`docs/06-attack-plan.md`).

Session 2: the code map, the recompiler, the first run. saturnkit's
function discovery learned GCC's and SGL's code (1 250 of the 1 252
functions Ghidra finds); the program is C++ that passes its self-test;
on saturnkit's runtime, which gained the SCU DSP (Deep Fear's ADX
decoder), the game boots, shows its title and plays its attract movie
with sound. After New Game the loading stalls on the CD block. Next:
past the loading, into the first room (`docs/07-next-session.md`).

## Documentation

* [00-sessions.md](docs/00-sessions.md) — what each session did
* [01-disc-layout.md](docs/01-disc-layout.md) — IP.BIN, tracks, the file tree, the two discs
* [02-data-formats.md](docs/02-data-formats.md) — first look at the game's files
* [03-executables.md](docs/03-executables.md) — the program, SGL, the frame, the slave, the SCU DSP, function discovery
* [04-curiosities.md](docs/04-curiosities.md) — things found on the way
* [05-open-questions.md](docs/05-open-questions.md) — what is not known yet
* [06-attack-plan.md](docs/06-attack-plan.md) — feasibility, where to cut, what a better Deep Fear means, the phases
* [07-next-session.md](docs/07-next-session.md) — the next session's list
* [09-recompiler.md](docs/09-recompiler.md) — the program as C++: discovery on GCC and SGL, the counts, the self-test
* [11-runtime.md](docs/11-runtime.md) — the program on saturnkit's Saturn: how far it runs, the SCU DSP, the loading stall
* [10-saturnkit.md](docs/10-saturnkit.md) — what this port gave saturnkit

## Licence

MIT — see [LICENSE](LICENSE). Deep Fear is © 1998 Sega; this project
contains none of it.
