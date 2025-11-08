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

class RegisterFieldOutOfBoundError(Exception):
    pass

class RegisterField(object):
    """
    Class that represents a register field
    """
    def __init__(self, name, width, shift, value, name_value_dict, conversion_function=None):
        self.name = name
        self.width = width
        self.shift = shift
        self.value = value
        self.name_value_dict = name_value_dict
        self.conversion_function = conversion_function

    def set_value(self, value):
        """
        Set register field value.

        Raises:
            RegisterFieldOutOfBoundError: if the value is larger than
            the width of the register field
        """
        if value > (pow(2, self.width) - 1):
            raise RegisterFieldOutOfBoundError

        self.value = value

    def get_value(self):
        """
        Returns the value of the register field.
        An optional conversion function is executed
        to modify the value before returning
        if given during construction
        """
        if self.conversion_function:
            return self.conversion_function(self.value)
        return self.value

    def get_name(self):
        """
        Return register field name

        Returns:
            A string which describes the register field
        """
        return self.name

    def get_value_name(self):
        """
        Returns the meaning of the current register field value

        Returns:
            A string which describes the current value of the
            register field
        """
        if not self.name_value_dict:
            return False
        return self.name_value_dict[self.value]

    def print(self):
        """
        Print the register field name and value
        to stdout
        """
        print(self.name, self.value, self.get_value_name())


class Register(object):
    """
    Class that represents a Register
    """
    def __init__(self, fields):
        """
        Initialize an instance of the Register class

        Args:
            fields - a dictionary of strings to RegisterFields, e.g.:
            {
                'field1' : RegisterField(...),
                'field2' : RegisterField(...)
            }
        """
        self.fields = fields

    def set_value(self, register_value):
        for field in self.fields:
            shift = self.fields[field].shift
            width = self.fields[field].width
            mask = pow(2, width) - 1
            field_value = (register_value & (mask << shift)) >> shift
            self.fields[field].set_value(field_value)

    def set_field(self, field, field_value):
        self.fields[field].set_value(field_value)

    def get_field(self, field):
        return self.fields[field].get_value()

    def get_field_name(self, field):
        return self.fields[field].get_name()

    def get_field_value_name(self, field):
        return self.fields[field].get_value_name()

    def print(self):
        for field in self.fields:
            self.fields[field].print()
