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
import struct

"""
Custom python import statements
"""
from arm.register import *
from arm.arm_register import *

class OutputTestCase(unittest.TestCase):
    #FIXME: Move to common unittest infrastructure module
    def setUp(self):
        self.addl_setUp()

    def create_output_dir(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def addl_setUp(self):
        pass

class ARMTestUtil(OutputTestCase):
    #FIXME: Move to top level configuration dictionary
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

    base_linux_gcc_path    = os.path.expanduser('~/Downloads/gcc-arm-8.3-2019.03-x86_64-aarch64_be-linux-gnu/bin/')
    gcc_linux_prefix   = 'aarch64_be-linux-gnu-'
    gcc_linux_path     = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'gcc')
    ld_linux_path      = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'ld')
    as_linux_path      = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'as')
    objdump_linux_path = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'objdump')
    nm_linux_path      = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'nm')
    strip_linux_path   = '{}{}{}'.format(base_gcc_path, gcc_prefix, 'strip')

class ARMInstructionTest(ARMTestUtil):

    @property
    def this_dir(self):
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def output_dir(self):
        """
        Compute difference between base output dir and this dir to place
        all output files in unique output dir
        """
        rel_path = os.path.relpath(os.path.realpath(__file__), start=self.config_data['base_dir'])
        split_rel_path = os.path.splitext(rel_path)
        return os.path.join(self.config_data['base_output_dir'], split_rel_path[0], self._testMethodName)

    @property
    def asm_source_file(self):
        return os.path.join(self.this_dir, self._testMethodName, 'test.asm')

    @property
    def c_source_file(self):
        return os.path.join(self.this_dir, self._testMethodName, 'test.c')

    @property
    def linker_source_file(self):
        return os.path.join(self.this_dir, self._testMethodName, 'test.ld')

    @property
    def obj_output_file(self):
        return os.path.join(self.output_dir, 'test.o')

    @property
    def elf_output_file(self):
        return os.path.join(self.output_dir, 'test.elf')

    def addl_setUp(self):
        self.create_output_dir(self.output_dir)

    def test_gnu_arm_assembly_strip_debug_symbols(self):

        return
        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.objdump_path, '-t', self.obj_output_file])
        completed_process = subprocess.run([self.strip_path, '-g', self.obj_output_file])
        completed_process = subprocess.run([self.objdump_path, '-t', self.obj_output_file])
        #FIXME: Add assert statements

    def test_gnu_arm_linker_simple_1(self):

        return
        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.strip_path, '-d', self.obj_output_file])
        completed_process = subprocess.run([self.ld_path, '-M', '-print-memory-usage', '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.objdump_path, '-t', '-d', self.elf_output_file])
        #FIXME: Add assert statements

    def test_qemu_ID_AA64PFR0_EL1(self):
        """
        Verify the contents of the ID_AA64PFR0_EL1 register report
        that all 4 exception levels are implemented.
        """
        return  #FIXME: Currently failing due to qemu returning 0x22, meaning only EL0 and EL1 implemented
        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.ld_path, '-M', '-print-memory-usage', '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.objdump_path, '-t', '-d', self.elf_output_file])
        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            self.elf_output_file],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        print(completed_process.stdout)
        print(completed_process.stderr)
        print(completed_process.returncode)
        self.assertEqual(0x2222, completed_process.returncode)

    def test_qemu_semihosting_test(self):
        """
        Verify that the assembly program can return values to the test via
        the ARM Angel semihosting API
        """
        return

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.ld_path, '-M', '-print-memory-usage', '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            self.elf_output_file],
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

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.ld_path, '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            self.elf_output_file],
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

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.ld_path, '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            self.elf_output_file],
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

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.ld_path, '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            self.elf_output_file],
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

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.strip_path, '-d', 'test.o'])
        completed_process = subprocess.run([self.ld_path, '-M', '-print-memory-usage', '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.objdump_path, '-t', '-d', self.elf_output_file])
        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            self.elf_output_file],
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

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.ld_path, '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            self.elf_output_file],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        print(completed_process.stdout)
        print('stderr is')
        print(completed_process.stderr)
        print(completed_process.returncode)
        self.assertEqual(0x77, completed_process.returncode)
        self.assertEqual(b'\x44\x33\x22\x11', completed_process.stderr)

    def test_rvbaraddr(self):
        """
        Verify the value of the rvbaraddr register
        """
        return

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.ld_path, '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.objdump_path, '-t', '-d', self.elf_output_file])
        print(completed_process.stdout)
        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            self.elf_output_file],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        print('stdout is')
        print(completed_process.stdout)
        print('stderr is')
        print(completed_process.stderr)
        print('returncode is')
        print(completed_process.returncode)
        self.assertEqual(0x77, completed_process.returncode)
        self.assertEqual(b'\x00\x00\x00\x00', completed_process.stderr)

    def test_mmu_config_init(self):
        """
        Initialize the mmu
        """
        return
        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.ld_path, '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.objdump_path, '-t', '-d', self.elf_output_file])
        print(completed_process.stdout)
        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            self.elf_output_file],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        print('stdout is')
        print(completed_process.stdout)
        print('stderr is')
        qemu_stderr = completed_process.stderr.hex()
        print(qemu_stderr)
        print('returncode is')
        print(completed_process.returncode)
        self.assertEqual(0x77, completed_process.returncode)
        self.assertEqual('1ae00f700ae01f202300200a22110000', qemu_stderr)

        swapped = struct.unpack('>i', struct.pack('<i', int(qemu_stderr[0:8], 16)))
        print('ccsidr for cache level 1 is', '{:#010x}'.format(swapped[0]))
        ccsidr = CCSIDR_EL1()
        ccsidr.set_value(swapped[0])
        print('Cache Level 1 Line Size is', ccsidr.get_field('LineSize'), 'Bytes')
        print('Cache Level 1 Associativity is', ccsidr.get_field('Associativity'))
        print('Cache Level 1 Number of Sets is', ccsidr.get_field('NumSets'))
        print('Cache Level 1 size is', ccsidr.cache_size(), 'Bytes')
        self.assertEqual(64, ccsidr.get_field('LineSize'))
        self.assertEqual(4, ccsidr.get_field('Associativity'))
        self.assertEqual(128, ccsidr.get_field('NumSets'))
        self.assertEqual(32768, ccsidr.cache_size())

        swapped = struct.unpack('>i', struct.pack('<i', int(qemu_stderr[8:16], 16)))
        print('ccsidr for cache level 2 is', '{:#010x}'.format(swapped[0]))
        ccsidr = CCSIDR_EL1()
        ccsidr.set_value(swapped[0])
        print('Cache Level 2 Line Size is', ccsidr.get_field('LineSize'), 'Bytes')
        print('Cache Level 2 Associativity is', ccsidr.get_field('Associativity'))
        print('Cache Level 2 Number of Sets is', ccsidr.get_field('NumSets'))
        print('Cache Level 2 size is', ccsidr.cache_size(), 'Bytes')
        self.assertEqual(64, ccsidr.get_field('LineSize'))
        self.assertEqual(2, ccsidr.get_field('Associativity'))
        self.assertEqual(256, ccsidr.get_field('NumSets'))
        self.assertEqual(32768, ccsidr.cache_size())

        swapped = struct.unpack('>i', struct.pack('<i', int(qemu_stderr[16:24], 16)))
        print('clidr is', '{:#010x}'.format(swapped[0]))
        clidr = CLIDR_EL1()
        clidr.set_value(swapped[0])
        print('Cache Level 1 has', clidr.get_field_value_name('Ctype1'))
        print('Cache Level 2 has a', clidr.get_field_value_name('Ctype2'))
        print('LoUIS is', clidr.get_field('LoUIS'))
        print('LoC is', clidr.get_field('LoC'))
        print('LoUU is', clidr.get_field('LoUU'))
        print('ICB is', clidr.get_field_value_name('ICB'))

        swapped = struct.unpack('>i', struct.pack('<i', int(qemu_stderr[24:32], 16)))
        print('id_aa64mmfr0_el1 is', '{:#010x}'.format(swapped[0]))
        id_aa64mmfr0_el1 = ID_AA64MMFR0_EL1()
        id_aa64mmfr0_el1.set_value(swapped[0])
        print('QEMU Raspi3 suports', id_aa64mmfr0_el1.get_field_value_name('PARange'), 'of Physical Memory')
        print('QEMU Raspi3 suports', id_aa64mmfr0_el1.get_field_value_name('ASIDBits'), 'of ASID')
        print('QEMU Raspi3 has', id_aa64mmfr0_el1.get_field_value_name('BigEnd'))
        print('QEMU Raspi3', id_aa64mmfr0_el1.get_field_value_name('SNSMem'))
        print('QEMU Raspi3 has', id_aa64mmfr0_el1.get_field_value_name('BigEndEL0'))
        print('QEMU Raspi3 has', id_aa64mmfr0_el1.get_field_value_name('TGran16'))
        print('QEMU Raspi3 has', id_aa64mmfr0_el1.get_field_value_name('TGran64'))
        print('QEMU Raspi3 has', id_aa64mmfr0_el1.get_field_value_name('TGran4'))

        ccsidr.print()
        clidr.print()
        id_aa64mmfr0_el1.print()

        #TODO: Once TLB's and MMU's are initialized, use an Address Translation
        #instruction to query the translation for a specific address, to verify
        #that they were initialized correctly. The result (the PA) will be in the
        #PAR_EL1 register.

        #TODO: For a Virtual Address, the top 16 bits must be all 0s or 1s,
        #otherwise the address triggers a fault.

    def test_multicore_lock_critical_section(self):
        """
        Verify that a critical section mutex can be achieved using
        load and store exclusives.
        """

        return
        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.ld_path, '-M', '-print-memory-usage', '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.objdump_path, '-t', '-d', self.elf_output_file])

        for i in range(0, 100):
            completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                                '-semihosting',
                                                '-machine', 'raspi3',
                                                '-cpu', 'cortex-a53',
                                                '-nographic',
                                                '-kernel',
                                                self.elf_output_file],
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
            print(completed_process.stdout)
            print('stderr is')
            print(completed_process.stderr)
            print(completed_process.returncode)
            self.assertEqual(0x77, completed_process.returncode)
            self.assertEqual(b'\x04\x00\x00\x00', completed_process.stderr)

    def test_pre_post_increment(self):
        return
        completed_process = subprocess.run([self.gcc_linux_path, '-nostartfiles', '-nodefaultlibs', '-nostdlib', self.c_source_file,
                                            '-o', self.elf_output_file],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE);
        print(completed_process)

        completed_process = subprocess.run([self.objdump_linux_path, '-t', '-d', self.elf_output_file])
        print(completed_process.stdout)

    def test_set_bit(self):
        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.ld_path, '-M', '-print-memory-usage', '-T', self.linker_source_file, self.obj_output_file, '-o', self.elf_output_file]);
        completed_process = subprocess.run([self.objdump_path, '-t', '-d', self.elf_output_file])
        completed_process = subprocess.run([self.qemu_system_aarch64_path,
                                            '-semihosting',
                                            '-machine', 'raspi3',
                                            '-cpu', 'cortex-a53',
                                            '-nographic',
                                            '-kernel',
                                            self.elf_output_file],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           input=b'\x77')
        print(completed_process.stdout)
        print('stderr is')
        print(completed_process.stderr)
        print(completed_process.returncode)
        self.assertEqual(b'\xab\xcd\xef\x12', completed_process.stderr)

def load_tests(loader, standard_tests, pattern):
    test_cases = [ARMInstructionTest]
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        loader.add_configurable_test(test_class)
        suite.addTests(tests)
    return suite

if __name__ == '__main__':
    unittest.main()
