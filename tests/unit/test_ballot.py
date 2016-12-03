# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0

import unittest
import _test_aids

from _src import sb1288
from sb1288 import ballot
from sb1288 import constants as K
from sb1288.constants import Decimal
from sb1288.validate import str_tuple

import re

class TestBallot(unittest.TestCase):
  """Test the ballot module and Ballot class"""

  def setUp(self):
    self.save_maxDiff = self.maxDiff

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

  def test_ballot_create(self):
    test_ballot = ballot.Ballot(3, ('A', 'B', 'C'))
    self.assertEqual(test_ballot._multiple, 3)
    self.assertEqual(test_ballot._transfer_value, Decimal(1))
    self.assertEqual(test_ballot._rankings, ('A', 'B', 'C'))
    self.assertEqual(test_ballot._current_index, 0)

  def test_ballot_accessors(self):
    test_ballot = ballot.Ballot(7, ('C', 'B', 'A'))
    self.assertEqual(test_ballot.get_multiple(), 7)
    self.assertEqual(test_ballot.get_transfer_value(), Decimal(1))

  def test_ballot_as_string(self):
    test_ballot = ballot.Ballot(7, ('C', 'B', 'A'))
    self.assertEqual(repr(test_ballot), "(7, 1.00000, ('C', 'B', 'A'))")
    self.assertEqual(str(test_ballot), "(7, ('C', 'B', 'A'))")

  def test_ballot_get_hrcc_1(self):
    test_ballot = ballot.Ballot(5, str_tuple(' A B C'))
    self.assertEqual(test_ballot.get_hrcc(('A',), 3), 'A')
    self.assertEqual(test_ballot.get_hrcc(('A',), 3), 'A')
    self.assertEqual(test_ballot.get_hrcc(('B',), 3), 'B')
    self.assertEqual(test_ballot.get_hrcc(('B',), 3), 'B')
    self.assertEqual(test_ballot.get_hrcc(('C',), 3), 'C')
    self.assertEqual(test_ballot.get_hrcc(('C',), 3), 'C')
    self.assertEqual(test_ballot.get_hrcc(('D',), 3), ':Other exhausted')
    self.assertEqual(test_ballot.get_hrcc(('D',), 3), ':Other exhausted')
    self.assertEqual(test_ballot.get_hrcc(('D',), 4), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 4), ':Abstentions')

  def test_ballot_get_hrcc_ov(self):
    test_ballot = ballot.Ballot(5, str_tuple(' A # C'))
    self.assertEqual(test_ballot.get_hrcc(('A',), 3), 'A')
    self.assertEqual(test_ballot.get_hrcc(('A',), 3), 'A')
    self.assertEqual(test_ballot.get_hrcc(('B',), 3), ':Overvotes')
    self.assertEqual(test_ballot.get_hrcc(('B',), 3), ':Overvotes')
    self.assertEqual(test_ballot.get_hrcc(('C',), 3), ':Overvotes')
    self.assertEqual(test_ballot.get_hrcc(('C',), 3), ':Overvotes')
    self.assertEqual(test_ballot.get_hrcc(('D',), 3), ':Overvotes')
    self.assertEqual(test_ballot.get_hrcc(('D',), 3), ':Overvotes')
    self.assertEqual(test_ballot.get_hrcc(('D',), 4), ':Overvotes')
    self.assertEqual(test_ballot.get_hrcc(('D',), 4), ':Overvotes')

  def test_ballot_get_hrcc_skipped_1(self):
    test_ballot = ballot.Ballot(5, str_tuple(' A  C'))
    self.assertEqual(test_ballot.get_hrcc(('A',), 3), 'A')
    self.assertEqual(test_ballot.get_hrcc(('A',), 3), 'A')
    self.assertEqual(test_ballot.get_hrcc(('B', 'C'), 3), 'C')
    self.assertEqual(test_ballot.get_hrcc(('B', 'C'), 3), 'C')
    self.assertEqual(test_ballot.get_hrcc(('C',), 3), 'C')
    self.assertEqual(test_ballot.get_hrcc(('C',), 3), 'C')
    self.assertEqual(test_ballot.get_hrcc(('D',), 3), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 3), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 4), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 4), ':Abstentions')

  def test_ballot_get_hrcc_skipped_2(self):
    test_ballot = ballot.Ballot(5, str_tuple(' A   C'))
    self.assertEqual(test_ballot.get_hrcc(('A',), 4), 'A')
    self.assertEqual(test_ballot.get_hrcc(('A',), 4), 'A')
    self.assertEqual(test_ballot.get_hrcc(('B', 'C'), 4), 'C')
    self.assertEqual(test_ballot.get_hrcc(('B', 'C'), 4), 'C')
    self.assertEqual(test_ballot.get_hrcc(('C',), 4), 'C')
    self.assertEqual(test_ballot.get_hrcc(('C',), 4), 'C')
    self.assertEqual(test_ballot.get_hrcc(('D',), 4), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 4), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 5), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 5), ':Abstentions')

  def test_ballot_get_hrcc_skipped_3(self):
    test_ballot = ballot.Ballot(5, str_tuple('    C'))
    self.assertEqual(test_ballot.get_hrcc(('A', 'C'), 4), 'C')
    self.assertEqual(test_ballot.get_hrcc(('A', 'C'), 4), 'C')
    self.assertEqual(test_ballot.get_hrcc(('B', 'C'), 4), 'C')
    self.assertEqual(test_ballot.get_hrcc(('B', 'C'), 4), 'C')
    self.assertEqual(test_ballot.get_hrcc(('C',), 4), 'C')
    self.assertEqual(test_ballot.get_hrcc(('C',), 4), 'C')
    self.assertEqual(test_ballot.get_hrcc(('D',), 4), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 4), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 5), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 5), ':Abstentions')

  def test_ballot_get_hrcc_dups_1(self):
    test_ballot = ballot.Ballot(5, str_tuple(' A A A'))
    self.assertEqual(test_ballot.get_hrcc(('A', 'C'), 3), 'A')
    self.assertEqual(test_ballot.get_hrcc(('A', 'C'), 3), 'A')
    self.assertEqual(test_ballot.get_hrcc(('B', 'C'), 3), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('B', 'C'), 3), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('C',), 3), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('C',), 3), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 3), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 3), ':Abstentions')
    self.assertEqual(test_ballot.get_hrcc(('D',), 5), ':Abstentions')


  def test_ballot_update_transfer_value_1(self):
    test_ballot = ballot.Ballot(5, str_tuple(' A B C'))
    self.assertEqual(test_ballot.update_transfer_value(
          Decimal(5)/7), Decimal(0.71428))
    self.assertEqual(test_ballot.update_transfer_value(
          Decimal(5)/7), Decimal(0.51019))
    self.assertEqual(test_ballot.update_transfer_value(
          Decimal(5)/7), Decimal(0.36441))

