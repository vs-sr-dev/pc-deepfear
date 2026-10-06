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
stray pixels in the letterbox's bands, fixed). For what goes wrong next,
`python tools/run.py --play -- --record-input FILE` keeps the play, to be
given back headless (`--input @FILE`).

* **Out of the ERS Room**: the next room through a door (the loading
  between rooms, its camera cut), with a pad script or the user's
  recorded play; Beetle at the same place with `tools/oracle.py`.
* **The room's foreground** (open question 4): the player behind
  something of the room, NBG0/NBG3 at priority 7 over him; `--dump`
  there.
* **The in-game menu** (Beetle's `t82`: ITEM, WEAPON, MAP, FILE, OPTION)
  and an examined object's text.

## Keep in mind

* Every saturnkit change is checked on Virtual Hydlide (recompile,
  self-test 51 542 vectors, the run to the field: 3 program starts,
  1 539 frame changes) and on X JAPAN (self-test 11 632 vectors, the run
  to 10 200 VBlanks: 2 529 frame changes), then their submodules move.
* The ADX decode (the SCU DSP) against ffmpeg's of the same file (open
  question 3): the room's `SEBGM04.ADX` with `-- --wav`.
* The frame rate (open question 1): a store watch on the player's
  position while he walks.
