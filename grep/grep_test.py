#!/usr/bin/python3

"""
Standard python import statements
"""
import unittest
import subprocess
import re
import os

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
        grep_version_output_string = grep_version_output.decode()
        result = re.match(r'grep \(GNU grep\) [0-9].[0-9]', grep_version_output_string)
        self.assertNotEqual(result, None)

    def test_grep_version_short_long_are_equal(self):
        """
        Verify that the --v and --version arguments produce the same output.
        """
        grep_short_version_output = subprocess.check_output(['grep', '--v'])
        grep_long_version_output = subprocess.check_output(['grep', '--version'])
        self.assertEqual(grep_short_version_output, grep_long_version_output)

    def test_grep_finds_string(self):
        """
        Verify that the string is found.
        """
        current_file_dir = os.path.dirname(os.path.realpath(__file__))
        grep_results = subprocess.check_output(['grep',
                                                'findme',
                                                os.path.join(current_file_dir,
                                                             'file_to_search_in.txt')])
        self.assertEqual(grep_results, b'findme\n')

    def test_grep_count(self):
        """
        Verify -c output.
        """
        current_file_dir = os.path.dirname(os.path.realpath(__file__))
        grep_results = subprocess.check_output(['grep',
                                                '-c',
                                                'findme',
                                                os.path.join(current_file_dir,
                                                             'file_to_search_in.txt')])
        self.assertEqual(grep_results, b'1\n')

    def test_grep_files_with_matches(self):
        """
        Verify -l output.
        """
        current_file_dir = os.path.dirname(os.path.realpath(__file__))
        full_file_path_to_search = os.path.join(current_file_dir, 'file_to_search_in.txt')
        grep_results = subprocess.check_output(['grep', '-l', 'findme', full_file_path_to_search])
        self.assertEqual(grep_results, '{}\n'.format(full_file_path_to_search).encode())

    def test_grep_does_not_find_string(self):
        """
        Verify that grep does not find the given string.
        """
        self.assertRaises(subprocess.CalledProcessError,
                          subprocess.check_output,
                          ['grep',
                           'doesn\'t exist',
                           'file_to_search_in.txt'])

    def test_grep_recursive_search(self):
        """
        Verify that grep finds the expected string in a subdirectory.
        """
        current_file_dir = os.path.dirname(os.path.realpath(__file__))
        sub_dir_to_search = os.path.join(current_file_dir, 'sub_dir')
        grep_results = subprocess.check_output(['grep', '-r', 'findmesubdir1', sub_dir_to_search])
        expected_file_match = os.path.join(sub_dir_to_search,
                                           'sub_dir1',
                                           'file_to_search_in_sub_dir1.txt')
        expected_results = '{}:{}\n'.format(expected_file_match, 'findmesubdir1').encode()
        self.assertEqual(grep_results, expected_results)

    def test_grep_recursive_regex_search(self):
        """
        Verify that grep finds the expected string in a subdirectory using a regex.
        """
        current_file_dir = os.path.dirname(os.path.realpath(__file__))
        sub_dir_to_search = os.path.join(current_file_dir, 'sub_dir')
        grep_results = subprocess.check_output(['grep',
                                                '-r',
                                                '-G',
                                                'findmesubdir',
                                                sub_dir_to_search])
        self.assertEqual(True, 'findmesubdir1' in grep_results.decode())
        self.assertEqual(True, 'findmesubdir2' in grep_results.decode())
        self.assertEqual(True, 'findmesubdir3' in grep_results.decode())

    def test_grep_recursive_regex_exclude_one_dir_search(self):
        """
        Verify that grep finds the expected string in a subdirectory using a regex.
        """
        current_file_dir = os.path.dirname(os.path.realpath(__file__))
        sub_dir_to_search = os.path.join(current_file_dir, 'sub_dir')
        grep_results = subprocess.check_output(['grep',
                                                '-r',
                                                '-G',
                                                '--exclude-dir=sub_dir2',
                                                'findmesubdir', sub_dir_to_search])
        self.assertEqual(True, 'findmesubdir1' in grep_results.decode())
        self.assertEqual(False, 'findmesubdir2' in grep_results.decode())
        self.assertEqual(True, 'findmesubdir3' in grep_results.decode())

    def test_grep_recursive_regex_exclude_two_dir_search(self):
        """
        Verify that grep finds the expected string in a subdirectory using a regex.
        """
        current_file_dir = os.path.dirname(os.path.realpath(__file__))
        sub_dir_to_search = os.path.join(current_file_dir, 'sub_dir')
        grep_results = subprocess.check_output(['grep',
                                                '-r',
                                                '-G',
                                                '--exclude-dir=sub_dir2',
                                                '--exclude-dir=sub_dir3',
                                                'findmesubdir', sub_dir_to_search])
        self.assertEqual(True, 'findmesubdir1' in grep_results.decode())
        self.assertEqual(False, 'findmesubdir2' in grep_results.decode())
        self.assertEqual(False, 'findmesubdir3' in grep_results.decode())

if __name__ == '__main__':
    unittest.main()
