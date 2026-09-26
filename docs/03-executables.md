# The program

Deep Fear is **one program**: `1ST.BIN`, 360 464 bytes, loaded by the
BIOS at 0x06004000 and never replaced. No other file on either disc holds
SH-2 code (session 1 counted prologues and `rts`/`nop` densities in every
file; `SDDRVS.TSK` is the 68000's). Nothing is swapped at one address,
and there is no resident system program: the opposite of Virtual
Hydlide's fifteen.

Addresses are disc 1's; disc 2's program is the same except for the disc
number (`01-disc-layout.md`). Function names taken from SGL are given
where the code does what SGL's documented function does; they are
**inferred from behaviour**, not from symbols (there are none).

## Toolchain and libraries

* **Compiler: GCC** (Cygnus's SH port, as SGL's kit shipped), not
  Hitachi's SHC. The evidence: newlib in the program (`bug in vfprintf:
  bad base`, `Heap and stack collision`, `0123456789abcdef`); GCC's
  prologue (`mov.l r8…r14,@-r15; sts.l pr,@-r15`, and `mov r15,r14` often
  in the delay slot of the first `jsr`); GCC's switch, which saturnkit
  had not met (below). Some library code is compiled without optimisation
  (every local through the stack frame: the SCU DSP routines).
* **SGL**, Sega's graphics library, by its code: hand-written assembly
  working in a system area at **0x060FFC00 through GBR** (`mov.b
  @(176,gbr),r0`…), the frame and interrupt machinery below, the slave
  started through 0x06000250. Its file system and backup libraries carry
  their versions: **`GFS_SGL Version 2.14 1997-04-11`**, **`BUP Version
  1.25 1997-06-20`**.
* **The SCU DSP** is used (below): Sega's DSP routines load a program
  and data into it.
* **A movie player** for AVI with Duck TrueMotion 1 video (`DUCK`) and
  ADPCM sound: its AVI chunk names are 32-bit constants in the code
  (`LIST`, `hdrl`, `strl`, `strh`, `strf`, `movi`, `idx1`).
* **CRI ADX**: the boot shows CRI's ADX logo ("Copyright © 1996, 1997
  CRI", `ADX1.SPR`); the program has no library version string for it.

## crt0 and the memory map

`0x06004000`: SR = 0xF0, r15 = `*0x0605A460` = 0x060FFC00, CCR
(0xFFFFFE92) = 0x11 (cache on, purged), GBR = 0x060FFC00, jump to
`0x06004040`: static constructors once (`0x06043364`), BSS cleared
(0x0605C010–0x060BFF38), SGL's system area cleared (0x060FFC00–0x060FFFFF),
then `main` at **0x060040C4**. The BSS starts exactly where the file ends
(0x06004000 + 360 464 = 0x0605C010), which confirms the load address
`saturnkit.sh2 --find-base` ranks first (1 748 prologue hits; the next,
279).

| Range | What |
|---|---|
| 0x06000000–0x06001000 | BIOS work area and service pointers |
| 0x06001E00 (down) | the slave's stack (`*0x0605A464`) |
| **0x06004000–0x0605C010** | **the program**: text, then data from about 0x0605A000 |
| 0x0605C010–0x060BFF38 | BSS |
| 0x060C0000–0x060FB800… | SGL's work areas, from the pointer table at 0x0605A460: 0x060C0000 (the table of the level-1 DMA at VBlank-OUT), 0x060C4FF8, 0x060C57F8, 0x060E37C8, 0x060ED408, 0x060EE008, 0x060FB800 (the table of the level-2 DMA at VBlank-IN) |
| below 0x060FFC00 | the master's stack |
| 0x060FFC00–0x06100000 | SGL's system area (GBR) |
| 0x00200000–0x002FFFFF | WRAM-L: buffers (0x00200000, 0x00258DE0, 0x00280000, 0x002A48D0, 0x002C0000, 0x002D0000 are loaded by the code) |
| 0x25A78000 | sound RAM: in SGL's table, by all appearances SGL's PCM work area (`PCM_Work`) |

## The main loop

`main` (0x060040C4) runs the game's initialisation (`0x06004314`, below)
and `0x0600C5A4`, then loops over **a state machine**: the byte at
0x06063410 (1–8, set to 8 at the start) chooses the state through a GCC
switch at 0x06004110. The states call the game's top-level functions,
named in session 2 by the files their call trees use
(`tools/names-1st.tsv`):

| Function | What |
|---|---|
| `0x060044A4` boot_and_title | state 1: the logos (`SEGALOGO`, `TMLOGO2`, `ADX1`), the attract movie `MV000M00`, the title |
| `0x06004B24` title_menu | state 3: New Game, Option |
| `0x06025A24` wrong_disc | `WRONG.SPR` |
| `0x060260FC`, `0x06023AEC` | the save on the backup memory (`DEEPFEAR_01`) |
| `0x060106A8` load_game | the tables, the models, the weapons' sounds, the room's `ATR` and `SF` ("Now Loading") |
| `0x06023BF8` save_screen | `SAV_BG`, `DIALOG`, `SAVE` |
| `0x06010D40` game_loop | the rooms: room names, the player, events, cutscenes |

Below them: `0x06004404` next_frame (the pad, the reset combination,
`slSynch`: called once per frame by every loop), `0x0602C488` the AVI
player, `0x06026C14` the event player, `0x0602A5E8` the in-engine
cutscene loader. That loader builds `%s.NHD`, `%s.BG0`, `%s.NMO` and
`%s.ADX` from `MVnnnNmm`, and no format string anywhere builds a
`MV….SPR`: **the European program never loads the Japanese subtitles**
(open question 7).

The initialisation, `0x06004314`:

1. **`slInitSystem(2, *0x0605A500, 2)`** (0x0603B784): TV mode 2 and a
   frame rate of 2. SGL's mode table (0x06054530: half-widths and
   half-heights) makes mode 2 **320×256**, a PAL mode, and the argument
   is a constant (`mov #2,r4`): this European program only ever sets up
   256 lines. The function does what SGL's does: the system clock by the
   mode (`SYS_GETSYSCK`/`SYS_CHGSYSCK`), the VDP and interrupt setup, a
   SINIT to the slave, `SYS_CHGSCUIM`.
2. **`slDynamicFrame(ON)`** (0x0604AF60 with 1): bit 7 of the system
   byte at GBR+176. With it, SGL changes frames when VDP1 has finished
   drawing, not on a fixed count (below).
3. `0x0604BF7C(0, 16, 319, 239)`: by its arguments a window of 320×224
   inside the 256 lines (to read).
4. `0x060452F8(0x25C45000, 0, 0x25000)` (by its arguments a fill of VDP1
   VRAM), the game's own initialisations, the disc number (0x0606341F).

## The frame: SGL's

`slInitSystem` hands the frame rate to `0x06055560`, which installs SGL's
interrupt handlers and stores the rate as `(rate << 8) | (rate − 1)` in
the halfword at GBR+18 (a negative rate sets the dynamic bit; the rate is
capped at 120).

| Vector | Source | Handler |
|---|---|---|
| 0x40 | VBlank-IN | 0x060552A6 |
| 0x41 | VBlank-OUT | 0x060553FE |
| 0x4B / 0x4A / 0x49 | SCU DMA end, levels 0 / 1 / 2 | 0x06055270 / 0x06055282 / 0x06055294 |
| 0x47 | SMPC | 0x0605A360 |

`slInitSystem` then calls `SYS_CHGSCUIM(0xFFFFF17C, 0)`, which unmasks
those six sources.

* **VBlank-IN** (0x060552A6) latches the FRT count, and when the frame's
  countdown (GBR+19) has run out: copies SGL's VDP2 register image
  (0x060FFCC0, 0x90 bytes) to VDP2 (0x25F80000) with **the SH-2's own
  DMA controller** (channel 1, CHCR 0x5601, DMAOR 9); starts an **SCU
  level-2 DMA in indirect mode** from the table at `*0x0605A484` (VDP2
  transfers, by all appearances); calls the user's VBlank function
  (GBR+20), `0x0604B2A8` (the pads: it reads the SMPC's ports), and
  `0x06055628` (by its accesses, the sound driver's command queue at
  0x25A007A0 in sound RAM); then more work bounded by the FRT.
* **VBlank-OUT** (0x060553FE) counts the frame down (GBR+19), writes
  VDP1's FBCR and starts an **SCU level-1 DMA in indirect mode** from
  `*0x0605A468` (the VDP1 commands, by all appearances), along paths
  chosen by SGL's mode bits (dynamic frame, interlace from TVSTAT's ODD
  bit).
* **`slSynch`** (0x0604BFBE, called from 12 places, and entered at
  0x0604BFA4 once by the initialisation): hands the slave its command
  lists (GBR+72, a SINIT, twice per frame), then loops calling the idle
  function (GBR+972) until the countdown GBR+19 goes negative.

**So the pace is SGL's: a frame every 2 VBlanks at best, 30 fps at 60 Hz
and 25 fps on this European Saturn, in dynamic mode**: when a frame's
drawing runs over, the frame changes when VDP1 is done, not a fixed
number of VBlanks later. Nothing else sets the rate. Whether the game's
logic steps per frame or by elapsed time is the first thing to measure
once it runs (`06-attack-plan.md`).

## The slave SH-2: SGL's

`0x0605425C` writes the slave's entry, **0x0605427C**, to 0x06000250 (the
BIOS's slave boot vector) and turns the slave on. The slave: SR = 0xF0,
IPRA and IPRB 0, TIER = 1 (no FRT interrupt), its stack from
`*0x0605A464` (0x06001E00); then it loops **polling FTCSR's
input-capture flag** (0xFFFFFE11, bit 7), clears it, and calls the
function at **0x060542C4** (read cache-through), clearing it first. The
master pulses SINIT (0x21000000) to wake it: once in `slInitSystem`,
twice in every `slSynch`. This is the same handshake as Virtual Hydlide's
SPR (a pointer and the FRT input), so saturnkit's slave coroutine, woken
at SINIT, should hold; the difference is that SGL gives the slave work
**every frame** (its share of the polygon work), not opportunistically.

## The SCU DSP

Sega's DSP routines, compiled without optimisation: `0x06032574` (stop the
DSP, write a program through PPAF/PPD), `0x06032610` (write data RAM
through PDA/PDD), `0x0603270C`, `0x06032740`, `0x06032758` (control and
status). The game's use:

* `0x060302C0`: loads **a 256-word program** from 0x0605AB94 at PC 0,
  clears two buffers (0x060BAF90, 0xC0 bytes; 0x060BAF70), writes 48
  words from 0x060BAF90 into data RAM 2 (PDA 0x80), and sets 0x0605AF94.
* `0x060304E0`: for **8 records of 24 bytes** at 0x060BAF90, writes each
  one that is set into data RAM 2 (6 words each, at 0x80 + 6·i), starts
  the DSP if any was written.
* `0x06030588`: whether the DSP has finished.

**The program is the ADX decoder** (session 2, with saturnkit's new
`scudsp` disassembler; `11-runtime.md`): for each of the 8 channel
records it DMAs an 18-byte ADX block into data RAM, unpacks and
sign-extends its 32 4-bit samples, scales them through the multiplier,
and DMAs 32 16-bit samples to sound RAM. The runtime now has an SCU DSP
interpreter, and with it the game's music plays.

## Interrupts, BIOS services, and the reset

Besides SGL's handlers: `SYS_SETUINT`, `SYS_SETSCUIM`, `SYS_CHGSCUIM`,
`SYS_GETSCUIM` (the SCU mask), `SYS_CHGSYSCK`, `SYS_GETSYSCK`, the BUP
pointers (0x06000354, 0x06000358: saves, the name `DEEPFEAR_01`), the
slave vector 0x06000250, **0x06000280**, called once by `slInitSystem`
with the pointer 0x0605AFDC (`SYS_CHGUIPR`: the table holds 32 words,
one per SCU interrupt 0x40–0x5F, the SCU mask its handler runs under;
session 2), and **0x0600026C**, loaded
at 14 sites: at 0x06004404 it is called when the pad reads A+B+C+START,
so it is the reset to the system, as in Virtual Hydlide.

## Hardware touched

`python -m saturnkit.sh2 1ST.BIN --base 06004000 --refs …` (literal
loads; about 30 hits in unclassified data are not addresses and are left
out):

| Block | Registers / areas |
|---|---|
| VDP1 | TVMR, FBCR, EDSR (by offset from TVMR); VRAM (24 sites) |
| VDP2 | TVMD, TVSTAT, HCNT, VCNT, RAMCTL; VRAM (73 sites), CRAM (9); the register image copied every VBlank |
| SCU | DMA levels 0, 1, 2 (D0R, D1R, D2R, DSTA), IMS, **the DSP** (PPAF, PPD, PDA, PDD) |
| SMPC | COMREG, SR, SF, IREG0, OREG0, and **the direct ports**: PDR1, PDR2, DDR1, DDR2, IOSEL, EXLE (read by 0x0604B040/0x0604B048) |
| CD block | HIRQ, HIRQMASK, CR1–CR4, the data port (GFS_SGL) |
| SCSP | sound RAM (61 sites: the driver, its command area at 0x25A00700, a flag at 0x25A004E0, the queue at 0x25A007A0, buffers at 0x25A54000–0x25A7B000), the common registers at 0x25B00400, 0x25B00BD0–0x25B00BE3 |
| Slave | SINIT (10 sites) |
| SH-2 on-chip | CCR, BCR1, DVSR (division unit), FTCSR, IPRA, IPRB, SMR, VCRWDT, TIER, **the DMAC** (channel 1, DRCR1, DMAOR) |

## Sound

The program names `SDDRVS.TSK` (Ver-2.10), its map `DEEP_REV.BIN` and
the reverb `EREV2.EXA` together at 0x060198F0, with the player's sound
bank `MYSE.ACX` (the code before them writes to sound RAM at
0x25A62000…: loading them, by all appearances), and talks to the
driver through its command area (0x25A00700) and SGL's queue (0x25A007A0,
flushed at every VBlank-IN). There are no sequences on the disc: the
music and voices are ADX files decoded in software into PCM buffers in
sound RAM, which the driver plays (0x25A78000, SGL's PCM area): the
SH-2 writes the channel records into the SCU DSP, which fetches the
blocks by DMA, decodes them and writes the PCM out (above).

## Function discovery

`python -m saturnkit.recomp.discover 1ST.BIN --base 06004000 --report`,
the discovery written for SHC's code, on GCC's:

| | |
|---|---|
| functions | 1 610 |
| code / data / unclassified bytes | 240 448 / 36 408 / 83 608 |
| switch tables | **0** |
| unresolved indirect jumps | 153 |
| entries inside other functions | 204 |
| functions with problems | 1 (0x06053D48 runs into data at 0x0605857C) |

**Against Ghidra** (12.1.2, headless, the SH-2 language, entry seeded at
0x06004000; saturnkit's `ghidra/ExportFuncs.java`): Ghidra finds 1 252
functions, **1 238 of them found by discover too (98.9 %)**. The
differences:

* **GCC's switch** (`mov rX,r1; add r1,r1; mova TABLE,r0; mov.w
  @(r0,r1),r1; add r1,r0; jmp @r0`, halfword offsets from the table, the
  bound a `cmp/hi` before it): 44 of the 153 unresolved jumps; Ghidra
  resolves them, and its bodies are larger in 33 functions (main's 256
  bytes against 86).
* **SGL's hand-written handlers** (the interrupt handlers above, which
  start by saving r0–r7, not with GCC's prologue) and code reached only
  through pointer tables: 14 functions only Ghidra has, and 56 blocks
  Ghidra disassembles that discover leaves unclassified (about 30
  renderer routines at 0x0603D61C–0x0603FB18 among them).
* **Strings taken for code**: 39 of discover's extra entries are strings
  passed as arguments ("SOUND", "MOVIE", "%4d", "S%02d%02d%02d.C%02d",
  "f01"…), 3 more are data words.
* The other extra entries are real: 186 functions nothing references
  (dead code linked in), about 100 reached by pointer that Ghidra
  disassembles but does not make functions of, 26 labels inside large
  GCC functions.

discover is close on GCC's code, and what it misses is known: GCC's switch
form, SGL's handlers and pointer tables, and a stricter test for text.
**Session 2 taught it all three**: 1 688 functions, 1 250 of Ghidra's
1 252, 45 switch tables, no function with problems (`09-recompiler.md`).
