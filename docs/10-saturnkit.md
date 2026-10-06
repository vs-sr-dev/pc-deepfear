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

| — | 4061b12, b9cbbb8 (from X JAPAN) | the third port's: XA discs, discovery through far jumps, TVSTAT's HBLANK, the pad read directly, `--record-input`. Checked here by that session: the headless run's pictures and sound byte-identical |
| 3 | be42e26 | the CD block's Play as Mednafen's: mode 0xFF changes nothing, bit 7 keeps the pickup where it reads, 0xFFFFFF the last Play's position, the play ending when the position leaves its range. GFS_SGL's stream and file reads then share the drive (open question 14) |
| 3 | 1413f52 | the division unit's shadows of DVDNTH/DVDNTL at 0x118/0x11C, which SGL's `slLookAt` reads (every matrix was zero, so every vertex); the SH-2 DMAC's 16-byte transfers whole (they moved a quarter: the logos' and the menu's missing lines, open question 15, and the room's name box) |
| 3 | 4235bbc, 65e9f59 | `--dump` holds VDP2's registers; the windows note reads WCTL; the README's ports table and checks |
| 3 | 5d0471b, 88d5062 | VDP2's windows 0 and 1 (rectangles or line tables, inside or outside, OR or AND) on NBG0–NBG3 and the sprite layer: the letterbox's bands, where the user saw stray pixels |

Each change was checked on Virtual Hydlide: its 15 programs recompiled,
the self-test (51 485 of 51 485 vectors; 51 542 in session 3), the
headless run to the field (same frames, same sound); its submodule moved
to 6f6b437 (its commit a5d8199), then 65e9f59 (074c9ac) and 88d5062
(c69eadb). From session 3 also on X JAPAN (self-test 11 632 of 11 632,
the headless run the same before and after), moved to 65e9f59 (ab4c653)
and 88d5062 (f384478). For the windows both runs' pictures were compared
before and after: 48 and 51 shots, pixel-identical.

## What Deep Fear will ask next

* A second disc and the tray.
* Small: `disc --info` prints the ISO 9660 creation date raw
  (`1998071120214100$`, the last byte the time zone).
