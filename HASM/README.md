Hasm: Hexadecimal-Assembly Language
Definition:
Hasm is a symbolic programming language that bridges raw hexadecimal representation and low-level assembly semantics. Designed for maximal control over binary structure, it allows developers to write programs where each opcode, byte alignment, and memory layout is explicitly defined in hex form—but with symbolic tags, macros, and minimal syntax sugar for legibility and structure.

Core Characteristics:
Hex-Centric Syntax: Every instruction, data block, or directive is structured around hexadecimal literals.

Assembly Semantics: Maps directly to x86_64 (or other arch-specific) assembly instructions, but abstracted into clean symbolic hex patterns.

Zero-Parser Flow: Each line is meant to be instantly translatable—1-to-1—from symbol to binary, suitable for bootloaders, exploit crafting, bare metal firmware, or ROM injection.

Direct Memory Manipulation: Exposes direct hex-level control over stack, heap, and registers.

Visual Patterning: Programmers can see opcode flows and segment transitions through color-coded or spatial hex groupings.

Applications of Hasm:
Bootloader design

Manual shellcode crafting

Reverse engineering education

Obfuscated code training

Custom OS devkits

Low-level hardware driver experiments

Features of Hasm Mode in Forester:
Hex Table Blocks: Encodes directly into machine-ready bytes.

Symbolic Labels: Auto-resolved or manually defined for address jumps.

Commented Opcodes: Documentation of byte function using semicolon (;) inline.

Integration with Forester Macros: Can invoke macros or embed raw hex as part of |...| blocks.

Compilation Flow: Hasm sections are passed as binary hex directly into the NASM output stream.

Forester Compiler Behavior:
During parsing, :hasm and :endhasm delimit regions interpreted as raw binary.

Any symbolic aliasing in Hasm blocks is expanded during Forester’s macro pass.

Byte offsets are auto-calculated unless user specifies them.

Keyboard Sequences (Gesture-Glyphs)

Special sequences trigger specific operations:

F+H → Forge Hasm

S+R → Scroll & Run

V+X+X → Void Hex Output

Live Scroll Pane

The .fstr file unrolls visually in a scroll format. You move through sections like exploring a dungeon, left to right, rune by rune.

Can include word-swapping ("inscribe"), back-burning ("undo"), and glyph-sealing ("save").

