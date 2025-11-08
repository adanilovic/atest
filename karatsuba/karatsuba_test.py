#!/usr/bin/python3

"""
Standard python import statements
"""
import unittest
import math
import sys

def is_multiple_of_2(x):
    """
    Returns True if x is an even multiple of 2, False otherwise
    """
    return (x % 2 == 0)

def is_power_of_2(x):
    """
    Returns True if x is a power of 2, False otherwise
    """
    assert(x > 0)
    return (x & (x - 1) == 0)

def lengthen(x, length_to_extend_to):
    """
    Multiply x by 10 until its length is equal to
    length_to_extend_to.

    Returns:
        A list with 2 elements:
            1. The new value of x as a string
            2. How much the length of x increased by
    """
    assert(type(x) == str)
    length_of_x = len(x)
    assert(length_of_x <= length_to_extend_to)
    new_x_length = length_of_x
    x_multiplicand = 1
    while new_x_length != length_to_extend_to:
        new_x_length = new_x_length + 1
        x_multiplicand = x_multiplicand * 10

    return [str(int(x) * x_multiplicand), new_x_length - length_of_x]

def increase_to_next_power_of_2(x):
    """
    Increment x until it is a power of 2

    Returns:
        The incremented value of x, now a power of 2
    """
    new_x = x
    while(is_power_of_2(new_x) is False):
        new_x = new_x + 1

    return new_x

def _karatsuba(x, y):
    assert(type(x) == str)
    assert(type(y) == str)

    length_of_x = len(x)
    length_of_y = len(y)

    assert(length_of_x == length_of_y)
    # print(length_of_x)
    # print(length_of_y)

    result = 0

    if((length_of_x == 1) or (length_of_y == 1)):
        result = int(x) * int(y)
        print('result = ', result, '\n')
    else:

        max_length = max(length_of_x, length_of_y)
        max_length = increase_to_next_power_of_2(max_length)
        print('max_length = ', max_length)

        [x, x_multiplicand] = lengthen(x, max_length)
        [y, y_multiplicand] = lengthen(y, max_length)

        x_multiplicand = x_multiplicand * 10
        y_multiplicand = y_multiplicand * 10

        if x_multiplicand == 0:
            x_multiplicand = 1

        if y_multiplicand == 0:
            y_multiplicand = 1

        print('new x 1 = ', x)
        print('new y 1 = ', y)

        # m = min(new_x_length, new_y_length)
        m = max_length
        m2 = int(math.floor(int(m)/2))

        print('m2 = ', m2)

        a = x[ : m2]
        b = x[   m2 : ]

        c = y[ : m2]
        d = y[   m2 : ]

        print('a = ', a)
        print('b = ', b)
        print('c = ', c)
        print('d = ', d)

        a_c = _karatsuba(a, c)
        a_d = _karatsuba(a, d)
        b_c = _karatsuba(b, c)
        b_d = _karatsuba(b, d)
        print('\na_c = ', a_c)
        print('a_d = ',   a_d)
        print('b_c = ',   b_c)
        print('b_d = ',   b_d)

        # first_term = math.pow(10, m2 * 2) * int(a_c)
        first_term = int(karatsuba(str(int(math.pow(10, m2 * 2))), a_c))
        print('first_term = ', first_term, ', m2 = ', m2)
        second_term = math.pow(10, m2) * (int(a_d) + int(b_c))
        print('second_term = ', second_term, ', m2 = ', m2)
        result = first_term + second_term + int(b_d)
        print('result = ', result, ', m2 = ', m2)

        result = int(int(result) / (x_multiplicand * y_multiplicand))

    return str(result)

def karatsuba(x, y):

    assert(type(x) == str)
    assert(type(y) == str)

    length_of_x = len(x)
    length_of_y = len(y)

    max_length = max(length_of_x, length_of_y)
    max_length = increase_to_next_power_of_2(max_length)
    print('max_length = ', max_length)

    [x, x_multiplicand] = lengthen(x, max_length)
    [y, y_multiplicand] = lengthen(y, max_length)

    x_multiplicand = x_multiplicand * 10
    y_multiplicand = y_multiplicand * 10

    if x_multiplicand == 0:
        x_multiplicand = 1

    if y_multiplicand == 0:
        y_multiplicand = 1

    print('new x 2 = ', x, ', x_multiplicand = ', x_multiplicand)
    print('new y 2 = ', y, ', y_multiplicand = ', y_multiplicand)

    result = _karatsuba(x, y)
    result = int(int(result) / (x_multiplicand * y_multiplicand))
    return str(result)

class KaratsubaTest(unittest.TestCase):
    """
    Tests of the karatsuba integer multiplication algorithm.
    """

    # def test_is_multiple_of_2(self):
        # self.assertEqual(True, is_multiple_of_2(2))
        # self.assertEqual(False, is_multiple_of_2(3))
        # self.assertEqual(True, is_multiple_of_2(4))
        # self.assertEqual(True, is_multiple_of_2(6))
        # self.assertEqual(True, is_multiple_of_2(8))
        # self.assertEqual(True, is_multiple_of_2(10))
        # self.assertEqual(False, is_multiple_of_2(11))
        # self.assertEqual(True, is_multiple_of_2(100000))

    # def test_lengthen(self):
        # self.assertEqual(['1',   0],   lengthen('1', 1))
        # self.assertEqual(['10',  1],  lengthen('1', 2))
        # self.assertEqual(['100', 2], lengthen('1', 3))
        # self.assertEqual(['123', 0], lengthen('123', 3))

    # def test_is_power_of_2(self):
        # self.assertEqual(True,  is_power_of_2(1))
        # self.assertEqual(True,  is_power_of_2(2))
        # self.assertEqual(False, is_power_of_2(3))
        # self.assertEqual(True,  is_power_of_2(4))
        # self.assertEqual(False, is_power_of_2(5))
        # self.assertEqual(False, is_power_of_2(6))
        # self.assertEqual(False, is_power_of_2(7))
        # self.assertEqual(True,  is_power_of_2(8))
        # self.assertEqual(True,  is_power_of_2(16))
        # self.assertEqual(False, is_power_of_2(17))
        # self.assertEqual(True,  is_power_of_2(32))
        # self.assertEqual(True,  is_power_of_2(64))
        # self.assertEqual(False, is_power_of_2(65))

    # def test_increase_to_next_power_of_2(self):
        # self.assertEqual(1, increase_to_next_power_of_2(1))
        # self.assertEqual(2, increase_to_next_power_of_2(2))
        # self.assertEqual(4, increase_to_next_power_of_2(3))
        # self.assertEqual(4, increase_to_next_power_of_2(4))
        # self.assertEqual(8, increase_to_next_power_of_2(5))
        # self.assertEqual(8, increase_to_next_power_of_2(6))
        # self.assertEqual(8, increase_to_next_power_of_2(7))
        # self.assertEqual(8, increase_to_next_power_of_2(8))

    # def test_karatsuba_small_1(self):
        # self.assertEqual('1', karatsuba('1', '1'))

    def test_karatsuba_small_1(self):
        self.assertEqual('100', karatsuba('10', '10'))

    # def test_karatsuba_small_2(self):
        # self.assertEqual('4', karatsuba('2', '2'))

    # def test_karatsuba_medium_1(self):
        # self.assertEqual('408', karatsuba('12', '34'))

    # def test_karatsuba_medium_2(self):
        # self.assertEqual('56088', karatsuba('123', '456'))

    # def test_karatsuba_medium_3(self):
        # self.assertEqual('5635678', karatsuba('1234', '4567'))

    # def test_karatsuba_medium_4(self):
        # self.assertEqual('152415765279684', karatsuba('12345678', '12345678'))

    # def test_karatsuba_large(self):
        # operand1 = '3141592653589793238462643383279502884197169399375105820974944592'
        # operand2 = '2718281828459045235360287471352662497757247093699959574966967627'
        # expected_result = '8539734222673567065463550869546574495034888535765114961879601127067743044893204848617875072216249073013374895871952806582723184'
        # self.assertEqual(expected_result, karatsuba(operand1, operand2))

if __name__ == '__main__':
    unittest.main()
