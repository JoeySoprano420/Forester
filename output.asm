section .data
    out_gt db "Greater than ten", 0
    out_le db "Ten or less", 0

section .text
    global main
    extern printf

main:
    mov rax, 5
    mov rbx, 3
    add rax, rbx
    imul rax, rax, 2
    cmp rax, 10
    jg  _greater
    jmp _less

_greater:
    mov rcx, out_gt
    call printf
    jmp _exit

_less:
    mov rcx, out_le
    call printf

_exit:
    ret
