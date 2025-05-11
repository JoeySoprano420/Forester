; Forester Compiler Runtime - x64 NASM for Windows

section .data
    msg_gt db "Greater than ten", 0
    msg_le db "Ten or less", 0

section .text
    global main
    extern printf

main:
    ; Initialize values
    mov rax, 5      ; a
    mov rbx, 3      ; b
    add rax, rbx    ; c = a + b
    shl rax, 1      ; d = c * 2 (multiply by 2 via shift left)

    ; Conditional
    cmp rax, 10
    jg  .greater
    jmp .lesser

.greater:
    mov rcx, msg_gt
    call printf
    jmp .exit

.lesser:
    mov rcx, msg_le
    call printf

.exit:
    ret
