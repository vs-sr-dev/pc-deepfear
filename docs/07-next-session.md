# Next session: past the loading, into the first room

Where things stand: the program is C++ and self-tested
(`09-recompiler.md`); on saturnkit's runtime it boots, shows the title and
plays the attract movie with sound (`11-runtime.md`); after New Game the
loading stalls. `python tools/recomp.py --build --test`, then
`python tools/run.py` (headless, to VBlank 3000 with the pad script that
should reach the first room), `-- --trace` for the CD block's commands,
`-- --shot N,...` for pictures.

## First: the stream and the file on one drive (open question 14)

GFS_SGL streams the title music through filter 0 / partition 0 while it
reads the game's files through filter 1 / partition 1. In the runtime the
stream's Play commands (0x10 with start 0x4C45 and growing lengths) keep
the drive on the music, partition 0 fills (200 sectors), the file's
range (FAD 0x1117) is never read, and GFS's read loop (0x06032342)
retries 20 000 times.

1. Read what GFS_SGL does between setting filter 1 and waiting (the code
   around 0x06031EAC, 0x06032114, 0x06032342): does it expect the
   stream's play to end (PEND) or the buffer-full pause, then issue its
   own play (0x10 at 0x1117 with command 0x30 to filter 1)? What status
   or HIRQ bits does it poll?
2. Check the runtime's CD block (`saturnkit/runtime/cdblock.cpp`) against
   Sega's manual for: Play (0x10) whose start is the current position or
   inside the range being read (resume, not seek back); a play's length
   ending (PEND, the drive pausing); the buffer full (the drive pausing,
   BFUL, the status); the start position 0xFFFFFF (keep).
3. Beetle as the reference if needed: the same moment there works.

## Then: on screen (phase 5)

* The logo screens draw only their first ~80 lines; the title menu's text
  is missing (open question 15, seen by the user too): the game enables
  VDP2's rotation planes (RBG0/RBG1) and windows, which saturnkit's VDP2
  does not draw yet; `--dump` at those VBlanks, then implement them.
* The first room: the background (336×240, 8 bpp cells) and its mask on
  VDP2 (open question 4), the player on VDP1; against Beetle's picture
  (`tools/oracle.py --at 36:START,39:START,60:START,66:shot`).
* Let the user play it (`python tools/run.py --play`).

## Keep in mind

* Every saturnkit change is checked on Virtual Hydlide (recompile,
  self-test 51 485 vectors, the run to the field with 1 539 frame
  changes), then its submodule moves.
* In the headless run, the title takes START from about VBlank 1000; the
  pad script is `tools/run.py`'s `ROOM_SCRIPT`.
* The ADX decode (the SCU DSP) should be compared with ffmpeg's decode
  of the same file once a stretch of music is recorded (`--wav`).
