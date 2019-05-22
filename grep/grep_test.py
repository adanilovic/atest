#!/usr/bin/python3

"""
Standard python import statements
"""
import unittest
import subprocess
import re

class GrepTest(unittest.TestCase):
    """
    Tests of the grep linux command line utility.
    """

    def test_grep_version(self):
        """
        Verify that the grep version output contains a version number with the expected format.
        """
        grep_version_output = subprocess.check_output(['grep', '--v'])
        self.assertEqual(type(grep_version_output), bytes)
        grep_version_output_string =  grep_version_output.decode()
        result = re.match('grep \(GNU grep\) [0-9].[0-9]', grep_version_output_string)
        self.assertNotEqual(result, None)

    def test_grep_version_short_long_are_equal(self):
        """
        Verify that the --v and --version arguments produce the same output.
        """
        grep_short_version_output = subprocess.check_output(['grep', '--v'])
        grep_long_version_output  = subprocess.check_output(['grep', '--version'])
        self.assertEqual(grep_short_version_output, grep_long_version_output)

if __name__ == '__main__':
    unittest.main()
