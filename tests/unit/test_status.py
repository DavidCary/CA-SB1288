# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0

import unittest
import _test_aids

from _src import sb1288
from sb1288 import status
from sb1288 import constants as K
from sb1288.constants import Decimal
from sb1288.validate import str_tuple

import re

class TestStatus(unittest.TestCase):
  """Test the status module and status.Status class"""

  def setUp(self):
    self.save_maxDiff = self.maxDiff
    self.maxDiff = None

  def tearDown(self):
    self.maxDiff = self.save_maxDiff

  def get_exception_message(self, exception_type, args):
    """Get an exception's string representation"""
    message = None
    try:
      raise exception_type(*args)
    except exception_type as exc:
      message = str(exc)
    return message

  def make_status_1(self):
    return status.Status('E', 13, 4, K.STATUS_ELECTED)

  def make_status_2(self):
    return status.Status('F', K.ONE * 17, 3, K.STATUS_CONTINUING)

  def test_status_create_1(self):
    test_status = status.Status('A')
    self.assertEqual(test_status.candidate, 'A')
    self.assertEqual(test_status.votes, 0)
    self.assertEqual(test_status.nbr_round, None)
    self.assertEqual(test_status.status, K.STATUS_CONTINUING)

  def test_status_create_2(self):
    test_status = status.Status('B', K.ZERO)
    self.assertEqual(test_status.candidate, 'B')
    self.assertEqual(test_status.votes, K.ZERO)
    self.assertEqual(test_status.nbr_round, None)
    self.assertEqual(test_status.status, K.STATUS_CONTINUING)

  def test_status_create_3(self):
    test_status = status.Status('C', K.ONE * 5, 3, K.STATUS_ELECTED)
    self.assertEqual(test_status.candidate, 'C')
    self.assertEqual(test_status.votes, K.Decimal(5))
    self.assertEqual(test_status.nbr_round, 3)
    self.assertEqual(test_status.status, K.STATUS_ELECTED)

  def test_status_create_4(self):
    status_dict = {'candidate': 'D', 'votes': 7, 'nbr_round': 2,
          'status': K.STATUS_DEFEATED}
    test_status = status.Status(status_dict)
    self.assertEqual(test_status.candidate, 'D')
    self.assertEqual(test_status.votes, 7)
    self.assertEqual(test_status.nbr_round, 2)
    self.assertEqual(test_status.status, K.STATUS_DEFEATED)

  def test_status_as_dict_1(self):
    status_dict = {'candidate': 'D', 'votes': 7, 'nbr_round': 2,
          'status': K.STATUS_DEFEATED}
    test_status = status.Status(status_dict)
    self.assertEqual(test_status.as_dict(), status_dict)

  def test_status_eq(self):
    test_status_1 = self.make_status_1()
    test_status_2 = self.make_status_1()
    test_status_3 = self.make_status_2()
    self.assertTrue(test_status_1 == test_status_2)
    self.assertFalse(test_status_1 != test_status_2)
    self.assertFalse(test_status_1 == test_status_3)
    self.assertTrue(test_status_1 != test_status_3)

  def test_status_as_str(self):
    test_status = self.make_status_1()
    test_status_as_str = str(test_status)
    self.assertEqual(str(test_status),
          "{candidate: 'E', status: 'elected', nbr_round: 4, votes: 13}")
    
