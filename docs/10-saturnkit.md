# What this port gave saturnkit

saturnkit (`saturnkit/`, a submodule from
https://github.com/vs-sr-dev/saturnkit) was started by Virtual Hydlide's
port. Deep Fear is its second game, and the first on SGL and GCC. Each
entry is a saturnkit commit and what Deep Fear asked of it.

| Session | saturnkit | What |
|---|---|---|
| 1 | ce321fe (unchanged) | used as it is: `disc` (both discs, extraction, the audio track), `sh2` (`--find-base`, `--census`, `--refs`), `hw`, `recomp.discover --report`, `ghidra/ExportFuncs.java`. Nothing had to change to survey the discs and the code |
| 2 | ed37c63 | `recomp.discover` for GCC and SGL: GCC's switch (16-bit, 8-bit, absolute 32-bit), `mova` not marking data, literal and table pointer seeds with text and pointer-pair guards (1 250 of Ghidra's 1 252 here). `scudsp`: the SCU DSP's instructions decoded and disassembled |
| 2 | 1f04233, 6f6b437 | the runtime's SCU DSP interpreter (`runtime/scudsp.cpp`); `SYS_CHGUIPR` and the per-interrupt SCU masks in the BIOS dispatcher; discovery of `mova`-stored pointers, tables of records, computed jumps into unrolled code, GCC's switch dispatched after a `bra`; the emitter's volatile pool slots written through `mova`, calls through them at run time. (1f04233 holds only `scudsp.cpp` by mistake; 6f6b437 the rest) |

Each change was checked on Virtual Hydlide: its 15 programs recompiled,
the self-test (51 485 of 51 485 vectors), the headless run to the field
(same frames, same sound); its submodule moved to 6f6b437 (its commit
a5d8199).

## What Deep Fear will ask next

* The CD block: GFS_SGL's stream and file reads sharing the drive (open
  question 14).
* VDP2 and VDP1: the logo screens' missing lines, the menu's text, then
  the rooms' backgrounds and masks.
* A second disc and the tray.
* Small: `disc --info` prints the ISO 9660 creation date raw
  (`1998071120214100$`, the last byte the time zone).
