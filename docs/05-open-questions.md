# Open questions

| # | Question | How to answer |
|---|---|---|
| 1 | Does the game's logic step once per frame or by elapsed VBlanks (the first question for the frame rate)? | the runtime's store watch on the player's position; read the update of `main`'s states |
| 2 | What does the SCU DSP's 256-word program (0x0605AB94) compute over its 8 records of 6 words? ADX decoding? | an SCU DSP disassembler (saturnkit); its callers' data |
| 3 | Who decodes ADX, the SH-2s or the DSP, and how does the PCM reach the driver (SGL's PCM area at 0x25A78000)? | read the ADX code (find the 0x8000 header check); the runtime |
| 4 | How is a 336×240 background shown in a 320×256 screen, and the 1 bpp mask used (a VDP2 layer? VDP1 sprites?) | the room loader (`S%02d%02d%02d.C%02d` at 0x06011EBC); the runtime's VDP2 registers |
| 5 | How does the game ask for and check the other disc (`CHG_DISC.SPR`, `WRONG.SPR`, the disc number at 0x0606341F)? | read their users; play to the change in Beetle |
| 6 | What are `main`'s 8 states (0x06063410)? | read them, the runtime |
| 7 | Does the European game show the Japanese subtitles (`MV*.SPR`)? The cutscene voices: English? | play in Beetle; listen to an `MV*N*.ADX` |
| 8 | Is 0x06000280 `SYS_CHGUIPR` (the interrupt-priority table)? What does the table at 0x0605AFDC hold? | the table's bytes against the SCU vectors |
| 9 | Does the game use the SMPC's direct ports (PDR/DDR, read at 0x0604B040/0x0604B048), and for which peripheral (the 3D pad, `JE` in IP.BIN)? | read 0x0604B2A8; the runtime |
| 10 | The SPR sizes (not in the files), `SF`, the `TBL`s, the `NHD` variants and the `NMO` tails, `MN01`'s missing `ARW` | the loaders in `1ST.BIN`, as needed |
| 11 | The audio track (16 s, both discs): the usual warning for CD players? | listen to `build/audio/disc1` |
| 12 | `PLAYALL.AVI` and `PLAYONCE.AVI` in the program's strings are not on the discs: a movie theatre mode, or leftovers? | their users in the code |
| 13 | What is in the SGL work areas at 0x060C0000–0x060FB800 (the level-1 DMA table at 0x060C0000, the level-2 at 0x060FB800)? | SGL's `workarea.c` layout against the table at 0x0605A460 |
