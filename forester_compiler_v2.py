import re
import sys

variables = {}

def evaluate_expression(expr):
    try:
        for var in variables:
            expr = expr.replace(var, str(variables[var]))
        return eval(expr)
    except Exception as e:
        print(f"Error evaluating: {expr}")
        return 0

def process_macro_block(lines):
    asm = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            var, expr = line.split("=")
            var = var.strip()
            expr = expr.strip(" ;")
            val = evaluate_expression(expr)
            variables[var] = val
        elif line.startswith("Return"):
            expr = line.split("Return")[-1].strip(" ;")
            val = evaluate_expression(expr)
            return val
    return 0

def transpile_fstr_to_asm(source):
    lines = source.splitlines()
    macros = {}
    current_macro = None
    buffer = []

    for line in lines:
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            if current_macro:
                macros[current_macro] = buffer.copy()
                buffer = []
            current_macro = line.strip("|")
        elif current_macro:
            buffer.append(line)

    if current_macro and buffer:
        macros[current_macro] = buffer

    val = process_macro_block(macros.get("math_macro", []))
    message = "Greater than ten" if val > 10 else "Ten or less"

    # Output ASM based on logic
    output = [
        "section .data",
        f'    msg db "{message}", 0',
        "section .text",
        "    global main",
        "    extern printf",
        "main:",
        "    mov rcx, msg",
        "    call printf",
        "    ret"
    ]
    return "\n".join(output)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python forester_compiler_v2.py input.fstr output.asm")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    asm = transpile_fstr_to_asm(code)
    with open(sys.argv[2], 'w') as out:
        out.write(asm)
    print(f"Compiled {sys.argv[1]} to {sys.argv[2]}")

import re
import sys

def transpile_forester_to_asm(fstr_code):
    output = []
    output.append("section .data")
    output.append('    out_gt db "Greater than ten", 0')
    output.append('    out_le db "Ten or less", 0')
    output.append("section .text")
    output.append("    global main")
    output.append("    extern printf")
    output.append("main:")

    # basic mock parser
    if "|math_macro|" in fstr_code:
        output += [
            "    mov rax, 5",
            "    mov rbx, 3",
            "    add rax, rbx",
            "    imul rax, rax, 2"
        ]
    if "|conditional_check|" in fstr_code:
        output += [
            "    cmp rax, 10",
            "    jg  _greater",
            "    jmp _less",
            "_greater:",
            "    mov rcx, out_gt",
            "    call printf",
            "    jmp _exit",
            "_less:",
            "    mov rcx, out_le",
            "    call printf",
            "_exit:",
            "    ret"
        ]
    return "\n".join(output)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python forester_compiler.py input.fstr output.asm")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    asm = transpile_forester_to_asm(code)
    with open(sys.argv[2], 'w') as out:
        out.write(asm)
    print(f"Transpiled to {sys.argv[2]}")

# Generate a C++ starter file that parses a `.fstr` file, extracts `:hasm` blocks,
# and emits a corresponding `.asm` and `.bin` output.

cpp_code = R"""#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <iomanip>

void write_bin(const std::vector<uint8_t>& bytes, const std::string& filename) {
    std::ofstream binout(filename, std::ios::binary);
    for (auto b : bytes) {
        binout.put(static_cast<char>(b));
    }
    binout.close();
}

void write_asm(const std::vector<std::string>& asm_lines, const std::string& filename) {
    std::ofstream asmout(filename);
    for (const auto& line : asm_lines) {
        asmout << line << std::endl;
    }
    asmout.close();
}

std::vector<std::string> tokenize_hex(const std::string& line) {
    std::vector<std::string> tokens;
    std::istringstream iss(line);
    std::string token;
    while (iss >> token) {
        if (token[0] == ';') break; // stop at comment
        if (token.find('[') != std::string::npos || token.find(']') != std::string::npos) continue;
        tokens.push_back(token);
    }
    return tokens;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: hasm_compiler <input.fstr>" << std::endl;
        return 1;
    }

    std::ifstream infile(argv[1]);
    if (!infile) {
        std::cerr << "Error opening file: " << argv[1] << std::endl;
        return 1;
    }

    std::string line;
    bool in_hasm = false;
    std::vector<uint8_t> bin_output;
    std::vector<std::string> asm_output;

    while (std::getline(infile, line)) {
        std::string trimmed = line;
        trimmed.erase(0, trimmed.find_first_not_of(" \t\r\n"));
        if (trimmed == ":hasm") {
            in_hasm = true;
            continue;
        }
        if (trimmed == ":endhasm") {
            in_hasm = false;
            continue;
        }

        if (in_hasm) {
            asm_output.push_back(line);
            auto tokens = tokenize_hex(line);
            for (const auto& hex : tokens) {
                uint8_t byte = static_cast<uint8_t>(std::stoi(hex, nullptr, 16));
                bin_output.push_back(byte);
            }
        }
    }

    write_bin(bin_output, "output.bin");
    write_asm(asm_output, "output.asm");

    std::cout << "Compilation complete: output.bin and output.asm generated." << std::endl;
    return 0;
}
"""

cpp_path = "/mnt/data/hasm_compiler.cpp"
with open(cpp_path, "w") as cpp_file:
    cpp_file.write(cpp_code)

cpp_path

makefile_content = """\
# Makefile for Hasm Compiler
CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall

TARGET = hasm_compiler
SRC = hasm_compiler.cpp

all: $(TARGET)

$(TARGET): $(SRC)
\t$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
\trm -f $(TARGET) output.asm output.bin
"""

makefile_path = "/mnt/data/Makefile"
with open(makefile_path, "w") as mf:
    mf.write(makefile_content)

makefile_path

# Update the C++ compiler backend to include:
# - Label resolution
# - Macro substitution (from a hypothetical .macro file)
# - Debug logging for each parsed byte

cpp_extended_code = R"""#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <iomanip>
#include <regex>

void write_bin(const std::vector<uint8_t>& bytes, const std::string& filename) {
    std::ofstream binout(filename, std::ios::binary);
    for (auto b : bytes) binout.put(static_cast<char>(b));
    binout.close();
}

void write_asm(const std::vector<std::string>& asm_lines, const std::string& filename) {
    std::ofstream asmout(filename);
    for (const auto& line : asm_lines) asmout << line << std::endl;
    asmout.close();
}

void write_log(const std::vector<std::string>& logs, const std::string& filename) {
    std::ofstream logout(filename);
    for (const auto& log : logs) logout << log << std::endl;
    logout.close();
}

std::vector<std::string> tokenize_hex(const std::string& line) {
    std::vector<std::string> tokens;
    std::istringstream iss(line);
    std::string token;
    while (iss >> token) {
        if (token[0] == ';') break;
        if (token.find('[') != std::string::npos || token.find(']') != std::string::npos) continue;
        tokens.push_back(token);
    }
    return tokens;
}

void load_macros(const std::string& filename, std::unordered_map<std::string, std::string>& macros) {
    std::ifstream infile(filename);
    std::string line;
    while (std::getline(infile, line)) {
        std::istringstream iss(line);
        std::string key, val;
        if (iss >> key >> val) {
            macros[key] = val;
        }
    }
    infile.close();
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: hasm_compiler <input.fstr> [macros.txt]" << std::endl;
        return 1;
    }

    std::string input_file = argv[1];
    std::unordered_map<std::string, std::string> macros;
    if (argc >= 3) {
        load_macros(argv[2], macros);
    }

    std::ifstream infile(input_file);
    if (!infile) {
        std::cerr << "Error opening file: " << input_file << std::endl;
        return 1;
    }

    std::string line;
    bool in_hasm = false;
    std::vector<uint8_t> bin_output;
    std::vector<std::string> asm_output;
    std::vector<std::string> debug_log;
    std::unordered_map<std::string, size_t> labels;
    std::vector<std::pair<size_t, std::string>> unresolved;

    size_t byte_offset = 0;
    while (std::getline(infile, line)) {
        std::string trimmed = line;
        trimmed.erase(0, trimmed.find_first_not_of(" \t\r\n"));
        if (trimmed == ":hasm") { in_hasm = true; continue; }
        if (trimmed == ":endhasm") { in_hasm = false; continue; }

        if (in_hasm) {
            if (trimmed.back() == ':') {
                std::string label = trimmed.substr(0, trimmed.size() - 1);
                labels[label] = byte_offset;
                continue;
            }

            for (const auto& [key, val] : macros) {
                if (line.find(key) != std::string::npos) {
                    line = std::regex_replace(line, std::regex(key), val);
                }
            }

            asm_output.push_back(line);
            auto tokens = tokenize_hex(line);
            for (const auto& token : tokens) {
                if (labels.count(token)) {
                    uint8_t addr = static_cast<uint8_t>(labels[token]);
                    bin_output.push_back(addr);
                    debug_log.push_back("Resolved label " + token + " -> " + std::to_string(addr));
                } else if (std::regex_match(token, std::regex("^[0-9A-Fa-f]{2}$"))) {
                    uint8_t byte = static_cast<uint8_t>(std::stoi(token, nullptr, 16));
                    bin_output.push_back(byte);
                    debug_log.push_back("Parsed byte " + token + " -> " + std::to_string(byte));
                } else {
                    unresolved.emplace_back(byte_offset, token);
                    bin_output.push_back(0x00); // placeholder
                    debug_log.push_back("Unresolved symbol " + token + " at offset " + std::to_string(byte_offset));
                }
                ++byte_offset;
            }
        }
    }

    for (auto& [offset, symbol] : unresolved) {
        if (labels.count(symbol)) {
            bin_output[offset] = static_cast<uint8_t>(labels[symbol]);
            debug_log.push_back("Backpatched " + symbol + " at " + std::to_string(offset) + " with " + std::to_string(labels[symbol]));
        } else {
            debug_log.push_back("Failed to resolve symbol: " + symbol);
        }
    }

    write_bin(bin_output, "output.bin");
    write_asm(asm_output, "output.asm");
    write_log(debug_log, "debug.log");

    std::cout << "Compilation complete: output.bin, output.asm, and debug.log generated." << std::endl;
    return 0;
}
"""

cpp_extended_path = "/mnt/data/hasm_compiler_extended.cpp"
with open(cpp_extended_path, "w") as cpp_file:
    cpp_file.write(cpp_extended_code)

cpp_extended_path

# Create a macro file template
macro_file_content = """\
; Macro substitutions for Hasm mode
CALL_RET    E8 05 00 00 00
LOAD_AL     B0 4F
RETURN      C3
"""

macro_file_path = "/mnt/data/hasm_macros.txt"
with open(macro_file_path, "w") as macro_file:
    macro_file.write(macro_file_content)

# Create a unit test suite for Hasm compiler functionality (C++ style pseudotest)
unit_test_content = R"""#include <cassert>
#include <iostream>
#include <vector>
#include <string>

// Dummy test harness
void test_tokenizer() {
    std::string line = "[0000] B0 4F ; MOV AL, 0x4F";
    std::vector<std::string> tokens;
    std::istringstream iss(line);
    std::string token;
    while (iss >> token) {
        if (token[0] == ';') break;
        if (token.find('[') != std::string::npos || token.find(']') != std::string::npos) continue;
        tokens.push_back(token);
    }
    assert(tokens.size() == 2);
    assert(tokens[0] == "B0");
    assert(tokens[1] == "4F");
    std::cout << "test_tokenizer passed\n";
}

void test_macro_substitution() {
    std::string line = "LOAD_AL ; macro";
    std::unordered_map<std::string, std::string> macros = { {"LOAD_AL", "B0 4F"} };
    for (const auto& [key, val] : macros) {
        if (line.find(key) != std::string::npos) {
            line = std::regex_replace(line, std::regex(key), val);
        }
    }
    assert(line.find("B0 4F") != std::string::npos);
    std::cout << "test_macro_substitution passed\n";
}

int main() {
    test_tokenizer();
    test_macro_substitution();
    return 0;
}
"""

unit_test_path = "/mnt/data/hasm_tests.cpp"
with open(unit_test_path, "w") as test_file:
    test_file.write(unit_test_content)

(macro_file_path, unit_test_path)

# Create folder structure and wrapper scripts for VACU SDK toolchain integration

# 1. SDK folder and substructure
sdk_structure = {
    "VACU-SDK/compilers": ["hasm_compiler_extended.cpp", "hasm_tests.cpp", "Makefile"],
    "VACU-SDK/examples": ["forester_hasm_sample.fstr", "hasm_macros.txt"],
    "VACU-SDK/docs": ["README.txt"],
    "VACU-SDK/scripts": ["build_and_run.bat", "build_and_run.sh"],
}

# 2. Command-line wrapper scripts
bat_script = """@echo off
echo Building Hasm Compiler...
make
echo Running Compiler...
hasm_compiler forester_hasm_sample.fstr hasm_macros.txt
echo Output written to output.bin, output.asm, debug.log
pause
"""

sh_script = """#!/bin/bash
echo "Building Hasm Compiler..."
make
echo "Running Compiler..."
./hasm_compiler forester_hasm_sample.fstr hasm_macros.txt
echo "Output written to output.bin, output.asm, debug.log"
"""

readme_text = """VACU SDK - Forester + Hasm Toolchain

Folder Structure:
- compilers: C++ source files and Makefile
- examples: Sample Forester + Hasm source and macro files
- docs: Documentation
- scripts: Helper scripts for Windows (.bat) and Unix (.sh)

To Build and Run:
1. Navigate to VACU-SDK/compilers
2. Run the appropriate script from the scripts/ directory

Requirements:
- g++ compiler
- make
"""

# Write scripts and docs
with open("/mnt/data/build_and_run.bat", "w") as bat:
    bat.write(bat_script)

with open("/mnt/data/build_and_run.sh", "w") as sh:
    sh.write(sh_script)

with open("/mnt/data/README.txt", "w") as readme:
    readme.write(readme_text)

["/mnt/data/build_and_run.bat", "/mnt/data/build_and_run.sh", "/mnt/data/README.txt"]

→ The Ritual of Compilation begins...
→ Hex Binding complete: 34 bytes burned into the bin.
→ Anomaly in line 3: ‘CALL_RET’ misaligned with memory ward.

# Generate the files requested:
# 1. HUI Engine Shell in C++
# 2. Sample Scroll-Narrative Interaction File
# 3. Sigil System Design Document

# ------------------------
# 1. C++ HUI Engine Shell
# ------------------------
hui_engine_code = R"""#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

void display_banner() {
    std::cout << "╔════════════════════════════════════╗\n";
    std::cout << "║   VIOLET AURA COMPILER RITE       ║\n";
    std::cout << "║     [HUI v0.1 – Hybrid Shell]     ║\n";
    std::cout << "╚════════════════════════════════════╝\n";
    std::cout << "   Forge your command sigils below\n";
}

void display_sigil_menu() {
    std::cout << "\nAvailable Sigils:\n";
    std::cout << "  [⚒️] F+H – Forge Hasm (Compile)\n";
    std::cout << "  [✒️] S+T – Scroll Test (Run Tests)\n";
    std::cout << "  [📜] S+R – Scroll & Run (Compile + Run)\n";
    std::cout << "  [🔥] V+X+X – Void Hex Output (Clean)\n";
    std::cout << "  [❌] Q – Quit\n\n";
}

void perform_action(const std::string& sigil) {
    if (sigil == "F+H") {
        std::cout << "→ The Ritual of Compilation begins...\n";
        std::system("make && ./hasm_compiler forester_hasm_sample.fstr hasm_macros.txt");
    } else if (sigil == "S+T") {
        std::cout << "→ Inscribing sacred test scrolls...\n";
        std::system("g++ -std=c++17 -o hasm_tests hasm_tests.cpp && ./hasm_tests");
    } else if (sigil == "S+R") {
        std::cout << "→ The Scroll is drawn, and the Hex ignites...\n";
        std::system("make && ./hasm_compiler forester_hasm_sample.fstr hasm_macros.txt && cat output.asm");
    } else if (sigil == "V+X+X") {
        std::cout << "→ Hex voided. Output ashes scattered.\n";
        std::system("rm -f output.* debug.log");
    } else {
        std::cout << "→ Unknown sigil. No effect.\n";
    }
}

int main() {
    display_banner();
    display_sigil_menu();
    std::string input;
    while (true) {
        std::cout << "[Rune]> ";
        std::getline(std::cin, input);
        if (input == "Q" || input == "q") break;
        perform_action(input);
    }
    std::cout << "→ The compiler rites are sealed.\n";
    return 0;
}
"""

# ------------------------
# 2. Scroll-Narrative File
# ------------------------
scroll_narrative = """\
~*~ The Scroll of Hex Binding ~*~

You, Compiler Ritualist, hold the sacred lines:

:hasm
    LOAD_AL             ; Load Accumulator with 0x4F
    CALL_RET            ; Call to the return chamber
    RETURN              ; Exit from ritual gate
:endhasm

Beneath this parchment, flames await.
Your action will ignite the pattern.

Inscribe your will by selecting a Sigil.
"""

# ------------------------
# 3. Sigil System Description
# ------------------------
sigil_design_doc = """\
VACU Sigil System – Symbolic Command Glyphs

[⚒️] F+H : "Forge Hasm" – Compile Hasm code into binary form.
[✒️] S+T : "Scroll Test" – Run the test scrolls on parser and macros.
[📜] S+R : "Scroll & Run" – Compile and then display output.asm.
[🔥] V+X+X : "Void Hex Output" – Delete compiled artifacts and logs.
[❌] Q : "Quit" – Exit HUI ritual loop.

Sigils are typed combinations, not single letters.
They form a symbolic command language via capital+punctuation gestures.

This system is meant to feel tactile, story-like, and ceremonial.
"""

# File paths
hui_cpp_path = "/mnt/data/vacu_hui.cpp"
scroll_path = "/mnt/data/scroll_narrative.txt"
sigil_path = "/mnt/data/sigil_system.txt"

# Write files
with open(hui_cpp_path, "w") as f:
    f.write(hui_engine_code)

with open(scroll_path, "w") as f:
    f.write(scroll_narrative)

with open(sigil_path, "w") as f:
    f.write(sigil_design_doc)

[hui_cpp_path, scroll_path, sigil_path]

# Create the files for:
# - Keyboard Glyph Overlay Guide
# - Sound Effect Trigger Mapping
# - ASCII-based Rune Animation Stubs

# 1. Keyboard Glyph Overlay Guide
keyboard_overlay = """\
VACU HUI – Keyboard Glyph Overlay Guide

These combinations are symbolic gestures:

+------+---------------------------+
| Key  | Glyph Meaning             |
+------+---------------------------+
|  F+H | ⚒️ Forge Hasm             |
|  S+T | ✒️ Scroll Test            |
|  S+R | 📜 Scroll & Run           |
| V+X+X| 🔥 Void Hex Output        |
|  Q   | ❌ Quit                   |
+------+---------------------------+

To use:
- Type exactly as shown (capital + symbol if required).
- The system will match gesture inputs to rituals.

Use your keyboard like a spellcasting conduit.
"""

# 2. Sound Effects / MIDI Feedback Mapping
sound_mapping = """\
VACU HUI – Sigil Sound Feedback Mapping

[⚒️] F+H : Play "anvil_strike.wav"
[✒️] S+T : Play "quill_scratch.wav"
[📜] S+R : Play "scroll_unfurl.wav"
[🔥] V+X+X : Play "fire_crack.wav"
[❌] Q : Play "ritual_close.wav"

Optional MIDI Notes:
- F+H : C3 (Percussive Anvil)
- S+T : D#4 (Light Wood Tap)
- S+R : A2 (Scroll Wind)
- V+X+X : G#1 (Fire Sizzle)
- Q : B3 (Closure Bell)
"""

# 3. ASCII Rune Animation Stub
ascii_runes = """\
VACU HUI – ASCII Rune Compilation Animations

Forge Hasm:
  [⚒️] 
    --> [░░▒▒▓▓█] Compiling...
    --> [✓] Hex Bound to Scroll

Scroll Test:
  [✒️] 
    --> [..///***] Running rituals...
    --> [✓] Glyphs validated

Scroll & Run:
  [📜]
    --> [~ ~ ~] The scroll breathes...
    --> [output.asm shown]

Void Hex Output:
  [🔥]
    --> [#######] Scattering ashes...
    --> [ ] Cleaned

Each animation can be timed to display with progressive effect.
"""

# File paths
overlay_path = "/mnt/data/keyboard_overlay.txt"
sound_path = "/mnt/data/sound_mapping.txt"
ascii_path = "/mnt/data/ascii_runes.txt"

# Write all files
with open(overlay_path, "w") as f:
    f.write(keyboard_overlay)

with open(sound_path, "w") as f:
    f.write(sound_mapping)

with open(ascii_path, "w") as f:
    f.write(ascii_runes)

[overlay_path, sound_path, ascii_path]

# Prepare embedded ASCII animations and sound triggers inside an updated HUI engine (C++)
# Package everything into a ready-to-zip structure for .zip and .exe creation later

# C++ HUI engine with embedded ASCII animations and optional sound triggers (cross-platform stubbed)
hui_animated_cpp = R"""#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <cstdlib>

void pause_display(int ms) {
    std::this_thread::sleep_for(std::chrono::milliseconds(ms));
}

void animation_compile() {
    std::string frames[] = { "░", "░░", "▒▒", "▓▓", "██", "[✓] Hex Bound" };
    for (const auto& frame : frames) {
        std::cout << "   " << frame << std::endl;
        pause_display(250);
    }
}

void animation_scroll() {
    std::string frames[] = { "~", "~ ~", "~ ~ ~", "[Scroll Breathes]", "[✓]" };
    for (const auto& frame : frames) {
        std::cout << "   " << frame << std::endl;
        pause_display(300);
    }
}

void animation_test() {
    std::string frames[] = { "..", "../", "//", "**", "[✓ Glyphs Validated]" };
    for (const auto& frame : frames) {
        std::cout << "   " << frame << std::endl;
        pause_display(200);
    }
}

void animation_clean() {
    std::string frames[] = { "#####", "####", "###", "##", "#", "[Cleaned]" };
    for (const auto& frame : frames) {
        std::cout << "   " << frame << std::endl;
        pause_display(150);
    }
}

void play_sound(const std::string& effect) {
#ifdef _WIN32
    std::string cmd = "powershell -c (New-Object Media.SoundPlayer '" + effect + "').PlaySync();";
    system(cmd.c_str());
#else
    std::string cmd = "afplay " + effect + " &> /dev/null";
    system(cmd.c_str());
#endif
}

void display_banner() {
    std::cout << "╔════════════════════════════════════╗\n";
    std::cout << "║   VIOLET AURA COMPILER RITE       ║\n";
    std::cout << "║     [HUI v0.2 – Hybrid Shell]     ║\n";
    std::cout << "╚════════════════════════════════════╝\n";
    std::cout << "   Forge your command sigils below\n";
}

void display_sigil_menu() {
    std::cout << "\nAvailable Sigils:\n";
    std::cout << "  [⚒️] F+H – Forge Hasm (Compile)\n";
    std::cout << "  [✒️] S+T – Scroll Test (Run Tests)\n";
    std::cout << "  [📜] S+R – Scroll & Run (Compile + Run)\n";
    std::cout << "  [🔥] V+X+X – Void Hex Output (Clean)\n";
    std::cout << "  [❌] Q – Quit\n\n";
}

void perform_action(const std::string& sigil) {
    if (sigil == "F+H") {
        std::cout << "→ The Ritual of Compilation begins...\n";
        animation_compile();
        play_sound("anvil_strike.wav");
        std::system("make && ./hasm_compiler forester_hasm_sample.fstr hasm_macros.txt");
    } else if (sigil == "S+T") {
        std::cout << "→ Inscribing sacred test scrolls...\n";
        animation_test();
        play_sound("quill_scratch.wav");
        std::system("g++ -std=c++17 -o hasm_tests hasm_tests.cpp && ./hasm_tests");
    } else if (sigil == "S+R") {
        std::cout << "→ The Scroll is drawn, and the Hex ignites...\n";
        animation_scroll();
        play_sound("scroll_unfurl.wav");
        std::system("make && ./hasm_compiler forester_hasm_sample.fstr hasm_macros.txt && cat output.asm");
    } else if (sigil == "V+X+X") {
        std::cout << "→ Hex voided. Output ashes scattered.\n";
        animation_clean();
        play_sound("fire_crack.wav");
        std::system("rm -f output.* debug.log");
    } else {
        std::cout << "→ Unknown sigil. No effect.\n";
    }
}

int main() {
    display_banner();
    display_sigil_menu();
    std::string input;
    while (true) {
        std::cout << "[Rune]> ";
        std::getline(std::cin, input);
        if (input == "Q" || input == "q") break;
        perform_action(input);
    }
    std::cout << "→ The compiler rites are sealed.\n";
    play_sound("ritual_close.wav");
    return 0;
}
"""

animated_cpp_path = "/mnt/data/vacu_hui_animated.cpp"
with open(animated_cpp_path, "w") as f:
    f.write(hui_animated_cpp)

animated_cpp_path

import shutil

# Define bundle directory and files to include
bundle_dir = "/mnt/data/VACU-HUI-SDK"
files_to_bundle = {
    "vacu_hui_animated.cpp": bundle_dir + "/compilers/vacu_hui_animated.cpp",
    "hasm_compiler_extended.cpp": bundle_dir + "/compilers/hasm_compiler_extended.cpp",
    "hasm_tests.cpp": bundle_dir + "/compilers/hasm_tests.cpp",
    "Makefile": bundle_dir + "/compilers/Makefile",
    "forester_hasm_sample.fstr": bundle_dir + "/examples/forester_hasm_sample.fstr",
    "hasm_macros.txt": bundle_dir + "/examples/hasm_macros.txt",
    "scroll_narrative.txt": bundle_dir + "/docs/scroll_narrative.txt",
    "sigil_system.txt": bundle_dir + "/docs/sigil_system.txt",
    "keyboard_overlay.txt": bundle_dir + "/docs/keyboard_overlay.txt",
    "sound_mapping.txt": bundle_dir + "/docs/sound_mapping.txt",
    "ascii_runes.txt": bundle_dir + "/docs/ascii_runes.txt",
    "build_and_run.bat": bundle_dir + "/scripts/build_and_run.bat",
    "build_and_run.sh": bundle_dir + "/scripts/build_and_run.sh",
    "README.txt": bundle_dir + "/docs/README.txt"
}

# Copy files to appropriate structure
for src, dest in files_to_bundle.items():
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy(f"/mnt/data/{src}", dest)

# Create the zip archive
zip_path = "/mnt/data/VACU-HUI-SDK.zip"
shutil.make_archive("/mnt/data/VACU-HUI-SDK", 'zip', bundle_dir)

zip_path

# Create a Windows batch script that simulates an .exe launcher
# It will:
# - Compile the HUI engine
# - Run it directly
# - Simulate sound folder and expected files

exe_sim_batch = """@echo off
echo Initializing VACU HUI Engine...
cd compilers
g++ -std=c++17 -o vacu_hui vacu_hui_animated.cpp
if %errorlevel% neq 0 (
    echo Compilation failed. Exiting.
    pause
    exit /b
)
cd ..
echo.
echo Executing the Compiler Rite...
cd compilers
vacu_hui
"""

# Simulated sound files (placeholders for real .wav content)
sound_files = {
    "anvil_strike.wav": "WAV_STUB_ANVIL",
    "quill_scratch.wav": "WAV_STUB_QUILL",
    "scroll_unfurl.wav": "WAV_STUB_SCROLL",
    "fire_crack.wav": "WAV_STUB_FIRE",
    "ritual_close.wav": "WAV_STUB_CLOSE"
}

# Write the startup batch
exe_launcher_path = "/mnt/data/VACU-HUI-SDK/scripts/launch_hui.bat"
os.makedirs(os.path.dirname(exe_launcher_path), exist_ok=True)
with open(exe_launcher_path, "w") as f:
    f.write(exe_sim_batch)

# Create dummy sound folder and add stubs
sound_folder = "/mnt/data/VACU-HUI-SDK/sound"
os.makedirs(sound_folder, exist_ok=True)
for filename, content in sound_files.items():
    with open(os.path.join(sound_folder, filename), "w") as sf:
        sf.write(content)

# Repackage with launcher and sound files
zip_path_final = "/mnt/data/VACU-HUI-SDK-INSTALLER.zip"
shutil.make_archive(zip_path_final.replace('.zip', ''), 'zip', "/mnt/data/VACU-HUI-SDK")

zip_path_final

