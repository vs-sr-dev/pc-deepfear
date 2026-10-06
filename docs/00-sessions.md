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
  attract movie with its TrueMotion decoder and its sound, at SGL's 30
  fps. Played by the user in a window: the title menu right but for its
  text, the logos cut to their top, the menu's sound effects right; the
  title is silent, as on Beetle. saturnkit gained the SCU DSP interpreter
  and `SYS_CHGUIPR`. After New Game, loading stalls: GFS_SGL's music
  stream and a file read do not share the drive as on the Saturn (open
  question 14).
* saturnkit: ed37c63, 1f04233, 6f6b437 (`10-saturnkit.md`); Virtual
  Hydlide checked (51 485 of 51 485 vectors, the field reached with the
  same frames and sound) and moved to them.

## Session 3 (2026-10-06) — the first room

* **Past the loading** (open question 14): GFS_SGL streams the music
  with Play commands of mode 0xFF that only push the end on, and reads
  the next file once the stream's play has ended. saturnkit's CD block
  took 0xFF as "repeat for ever" and every Play as a seek back; its Play
  now follows Mednafen's. "Now Loading...", the opening movie, then the
  first room's files.
* **The ERS Room** (`11-runtime.md`): the background on NBG1 (open
  question 4), but nothing of VDP1 in place. The slave's polygons came
  from a zero matrix: SGL's `slLookAt` reads its quotient from the
  division unit's shadow register 0xFFFFFF1C, which the runtime never
  wrote. With it, John Mayor on the hatch, his shadow, the AIR and HP
  gauges; UP makes him walk.
* **The SH-2 DMAC's 16-byte transfers moved a quarter of their bytes**:
  the room's name box half grey, and the cause of session 2's cut logos
  and missing menu text (open question 15) — not VDP2's rotation planes,
  which the game never turns on.
* Headless, from the boot to the room, every screen as Beetle's.
* **Played by the user** into the room: everything works, but for stray
  pixels in the black bands. They were the background's top and bottom
  rows: the game letterboxes the screen to lines 16–239 with VDP2's
  window 0, which saturnkit did not draw. Windows 0 and 1 now done;
  the user played it again: the bands clean.
* **Room to room, played by the user**: the doors and the transitions
  between rooms work. The menu works; the item screen's colours were
  wrong and the map looked different: the runtime's CD drive read at 4x
  with no seek, so a file's palette was overwritten by the next file
  before SGL's VBlank copy. Now 2x with Mednafen's seek times; both
  screens as Beetle's.
* The player's trousers show 2–3 pixels over the Conference Room's
  table: the foreground mask's own edge, **the same on Beetle and on the
  user's Saturn**.
* Three loud buzzes heard by the user: after a seek the runtime showed
  PLAY before the first sector, and the movie player read its stale
  buffers. PLAY now waits for a sector, as in Mednafen; the user's
  recorded play, given back, is clean.
* saturnkit: be42e26, 1413f52, 4235bbc, 65e9f59, 5d0471b, 88d5062
  (`10-saturnkit.md`); Virtual Hydlide (51 542 of 51 542 vectors, the
  field with the same frames, the same pictures) and X JAPAN (11 632 of
  11 632, the same run and pictures) checked and moved to them.
