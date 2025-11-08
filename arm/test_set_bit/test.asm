.section INTERRUPT_VECTOR, "x"
.global _Reset
_Reset:
    B Reset_Handler /* Reset */

write_byte_to_stderr:
    mov w0, #0x03
    hlt #0xf000
    ret

read_byte_from_stdin:
    mov x1, #0x0
    mov w0, #0x07
    hlt #0xf000
    ret

Reset_Handler:
    mrs x0, MPIDR_EL1
    and x0, x0, #0xFFFF
    cbz x0, boot

sleep:
    wfi
    B sleep

set_bit:
    /*
    Args:
        x0 - Input,Output, contains the 64-bit value to modify
        x1 - Input, contains bit number to set
    */
    stp x29, x30, [sp, #-32]!   //Save LR and FR, and decrement SP
    mov x29, sp

    orr x0, x0, x1

    ldp x29, x30, [sp], 32
    ret


reverse_byte:
    /*
    Args:
        x0 - Input,Output, contains the 64-bit value to modify
    */
    stp x29, x30, [sp, #-32]!   //Save LR and FR, and decrement SP
    mov x29, sp

    and w1, w0, #0x000000ff
    lsl w1, w1, #24

    and w2, w0, #0x0000ff00
    lsl w2, w2, #8

    and w3, w0, #0xff000000
    lsr w3, w3, #24

    and w4, w0, #0x00ff0000
    lsr w4, w4, #8

    orr w1, w1, w2
    orr w1, w1, w3
    orr w1, w1, w4

    mov x0, x1

    ldp x29, x30, [sp], 32
    ret

boot:
    //initialize stack pointer
    adr x0, stack_top_cpu0
    mov sp, x0

    //set bit in word
    ldr w0, =0xabcdef12
    rev w0, w0
    //bl reverse_byte

    //write output to memory
    adr x1, output
    str x0, [x1]

    //write byte from memory to stdout
    mov x12, #0x4
    loop_start:
    bl write_byte_to_stderr
    add x1, x1, 1
    sub x12, x12, #0x1
    cbnz x12, loop_start

    mov w0, #0x18
    adr x1, code
    hlt #0xf000

.data
.balign 8
code:   .dword 0x00020026
status: .dword 0x77777777
output: .dword 0x88888888
.end
