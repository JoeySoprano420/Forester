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

