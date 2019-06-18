#!/usr/bin/python3

"""
Standard python import statements
"""
import unittest
import math
import sys
import textwrap
import subprocess
import os

class ARMTestUtil(unittest.TestCase):
    base_gcc_path    = os.path.expanduser('~/Downloads/gcc-arm-8.3-2019.03-x86_64-aarch64-elf/bin/')
    gcc_prefix   = 'aarch64-elf-'
    gcc_path     = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'gcc')
    ld_path      = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'ld')
    as_path      = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'as')
    objdump_path = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'objdump')
    nm_path      = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'nm')
    strip_path   = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'strip')

    base_qemu_path           = os.path.expanduser('~/Projects/qemu/qemu-install/bin/')
    qemu_aarch64_path        = '{}{}'.format(base_qemu_path, 'qemu-aarch64')
    qemu_system_aarch64_path = '{}{}'.format(base_qemu_path, 'qemu-system-aarch64')

class ARMInstructionTest(ARMTestUtil):

    def test_gnu_arm_assembly_strip_debug_symbols(self):
        return
        assembly_file_contents = '''
            .section INTERRUPT_VECTOR, "x"
            .global _Reset
            _Reset:
              B Reset_Handler /* Reset */
              B . /* Undefined */
              B . /* SWI */
              B . /* Prefetch Abort */
              B . /* Data Abort */
              B . /* reserved */
              B . /* IRQ */
              B . /* FIQ */

            Reset_Handler:
              movz x5, #0x1
              B .
        '''

        with open('test.s', 'w') as f:
            f.write(textwrap.dedent(assembly_file_contents))

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', 'test.s', '-o', 'test.o']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.objdump_path, '-t', 'test.o'])
        print(completed_process.stdout)

        completed_process = subprocess.run([self.strip_path, '-g', 'test.o'])
        print(completed_process.stdout)

        completed_process = subprocess.run([self.objdump_path, '-t', 'test.o'])
        print(completed_process.stdout)

    def test_gnu_arm_linker_simple_1(self):
        return
        assembly_file_contents = '''
            .section INTERRUPT_VECTOR, "x"
            .global _Reset
            _Reset:
              B Reset_Handler /* Reset */
              B . /* Undefined */
              B . /* SWI */
              B . /* Prefetch Abort */
              B . /* Data Abort */
              B . /* reserved */
              B . /* IRQ */
              B . /* FIQ */

            Reset_Handler:
              movz x5, #0x1
              B .
        '''

        linker_script_contents = '''
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

                . = ALIGN(8);
                . = . + 0x1000; /* 4kB of stack memory */
                stack_top = .;
            }
        '''

        with open('test.s', 'w') as f:
            f.write(textwrap.dedent(assembly_file_contents))

        with open('test.ld', 'w') as f:
            f.write(textwrap.dedent(linker_script_contents))

        # subprocess.run(self.gcc_path, '-c', '-mcpu=cortec-a53', 'g', 'test.c', '-o', 'test.o', '-march=armv8-a');
        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', 'test.s', '-o', 'test.o']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.strip_path, '-d', 'test.o'])
        print(completed_process.stdout)

        completed_process = subprocess.run([self.ld_path, '-M', '-print-memory-usage', '-T', 'test.ld', 'test.o', '-o', 'test.elf']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.objdump_path, '-t', '-d', 'test.elf'])
        print(completed_process.stdout)

    def test_qemu_ID_AA64PFR0_EL1(self):
        """
        Verify the contents of the ID_AA64PFR0_EL1 register report
        that all 4 exception levels are implemented.
        """
        return

        assembly_file_contents = '''
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

              mrs x0, ID_AA64PFR0_EL1
              adr x1, status
              str w0, [x1]
              mov w0, #0x18
              adr x1, code
              hlt #0xf000

             .data
             .balign 8

      code:   .dword 0x00020026
      status: .dword 0x00000000
            .end
        '''

        linker_script_contents = '''
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
        '''

        with open('test.s', 'w') as f:
            f.write(textwrap.dedent(assembly_file_contents))

        with open('test.ld', 'w') as f:
            f.write(textwrap.dedent(linker_script_contents))

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', 'test.s', '-o', 'test.o']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.ld_path, '-M', '-print-memory-usage', '-T', 'test.ld', 'test.o', '-o', 'test.elf']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.objdump_path, '-t', '-d', 'test.elf'])
        print(completed_process.stdout)

        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            'test.elf'],
                                           stdout=subprocess.PIPE)
        print(completed_process.stdout)
        print(completed_process.returncode)
        self.assertEqual(0x77, completed_process.returncode)

    def test_qemu_semihosting_test(self):
        """
        Verify that the assembly program can return values to the test via
        the ARM Angel semihosting API
        """
        return

        assembly_file_contents = '''
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

              mov w0, #0x18
              adr x1, code
              hlt #0xf000

             .data
             .balign 8
      code:   .dword 0x00020026
      status: .dword 0x77777777
            .end
        '''

        linker_script_contents = '''
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
        '''

        with open('test.s', 'w') as f:
            f.write(textwrap.dedent(assembly_file_contents))

        with open('test.ld', 'w') as f:
            f.write(textwrap.dedent(linker_script_contents))

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', 'test.s', '-o', 'test.o']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.ld_path, '-M', '-print-memory-usage', '-T', 'test.ld', 'test.o', '-o', 'test.elf']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            'test.elf'],
                                           stdout=subprocess.PIPE)
        print(completed_process.stdout)
        print(completed_process.returncode)
        self.assertEqual(0x77, completed_process.returncode)

    def test_qemu_semihosting__sys_writec_test(self):
        """
        Verify that the assembly program can write a byte to
        stderr
        """
        return

        assembly_file_contents = '''
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
        '''

        linker_script_contents = '''
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
        '''

        with open('test.s', 'w') as f:
            f.write(textwrap.dedent(assembly_file_contents))

        with open('test.ld', 'w') as f:
            f.write(textwrap.dedent(linker_script_contents))

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', 'test.s', '-o', 'test.o']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.ld_path, '-T', 'test.ld', 'test.o', '-o', 'test.elf']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            'test.elf'],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        print(completed_process.stdout)
        print('stderr is')
        print(completed_process.stderr)
        print(completed_process.returncode)
        self.assertEqual(0x77, completed_process.returncode)
        self.assertEqual(b'\x88', completed_process.stderr)

    def test_qemu_semihosting__multiple_sys_writec_test(self):
        """
        Verify that the assembly program can write multiple bytes to
        stderr using bl and ret instructions
        """
        return

        assembly_file_contents = '''
            .section INTERRUPT_VECTOR, "x"
            .global _Reset
            _Reset:
              B Reset_Handler /* Reset */

            write_byte_to_stderr:
              adr x1, output
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

              bl write_byte_to_stderr
              bl write_byte_to_stderr
              bl write_byte_to_stderr
              bl write_byte_to_stderr

              mov w0, #0x18
              adr x1, code
              hlt #0xf000

             .data
             .balign 8
      code:   .dword 0x00020026
      status: .dword 0x77777777
      output: .dword 0x88888888
            .end
        '''

        linker_script_contents = '''
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
        '''

        with open('test.s', 'w') as f:
            f.write(textwrap.dedent(assembly_file_contents))

        with open('test.ld', 'w') as f:
            f.write(textwrap.dedent(linker_script_contents))

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', 'test.s', '-o', 'test.o']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.ld_path, '-T', 'test.ld', 'test.o', '-o', 'test.elf']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            'test.elf'],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        print(completed_process.stdout)
        print('stderr is')
        print(completed_process.stderr)
        print(completed_process.returncode)
        self.assertEqual(0x77, completed_process.returncode)
        self.assertEqual(b'\x88\x88\x88\x88', completed_process.stderr)

    def test_qemu_semihosting__multiple_sys_writec_loop_test(self):
        """
        Verify that the assembly program can write multiple bytes to
        stderr using bl and ret instructions and a loop
        """
        return
        assembly_file_contents = '''
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
      output: .dword 0x11223344
            .end
        '''

        linker_script_contents = '''
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
        '''

        with open('test.s', 'w') as f:
            f.write(textwrap.dedent(assembly_file_contents))

        with open('test.ld', 'w') as f:
            f.write(textwrap.dedent(linker_script_contents))

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', 'test.s', '-o', 'test.o']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.ld_path, '-T', 'test.ld', 'test.o', '-o', 'test.elf']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            'test.elf'],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        print(completed_process.stdout)
        print('stderr is')
        print(completed_process.stderr)
        print(completed_process.returncode)
        self.assertEqual(0x77, completed_process.returncode)
        self.assertEqual(b'\x44\x33\x22\x11', completed_process.stderr)

    def test_qemu_initial_exception_level_test(self):
        """
        Verify the exception level immediately after reset
        is Exception Level 3
        """
        return

        assembly_file_contents = '''
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

              mrs x0, CurrentEL
              ubfx x0, x0,2,2
              adr x1, status
              str w0, [x1]
              mov w0, #0x18
              adr x1, code
              hlt #0xf000

             .data
             .balign 8
      code:   .dword 0x00020026
      status: .dword 0x00000000
            .end
        '''

        linker_script_contents = '''
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
        '''

        with open('test.s', 'w') as f:
            f.write(textwrap.dedent(assembly_file_contents))

        with open('test.ld', 'w') as f:
            f.write(textwrap.dedent(linker_script_contents))

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', 'test.s', '-o', 'test.o']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.strip_path, '-d', 'test.o'])
        print(completed_process.stdout)

        completed_process = subprocess.run([self.ld_path, '-M', '-print-memory-usage', '-T', 'test.ld', 'test.o', '-o', 'test.elf']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.objdump_path, '-t', '-d', 'test.elf'])
        print(completed_process.stdout)

        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            'test.elf'],
                                           stdout=subprocess.PIPE)
        print(completed_process.stdout)
        print(completed_process.returncode)
        self.assertEqual(3, completed_process.returncode)

    def test_multicore_message_passing(self):
        """
        Verify that multi core message can be achieved
        using load acquire and store release instructions
        """
        return
        assembly_file_contents = '''
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
      output: .dword 0x11223344
            .end
        '''

        linker_script_contents = '''
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
        '''

        with open('test.s', 'w') as f:
            f.write(textwrap.dedent(assembly_file_contents))

        with open('test.ld', 'w') as f:
            f.write(textwrap.dedent(linker_script_contents))

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', 'test.s', '-o', 'test.o']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.ld_path, '-T', 'test.ld', 'test.o', '-o', 'test.elf']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            'test.elf'],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        print(completed_process.stdout)
        print('stderr is')
        print(completed_process.stderr)
        print(completed_process.returncode)
        self.assertEqual(0x77, completed_process.returncode)
        self.assertEqual(b'\x44\x33\x22\x11', completed_process.stderr)

    def test_multicore_lock_critical_section(self):
        """
        Verify that a critical section mutex can be achieved using
        load and store exclusives.
        """

        assembly_file_contents = '''
            .section INTERRUPT_VECTOR, "x"
            .global _Reset
            _Reset:
              B Reset_Handler /* Reset */

            write_byte_to_stderr:
              mov w0, #0x03
              hlt #0xf000
              ret

            Reset_Handler:

              /* Acquire Lock */
            critical_section_loop:
              mov x0, #0x1
              adr x1, lock
              ldxr x5, [x1]
              cmp x5, #0
              bne critical_section_loop
              stxr w5, x0, [x1]
              cmp w5, #0
              bne critical_section_loop
              dmb sy

              /* Entered Critical Section */
              adr x1, output
              ldr x2, [x1]
              add x2, x2, #1
              str x2, [x1]

              /* Release Lock */
              adr x1, lock
              mov x0, #0
              dmb sy
              str x0, [x1]

              mrs x0, MPIDR_EL1
              and x0, x0, #0xFFFF
              cbz x0, boot

            sleep:
              wfi
              B sleep

            boot:
              adr x1, output
              ldr x0, [x1]
              sub x0, x0, #4
              cbz x0, done_waiting
              b boot

              done_waiting:

              /* Write data to output */
              mov x12, #0x4
              adr x1, output

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
      output: .dword 0x00000000
      lock:   .dword 0x00000000
            .end
        '''

        linker_script_contents = '''
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
        '''

        with open('test.s', 'w') as f:
            f.write(textwrap.dedent(assembly_file_contents))

        with open('test.ld', 'w') as f:
            f.write(textwrap.dedent(linker_script_contents))

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', 'test.s', '-o', 'test.o']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.ld_path, '-M', '-print-memory-usage', '-T', 'test.ld', 'test.o', '-o', 'test.elf']);
        print(completed_process.stdout)

        completed_process = subprocess.run([self.objdump_path, '-t', '-d', 'test.elf'])
        print(completed_process.stdout)

        for i in range(0, 100):
            completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                                '-semihosting',
                                                '-machine', 'raspi3',
                                                '-cpu', 'cortex-a53',
                                                '-nographic',
                                                '-kernel',
                                                'test.elf'],
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
            print(completed_process.stdout)
            print('stderr is')
            print(completed_process.stderr)
            print(completed_process.returncode)
            self.assertEqual(0x77, completed_process.returncode)
            self.assertEqual(b'\x04\x00\x00\x00', completed_process.stderr)

if __name__ == '__main__':
    unittest.main()
