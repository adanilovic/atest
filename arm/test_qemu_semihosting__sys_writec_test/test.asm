.section INTERRUPT_VECTOR, "x"
.global _Reset
_Reset:
    B Reset_Handler /* Reset */

Reset_Handler:
    mrs x0, MPIDR_EL1
    and x0, x0, #0xFFFF
    cbz x0, boot

sleep:
    wfi
    B sleep

boot:
    adr x1, output
    mov w0, #0x03
    hlt #0xf000

    mov w0, #0x18
    adr x1, code
    hlt #0xf000

.data
.balign 8
code:   .dword 0x00020026
status: .dword 0x77777777
output: .dword 0x88888888
.end
