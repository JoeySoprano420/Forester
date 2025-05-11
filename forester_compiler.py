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
