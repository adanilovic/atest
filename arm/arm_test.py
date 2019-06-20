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

class RegisterFieldOutOfBoundError(Exception):
    pass

class RegisterField(object):
    def __init__(self, width, value):
        self.width = width
        self.value = value

    def set_value(self, value):
        if value > (pow(2, self.width) - 1):
            raise RegisterFieldOutOfBoundError

        self.value = value

    def get_value(self):
        return self.value

class Register(object):
    def __init__(self, fields):
        self.fields = fields

class CLIDR_EL1(Register):
    def __init__(self):
        Register.__init__(self, {
            'ICB'    : RegisterField(width=3, value=0),
            'LoUU'   : RegisterField(width=3, value=0),
            'LoC'    : RegisterField(width=3, value=0),
            'LoUIS'  : RegisterField(width=3, value=0),
            'Ctype7' : RegisterField(width=3, value=0),
            'Ctype6' : RegisterField(width=3, value=0),
            'Ctype5' : RegisterField(width=3, value=0),
            'Ctype4' : RegisterField(width=3, value=0),
            'Ctype3' : RegisterField(width=3, value=0),
            'Ctype2' : RegisterField(width=3, value=0),
            'Ctype1' : RegisterField(width=3, value=0),
        })

    def set_value(self, field, value):
        self.fields[field].set_value(value)

    def get_value(self, field):
        return self.fields[field].get_value()

class RegisterTests(unittest.TestCase):
    def test_basic_register_get_set(self):
        clidr = CLIDR_EL1()
        self.assertEqual(0, clidr.get_value('ICB'))
        clidr.set_value('ICB', 3)
        self.assertEqual(3, clidr.get_value('ICB'))

    def test_basic_register_invalid_set(self):
        clidr = CLIDR_EL1()
        clidr.set_value('ICB', 7)
        self.assertEqual(7, clidr.get_value('ICB'))
        self.assertRaises(RegisterFieldOutOfBoundError, clidr.set_value, 'ICB', 8)
        self.assertEqual(7, clidr.get_value('ICB'))

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

        completed_process = subprocess.run([self.as_path, '-mcpu=cortex-a53', '-g', self.asm_source_file, '-o', self.obj_output_file]);
        completed_process = subprocess.run([self.objdump_path, '-t', self.obj_output_file])
        completed_process = subprocess.run([self.strip_path, '-g', self.obj_output_file])
        completed_process = subprocess.run([self.objdump_path, '-t', self.obj_output_file])
        #FIXME: Add assert statements

    def test_gnu_arm_linker_simple_1(self):

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

        cache_line_size = qemu_stderr[0:2]
        number_of_sets = qemu_stderr[2:4]
        number_of_ways = qemu_stderr[4:6]
        # number_of_caches =
        print(cache_line_size)
        print(number_of_sets)
        print(number_of_ways)
        #6 means cache line size of 64 bytes
        #0x7f means 128 sets
        #3 means 4 ways

        self.assertEqual('067f032300200a', qemu_stderr)

    def test_multicore_lock_critical_section(self):
        """
        Verify that a critical section mutex can be achieved using
        load and store exclusives.
        """
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

def load_tests(loader, standard_tests, pattern):
    test_cases = [ARMInstructionTest, RegisterTests]
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        loader.add_configurable_test(test_class)
        suite.addTests(tests)
    return suite

if __name__ == '__main__':
    unittest.main()
