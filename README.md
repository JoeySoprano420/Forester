# Forester

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

