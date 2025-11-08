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

class RegisterFieldTest(unittest.TestCase):
    def test_set_get_value(self):
        field = RegisterField(name='field',
                              width=3,
                              shift=0,
                              value=7,
                              name_value_dict={})
        self.assertEqual(7, field.get_value())
        field.set_value(1)
        self.assertEqual(1, field.get_value())

    def test_set_value_out_of_range(self):
        field = RegisterField(name='field',
                              width=3,
                              shift=0,
                              value=7,
                              name_value_dict={})
        self.assertRaises(RegisterFieldOutOfBoundError,
                          field.set_value, 8)

    def test_set_get_name(self):
        field = RegisterField(name='field',
                              width=3,
                              shift=0,
                              value=7,
                              name_value_dict={})

        self.assertEqual('field', field.get_name())

    def test_set_get_value_name(self):
        field = RegisterField(name='field',
                              width=3,
                              shift=0,
                              value=7,
                              name_value_dict={})

        self.assertEqual(False, field.get_value_name())

        field = RegisterField(name='field',
                              width=3,
                              shift=0,
                              value=7,
                              name_value_dict={7:'7'})

        self.assertEqual('7', field.get_value_name())

class RegisterTest(unittest.TestCase):
    def test_register_get_field(self):
        fields = {'field1' : RegisterField(name='field1',
                              width=3,
                              shift=0,
                              value=6,
                              name_value_dict={}),
                  'field2': RegisterField(name='field2',
                              width=3,
                              shift=0,
                              value=7,
                              name_value_dict={})}

        reg = Register(fields)
        self.assertEqual(6, reg.get_field('field1'))
        self.assertEqual(7, reg.get_field('field2'))

if __name__ == '__main__':
    unittest.main()
