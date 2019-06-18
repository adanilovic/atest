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
        print('list of configurable test suites:')
        print(self.list_of_configurable_tests)

    def send_config_data(self):
        for test_case in self.list_of_configurable_tests:
            test_case.config_data = test_configuration_data

def create_test_base_output_dir():
    output_dir = test_configuration_data['base_output_dir']
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

if __name__ == '__main__':
    """
    Run all unit tests in all subdirectories
    """
    create_test_base_output_dir()
    loader = ConfigurableTestLoader()
    test_suites = loader.discover('.', pattern='*test.py')
    loader.print_configurable_tests()
    loader.send_config_data()
    print(test_suites)
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suites)
