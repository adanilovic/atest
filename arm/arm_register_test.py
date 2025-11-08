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

class ARMRegisterTests(unittest.TestCase):
    def test_basic_register_get_set(self):
        clidr = CLIDR_EL1()
        self.assertEqual(0, clidr.get_field('ICB'))
        clidr.set_field('ICB', 3)
        self.assertEqual(3, clidr.get_field('ICB'))

    def test_basic_register_invalid_set(self):
        clidr = CLIDR_EL1()
        clidr.set_field('ICB', 7)
        self.assertEqual(7, clidr.get_field('ICB'))
        self.assertRaises(RegisterFieldOutOfBoundError, clidr.set_field, 'ICB', 8)
        self.assertEqual(7, clidr.get_field('ICB'))

    def test_get_field_name(self):
        clidr = CLIDR_EL1()
        self.assertEqual('Cache Type 1', clidr.get_field_name('Ctype1'))
        self.assertEqual('Cache Type 2', clidr.get_field_name('Ctype2'))
        self.assertEqual('Cache Type 3', clidr.get_field_name('Ctype3'))
        self.assertEqual('Cache Type 4', clidr.get_field_name('Ctype4'))
        self.assertEqual('Cache Type 5', clidr.get_field_name('Ctype5'))
        self.assertEqual('Cache Type 6', clidr.get_field_name('Ctype6'))
        self.assertEqual('Cache Type 7', clidr.get_field_name('Ctype7'))
        self.assertEqual('Level of Unfication Inner Shareable', clidr.get_field_name('LoUIS'))
        self.assertEqual('Level of Coherence', clidr.get_field_name('LoC'))
        self.assertEqual('Level of Unification Uniprocessor', clidr.get_field_name('LoUU'))
        self.assertEqual('Inner Cache Boundary', clidr.get_field_name('ICB'))

    def test_set_value_get_individual_field(self):
        clidr = CLIDR_EL1()
        self.assertEqual(0, clidr.get_field('Ctype1'))
        self.assertEqual(0, clidr.get_field('Ctype2'))
        self.assertEqual(0, clidr.get_field('Ctype3'))
        self.assertEqual(0, clidr.get_field('Ctype4'))
        self.assertEqual(0, clidr.get_field('Ctype5'))
        self.assertEqual(0, clidr.get_field('Ctype6'))
        self.assertEqual(0, clidr.get_field('Ctype7'))
        self.assertEqual(0, clidr.get_field('LoUIS'))
        self.assertEqual(0, clidr.get_field('LoC'))
        self.assertEqual(0, clidr.get_field('LoUU'))
        self.assertEqual(0, clidr.get_field('ICB'))

        clidr.set_value(0x49249249)
        self.assertEqual(1, clidr.get_field('Ctype1'))
        self.assertEqual(1, clidr.get_field('Ctype2'))
        self.assertEqual(1, clidr.get_field('Ctype3'))
        self.assertEqual(1, clidr.get_field('Ctype4'))
        self.assertEqual(1, clidr.get_field('Ctype5'))
        self.assertEqual(1, clidr.get_field('Ctype6'))
        self.assertEqual(1, clidr.get_field('Ctype7'))
        self.assertEqual(1, clidr.get_field('LoUIS'))
        self.assertEqual(1, clidr.get_field('LoC'))
        self.assertEqual(1, clidr.get_field('LoUU'))
        self.assertEqual(1, clidr.get_field('ICB'))

        clidr.set_value(0x0a200023)
        self.assertEqual(3, clidr.get_field('Ctype1'))
        self.assertEqual(4, clidr.get_field('Ctype2'))
        self.assertEqual(0, clidr.get_field('Ctype3'))
        self.assertEqual(0, clidr.get_field('Ctype4'))
        self.assertEqual(0, clidr.get_field('Ctype5'))
        self.assertEqual(0, clidr.get_field('Ctype6'))
        self.assertEqual(0, clidr.get_field('Ctype7'))
        self.assertEqual(1, clidr.get_field('LoUIS'))
        self.assertEqual(2, clidr.get_field('LoC'))
        self.assertEqual(1, clidr.get_field('LoUU'))
        self.assertEqual(0, clidr.get_field('ICB'))

        self.assertEqual('Separate instruction and data caches', clidr.get_field_value_name('Ctype1'))
        self.assertEqual('Unified cache', clidr.get_field_value_name('Ctype2'))
        self.assertEqual('No cache', clidr.get_field_value_name('Ctype3'))
        self.assertEqual('No cache', clidr.get_field_value_name('Ctype4'))
        self.assertEqual('No cache', clidr.get_field_value_name('Ctype5'))
        self.assertEqual('No cache', clidr.get_field_value_name('Ctype6'))
        self.assertEqual('No cache', clidr.get_field_value_name('Ctype7'))
        self.assertEqual(False, clidr.get_field_value_name('LoUIS'))
        self.assertEqual(False, clidr.get_field_value_name('LoC'))
        self.assertEqual(False, clidr.get_field_value_name('LoUU'))
        self.assertEqual('Not disclosed by this mechanism', clidr.get_field_value_name('ICB'))

class CCSIDR_tests(unittest.TestCase):
    def test_calc_cache_line_size(self):
        ccsidr = CCSIDR_EL1()
        self.assertEqual(16,  ccsidr.calc_cache_line_size_from_register_value(0))
        self.assertEqual(32,  ccsidr.calc_cache_line_size_from_register_value(1))
        self.assertEqual(64,  ccsidr.calc_cache_line_size_from_register_value(2))
        self.assertEqual(128, ccsidr.calc_cache_line_size_from_register_value(3))
