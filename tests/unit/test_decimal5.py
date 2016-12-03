# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0

import unittest
import _test_aids

from _src import sb1288
from sb1288 import decimal5

ONECK = 100000
D5 = decimal5.Decimal5
D5TOTAL = decimal5.Decimal5Total

def test_compare(test_case, x, y, comparison):
  """Test all order comparisons for a pair of values"""
  test_case.assertEqual(x.__lt__(y), comparison < 0)
  test_case.assertEqual(x < y, comparison < 0)
  test_case.assertEqual(x.__le__(y), comparison <= 0)
  test_case.assertEqual(x <= y, comparison <= 0)
  test_case.assertEqual(x.__eq__(y), comparison == 0)
  test_case.assertEqual(x == y, comparison == 0)
  test_case.assertEqual(x.__ne__(y), comparison != 0)
  test_case.assertEqual(x != y, comparison != 0)
  test_case.assertEqual(x.__ge__(y), comparison >= 0)
  test_case.assertEqual(x >= y, comparison >= 0)
  test_case.assertEqual(x.__gt__(y), comparison > 0)
  test_case.assertEqual(x > y, comparison > 0)

class TestBasicDecimal5(unittest.TestCase):
  """Test basic Decimal5"""

  def test_decimal5_creation_with_ints(self):
    self.assertEqual(D5()._get_value(), 0)
    self.assertEqual(D5(1)._get_value(), 1 * ONECK)
    self.assertEqual(D5(2)._get_value(), 2 * ONECK)
    self.assertEqual(D5(-1)._get_value(), -1 * ONECK)
    self.assertEqual(D5(10)._get_value(), 10 * ONECK)
    self.assertEqual(D5(-123)._get_value(), -123 * ONECK)
    self.assertEqual(D5(9, 0)._get_value(), 9 * ONECK)
    self.assertEqual(D5(11, -5)._get_value(), 11)
    self.assertEqual(D5(7, -3)._get_value(), 700)
    self.assertEqual(D5(100000, -5)._get_value(), 1 * ONECK)
    self.assertEqual(D5(98765, -7)._get_value(), 987)
    self.assertEqual(D5(-98765, -7)._get_value(), -987)
    self.assertEqual(D5(65432, -7)._get_value(), 654)
    self.assertEqual(D5(-65432, -7)._get_value(), -654)
    self.assertEqual(D5(721, 2)._get_value(), 7210000000)
    self.assertEqual(D5(-721, 2)._get_value(), -7210000000)
    self.assertEqual(D5(-123, 2.4)._get_value(), -12300 * ONECK)
    self.assertEqual(D5(-123, 2.6)._get_value(), -123000 * ONECK)


  def test_decimal5_creation_with_longs(self):
    self.assertEqual(D5(987654321987654321)._get_value(),
          987654321987654321 * ONECK)
    self.assertEqual(D5(-987654321987654321)._get_value(),
          -987654321987654321 * ONECK)
    self.assertEqual(D5(987654321987654321, -2)._get_value(),
          987654321987654321000)
    self.assertEqual(D5(-987654321987654321, -2)._get_value(),
          -987654321987654321000)
    self.assertEqual(D5(987654321987654321, -5)._get_value(),
          987654321987654321)
    self.assertEqual(D5(-987654321987654321, -5)._get_value(),
          -987654321987654321)
    self.assertEqual(D5(987654321987654321, -7)._get_value(),
          9876543219876543)
    self.assertEqual(D5(-987654321987654321, -7)._get_value(),
          -9876543219876543)
    self.assertEqual(D5(987654321987654321, -11)._get_value(),
          987654321987)
    self.assertEqual(D5(-987654321987654321, -11)._get_value(),
          -987654321987)


  def test_decimal5_creation_with_floats(self):
    self.assertEqual(D5(1.7,)._get_value(), 170000)
    self.assertEqual(D5(1.2345678)._get_value(), 123457)
    self.assertEqual(D5(-0.00237)._get_value(), -237)
    self.assertEqual(D5(9876543219.87654321)._get_value(), 
          987654321987654)

  def test_decimal5_creation_with_string(self):
    #print()
    _test_aids.assertRaises_with_message(self,
          decimal5.Decimal5Error,
          'Value is not a supported type:',
          D5, ('2.8',))

  def test_decimal5_creation_with_list(self):
    #print()
    _test_aids.assertRaises_with_message(self,
          decimal5.Decimal5Error,
          'Value is not a supported type:',
          D5, ([-3.9],))

  def test_decimal5_to_str(self):
    self.assertEqual(str(D5()), '0.00000')
    self.assertEqual(str(D5(1)), '1.00000')
    self.assertEqual(str(D5(-21)), '-21.00000')
    self.assertEqual(str(D5(1, -5)), '0.00001')
    self.assertEqual(str(D5(-1, -5)), '-0.00001')
    self.assertEqual(str(D5(238, -4)), '0.02380')
    self.assertEqual(str(D5(238, -2)), '2.38000')
    self.assertEqual(str(D5(987654321987654321)), 
          '987654321987654321.00000')
    self.assertEqual(str(D5(-987654321987654321)), 
          '-987654321987654321.00000')
    self.assertEqual(str(D5(987654321987654321, -5)), 
          '9876543219876.54321')
    self.assertEqual(str(D5(-987654321987654321, -5)), 
          '-9876543219876.54321')


  def test_decimal5_to_repr(self):
    self.assertEqual(repr(D5(27182818, -7)), '2.71828')

  def test_decimal5_compare(self):
    test_compare(self, D5(), D5(), 0)
    test_compare(self, D5(), D5(0), 0)
    test_compare(self, D5(-1), D5(-1), 0)
    test_compare(self, D5(-3), D5(-2), -1)
    test_compare(self, D5(798, -5), D5(7987, -6), 0) 
    test_compare(self, D5(12) , D5(2), 1)
    test_compare(self, D5(122), D5(29), 1)
    self.assertFalse(D5() == None)
    #print()
    _test_aids.assertRaises_with_message(self,
          sb1288.decimal5.Decimal5Error, 
          'Value is not an instance of the required type:',
          D5().__eq__, (0,))
    _test_aids.assertRaises_with_message(self,
          sb1288.decimal5.Decimal5Error, 
          'Value is not an instance of the required type:',
          (lambda x, y: x < y), (D5(1), 7))


  def test_decimal5_add(self):
    self.assertEqual(D5(3).__add__(D5(4))._get_value(), 700000)
    self.assertEqual(D5(3) + D5(9), D5(12))
    self.assertEqual(D5(314159, -5) + D5(314159, -5), D5(628318, -5))
    self.assertEqual(D5(314159, -5) + D5(-314159, -5), D5())


  def test_decimal5_sub(self):
    self.assertEqual(D5(3).__sub__(D5(4))._get_value(), -100000)
    self.assertEqual(D5(3) - D5(9), D5(-6))
    self.assertEqual(D5(314159, -5) - D5(-314159, -5), D5(628318, -5))
    self.assertEqual(D5(314159, -5) - D5(314159, -5), D5())

  def test_decimal5_neg(self):
    self.assertEqual(D5(3).__neg__()._get_value(), -300000)
    self.assertEqual(-D5(-3), D5(3))
    self.assertEqual(-D5(314159, -5), D5(-314159, -5))
    self.assertEqual(-D5(), D5())

  def test_decimal5_mul(self):
    self.assertEqual(D5(3).__mul__(D5(4))._get_value(), 1200000)
    self.assertEqual(D5(3) * D5(-9), D5(-27))
    self.assertEqual(D5(-314159, -5) * D5(-314159, -5), D5(986958, -5))
    self.assertEqual(D5(3).__mul__(4)._get_value(), 1200000)
    self.assertEqual(D5(3) * -9, D5(-27))

  def test_decimal5_div(self):
    self.assertEqual(D5(24).__div__(D5(3))._get_value(), 800000)
    self.assertEqual(D5(2) / D5(3), D5(66666, -5))
    self.assertEqual(D5(-2) / D5(3), D5(-66666, -5))
    self.assertEqual(D5(2) / D5(-3), D5(-66666, -5))
    self.assertEqual(D5(-2) / D5(-3), D5(66666, -5))
    self.assertEqual(D5(2) / 3, D5(66666, -5))
    self.assertEqual(D5(2).divide_by(3, round_away=True), D5(66667, -5))
    self.assertEqual(D5(2).__div__(D5(3), round_away=True), 
          D5(66667, -5))
    self.assertEqual(D5(-2).__div__(D5(3), round_away=True), 
          D5(-66667, -5))
    self.assertEqual(D5(-314159, -5) / D5(-314159, -5), D5(1))
    self.assertEqual(D5(2).divide_by(D5(-3)), D5(-66666, -5))
    self.assertEqual(D5(2).divide_by(D5(-3), round_away=True), 
          D5(-66667, -5))
    #print()
    _test_aids.assertRaises_with_message(self,
          ZeroDivisionError,
          ('integer division or modulo by zero',
          'long division or modulo by zero'),
          D5.divide_by, (D5(2), D5()))


  def test_decimal5total_create(self):
    self.assertEqual(D5TOTAL()._get_value(), 0)

  def test_decimal5total_add(self):
    self.assertEqual(D5TOTAL().__add__(D5(4))._get_value(), 400000)
    self.assertEqual(D5TOTAL() + D5(3) + D5(9), D5(12))
    self.assertEqual(D5TOTAL() + D5(314159, -5) + D5(314159, -5),
          D5(628318, -5))
    self.assertEqual(D5TOTAL() + D5(314159, -5) + D5(-314159, -5), D5())
    self.assertEqual((D5TOTAL() + D5(3)) + (D5TOTAL() + D5(-8)), D5(-5))

  def test_decimal5total_sub(self):
    self.assertEqual(D5TOTAL().__sub__(D5(4))._get_value(), -400000)
    self.assertEqual((D5TOTAL() + D5(3)).__sub__(D5(4))._get_value(), -100000)
    self.assertEqual(D5TOTAL() + D5(4).__sub__(D5(3)), D5(1))
    self.assertEqual(D5TOTAL() + D5(3) - D5(9), D5(-6))
    self.assertEqual(D5TOTAL() + D5(314159, -5) - D5(-314159, -5),
          D5(628318, -5))
    self.assertEqual(D5(314159, -5) - D5(314159, -5), D5())
    self.assertEqual((D5TOTAL() + D5(3)) - (D5TOTAL() + D5(-8)), D5(11))


  def test_confirm_types(self):
    self.assertTrue(decimal5._confirm_types(28, int, str))
    self.assertTrue(decimal5._confirm_types('abc', str))
    self.assertTrue(decimal5._confirm_types(D5TOTAL(), D5))
    _test_aids.assertRaises_with_message(self,
          sb1288.decimal5.Decimal5Error,
          'Value is not an instance of the required type:',
          decimal5._confirm_types, (3.4, int, str))


  def test_div_to_int(self):
    self.assertEqual(decimal5.div_to_int(6, 3), 2)
    self.assertEqual(decimal5.div_to_int(6, 3, round_away=True), 2)
    self.assertEqual(decimal5.div_to_int(7, 3), 2)
    self.assertEqual(decimal5.div_to_int(7, 3, round_away=True), 3)
    self.assertEqual(decimal5.div_to_int(8, 3), 2)
    self.assertEqual(decimal5.div_to_int(8, 3, round_away=True), 3)
    self.assertEqual(decimal5.div_to_int(-7, 3), -2)
    self.assertEqual(decimal5.div_to_int(-7, 3, round_away=True), -3)
    self.assertEqual(decimal5.div_to_int(-8, 3), -2)
    self.assertEqual(decimal5.div_to_int(-8, 3, round_away=True), -3)
    self.assertEqual(decimal5.div_to_int(7, -3), -2)
    self.assertEqual(decimal5.div_to_int(7, -3, round_away=True), -3)
    self.assertEqual(decimal5.div_to_int(8, -3), -2)
    self.assertEqual(decimal5.div_to_int(8, -3, round_away=True), -3)
    self.assertEqual(decimal5.div_to_int(-7, -3), 2)
    self.assertEqual(decimal5.div_to_int(-7, -3, round_away=True), 3)
    self.assertEqual(decimal5.div_to_int(-8, -3), 2)
    self.assertEqual(decimal5.div_to_int(-8, -3, round_away=True), 3)
