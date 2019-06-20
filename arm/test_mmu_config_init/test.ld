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

    stack_size = 0x1000;
    . = ALIGN(8);
    . = . + stack_size;
    stack_top_cpu0 = .;
    . = . + stack_size;
    stack_top_cpu1 = .;
    . = . + stack_size;
    stack_top_cpu2 = .;
    . = . + stack_size;
    stack_top_cpu3 = .;
}
