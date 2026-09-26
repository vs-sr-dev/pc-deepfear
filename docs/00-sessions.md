# Sessions

## Session 1 (2026-09-26) — the discs, the code, the plan

* **The discs** (`01-disc-layout.md`): the European release, MK-81804
  V1.001 (1998-07-13), two discs of one data track and one 16-second
  audio track each. Everything but the movies is in `SOUND/` (2 908
  files), byte-identical on both discs; the discs differ in `MOVIE/` (72
  distinct AVIs, 23 on both) and in one byte of the program, its disc
  number. No CD-DA music.
* **The code** (`03-executables.md`): one program, `1ST.BIN`, at
  0x06004000, never swapped; compiled with GCC, on **SGL** (GFS_SGL 2.14,
  BUP 1.25). `slInitSystem` with the 320×256 mode and a frame rate of 2,
  `slDynamicFrame(ON)`: 25 fps on a European Saturn at best, frames that
  change when VDP1 is done. SGL's interrupt handlers, VBlank work (the
  SH-2's DMAC, SCU DMA in indirect mode), `slSynch`, its slave loop (the
  same FTCSR handshake as SBL's, with work every frame). The SCU DSP runs
  a 256-word program of the game's. Sound: Sega's driver Ver-2.10 and
  ADX.
* **Discovery on GCC's code**: `saturnkit.recomp.discover` finds 1 610
  functions and 1 238 of the 1 252 Ghidra finds (98.9 %); it does not
  know GCC's switch, SGL's assembly handlers, some pointer tables, and
  takes 39 strings for code.
* **The formats at a glance** (`02-data-formats.md`): 336×240 8 bpp
  backgrounds with foreground masks, SGL-style models and VDP1 textures,
  animations, room boxes and cameras, ADX and ACX, TrueMotion 1 AVIs;
  nothing compressed. Pictures and models decoded as checks.
* **The oracle**: `tools/oracle.py`, Beetle Saturn with both discs in an
  .m3u; from the boot to the first room (the ERS Room, CCD-Area 2F) and
  the in-game menu.
* **The plan** (`06-attack-plan.md`): static recompilation, simpler than
  Virtual Hydlide's (one program, stills for backgrounds, all-ADX sound),
  with saturnkit to learn GCC's code, the SCU DSP, SGL's timing, a second
  disc; the frame rate and the resolution as the port's gains.
* saturnkit unchanged this session (`10-saturnkit.md`).
* **Heard and seen by the user** in Beetle: the 16-second audio track is
  a wordless jingle, not the spoken CD-player warning, and it is not
  played from the boot to the opening movie; the attract and opening
  movies have English voices and no subtitles.
