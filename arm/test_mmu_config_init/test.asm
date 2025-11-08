.section INTERRUPT_VECTOR, "x"
.global _Reset
_Reset:
    B Reset_Handler /* Reset */

.balign 0x800
vector_table_el3:
    curr_el_sp0_sync:

Reset_Handler:
    bl register_init
    bl disable_caches

    mov x0, #0      //init level 1 cache
    bl cache_init

    b cpu_boot      //doesn't return

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

write_dword_to_stderr:
    /*
    Write 4 bytes to stderr using the Angel semi-hosting
    interface

    Args:
        x1 - Address to write to stderr
    */
    mov w0, #0x03
    hlt #0xf000
    add x1, x1, #1
    mov w0, #0x03
    hlt #0xf000
    add x1, x1, #1
    mov w0, #0x03
    hlt #0xf000
    add x1, x1, #1
    mov w0, #0x03
    hlt #0xf000
    ret

disable_caches:
    mrs x0, SCTLR_EL3
    bic x0, x0, #(0x1 << 2)
    msr SCTLR_EL3, x0
    ret

cache_init:
    /*
    Initialize the given level of cache

    Args:
        x0 - Contains the level of cache that will be initialized
    */
    msr CSSELR_EL1, x0
    
    mrs x4, CCSIDR_EL1
    and x1, x4, #0x7
    add x1, x1, #0x4            //cache line size

    ldr x3, =0x7FFF
    and x2, x3, x4, LSR #13     //num sets - 1

    ldr x3, =0x3FF
    and x3, x3, x4, lsr #3      //num ways - 1

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

tlb_init:
    ldr x1, =0x3520
    msr TCR_EL3, x1

    ldr x1, =0xff440400
    msr MAIR_EL3, x1

    adr x0, ttbr0_el3_base
    msr TTBR0_EL3, x0

    ret

cpu_boot:
    mrs x0, MPIDR_EL1
    and x0, x0, #0xFFFF
    cmp x0, #0x00
    beq cpu0_boot
    cmp x0, #0x01
    beq cpu1_boot
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
    mov x0, #2      //init level 2 cache
    bl cache_init

    b .

    mov x0, #0
    msr CSSELR_EL1, x0

    mrs x8, CCSIDR_EL1
    adr x1, output
    str x8, [x1]
    bl write_dword_to_stderr

    mov x0, #1
    msr CSSELR_EL1, x0

    mrs x8, CCSIDR_EL1
    adr x1, output
    str x8, [x1]
    bl write_dword_to_stderr

    mrs x8, CLIDR_EL1
    adr x1, output
    str x8, [x1]
    bl write_dword_to_stderr

    mrs x8, ID_AA64MMFR0_EL1
    adr x1, output
    str x8, [x1]
    bl write_dword_to_stderr

    bl tlb_init 
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
output:                     .dword 0xffffffff

.macro PUT_64B high, low
.word \low
.word \high
.endm

.macro TABLE_ENTRY PA, ATTR
PUT_64B \ATTR, (\PA) + 0x3
.endm

.macro BLOCK_1GB PA, ATTR_HI, ATTR_LO
PUT_64B \ATTR_HI, ((\PA) & 0xC0000000) | \ATTR_LO | 0x1
.endm

.macro BLOCK_2MB PA, ATTR_HI, ATTR_LO
PUT_64B \ATTR_HI, ((\PA) & 0xFFE00000) | \ATTR_LO | 0x1
.endm

.align 12
ttbr0_el3_base:
TABLE_ENTRY level2_pagetable, 0
BLOCK_1GB 0x40000000, 0, 0x740
BLOCK_1GB 0x80000000, 0, 0x740
BLOCK_1GB 0xC0000000, 0, 0x740

.align 12
level2_pagetable:
.set ADDR, 0x000
.rept 0x200
BLOCK_2MB (ADDR << 20), 0, 0x74C
.set ADDR, ADDR+2
.endr
.end
