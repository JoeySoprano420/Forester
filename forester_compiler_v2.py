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
