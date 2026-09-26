# Curiosities

Things found on the way that the port does not need.

1. **The directory called `SOUND`** holds the whole game: backgrounds,
   models, textures, animations, tables, pictures, and the sound. Only the
   movies have a directory of their own.

2. **Japanese subtitles on the European disc.** The real-time cutscenes'
   subtitle pictures (`MV*.SPR`) are in Japanese: `MV002N01.SPR` is 26
   lines of the ERS crew's banter ("Chief!" "Hey, what's going on?" "It's
   April Fool's! Did you forget?" … "The base has felt gloomy lately…").
   The European release kept the Japanese files.

3. **"A game that uses a large number of movies."** The disc's abstract
   file, `DEEP_ABS.TXT`, in Japanese on the European disc too, describes
   the game as an action-adventure "that uses a large number of movies":
   1 h 20 min of them over the two discs.

4. **The disc number, and some junk.** The two discs' programs differ in
   35 bytes: one is the disc number (`mov #1` / `mov #2`), 34 are padding
   the linker left between sections with whatever was in memory; on disc
   1 the padding after crt0 is a scrap of code, on disc 2 a scrap of data.

5. **Boot credits.** Before the title the game shows, besides SEGA's
   licence, a screen for Duck's TrueMotion ("a registered trademark of The
   Duck Corporation") and one for CRI's ADX ("Copyright © 1996, 1997 CRI"),
   its two middleware licences. The title credits the music: "MUSIC ©
   1998 by KENJI KAWAI".

6. **A test picture.** `TEST.SEL` is a camera background (a corridor) in
   the room format, under a name no room uses.
