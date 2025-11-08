#!/usr/bin/python3

"""
Standard python import statements
"""
import unittest
import os

test_configuration_data = {
    'base_dir' : os.path.dirname(os.path.realpath(__file__)),
    'base_output_dir' : os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build')
}

class ConfigurableTestLoader(unittest.TestLoader):
    def __init__(self):
        super(ConfigurableTestLoader, self).__init__()
        self.list_of_configurable_tests = []

    def add_configurable_test(self, test):
        self.list_of_configurable_tests.append(test)

    def print_configurable_tests(self):
        print('Configurable Tests:')
        for test in self.list_of_configurable_tests:
            print('\t', test)

    def send_config_data(self):
        for test_case in self.list_of_configurable_tests:
            test_case.config_data = test_configuration_data

def create_test_base_output_dir():
    output_dir = test_configuration_data['base_output_dir']
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def print_test_names(test_suite):
    count = 0
    print('Tests:')
    for suite in test_suites._tests:
        for test in suite:
            try:
                for subtest in test:
                    print('\t Test Num:', count, ', Test Name:', subtest)
                    count = count + 1
            except TypeError:
                print('\t Test Num:', count, ', Test Name:', test)
                count = count + 1

if __name__ == '__main__':
    """
    Run all unit tests in all subdirectories
    """
    create_test_base_output_dir()
    loader = ConfigurableTestLoader()
    test_suites = loader.discover('.', pattern='*test.py')
    print_test_names(test_suites)
    loader.print_configurable_tests()
    loader.send_config_data()
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suites)
