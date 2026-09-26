# The data formats, a first look

Everything is in `SOUND/` (`01-disc-layout.md`), big-endian, and **none
of it is compressed**. Fixed-point values are SGL's: `FIXED` is signed
16.16, `ANGLE` a u16 with 0x10000 = 360°. Colours are the Saturn's 15-bit
RGB (`r = v & 31`, `g = (v >> 5) & 31`, `b = (v >> 10) & 31`, bit 15 the
MSB flag).

**[V]** verified: decoded into something that looks right, or a size
formula that holds for every file. **[I]** inferred. Session 1 read the
bytes only; which code loads each format, and how, is phase 2's.

| Ext | What | |
|---|---|---|
| `C00`–`C09`, `BG0`, `TEST.SEL` | pre-rendered backgrounds, 336×240, 8 bpp cells, optional 1 bpp foreground mask | V |
| `SPR` | 2D pictures: palette + 8×8 cells, 8 or 4 bpp; no size in the file | V pixels, I sizes |
| `SMD` | 3D models: SGL-style parts, points, polygons, attributes, normals | V |
| `STX` | the models' VDP1 textures: 16 colour tables, 4 bpp texels, a size table | V |
| `ANM` + `ARW` | animations: an index and the frames | V layout, I meaning |
| `NHD` + `NMO` | real-time cutscenes: header, and motion for several actors | I, partly V |
| `ATR` | per room: boxes (walls, floor zones, triggers) and cameras | V layout, I meaning |
| `SF` | per room: records of 56 or 52 bytes | V layout |
| `ADX`, `ACX` | CRI ADX sound; ACX a bank of ADX | V |
| `SDDRVS.TSK` | Sega's 68000 sound driver, Ver-2.10 | V |
| `EREV2.EXA`, `DEEP_REV.BIN` | SCSP DSP reverb program; its sound-RAM map | V / I |
| `MOVIE/*.AVI` | Duck TrueMotion 1 video, IMA DK4 ADPCM sound | V |

## Backgrounds: `S%02d%02d%02d.C%02d`, `*.BG0`, `TEST.SEL` [V]

Deep Fear draws its rooms the Resident Evil way: a still picture per
camera, the characters in 3D over it.

* 81 152 bytes (453 files): a 256-colour palette (512 bytes), then 1 260
  cells of 8×8 pixels at 8 bpp (64 bytes each), **42 × 30 cells in screen
  order, row by row: 336×240 pixels**. No name table: the cells are the
  picture.
* 91 232 bytes (335 files): the same, then at 0x13D00 a **1 bpp mask of
  336×240** (42 bytes a line, the leftmost pixel in the top bit): the
  parts of the picture that stand in front of the characters (the
  railing of `S010201.C03`).
* The room files pair up one to one: `S…` (the pictures of a room
  variant, one per camera), `A…ATR`, `M…SF` (206 sets for the 117 rooms of
  `ROOM.DAT`).

Decoded in session 1 from this description, `S0102xx.C0x` are the
hangar's cameras, pictures as the game shows them. 336 is wider than
the 320-pixel screen: how the game places it (a scroll, a 352-wide mode
for these screens, a crop) is to read in the code.

## `SPR`: 2D pictures [V pixels, I sizes]

A palette, then 8×8 cells in screen order, row by row; cell 0 usually
blank. Two kinds:

* 256 colours: a 512-byte palette, 8 bpp cells. Full screens are 72 256
  bytes = 512 + (1 + 40 × 28) × 64: 320×224 (`TITLE`, `SEGALOGO`,
  `TMLOGO2`, `ADX1`, `CHG_DISC`, `WRONG`, `NOSAVE`, `MAP_IMG`).
* 16 colours: a 32-byte palette, 4 bpp cells. `FI*.SPR` (the documents
  found in the game, 240 wide), `MV*.SPR` (cutscene subtitles, 272 wide,
  `32 + n × 1088` bytes).

The width and height are not in the file: they are in the program. The
widths used here were found by fitting and checked by eye: item boxes
(`GI`, 304×112), item pictures (`ITEM_nnn`), room name plates (`NM`,
128×40), text strips (`TP`, `WC`, 272×32), and others still unnamed
(`TT`, `UI`, `SP`).

**The subtitles are Japanese** on this European disc: `MV002N01.SPR`
renders 26 lines of Japanese dialogue (session 1). Whether the European
game shows them is open.

## `SMD`: models [V]

```
0x00  u16 nParts, nVerts, nPolys, nNormals (= nVerts or 0), nTex (= the STX's count), 0
0x0C  nParts × 44 bytes: u16 nV, vStart, nP, pStart, nN, nStart, parent (0xFFFF: root);
                          FIXED pos[3]; ANGLE rot[3]; FIXED scale[3] (= 1.0)
      nVerts × FIXED[3]                                   points (indices per part)
      nPolys × { FIXED normal[3]; u16 v[4] }              SGL's POLYGON
      nPolys × { u8 flag, sort; u16 texno, atrb, colno, gstb, dir }   SGL's ATTR
      nNormals × FIXED[3]                                 vertex normals
```

The formula holds for all 140 files. Each part placed by its parent ×
translate(pos) × Rx·Ry·Rz gives a standing man for `MN01` (21 parts), a
tentacled creature for `CN01`, a flat floor for `ON01`. The textured
polygons use `atrb` 0xCC (16-colour lookup table, Gouraud), `colno` the
colour table in the STX. Families: `CNnn` creatures (each with a
296-byte `.DAT` of parameters and a `CNnnS.ACX` of sounds), `MNnn`
humans, `PNnn`, `EF01`, `WN01`, `XN01`, `ZN01`, `ON01`/`ON02`.

## `STX`: textures [V]

```
u32 nTex, u32 dataSize; 16 colour tables × 16 colours (0x200 bytes); the 4 bpp texels;
then nTex × { u16 w, u16 h, u16 0, u16 VDP1 CMDSIZE = ((w / 8) << 8) | h }
```

The texel sizes add up to `dataSize` in 132 of 134 files (`ON02`, `ZN01`
differ); the textures render as coherent pictures.

## `ANM` + `ARW`: animations [V layout, I meaning]

* `ANM`: `u32 arwSize, u16 n`, n names of 4 bytes (`a01`…), n frame
  counts (u8), n offsets (u32) into the ARW. No padding.
* `ARW`: frames of **12 + 6 × nParts bytes**: the root's position
  (FIXED[3]), then an ANGLE[3] per part. All 132 pairs match on sizes
  and offsets; frame 40 of `PN01.ARW` on `PN01.SMD` is a coherent pose.
* `MN01.ANM` lists 83 animations but there is no `MN01.ARW`; `MN77.ANM`
  is empty.

## `NHD` + `NMO`: real-time cutscenes [I, partly V]

The cutscenes that are not movies play in the engine: `MVnnnNmm` sets of
an ADX (the voices), an NHD, an NMO, an SPR (the subtitles) and
sometimes a BG0.

* `NHD`: the number of actors and their kinds (`M` a 21-part human, `C` a
  creature), parts per actor, a frame count, camera data.
* `NMO`: per frame, each actor's ARW record in turn: frames × Σ(12 + 6 ×
  parts). Exact for 9 sets (`MV157N01`: 195 × (138 + 210) = 67 860);
  many two-actor sets have a tail of k × 152 bytes, and the one- and
  three-actor headers are not parsed yet.

## `ATR`: room boxes and cameras [V layout, I meaning]

`u16 c0…c4`, then c0 + c1 + c2 + c3 boxes of 24 bytes (FIXED min[3],
max[3]), then c4 cameras of 28 bytes (FIXED eye[3], target[3], u32
0x2AAA: 60°, the field of view). The formula holds for all 206. c4 is
the number of pictures of the room in 195 of 206; c1 = c3 in 205. In
`A010201`, the c0 boxes are full-height (walls), the c1 boxes tile the
floor one per camera (the zones that choose the camera, by all
appearances), the c2 boxes are 100 units high (triggers), the c3 boxes
small cubes. Y is negative upward, the floor at 0.

## `SF` [V layout]

`u8 n`, then n records of 56 bytes (203 files) or 52 (24). Per room
variant; meaning unknown (events? doors?).

## Sound [V]

* **ADX**: all 110 are CRI ADX (magic 0x8000, type 3, 18-byte blocks, 4
  bits a sample, header version 3); ffmpeg decodes them all. 43 are
  22 050 Hz mono, 65 22 050 Hz stereo, 2 44 100 Hz stereo (`M_5`,
  `MV117N01`). `SEBGM01`–`14`: the background music, stereo, 398 s;
  `M_*`: 7 more music pieces; `MV*`: 47 cutscene tracks, about 26
  minutes; `EV`, `SY`, `DO`, `WP`: short mono clips. 21 loop (all
  `SEBGM`, all `M_`, `SY09`).
* **ACX**: `u32 0, u32 n`, then n × {u32 offset, u32 size} of whole ADX
  files. 39 banks, 237 clips (218 at 11 025 Hz mono): the enemies'
  sounds (`CNnnS`), the weapons' (`WPnn`), the player's (`MYSE`).
* **`SDDRVS.TSK`**: a 68000 program (vectors: stack 0xA000, start
  0x1000), `Ver-2.10 -L << SEGASATURN >> Thu Apr 17 1997`: Sega's sound
  driver, a later version than Virtual Hydlide's.
* **No tone banks, no sequences, no CD-DA music**: every sound the game
  makes comes from ADX. ADX is decoded by software; whether the SH-2s or
  the SCU DSP decode it is open (`03-executables.md`).
* **`EREV2.EXA`** (internal name `Erev2.EXB`): an SCSP DSP effect
  program, a reverb. **`DEEP_REV.BIN`** (18 bytes), a sound-area map by
  all appearances: `20 00B000 00000540` (the DSP program at 0xB000, the
  EXA's size), `30 00C000 00012000` (the DSP's work RAM), then 0xFFFF.

## Tables [partly V]

`ROOM.DAT`: 117 × (area, room) [V]. `ITEM.TXT`: 40 item names of 32
bytes ("Lv.1 Navy Key"…), matching `ITEM_001`–`040.SPR` [V]. The rest
are small byte tables whose meaning is inferred from their names:
`ITEM_DAT`, `MAGAZINE` (10-byte records), `GUN_NM1`/`2`, `FILE_NM`,
`MVTYPE`, `ASIOTO.DAT` (the size of `ROOM.DAT`; *ashioto*, footsteps: a
footstep sound per room?), `ARnn.TBL` (the maps?), `F_POWER.NUM` (weapon
power), `TEXTSEL.NUM`; `AT`/`CS`/`ES`/`FS.TBL` unknown.

## Movies: `MOVIE/*.AVI` [V]

RIFF AVI with a video stream `DUCK` (Duck TrueMotion 1, RGB555,
**320×176, 15 fps**) and a sound stream of IMA DK4 ADPCM (22 050 Hz,
stereo). ffmpeg decodes both. The boot screens credit it: "TrueMotion® is
a registered trademark of The Duck Corporation". The program carries its
own player (an AVI parser whose chunk names, `hdrl`, `strl`, `movi`,
`idx1`, `DUCK`, are stored as 32-bit constants; `03-executables.md`).
