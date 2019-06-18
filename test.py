#!/usr/bin/ython3

"""
Standard python import statements
"""
import unittest

if __name__ == '__main__':
    """
    Run all unit tests in all subdirectories
    """
    test_suites = unittest.defaultTestLoader.discover('.', pattern='*test.py')
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suites)
