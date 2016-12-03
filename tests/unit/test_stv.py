# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0

import unittest
import _test_aids

from _src import sb1288
from sb1288 import rcv

import sys
import re

class TestStv(unittest.TestCase):
  """Test IRV"""

  def setUp(self):
    self.save_maxDiff = self.maxDiff
    self.maxDiff = 2000

  def test_stv_01(self):
    candidates = ' A B C D E'
    ballots = (
          (15, ' A B C D E'),
          (6,  ' B C A E D'),
          (3,  ' C B A D E'),
          (7,  ' D E A B C'),
          (9,  ' E D C B A'),
          )
    tie_breaker = ' A B C D E'
    options = {}
    exp_elected = ('A', 'B', 'D')
    exp_status = _test_aids.build_expected_status((
          ('A', 'elected', 1, 15.0),
          ('B', 'elected',  2, 10.99995),
          ('C', 'defeated', 3,  3.99975),
          ('D', 'elected', 4,  10.45435),
          ('E', 'defeated', 4, 9.54540)
          ))
    exp_tally = _test_aids.build_stv_tally({
          'A': [15.0, 10.0, 10.0, 10.0],
          'B': [6.0, 10.99995, 10.0, 10.0],
          'C': [3.0, 3.0, 3.99975],
          'D': [7.0, 7.0, 7.0, 10.45435],
          'E': [9.0, 9.0, 9.0, 9.54540],
          ':Overvotes': [0.0, 0.0, 0.0, 0.0],
          ':Abstentions': [0.0, 0.0, 0.0, 0.0],
          ':Other exhausted': [0.0, 0.0, 0.0, 0.0],
          ':Residual surplus': [0.0, 0.00005, 0.00025, 0.00025],
          })
    elected, status, tally = rcv.Tabulation(3, candidates, ballots,
          5, tie_breaker, options).tabulate()
    status_dict = {candidate: status.as_dict()
          for candidate, status in status.items()}
    self.assertEqual(set(elected), set(exp_elected))
    self.assertEqual(status_dict, exp_status)
    self.assertEqual(tally, exp_tally)


