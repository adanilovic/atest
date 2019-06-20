.section INTERRUPT_VECTOR, "x"
.global _Reset
_Reset:
    B Reset_Handler /* Reset */

.balign 0x800
vector_table_el3:
    curr_el_sp0_sync:

register_init:
    mov x0,  xzr
    mov x1,  xzr
    mov x2,  xzr
    mov x3,  xzr
    mov x4,  xzr
    mov x5,  xzr
    mov x6,  xzr
    mov x7,  xzr
    mov x8,  xzr
    mov x9,  xzr
    mov x10, xzr
    mov x11, xzr
    mov x12, xzr
    mov x13, xzr
    mov x14, xzr
    mov x15, xzr
    mov x16, xzr
    mov x17, xzr
    mov x18, xzr
    mov x19, xzr
    mov x20, xzr
    mov x21, xzr
    mov x22, xzr
    mov x23, xzr
    mov x24, xzr
    mov x25, xzr
    mov x26, xzr
    mov x27, xzr
    mov x28, xzr
    mov x29, xzr
    #x30 holds return address, don't initialize

    msr HCR_EL2, xzr
    ldr x1, =0x30c50838
    msr SCTLR_EL2, x1
    msr SCTLR_EL1, x1
    ret

write_byte_to_stderr:
    mov w0, #0x03
    hlt #0xf000
    ret

cache_init:
    mrs x0, SCTLR_EL3
    bic x0, x0, #(0x1 << 2)
    msr SCTLR_EL3, x0

    mov x0, #0x0
    msr CSSELR_EL1, x0
    
    mrs x4, CCSIDR_EL1
    and x1, x4, #0x7
    add x1, x1, #0x4

    adr x7, cache_line_size
    str x1, [x7]

    ldr x3, =0x7FFF
    and x2, x3, x4, LSR #13

    adr x7, cache_set_number
    str x2, [x7]

    ldr x3, =0x3FF
    and x3, x3, x4, lsr #3

    adr x7, cache_associativity_number
    str x3, [x7]

    clz w4, w3

    mov x5, #0
    way_loop:
    mov x6, #0
    set_loop:
    lsl x7, x5, x4
    orr x7, x0, x7
    lsl x8, x6, x1
    orr x7, x7, x8
    dc cisw, x7
    add x6, x6, #1
    cmp x6, x2
    ble set_loop
    add x5, x5, #1
    cmp x5, x3
    ble way_loop    

    ret

Reset_Handler:
    bl register_init
    bl cache_init
    mrs x0, MPIDR_EL1
    and x0, x0, #0xFFFF
    cbz x0, cpu0_boot
    cmp x0, #0x01
    cmp x0, #0x02
    beq cpu2_boot
    cmp x0, #0x03
    beq cpu3_boot

sleep:
    wfi
    B sleep

cpu0_boot:
    adr x0, stack_top_cpu0
    mov sp, x0
    b boot

cpu1_boot:
    adr x0, stack_top_cpu1
    mov sp, x0
    b .

cpu2_boot:
    adr x0, stack_top_cpu2
    mov sp, x0
    b .

cpu3_boot:
    adr x0, stack_top_cpu3
    mov sp, x0
    b .

boot:
    adr x1, cache_line_size
    bl write_byte_to_stderr

    adr x1, cache_set_number
    bl write_byte_to_stderr

    adr x1, cache_associativity_number
    bl write_byte_to_stderr

    mrs x8, CLIDR_EL1
    adr x1, number_of_caches
    str x8, [x1]
    bl write_byte_to_stderr
    add x1, x1, #1
    bl write_byte_to_stderr
    add x1, x1, #1
    bl write_byte_to_stderr
    add x1, x1, #1
    bl write_byte_to_stderr

    /*MMU Registers

    TLB Registers
        TCR_EL1
        TTBR0_EL1    
        TTBR1_EL1

    TLB Instructions
        tlbi all ;Invalidate all entries in the TLB

    Each Exception Level EL1, EL2, and EL3, has its own Virtual Address Space*/

    mov w0, #0x18
    adr x1, code
    hlt #0xf000

.data
.balign 8
code:                       .dword 0x00020026
status:                     .dword 0x77777777
number_of_caches:           .dword 0xffffffff
cache_line_size:            .dword 0xffffffff
cache_set_number:           .dword 0xffffffff
cache_associativity_number: .dword 0xffffffff
.end
