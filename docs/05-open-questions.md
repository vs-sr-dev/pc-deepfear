# Open questions

| # | Question | How to answer |
|---|---|---|
| 1 | Does the game's logic step once per frame or by elapsed VBlanks (the first question for the frame rate)? | the runtime's store watch on the player's position, once the rooms run |
| 2 | ~~What does the SCU DSP's program compute?~~ **ADX decoding** (session 2): per channel record, an 18-byte block in by DMA, 32 samples unpacked and scaled, PCM out by DMA to sound RAM (`11-runtime.md`) | — |
| 3 | ~~Who decodes ADX?~~ **The SCU DSP** (session 2). Still open: the ADX filter (the DSP program shows the scaling; where the prediction from the previous samples happens), to check against ffmpeg's decode of the same file | the runtime's PCM against `ffmpeg -i M_07.ADX` |
| 4 | How is a 336×240 background shown in a 320×256 screen, and the 1 bpp mask used (a VDP2 layer? VDP1 sprites?) | the room loader (`S%02d%02d%02d.C%02d` at 0x06011EBC); the runtime's VDP2 registers once a room runs |
| 5 | How does the game ask for and check the other disc (`CHG_DISC.SPR`, `WRONG.SPR`, the disc number at 0x0606341F)? | read `wrong_disc` (0x06025A24) and its callers; play to the change in Beetle |
| 6 | ~~What are `main`'s 8 states?~~ **Named** (session 2, `03-executables.md`): boot and title, title menu, wrong disc, save, load game, save screen, game loop. Still open: the order the game goes through them | the runtime, state by state |
| 7 | ~~Does the European game show the Japanese subtitles?~~ **No** (session 1, played; session 2, code): no subtitles at all, voices in English, text only when examining; no option; and the cutscene loader never builds a `MV….SPR` name, so the Japanese pictures are never loaded | — |
| 8 | ~~Is 0x06000280 `SYS_CHGUIPR`?~~ **Yes, by its table** (session 2): 32 words, one per SCU interrupt, the SCU mask each handler runs under. Inferred: that the BIOS adds it to the current mask (the runtime does) rather than replacing it | a game that masks a source the table unmasks |
| 9 | Does the game use the SMPC's direct ports (PDR/DDR, read at 0x0604B040/0x0604B048), and for which peripheral (the 3D pad)? | read 0x0604B2A8; the runtime |
| 10 | The SPR sizes (not in the files), `SF`, the `TBL`s, the `NHD` variants and the `NMO` tails, `MN01`'s missing `ARW` | the loaders in `1ST.BIN`, as needed |
| 11 | The audio track (16 s, both discs): **a wordless jingle** (heard by the user), not the spoken CD-player warning; not played from the boot to the opening movie. Does the game ever play it? | the CD block's play commands in the runtime; Beetle |
| 12 | `PLAYALL.AVI` and `PLAYONCE.AVI` in the program's strings are not on the discs: a movie theatre mode, or leftovers? | their users in the code |
| 13 | What is in the SGL work areas at 0x060C0000–0x060FB800? | SGL's `workarea.c` layout against the table at 0x0605A460 |
| 14 | **The stall after New Game** (session 2): how do GFS_SGL's stream (the music, filter 0) and a file read (filter 1) share the drive? What does the CD block do on a Play over a range already being read, on a full buffer, at the end of a play's length, that the runtime does not? | the trace of commands 0x10/0x30/0x40–0x48 and the status/HIRQ the game polls; GFS_SGL's code (0x06031xxx–0x06036xxx); Sega's CD block manual |
| 15 | The logo screens draw only their first ~80 lines, and the title menu's text is missing | the VDP2 and VDP1 state at those screens (`--dump`) |
