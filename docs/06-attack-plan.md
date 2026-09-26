# The porting route

## Verdict: feasible, by static recompilation, and simpler than Virtual Hydlide

| Road | Meaning | Verdict |
|---|---|---|
| Reimplementation | a new engine reading the assets | No: the formats are readable (`02-data-formats.md`), but the game's logic (rooms, events, enemies, the air, the cutscenes) lives in ~1 600 functions with no symbols |
| Decompilation | rebuild C source and compile it for PC | No: the same functions, by hand |
| Enhanced emulation | an emulator with more speed | Not a port, and GPL code. Beetle Saturn is the oracle only |
| **Static recompilation** | the SH-2 code to C++, the hardware reimplemented | **Yes**, the route Virtual Hydlide proved |

Why it is favourable here:

1. **One program.** `1ST.BIN`, 360 KB, about 1 600 functions, loaded once
   at 0x06004000: no program swapping, no module recognised by its crc32
   among many, no resident system to reach through pointers. Virtual
   Hydlide had 15 programs and 10 000 functions.
2. **SGL.** The engine sits on Sega's library, whose hardware use is
   regular and documented in spirit: one frame machine, one slave
   handshake, one sound interface. What saturnkit learns from it serves
   every SGL game, most of the Saturn's library.
3. **The pictures are stills.** The rooms are pre-rendered backgrounds,
   one per camera; the 3D is the characters over them (`02-data-formats.md`).
   Little VDP1 work a frame, and a clear line between the still and the
   moving: good for the frame rate and for the resolution.
4. **The sound is all ADX** (no sequences, no tone banks, no CD-DA
   music), played through Sega's driver on the 68000, which saturnkit
   already runs.
5. **The movies decode in the game's own code** (Duck TrueMotion 1),
   recompiled like the rest; the files are standard AVIs that ffmpeg reads,
   a check for whatever the runtime shows.

What is new, and so harder:

1. **GCC's code.** `discover` finds 98.9 % of Ghidra's functions, but not
   GCC's switch, SGL's assembly handlers and pointer tables, and it takes
   some strings for code (`03-executables.md`).
2. **The SCU DSP.** A 256-word program runs on it; the runtime needs an
   interpreter (and saturnkit a disassembler to read the program).
3. **SGL's timing.** The frame changes by VDP1's end of drawing (dynamic
   frame), the VDP2 registers arrive by the SH-2's DMAC every VBlank,
   VDP1 and VDP2 lists by SCU DMA in indirect mode, the slave works every
   frame. The runtime's order of events at VBlank has to be right for SGL.
4. **Two discs**, and a change of disc in the middle of the game.
5. **VDP2 in new ways**: 8 bpp cell pictures of 336×240 in a 320×256
   mode, a foreground mask, whatever else SGL sets (rotation, windows,
   line scroll) where the game uses it.

## Where to cut

The rule of saturnkit: **cut at the hardware registers, not at library
APIs**. SGL then needs no special case: its assembly runs recompiled like
the rest, against the same hardware. The table lists what Deep Fear asks
beyond what Virtual Hydlide already made.

| Subsystem | Deep Fear | saturnkit now | To add |
|---|---|---|---|
| Master SH-2 | GCC and SGL assembly, GBR-relative addressing | the recompiler, self-tested on every form | discovery: GCC's switch, handlers, pointer tables, strings |
| Slave SH-2 | SGL's loop (FTCSR poll, a pointer at 0x060542C4), work every frame | a coroutine woken at SINIT | check it holds with a job every frame |
| BIOS | SETUINT, SCU mask, clock, BUP, slave vector 0x06000250, 0x06000280, reset | HLE of ~15 services | 0x06000250 as the slave's entry, 0x06000280 |
| SCU | DMA levels 0–2, **indirect** mode at VBlank, the **DSP** | interrupts, timers, DMA direct and indirect | the DSP (interpreter; disassembler) |
| SH-2 on-chip | **DMAC channel 1** every VBlank, FRT for timing, division | division unit, FRT, DMAC | check the DMAC as SGL drives it |
| SMPC | INTBACK through SGL's handler, the direct ports PDR/DDR | INTBACK, a scripted pad | the direct mode if the game uses it |
| CD block | GFS_SGL 2.14, AVI streaming, two discs | the registers over .cue/.bin | a second disc and the tray (the change of disc) |
| VDP1 | SGL's command lists: textured Gouraud polygons, sprites; dynamic frame change | software, every command | its end-of-drawing timing as SGL reads it |
| VDP2 | 320×256; 8 bpp cell backgrounds, masks, text layers, the movies | NBG0–3 cells and bitmaps, zoom, priorities, colour calculation | what the game sets: rotation? windows? line scroll? |
| SCSP + 68000 | driver Ver-2.10, PCM streams from ADX, the DSP reverb | Musashi, the SCSP, its DSP | nothing expected; check the PCM streams |

## What "a better Deep Fear on PC" means

In order of what the player notices:

1. **No slowdown, the right speed.** SGL paces the game at a frame every
   2 VBlanks, in dynamic mode (`03-executables.md`): 25 fps on a European
   Saturn, lower whenever the drawing runs over. On a PC the drawing is
   instant, so the frame never runs over; and the VBlank can run at 60 Hz
   (TVSTAT reporting NTSC while the game keeps its 256 lines), which gives
   the 30 fps the game was made for, and 6/5 the European speed if the
   logic counts VBlanks or frames. First measure: does the logic step per
   frame or by elapsed VBlanks (Virtual Hydlide's lesson: both, in
   different places)?
2. **60 fps.** If the logic steps per frame, the port keeps it at 30 and
   draws the frames between by interpolation, as Virtual Hydlide's
   `--interp` does, and here it is easier: the background is still (per
   camera), and what moves are a few characters built of SMD parts,
   which a game layer can key by model and part without guessing. If the
   logic takes elapsed time, halving the rate (1 instead of 2) may be
   enough, checked in play.
3. **Instant loading.** "Now Loading…" and the room changes wait on the
   CD; the runtime can serve sectors as fast as they are asked for, and
   more if the game is found to wait on timing.
4. **Resolution.** The characters: VDP1 on the GPU at N×, with sub-pixel
   vertices taken before SGL rounds them. The backgrounds are 336×240
   pictures: shown filtered, or replaced by upscaled versions the player
   makes from their own disc (BYOA: a tool to dump them, the runtime to
   load replacements by name). The masks must follow the pictures.
5. **The movies.** 320×176 at 15 fps, the game's own decoder: shown
   filtered, full-screen. Nothing to gain from re-decoding them.
6. **One installation for two discs.** Both images mounted, the change of
   disc answered by the runtime (or the prompt removed, once its check is
   understood).
7. Widescreen is not realistic: the backgrounds are 336 pixels wide.

## Oracle

Beetle Saturn in RetroArch (`F:\RetroArch 2`), driven by `tools/oracle.py`
(buttons over UDP 55400, SCREENSHOT/QUIT on 55355, `--record` for the
sound, `--disc 2`), no backup-RAM cartridge. Session 1: from the boot to
the first room with `--at 36:START,39:START,60:START` (the title, New
Game, skip the opening movie). The user's eyes for play. Ghidra 12.1.2
headless for an independent function list (`03-executables.md`).

## Phases

| Phase | Goal | saturnkit gains |
|---|---|---|
| 1 ✓ | feasibility, the discs, the code survey, the plan | — (used as it is) |
| 2 ✓ | **code map**: discovery on GCC and SGL code, against Ghidra (the switch form, handlers, pointer tables, strings); SGL's functions named (`tools/names-1st.tsv`); the state machine of `main`; the SCU DSP program disassembled and understood; where ADX is decoded; the change of disc | `discover` for GCC, an SCU DSP disassembler, perhaps an SGL fingerprint |
| 3 ✓ | **recompiler**: `1ST.BIN` to C++, compiling, the self-test against the interpreter (`09-recompiler.md`) | volatile pool slots written through `mova` |
| 4 | **runtime core**: the boot to the title, headless (session 2: to the title and the attract movie with sound; loading stalls, `11-runtime.md`): SGL's init and frame machine, the DMAC, indirect DMA, the slave every frame, GFS_SGL on the CD block, the DSP | the SCU DSP interpreter, SGL's VBlank order, BIOS 0x06000250/0x06000280 |
| 5 | **on screen**: logos, title, menus, the first room, a movie; against Beetle | VDP2 as the game needs it (cell backgrounds, masks, whatever else) |
| 6 | **sound**: the driver, the ADX streams, the reverb; against Beetle's recording | checks of the PCM streams |
| 7 | **the game**: play through rooms, cutscenes, saves (BUP), the change of disc | the second disc and the tray |
| 8 | **the frame rate**: 60 Hz VBlank, 30 fps held, then 60 (per-frame or elapsed-time logic decides how) | `--interp` for SGL's models |
| 9 | **PC finish**: VDP1 on the GPU at N×, background packs, window, pad mapping, configuration | VDP1 on the GPU |

## Principles kept

* BYOA: nothing from the discs in git; `iso/` and `build/` are ignored.
* Game knowledge in this repository's `tools/`; everything else in
  saturnkit, checked on every port that uses it (Virtual Hydlide too).
* Every claim checked on the disc or the running game before it goes into
  the docs; what is inferred is marked.
