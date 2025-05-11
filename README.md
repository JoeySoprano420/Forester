# Forester



===========================================
         🌲 Forester SDK v1.0 🌲
   High-Performance Symbolic Language Compiler
===========================================

CONTENTS:
---------
This SDK includes all necessary tools and examples to write, compile, and run Forester programs using NASM x64 on Windows.

📁 /ForesterSDK/
├── forester_compiler_v2.py        → Python-based compiler frontend (macro + logic support)
├── example.fstr                   → Forester source code sample
├── build_forester.bat             → Build script: .fstr → .asm → .exe
├── forester.tmLanguage.json       → VSCode syntax highlighting definition
├── nasm.exe (optional)            → Portable NASM binary (if bundled)
└── README.txt                     → This file

REQUIREMENTS:
-------------
1. Python 3.8+
2. NASM x64 Assembler: https://www.nasm.us/pub/nasm/
3. Microsoft Visual Studio (with C++ tools and linker)
4. VSCode (optional for highlighting `.fstr` files)

USAGE:
------
➤ 1. Write your code:
    Edit `example.fstr` using your favorite editor or VSCode.

➤ 2. Compile to Assembly:
    Run the provided Python compiler:
        python forester_compiler_v2.py example.fstr output.asm

➤ 3. Assemble to Object:
    Using NASM:
        nasm -f win64 output.asm -o output.obj

➤ 4. Link to Executable:
    Using MSVC linker:
        link output.obj /subsystem:console /defaultlib:msvcrt.lib /out:forester.exe

➤ OR run the entire flow with:
        build_forester.bat

➤ 5. Run your program:
        forester.exe

SYNTAX HIGHLIGHTING:
---------------------
1. Copy `forester.tmLanguage.json` into a VSCode extension folder.
2. Or use the TextMate grammar to load via VSCode extensions like "Textmate Grammars".

SUPPORTED FEATURES:
--------------------
✔ Symbolic instruction macros
✔ Arithmetic & flow control
✔ Macro expansion
✔ Conditional branching
✔ NASM x64 binary generation
✔ Modular design for future expansion

TROUBLESHOOTING:
----------------
• If NASM is not recognized, add it to your PATH or use the bundled binary.
• Ensure `link.exe` is available in your developer command prompt.

FUTURE UPDATES:
---------------
• Function calls and namespace scoping
• Memory buffer management
• Full debugging symbol output
• IDE plugin & build preview system

CREDITS:
--------
Created by Violet Aura Creations  
Compiler powered by OpenAI support with x64 NASM backends

===========================================
        May your syntax never segfault!
===========================================


The **Forester Language** you've defined follows a minimalist, symbol-heavy, macro-extensible syntax designed to compile directly into NASM x64 assembly. Based on the document, here's a summarized **language specification and mapping**, combining its syntax with its NASM translation table:

---

### **Forester Core Syntax**

| Symbol                  | Meaning                                   |    |                                |
| ----------------------- | ----------------------------------------- | -- | ------------------------------ |
| `X = 0`, `Y = 1`        | Constants (bool-type logic)               |    |                                |
| `Int`                   | 0–9 (Numeric range)                       |    |                                |
| `Val`                   | a–z (Values)                              |    |                                |
| `Var`                   | Alphanumeric (variable identifiers)       |    |                                |
| `#`                     | Single-line comment                       |    |                                |
| `**`                    | Multiline comment                         |    |                                |
| `=`                     | Mutable assignment                        |    |                                |
| `==`                    | Immutable assignment                      |    |                                |
| `:`                     | Instruction fallback separator            |    |                                |
| `;`                     | End of instruction                        |    |                                |
| `Start`                 | Begin command or definition               |    |                                |
| \`                      | ...                                       | \` | Macro/definition block (CIAMS) |
| `...`                   | Continuation                              |    |                                |
| `Return`                | End execution or return from function     |    |                                |
| `()`                    | Texturizer (semantic modifier)            |    |                                |
| `@`                     | Specifier (type/hint/attribute)           |    |                                |
| `$`                     | Modifier (often macro or dollar-symbolic) |    |                                |
| `!`                     | Configuration                             |    |                                |
| `^`                     | Exponentiation                            |    |                                |
| `~>`                    | Raise/signal                              |    |                                |
| `->`                    | Progress/transition                       |    |                                |
| `[]`                    | Buffer, mediator, context switch          |    |                                |
| `<`, `>`                | Less than / greater than                  |    |                                |
| `<<`, `>>`              | Rollback / Run                            |    |                                |
| `<~`, `<-`              | Flag / Throw                              |    |                                |
| `+`, `-`, `*`, `/`, `%` | Arithmetic operations                     |    |                                |
| `\`                     | Lookup                                    |    |                                |
| `Init`                  | Initialization                            |    |                                |

---

### **Mapped NASM x64 Instruction Set (Excerpt)**

| **Forester Word** | **NASM Instruction**     | **Hex** | **Binary**   |
| ----------------- | ------------------------ | ------- | ------------ |
| `and`             | `AND r/m64, r64`         | `0x1D2` | `111010010`  |
| `or`              | `OR r/m64, r64`          | `0x1D3` | `111010011`  |
| `xor`             | `XOR r/m64, r64`         | `0x1D4` | `111010100`  |
| `not`             | `NOT r/m64`              | `0x1D5` | `111010101`  |
| `and_eq`          | AND with assignment      | `0x1D6` | `111010110`  |
| `or_eq`           | OR with assignment       | `0x1D7` | `111010111`  |
| `xor_eq`          | XOR with assignment      | `0x1D8` | `111011000`  |
| `not_eq`          | CMP + JNE                | `0x1D9` | `111011001`  |
| `nullptr`         | `XOR reg, reg`           | `0x1E0` | `111100000`  |
| `throw`           | `JMP throw_handler`      | `0x1E1` | `111100001`  |
| `if`              | `CMP + conditional jump` | `0x205` | `1000000101` |
| `for`             | `LOOP label`             | `0x20B` | `1000001011` |
| `new`             | `CALL malloc`            | `0x201` | `1000000001` |
| `delete`          | `CALL free`              | `0x202` | `1000000010` |

---

Here is a **Super-Massive, Extensive, Expansive, Tremendous Overview Paper** for the **Forester SDK**—suitable as a manifesto, technical whitepaper, and visionary framework document for distribution, collaboration, or publication.

---

# 🌲 Forester SDK: Language Manifesto and Technical Overview

*A Symbolic Macro-First Compiler System for Ultra-Fast, Zero-Cost Execution Precision*

## Table of Contents

1. Introduction
2. Design Philosophy
3. Language Syntax and Structure
4. NASM Mapping Architecture
5. Compiler Internals
6. Execution Pipeline
7. Developer Workflow
8. Visual Studio Code Integration
9. Use Cases and Target Applications
10. Security, Performance, and Reliability
11. Future Roadmap
12. Conclusion

---

## 1. Introduction

The **Forester Language** is a symbolic, macro-extensible, zero-cost abstraction language designed to compile directly into **x64 NASM Assembly** on **Windows**. Built for performance, human readability, and modular extensibility, Forester bridges the gap between expressive high-level structure and ultra-efficient low-level execution.

Forester is not just a language—it’s a **compiler philosophy**. It asserts that symbolic brevity and intentional design can outperform traditional code when paired with deterministic compilation paths and intelligent macro expansion.

---

## 2. Design Philosophy

* **Symbolism over verbosity:** Every operator, delimiter, and macro is chosen for clarity and brevity.
* **Contextual Inference Abstracted Macro Scripts (CIAMS):** Logic blocks are encapsulated in `|...|`, allowing for reusability, nesting, and contextual override.
* **Zero-cost abstractions:** No runtime interpreter overhead. All code compiles ahead-of-time into NASM, then links into native binaries.
* **Narrative meets machine:** Inspired by storytelling arcs, `Start`, `Return`, and `Init` mirror narrative control while translating into structured logic.

---

## 3. Language Syntax and Structure

### Core Constructs

| Symbol                 | Meaning                           |    |                                 |
| ---------------------- | --------------------------------- | -- | ------------------------------- |
| `Start`                | Begin block or logic              |    |                                 |
| `Return`               | End or output result              |    |                                 |
| `=` / `==`             | Mutable / Immutable assignment    |    |                                 |
| \`                     | macro                             | \` | Macro or CIAMS definition block |
| `;`                    | End of statement                  |    |                                 |
| `@`, `$`, `!`          | Specifiers, modifiers, configs    |    |                                 |
| `->`, `~>`, `<<`, `>>` | Progression, raise, rollback, run |    |                                 |
| `[]`, `()`             | Buffers, texturizers              |    |                                 |
| `#`, `**`              | Comment, multiline comment        |    |                                 |

### Example

```fstr
|math_logic|
    a = 4;
    b = 2;
    c = a * b + 10;
    Return c;
|

|main_program|
    result = |math_logic|;
    if result > 15:
        print("Large Result");
    else:
        print("Small Result");
Return;
```

---

## 4. NASM Mapping Architecture

Forester compiles directly to NASM using a 1:1 token map via its **Symbolic NASM Layer Table**, producing architecture-aligned hex and binary.

| Forester | NASM x64         | Hex   | Binary    |
| -------- | ---------------- | ----- | --------- |
| `add`    | `ADD r/m64, r64` | 0x300 | 110000000 |
| `sub`    | `SUB r/m64, r64` | 0x301 | 110000001 |
| `jmp`    | `JMP label`      | 0x305 | 110000101 |
| `print`  | `CALL puts`      | 0x308 | 110001000 |

This mapping ensures deterministic, optimized translation, facilitating easy extension.

---

## 5. Compiler Internals

Implemented in Python (v2), the Forester Compiler features:

* Lexical tokenizer for symbolic and structural elements
* Macro and variable tracker with contextual evaluation
* Expression resolver with math support
* Code generator that emits `.asm` NASM
* Modular design for adding control structures, functions, memory

### Compilation Phases

1. **Lexing:** Symbol and keyword classification
2. **Parsing:** Contextual AST construction
3. **Macro Expansion:** Inline evaluation and injection
4. **Code Generation:** NASM emission
5. **Assembly:** NASM -> .obj via `nasm`
6. **Linking:** `.obj` -> `.exe` via `link.exe`

---

## 6. Execution Pipeline

```plaintext
[ Forester .fstr ] 
     │
[ Python Compiler Frontend ]
     │
[ NASM .asm ]
     │
[ NASM Assembler ]
     │
[ Object File (.obj) ]
     │
[ MSVC Linker ]
     │
[ Executable (.exe) ]
```

---

## 7. Developer Workflow

1. Create `.fstr` file with macro-driven logic
2. Run `forester_compiler_v2.py`
3. Assemble with NASM
4. Link with MSVC
5. Execute native binary

Optional:

* Use `build_forester.bat` for automated flow
* Enable syntax highlighting in VSCode with `forester.tmLanguage.json`

---

## 8. Visual Studio Code Integration

Includes:

* `.tmLanguage.json` for highlighting keywords, macros, operators, numbers, comments
* Future: IntelliSense plugin, error hooks, and CIAMS expansion previews

---

## 9. Use Cases and Target Applications

* **Embedded Systems**
* **High-performance simulation tools**
* **Crypto/encoding algorithms**
* **VACU-themed game engines**
* **Story-driven control flows**
* **Custom OS bootstraps**

---

## 10. Security, Performance, and Reliability

* **No runtime environment required**
* **Predictable memory behavior**
* **No hidden GC or stack frame pollution**
* **Compile-time macro expansion ensures deterministic logic**

Planned:

* Symbol hashing for macro traceability
* Code verification mode (dry-run, visualize assembly)
* Safe-mode for avoiding direct register clobbering

---

## 11. Future Roadmap

| Feature                      | Status          |
| ---------------------------- | --------------- |
| Namespaces, object modeling  | 🟡 In Progress  |
| Multi-file modules           | 🟡 In Progress  |
| Memory management & buffers  | 🔜 Next Release |
| Forester IDE                 | 🔜 Planned      |
| Live macro injection testing | 🟡 In Design    |
| CI/CD tool integration       | 🔜 Planned      |

---

## 12. Conclusion

Forester is more than just a symbolic language—it's a new way of thinking about compilation, performance, and the poetry of code. Whether you’re building the next-gen engine for simulation, storytelling, or low-level system design, Forester gives you surgical control without sacrificing human-centric readability.

---

🜲 *“Write it once. Compile to metal. Speak it like a riddle.”*
— Forester Project Creed

