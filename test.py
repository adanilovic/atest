#!/usr/bin/python3

import unittest

import grep

if __name__ == '__main__':
    test_suites = unittest.defaultTestLoader.discover('.', pattern='*test.py')
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suites)
