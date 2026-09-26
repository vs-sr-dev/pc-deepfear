# What this port gave saturnkit

saturnkit (`saturnkit/`, a submodule from
https://github.com/vs-sr-dev/saturnkit) was started by Virtual Hydlide's
port. Deep Fear is its second game, and the first on SGL and GCC. Each
entry is a saturnkit commit and what Deep Fear asked of it.

| Session | saturnkit | What |
|---|---|---|
| 1 | ce321fe (unchanged) | used as it is: `disc` (both discs, extraction, the audio track), `sh2` (`--find-base`, `--census`, `--refs`), `hw`, `recomp.discover --report`, `ghidra/ExportFuncs.java`. Nothing had to change to survey the discs and the code |

## What Deep Fear will ask

From session 1's survey (`03-executables.md`, `06-attack-plan.md`), in
the order the phases meet them:

* `recomp.discover`: GCC's switch (16-bit and 32-bit tables), SGL's
  assembly handlers and pointer tables as entries, strings kept out of
  the entries.
* An SCU DSP disassembler, then an interpreter in the runtime.
* The runtime: BIOS 0x06000250 (the slave's entry) and 0x06000280; SGL's
  VBlank order (the SH-2's DMAC channel 1, SCU DMA in indirect mode, the
  frame change by VDP1's end of drawing); a second disc and the tray.
* VDP2: what the game's backgrounds and screens set.
* Small: `disc --info` prints the ISO 9660 creation date raw
  (`1998071120214100$`, the last byte the time zone).
