# The program on saturnkit's Saturn

`python tools/run.py` boots disc 1 into the recompiled program on
saturnkit's runtime, headless and deterministic (virtual time, VBlanks at
60 Hz), with a pad script; `--play` opens a window instead. `-- --shot
N,...` saves pictures at those VBlanks (`build/run/shot-N.png`), `--
--dump N,...` the video memories and registers.

## Where it gets (session 3)

| VBlank | What | |
|---|---|---|
| 0 | the HLE boot loads `1ST.BIN`, the `DISC1` module takes over | |
| ~150–450 | the Duck TrueMotion and CRI ADX screens | whole (session 2: only their top) |
| ~600 | **the title**, "Press Start Button" blinking | as Beetle's |
| 1100, 1250 | START on the title; the menu's "New Game" | the text drawn (session 2: missing) |
| ~1260–1450 | "Now Loading...": the sound banks, the room tables, the first room's attributes (`A020601.ATR`), the title music `SEBGM08.ADX` streaming meanwhile | (session 2: stalled here) |
| ~1460 | **the opening movie** `MV001M01.AVI` (Sega's logo, then the story) | |
| 1700 | START skips it; the first room loads: `S020601.C03` (the background), `NM0206.SPR` (the room's name), `SEBGM04.ADX` (its music, looped by GFS from sector 25 to 66) | |
| ~1760 | **the ERS Room**, CCD-Area 2F, fading in: the background, John Mayor on the hatch with his shadow, the AIR and HP gauges, the room's name in its box for two seconds | as Beetle's (`build/oracle/newgame/t66.png`, `t70.png`) |
| 2100–2200 | UP on the pad: he walks | |

`main`'s state byte (0x06063410) is 7, the game loop. Pictures of the
whole way: `-- --shot 150,300,...`.

## What the runtime needed

Session 2:

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

Session 3, three faults of saturnkit's that only SGL and GFS_SGL met:

* **The CD block's Play** (open question 14). After New Game GFS_SGL
  streams the title music through filter 0 (FAD 0x4C45) and then wants a
  file through filter 1 (FAD 0x1117). Its stream pushes the end of its
  play on with Play commands of mode 0xFF and growing lengths (0x19,
  0x32, 0x4D sectors from 0x4C45), and issues the file's play only once
  the stream's has ended (PEND). The runtime took mode 0xFF as "repeat
  for ever" and every Play as a seek back to its start, so the stream
  never ended and the file was never read. Now, as in Mednafen's CD
  block: the repeat count changes only when the mode's bits 4–6 are
  clear (0xFF: no change); bit 7 leaves the pickup where it is, so the
  stream reads on to its new end; a position 0xFFFFFF is the last Play's;
  an end in sectors counts from the start given; the play ends when the
  position leaves the range; the status's low nibble counts the repeats
  done.
* **The division unit's shadow registers.** Nothing on VDP1 was in
  place (the player, the gauges: every vertex at 0,0). The slave builds
  the polygons from a matrix the master hands it, and that matrix was
  zero: `slLookAt` (0x0604D6xx) divides 64/32 through DVSR, DVDNTH,
  DVDNTL and reads the quotient back from **0xFFFFFF1C**, a shadow of
  DVDNTL (0x18 is DVDNTH's), which the runtime left at 0. Its rotation
  (0x0604D9A2) then zeroed the camera matrix, and every matrix after it.
  The shadows are now written by each division (Mednafen: written by a
  division or a store there, read back as they are).
* **The SH-2 DMAC's 16-byte transfers.** TCR counts longwords, four to a
  16-byte unit; the runtime moved one unit per four counts *and* skipped
  three counts each time, so a quarter of the bytes. The room's name box
  (`NM0206.SPR`, its 5 184 bytes of cells copied to VDP2 by DMAC 0) came
  out with its first 1 296 bytes and the rest left as the game had
  cleared it, light grey; and **the logo screens' and the title menu's
  missing lines were the same fault** (open question 15), not VDP2's
  rotation planes as session 2 guessed: the game never turns those on
  in all of this.

The rest was there from Virtual Hydlide: the HLE boot, SGL's VBlank
work (the SH-2's DMAC channel 1 copying the VDP2 register image, SCU DMA
levels 1 and 2 in indirect mode), the slave woken by SINIT every frame,
the CD block over the .cue/.bin, the 68000 running Sega's driver
Ver-2.10, the SCSP.

## The first room on VDP2 and VDP1

From `-- --dump 2400` (open question 4, answered):

* **The background is NBG1**: 256 colours, 1×1 cells, one-word pattern
  names with 12-bit character numbers, palette 1; its 42×30 cells of the
  336×240 picture at VRAM 0x00000 (the `C03` file as it is), the map at
  0x14000. NBG0 (priority 7) and NBG3 hold the foreground, NBG2 the
  room's name box when it shows (priority 5, its cells at 0x20000).
* **The player and the gauges are VDP1**: distorted sprites built by the
  slave from SGL's polygon buffer (0x060D47E0, 0x24 bytes a command),
  sent by SCU DMA level 1 in indirect mode (its table at 0x060C0000).
* The screen is 320×256 (PAL); **window 0** shows lines 16–239 only
  (WCTL 0x0303, W0 = 0,16–319,239). saturnkit does not do windows yet;
  those lines are black here anyway.
* Colour offset A/B are on for every layer, at zero in the room (the
  fades use them).

## Other things seen

* The runtime runs VBlanks at 60 Hz: the European game at the speed it
  was made for.
* The music of the room plays (ADX through the SCU DSP); its decode
  against ffmpeg's is still to compare (open question 3).
