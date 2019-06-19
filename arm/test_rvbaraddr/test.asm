.section INTERRUPT_VECTOR, "x"
.global _Reset
_Reset:
    B Reset_Handler /* Reset */

write_byte_to_stderr:
    mov w0, #0x03
    hlt #0xf000
    ret

Reset_Handler:
    mrs x0, MPIDR_EL1
    and x0, x0, #0xFFFF
    cbz x0, boot

sleep:
    wfi
    B sleep

boot:
    mov x12, #0x4
    adr x1, output

    mrs x0, RVBAR_EL3
    str x0, [x1]

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
