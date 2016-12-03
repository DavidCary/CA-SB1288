# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0

import unittest
import _test_aids

from _src import sb1288
from sb1288 import rcv

import sys
import re

class TestIrv(unittest.TestCase):
  """Test IRV"""

  def setUp(self):
    self.save_maxDiff = self.maxDiff
    self.maxDiff = 800

  def test_irv_01(self):
    candidates = ' A B C'
    ballots = (
          (15, ' A B C'),
          (10, ' B C A'),
          (8,  ' C B A'),
          )
    tie_breaker = ' A B C'
    options = {}
    exp_elected = ('B',)
    exp_status = _test_aids.build_expected_status((
          ('A', 'defeated', 2, 15),
          ('B', 'elected',  2, 18),
          ('C', 'defeated', 1,  8),
          ))
    exp_tally = {
          'A': [15, 15],
          'B': [10, 18],
          'C': [8],
          ':Overvotes': [0, 0],
          ':Abstentions': [0, 0],
          ':Other exhausted': [0, 0],
          }
    elected, status, tally = rcv.Tabulation(1, candidates, ballots,
          3, tie_breaker, options).tabulate()
    status_dict = {candidate: status.as_dict()
          for candidate, status in status.items()}
    self.assertEqual(set(elected), set(exp_elected))
    self.assertEqual(status_dict, exp_status)
    self.assertEqual(tally, exp_tally)

  def test_irv_02(self):
    candidates = ' A B C D'
    ballots = (
          (15, ' A B C'),
          (8, ' B C D'),
          (1,  ' B'),
          (1,  ' B #'),
          (8,  ' C B A'),
          (5,  ' D C B'),
          )
    tie_breaker = ' A B C D'
    options = {}
    exp_elected = ('C',)
    exp_status = _test_aids.build_expected_status((
          ('A', 'defeated', 3, 15),
          ('B', 'defeated',  2, 10),
          ('C', 'elected', 3, 21),
          ('D', 'defeated',  1, 5),
          ))
    exp_tally = {
          'A': [15, 15, 15],
          'B': [10, 10],
          'C': [8, 13, 21],
          'D': [5],
          ':Overvotes': [0, 0, 1],
          ':Abstentions': [0, 0, 1],
          ':Other exhausted': [0, 0, 0],
          }
    elected, status, tally = rcv.Tabulation(1, candidates, ballots,
          3, tie_breaker, options).tabulate()
    status_dict = {candidate: status.as_dict()
          for candidate, status in status.items()}
    self.assertEqual(set(elected), set(exp_elected))
    self.assertEqual(status_dict, exp_status)
    self.assertEqual(tally, exp_tally)
