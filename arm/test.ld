
ENTRY(_Reset)
SECTIONS
{
    . = 0x0;

    .text : {
        *(INTERRUPT_VECTOR)
        *(.text)
    }

    .data : {
        *(.data)
    }

    .bss : {
        *(.bss)
    }
}
