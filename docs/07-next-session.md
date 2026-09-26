# Next session: the code map (phase 2)

Where things stand: the discs, the program and the formats are surveyed
(`01`–`03`, `02-data-formats.md`), Beetle reaches the first room, and the
route is planned (`06-attack-plan.md`). Nothing runs on saturnkit yet.

## First: discovery on GCC's code, in saturnkit

The recompiler can only be as good as the function list. Against Ghidra
(`03-executables.md`; its lists are in `build/ghidra/`, with the seed
script, and the command to remake them below):

1. **GCC's switch**: `mova TABLE,r0; mov.w @(r0,rN),rN; add rN,r0; jmp @r0`
   with halfword offsets from the table, bounded by a `cmp/hi` (or
   `cmp/hs`) and a branch before; there is a 32-bit form too (`mov.l
   @(r0,rN),rN; jmp @rN`: 0x0603F1A4, 0x0603F93C, 0x06055628). Add both
   to `discover`'s switch forms. Check: main's switch at 0x06004110
   resolves to its 8 states; the 44 GCC switches of the unresolved list
   go.
2. **SGL's handlers**: a pointer handed to `SYS_SETUINT` (or stored as a
   vector) is an entry whatever its first instruction (`mov.l r0,@-r15`…).
   More generally: a pointer target in an unclassified gap whose descent
   has no problems is an entry. Check: the 14 Ghidra-only functions, the
   56 blocks.
3. **Strings**: a pointer target whose bytes are printable text ending in
   a zero is data, not code. Check: the 39 false entries go.
4. Then: every change checked on Virtual Hydlide (its discovery counts,
   `tools/recomp.py --build --test`, `tools/run.py` to the field).

Ghidra, to remake the reference list (PowerShell):

```
$env:JAVA_HOME = 'J:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot'
D:\Tools\ghidra_12.1.2_PUBLIC\support\analyzeHeadless.bat build\ghidra\proj deepfear1st `
  -import build\extract\disc1\1ST.BIN -overwrite -processor SuperH:BE:32:SH-2 `
  -loader BinaryLoader -loader-baseAddr 0x06004000 -scriptPath build\ghidra\scripts `
  -preScript SeedEntry.java -postScript ExportFuncs.java build\ghidra\ghidra_funcs.tsv
```

(`-scriptPath` takes one directory through the .bat, so
`build/ghidra/scripts/` holds a copy of `saturnkit/ghidra/ExportFuncs.java`
beside `SeedEntry.java`, the pre-script that seeds the entry point; the
seed script could join saturnkit's `ghidra/`.)

## Then: the map of the program

* **SGL's functions named**: `tools/names-1st.tsv` with what is known
  (`slInitSystem` 0x0603B784, `slDynamicFrame` 0x0604AF60, `slSynch`
  0x0604BFBE, the handlers, the DSP routines, the BIOS calls), then the
  rest of SGL by reading (the matrix and polygon functions, `slPutPolygon`,
  the sprite functions, the sound and PCM calls, GFS).
* **`main`'s 8 states** (0x06063410): which is the title, the new game,
  the room loop, the movies, the menus.
* **The room loop**: where a room is loaded (backgrounds, ATR, SF, models),
  where the camera is chosen, how the background and its mask reach VDP2
  (open question 4).
* **The frame and the logic** (open question 1): read how the player's
  motion is stepped, to know before the runtime whether 60 fps will need
  interpolation.
* **The SCU DSP**: a disassembler in saturnkit (SCU DSP instruction set:
  ALU, X/Y buses, D1 bus, loads, DMA, jumps, END), then the program at
  0x0605AB94 read (open question 2), and where ADX is decoded (3).
* **The change of disc** (5): how the game asks, what it checks.
* The interpreter (`saturnkit.sh2emu`) on SGL's leaf routines as a first
  check that it runs GCC's and SGL's code: fixed-point multiply, divide,
  sine, matrix.

## Keep in mind

* The oracle's route to the first room: `python tools/oracle.py --at
  36:START,39:START,60:START,66:shot` (START at 30 s is too early: the
  title ignores it).
* Beetle runs the European disc at 50 Hz; the port will run 60 Hz VBlanks.
