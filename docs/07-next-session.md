# Next session: playing on, room to room

Where things stand: on saturnkit's runtime the game boots, loads, plays
its opening movie and reaches the ERS Room, every screen as Beetle's
headless, and the player walks (`11-runtime.md`).
`python tools/recomp.py --build --test`, then `python tools/run.py`
(headless, to VBlank 3000 with the pad script that reaches the room),
`-- --shot N,...` for pictures, `-- --dump N` for the video memories and
registers, `-- --trace` for the CD block's commands and the DMAs.

## The game

The user played session 3's build into the room: all of it works (the
stray pixels in the letterbox's bands, fixed and confirmed by the user). For what goes wrong next,
`python tools/run.py --play -- --record-input FILE` keeps the play, to be
given back headless (`--input @FILE`).

* ~~Out of the ERS Room~~: **the transitions between rooms work**
  (played by the user in session 3). A recorded play through several
  rooms, given back headless, would make a regression run.
* **The room's foreground** (open question 4): the player behind
  something of the room, NBG0/NBG3 at priority 7 over him; `--dump`
  there.
* The in-game menu: works (the user), the item screen and the map as
  Beetle's since the drive's timing. Still to see: FILE, OPTION, an
  examined object's text.
* **The player in front of the foreground by 2–3 pixels** (seen by the
  user at a corner and a table) before he goes correctly behind it: a
  recorded play there (`--record-input`), then `--dump` at those frames:
  the mask's layer, its scroll against the background's, the sprite's
  priority.

## Keep in mind

* Every saturnkit change is checked on Virtual Hydlide (recompile,
  self-test 51 542 vectors, the run to the field: 3 program starts,
  1 363 frame changes since the drive's real speed) and on X JAPAN
  (self-test 11 632 vectors, the run to 10 200 VBlanks: 2 506 frame
  changes), then their submodules move.
* The ADX decode (the SCU DSP) against ffmpeg's of the same file (open
  question 3): the room's `SEBGM04.ADX` with `-- --wav`.
* The frame rate (open question 1): a store watch on the player's
  position while he walks.
