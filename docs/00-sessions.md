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
  played from the boot to the opening movie; the movies and the
  real-time cutscenes have English voices and no subtitles at all (the
  Japanese subtitle pictures on the disc go unused), and text appears
  only when the player examines things; the title menu's "Option" is
  the in-game options screen, with no subtitle or language setting.

## Session 2 (2026-09-26) — the code map, the recompiler, the first run

* **Discovery for GCC and SGL** in saturnkit (`09-recompiler.md`): GCC's
  switch in its forms, tables of records, computed jumps into unrolled
  code, handlers and callbacks reached by literal, `mova` or table, text
  and pointer pairs kept out: 1 688 functions, **1 250 of Ghidra's
  1 252**, none of the false ones. Virtual Hydlide loses no function.
* **The map** (`03-executables.md`, `tools/names-1st.tsv`): `main`'s
  states named (boot and title, title menu, wrong disc, save, load game,
  save screen, game loop), the frame function, the AVI player, the event
  player, the cutscene loader; SGL's and libgcc's routines, the division
  and fixed-point helpers checked in saturnkit's interpreter.
* **The SCU DSP program is the ADX decoder**: saturnkit's new `scudsp`
  disassembler shows it fetching 18-byte blocks, decoding 32 samples,
  writing 16-bit PCM to sound RAM.
* **No subtitles in the European program**: its cutscene loader never
  builds a `MV….SPR` name (the user had seen none in Beetle).
* **The recompiler** (`tools/recomp.py`): both discs' programs as C++,
  160 234 instructions each, built with clang; self-test 7 227 of 7 227
  vectors (and saturnkit's 9 300).
* **The first run** (`tools/run.py`, `11-runtime.md`): the recompiled
  game boots on saturnkit's runtime, draws its logos and title, plays the
  attract movie with its TrueMotion decoder, and its music is heard (by
  the counts), at SGL's 30 fps. saturnkit gained the SCU DSP interpreter
  and `SYS_CHGUIPR`. After New Game, loading stalls: GFS_SGL's music
  stream and a file read do not share the drive as on the Saturn (open
  question 14).
* saturnkit: ed37c63, 1f04233, 6f6b437 (`10-saturnkit.md`); Virtual
  Hydlide checked (51 485 of 51 485 vectors, the field reached with the
  same frames and sound) and moved to them.
