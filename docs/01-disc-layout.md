# The discs

European release, two discs, each a Redump-style set: one .cue and two
.bin files (a data track and an audio track). Everything below comes from
`python -m saturnkit.disc CUE --info` and `--list`, and from comparing
the extracted trees.

## IP.BIN (system area, sectors 0–15 of track 1)

| Field | Disc 1 | Disc 2 |
|---|---|---|
| Hardware id | `SEGA SEGASATURN` | same |
| Maker | `SEGA ENTERPRISES` | same |
| Product | `MK-81804`, version `V1.001`, date `19980713` | same |
| Device | `CD-1/2` | `CD-2/2` |
| Areas | `E` (Europe), one area code block, "For EUROPE.", at 0x0E04 | same |
| Peripherals | `JE` (control pad, 3D control pad) | same |
| Title | `DEEP FEAR` | same |
| IP size | 0x1800 | same |
| Stacks | master 0, slave 0 (BIOS defaults) | same |
| 1st read | `/1ST.BIN` (360 464 bytes, LBA 89), loaded at **0x06004000**, whole file | same |

The two IP.BINs differ in three bytes, the disc number of the device
field. The 1st read address, 0x06004000, is where SGL programs load
(`03-executables.md`).

The ISO 9660 volumes are `DEEPFEAR`, system `SEGA SEGASATURN`, publisher
`SEGA ENTERPRISES`, preparer `SYSTEM SACOM`; copyright, abstract and
bibliography files `DEEP_CPY.TXT`, `DEEP_ABS.TXT`, `DEEP_BIB.TXT` (in
Shift-JIS). Created 1998-07-11 20:21:41 (disc 1) and 20:48:31 (disc 2),
two days before the IP.BIN date. The volume covers the whole disc, audio
included: 274 154 sectors on disc 1, 261 288 on disc 2.

The abstract, `DEEP_ABS.TXT`, reads 「ムービーを大量に使用したアクションアドベンチャーゲーム」:
"an action-adventure game that uses a large number of movies".

## Tracks

| Disc | Track 1 (MODE1/2352) | Track 2 (CD-DA) |
|---|---|---|
| 1 | LBA 0, 272 807 sectors (60:37) | LBA 272 957, 1 197 frames (0:15.96), pregap 150 |
| 2 | LBA 0, 259 941 sectors (57:45) | LBA 260 091, 1 197 frames (0:15.96), pregap 150 |

The one audio track is the same on both discs (the file system's
`SEGACDDA` entry points at it, byte-identical between the discs): 16
seconds of music with no voice, a jingle of the kind that goes with a
logo (heard by the user), not the usual spoken warning for CD players.
The game does not play it from the boot to the opening movie; whether it
does later is open (`05-open-questions.md`). **There is no
other CD-DA**: the music is ADX (`02-data-formats.md`).

## File tree

The trees are flat: two directories and five files at the root.

| Path | Disc 1 | Disc 2 | What |
|---|---|---|---|
| `/1ST.BIN` | 360 464 | 360 464 | the program, the only SH-2 code on either disc (`03-executables.md`) |
| `/DEEP_*.TXT` | 3 files | same | copyright, abstract, bibliography |
| `/SEGACDDA` | 2 451 456 | same | the audio track as a file |
| `/SOUND/` | 2 908 files, 193.5 MB | **byte-identical** | *all* the game's data, despite the name |
| `/MOVIE/` | 49 AVIs, 361 MB, 47:56 | 46 AVIs, 335 MB, 43:38 | full-motion video |

The two discs differ only in `MOVIE/` and in the disc number:

* **`1ST.BIN`**: 35 bytes differ. One is the disc number the program
  keeps (`mov #1,r1` / `mov #2,r1` at 0x06004378, stored at 0x0606341F);
  the others are link padding (0x06004028–0x0600403F, between crt0 and
  the first function, and 0x0605A456–0x0605A45F), leftovers with no
  meaning.
* **`MOVIE/`**: 23 AVIs are on both discs, byte-identical (the attract
  movie `MV000M00`, and 22 short ones); 26 are only on disc 1 and 23 only
  on disc 2. 72 distinct movies, 1 h 20 min in all. Disc 1's own movies
  are `MV001`–`MV084` and `MV142`, `MV143`; disc 2's are `MV090`–`MV141`:
  by all appearances the game changes disc once, part-way through the
  story (`CHG_DISC.SPR` and `WRONG.SPR`, by their names the screens that
  ask for the other disc).

### `SOUND/` by extension

| Ext | Files | Size | What (`02-data-formats.md`) |
|---|---|---|---|
| `C00`–`C09` | 788 | 75.3 MB | pre-rendered camera backgrounds, 336×240, one file per camera |
| `ADX` | 110 | 68.0 MB | CRI ADX: music, cutscene voices, effects |
| `SPR` | 816 | 24.0 MB | 2D pictures: screens, menus, item and document pictures, subtitles |
| `NMO` / `NHD` | 47 / 47 | 14.8 MB | real-time cutscenes: motion streams and their headers |
| `ARW` / `ANM` | 133 / 134 | 8.6 MB | animations and their index |
| `STX` | 134 | 4.3 MB | VDP1 textures of the models |
| `SMD` | 140 | 3.2 MB | 3D models |
| `BG0` | 22 | 1.8 MB | cutscene backgrounds (same format as `C0x`) |
| `ACX` | 39 | 1.2 MB | banks of ADX effects |
| `ATR` | 206 | 134 KB | per room: collision and zone boxes, the cameras |
| `SF` | 227 | 85 KB | per room: records of unknown meaning |
| `TBL`, `DAT`, `NUM`, `TXT` | 61 | 60 KB | tables: rooms, items, weapons, magazines, maps |
| `TSK` | 1 | 26 KB | `SDDRVS.TSK`, Sega's 68000 sound driver |
| `EXA`, `DEEP_REV.BIN` | 2 | 1.4 KB | the SCSP DSP's reverb program and its sound-RAM map |
| `SEL` | 1 | 81 KB | `TEST.SEL`, a camera background (a test picture) |

The rooms are named by area and room number, `aaRR` (`ROOM.DAT` lists
117), plus a variant and a camera: `S010201.C03` is area 01, room 02,
variant 01, camera 3; `A010201.ATR` and `M010201.SF` go with it.

## The two discs in the port

Only `MOVIE/` and one byte of code differ, so the port could run from
disc 1's data plus both `MOVIE/` directories. But the program keeps its
disc number and checks the disc it is given (open question), so the
first plan is the faithful one: the runtime mounts both images and
changes the disc when the game asks for it (`06-attack-plan.md`).
