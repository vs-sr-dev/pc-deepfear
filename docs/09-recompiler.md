# The program as C++

`python tools/recomp.py --build --test` (session 2): `1ST.BIN` of each
disc through saturnkit's recompiler, built with clang (MSYS2), checked
against saturnkit's SH-2 interpreter.

## Two modules

The two discs' programs differ in one instruction, `mov #1,r1` /
`mov #2,r1` at 0x06004378 (the disc number, `01-disc-layout.md`), so the
recompiled code differs too. Each disc's program is its own module
(`DISC1`, `DISC2`), recognised in memory by its crc32 like Virtual
Hydlide's fifteen; the runtime activates the one the BIOS loaded.

## The counts

| | DISC1 (DISC2 the same) |
|---|---|
| functions | 1 688 |
| instructions | 160 234 |
| calls by `bsr` | 242 |
| switches | 55 |
| calls and jumps through a literal | 5 459 |
| through a constant (propagated) | 740 |
| through a pointer (BIOS vectors) | 21 |
| calls dispatched at run time | 103 |
| jumps dispatched at run time | 79 (SGL's threaded code: `mov.l @r9+,r0; jmp @r0` over command lists) |
| volatile pool slots | 37 (SGL's assembly keeps variables in its literal pools) |
| static targets outside the module or not an entry | 0 |

Generation takes about 10 s, the build under a minute.

## Discovery on GCC and SGL

Session 1 found `discover` close on GCC's code (1 238 of Ghidra's 1 252
functions). Session 2 taught saturnkit what was missing, each form found
in this program and checked on Virtual Hydlide's fifteen (no function
lost there, five gained, all real):

* **GCC's switch**: `mova TABLE,r0; mov.w @(r0,rI),rI; add rI,r0; jmp
  @r0`, 16-bit offsets from the table; 8-bit ones in SGL's assembly;
  32-bit absolute entries (`mov.l @(r0,rI),rJ; jmp @rJ`); bounded by
  `cmp/hi`/`cmp/hs` against a constant or by an `and` mask, never
  running into its own targets; and the computation followed by a `bra`
  to a `jmp @r0` after a literal pool (newlib's `vfprintf`, 89 cases).
  Main's switch resolves to its 8 states.
* **Tables of records** whose first word is the target (SGL, 32 records
  of 8 bytes at 0x060561D0).
* **Computed jumps into straight code** (`mova T,r0; add rX,r0; jmp
  @r0`: an unrolled copy entered part-way, 0x06045030): the label and
  the code before it belong to the function.
* **Pointer seeds**: values the code loads as literals, `mova` addresses
  stored as pointers (the slave's entry for the BIOS vector, SGL's
  default callbacks in GBR's area), words of pointer tables; not text,
  not a pair of pointers, not a descent through pointers, and at least 8
  instructions when only a literal or a table vouches for them.
* A `mova` no longer marks its target as data: SGL takes code
  addresses with it.

The result: **1 250 of Ghidra's 1 252** functions (the other two are
shared tails, covered as code), none of the 39 strings it used to take
for code, SGL's interrupt handlers and renderer among the entries.

The emitter learned that a pool slot written through `mova` (at once or
a few instructions later, with or without a displacement) is a variable:
its loads read memory, and a call through it is dispatched at run time.
Without that the TrueMotion decoder's row functions, whose addresses it
stores in its own pool, were called at the addresses on the disc (0).

## The self-test

`build/recomp/selftest/disc1.txt`: the vectors of every function that
runs alone (on its stack, or on what its pointer arguments point at),
recorded with the interpreter, and the named helpers (`__sdivsi3`,
`__udivsi3`, `slMulFX`).

| | functions | vectors | failures |
|---|---|---|---|
| saturnkit's instruction test | 775 | 9 300 | 0 |
| DISC1 | 453 | 7 227 | 0 |
