# The program on saturnkit's Saturn

`python tools/run.py` boots disc 1 into the recompiled program on
saturnkit's runtime, headless and deterministic (virtual time, VBlanks at
60 Hz), with a pad script; `--play` opens a window instead.

## Where it gets (session 2)

| VBlank | What | |
|---|---|---|
| 0 | the HLE boot loads `1ST.BIN`, the `DISC1` module takes over | |
| ~200–450 | the Duck TrueMotion and CRI ADX screens | only their first lines are drawn (below) |
| ~600 | **the title**, "Press Start Button" blinking | as Beetle's |
| ~1430 | **the attract movie** `MV000M00.AVI`: TrueMotion decoded by the game's own code, drawn through VDP1 | the frames look right |
| | **sound**: the ADX music and the movie's sound, 2.6 million of 3.7 million samples not silent in 5 000 VBlanks | not listened to yet |
| 1100, 1250 | START on the title, START on New Game | the menu's text is not drawn (below) |
| ~1500 | loading the game (`load_game`, 0x060106A8): **stalls** | GFS waits for sectors that never come (below) |

The game keeps SGL's pace: **578 VDP1 frame changes in 1 200 VBlanks**
on the title, a frame every 2.07 VBlanks, 30 fps at 60 Hz. With the
drawing instant, dynamic frame never has to wait.

## What the runtime needed

* **`SYS_CHGUIPR`** (BIOS 0x06000280): `slInitSystem` hands it a table
  of 32 words, one per SCU interrupt 0x40–0x5F; by its content the SCU
  mask each handler runs under (VBlank-IN: 0xE1FB, which lets the
  HBlank and the DMA ends in). The dispatcher now adds the vector's mask
  while the handler runs: SGL's VBlank-IN handler clears SR and waits for
  the level-2 DMA-end interrupt inside it, which has to nest, while
  another VBlank must not.
* **The SCU DSP**, an interpreter (`saturnkit/runtime/scudsp.cpp`),
  running to its end when the SH-2 starts it. The program the game loads
  is **its ADX decoder** (open question 2, answered):
  `python -m saturnkit.scudsp 1ST.BIN --base 06004000 --at 0605AB94`
  shows, per channel record, a DMA of 9 longwords (an 18-byte ADX block)
  into data RAM, the 32 4-bit samples unpacked and sign-extended, scaled
  through the multiplier, and 16 longwords of 16-bit PCM written by DMA
  to sound RAM at `WA0`. So the SH-2 feeds ADX blocks, the DSP decodes
  them straight into the sound driver's PCM buffers.
* The recompiler's fixes for SGL's assembly (`09-recompiler.md`).

The rest was there from Virtual Hydlide: the HLE boot, SGL's VBlank
work (the SH-2's DMAC channel 1 copying the VDP2 register image, SCU DMA
levels 1 and 2 in indirect mode), the slave woken by SINIT every frame,
the CD block over the .cue/.bin (GFS_SGL reads the AVI and ADX files
right: the movie buffer in WRAM-L matches `MV000M00.AVI` byte for
byte), the 68000 running Sega's driver Ver-2.10, the SCSP.

## The stall: a stream and a file on one drive

After New Game, GFS reads the game's files (the models) while the title
music streams. From the CD block's trace (`--trace`):

* the music's ADX streams through filter 0 into buffer partition 0
  (range FAD 0x4C45, 368 sectors), consumed a sector at a time (command
  0x63, Get Then Delete Sector Data);
* the file to read gets filter 1, range FAD 0x1117, 15 sectors, into
  partition 1 (commands 0x40, 0x44, 0x46, 0x48), but the drive stays
  connected to filter 0 (command 0x30) and no play is issued at 0x1117;
* instead the stream re-issues Play from 0x4C45 with growing lengths
  (0x19, 0x32, 0x48 sectors), and each time the runtime seeks back to
  0x4C45; partition 0 fills to 200 sectors, partition 1 stays empty, and
  GFS's read loop (0x06032342) retries 20 000 times with a delay.

On the Saturn, GFS_SGL's stream and file reads share the drive through
its own scheduling, which must see something from the CD block that the
runtime does not give: most likely what a Play whose range is already
being read does (continue, not seek back), the drive pausing when the
buffer is full, or the end of a play's length (PEND). That is session 3's
first task (`07-next-session.md`).

## Other things seen

* The logo screens draw only their first ~80 lines, and the title menu's
  text ("New Game") is missing. **Seen by the user** in the window
  (`tools/run.py --play`, with a gamepad): the title menu otherwise right,
  the logos only a small part at the top. At the boot the runtime reports
  that the game turns on **VDP2's rotation planes (RBG0/RBG1, BGON 0x0013)
  and its windows (WCTL)**, which saturnkit does not draw yet: the likely
  cause of both, and phase 5's first VDP2 work.
* The runtime runs VBlanks at 60 Hz: the European game at the speed it
  was made for.
