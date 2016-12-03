# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0

from __future__ import print_function

import unittest
import _test_aids

from _src import sb1288
from sb1288 import rcv
from sb1288 import ballot
from sb1288 import constants as K
from sb1288 import validate
from sb1288.validate import str_tuple

import sys
import re

class TestRcv(unittest.TestCase):
  """Test RCV routines"""

  def setUp(self):
    self.save_maxDiff = self.maxDiff
    self.maxDiff = None

  def tearDown(self):
    self.maxDiff = self.save_maxDiff

  def make_irv_01(self):
    candidates = ' A B C'
    ballots = (
          (15, ' A B C'),
          (10, ' B C A'),
          (8,  ' C B A'),
          )
    tie_breaker = ' A B C'
    options = {}
    return rcv.Tabulation(1, candidates, ballots, 3, tie_breaker, options)

  def make_irv_02(self):
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
    return rcv.Tabulation(1, candidates, ballots, 3, tie_breaker, options)

  def make_stv_01(self):
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
    return rcv.Tabulation(3, candidates, ballots, 3, tie_breaker, options)

  def test_irv_01(self):
    self.maxDiff = None
    test_tabulation = self.make_irv_01()
    self.assertEqual(test_tabulation.nbr_seats_to_fill, 1)
    self.assertEqual(test_tabulation.candidates, ('A', 'B', 'C'))
    ballot0 = test_tabulation.ballots[0]
    ballots_as_tuples = tuple((ballot.as_tuple()
          for ballot in test_tabulation.ballots))
    self.assertEqual(ballots_as_tuples, (
          (15, K.ONE, ('A', 'B', 'C')),
          (10, K.ONE, ('B', 'C', 'A')),
          (8, K.ONE, ('C', 'B', 'A'))))
    self.assertEqual(test_tabulation.max_ranking_levels, 3)
    self.assertEqual(test_tabulation.tie_breaker, {'A': 0, 'B': 1, 'C': 2})
    self.assertEqual(test_tabulation.options,
          {'stop_at_majority': False, 'alternative_defeats': 'N'})

  def test_as_irv_1(self):
    test_tabulation = self.make_irv_01()
    self.assertEqual(test_tabulation.is_irv(), True)
    self.assertEqual(test_tabulation.zero_votes(), 0)
    test_ballot = ballot.Ballot(7, ' C B A')
    self.assertEqual(test_tabulation.ballot_votes(test_ballot), 7)
    self.assertEqual(test_tabulation.other_categories(),
          {':Other exhausted': [], ':Abstentions': [], ':Overvotes': []})
    test_votes = test_tabulation.votes_for_previously_elected(12)
    self.assertEqual(test_votes, 12)

  def test_as_stv_1(self):
    test_tabulation = self.make_stv_01()
    self.assertEqual(test_tabulation.is_irv(), False)
    self.assertEqual(test_tabulation.zero_votes(), K.ZERO)
    test_ballot = ballot.Ballot(7, ' C B A')
    self.assertEqual(test_tabulation.ballot_votes(test_ballot), K.ONE * 7)
    self.assertEqual(test_tabulation.other_categories(),
          {':Other exhausted': [], ':Abstentions': [], ':Overvotes': [],
          ':Residual surplus': []})
    test_tabulation.tabulate(stop_after_tally=1)
    test_votes = test_tabulation.votes_for_previously_elected(K.ONE * 19)
    self.assertEqual(test_votes, K.Decimal(9.5))

  def test_assign_ballots(self):
    test_tabulation = self.make_irv_01()
    test_tabulation.tabulate(stop_at_begin=1)
    self.assertEqual(test_tabulation.ballots_for['A'], [])
    test_tabulation.assign_ballots(test_tabulation.ballots)
    self.assertEqual(test_tabulation.ballots_for['A'],
          [ballot.Ballot(15, ('A', 'B', 'C'))])

  def test_tally_votes(self):
    test_tabulation = self.make_irv_01()
    test_tabulation.tabulate(stop_at_begin=1)
    test_tabulation.assign_ballots(test_tabulation.ballots)
    self.assertEqual(test_tabulation.tallies['B'], [])
    test_tabulation.tally_votes_for_assigned_ballots()
    self.assertEqual(test_tabulation.tallies['B'], [10])

  def test_update_candidate_status_tally(self):
    test_tabulation = self.make_irv_01()
    test_tabulation.tabulate(stop_at_begin=1)
    test_tabulation.assign_ballots(test_tabulation.ballots)
    test_tabulation.tally_votes_for_assigned_ballots()
    self.assertEqual(test_tabulation.status['B'].votes, 0)
    test_tabulation.update_candidate_status_tally()
    self.assertEqual(test_tabulation.status['B'].votes, 10)

  def test_defeat_candidate(self):
    test_tabulation = self.make_irv_01()
    test_tabulation.tabulate(stop_after_status_update=1)
    self.assertEqual(test_tabulation.status['B'].status, K.STATUS_CONTINUING)
    self.assertEqual(test_tabulation.continuing(), set(str_tuple(' A B C')))
    self.assertEqual(test_tabulation.elected(), set())
    test_tabulation.defeat_candidates(set(['B']))
    self.assertEqual(test_tabulation.status['B'].status, K.STATUS_DEFEATED)
    self.assertEqual(test_tabulation.continuing(), set(str_tuple(' A C')))
    self.assertEqual(test_tabulation.elected(), set())

  def test_elect_candidate(self):
    test_tabulation = self.make_irv_01()
    test_tabulation.tabulate(stop_after_status_update=1)
    self.assertEqual(test_tabulation.status['B'].status, K.STATUS_CONTINUING)
    self.assertEqual(test_tabulation.status['C'].status, K.STATUS_CONTINUING)
    self.assertEqual(test_tabulation.continuing(), set(str_tuple(' A B C')))
    self.assertEqual(test_tabulation.elected(), set())
    test_tabulation.elect_candidates(set(['C', 'B']))
    self.assertEqual(test_tabulation.status['B'].status, K.STATUS_ELECTED)
    self.assertEqual(test_tabulation.status['C'].status, K.STATUS_ELECTED)
    self.assertEqual(test_tabulation.continuing(), set(('A',)))
    self.assertEqual(test_tabulation.elected(), set(str_tuple(' B C')))

  def test_resolve_tie_1(self):
    test_tabulation = self.make_irv_01()
    test_tabulation.tabulate(stop_after_status_update=1)
    self.assertEqual(test_tabulation.tie_breaker, {'A':0, 'B':1, 'C':2})
    self.assertEqual(test_tabulation.resolve_tie(set(str_tuple(' A B C'))),
          'A')
    self.assertEqual(test_tabulation.resolve_tie(set(str_tuple(' B C'))), 'B')

  def test_get_single_defeat_candidate_1(self):
    test_tabulation = self.make_irv_01()
    test_tabulation.tabulate(stop_after_status_update=1)
    self.assertEqual(test_tabulation.get_single_defeat_candidate(),
          set(('C',)))
    test_tabulation.status['A'].votes = 8
    self.assertEqual(test_tabulation.get_single_defeat_candidate(),
          set(('A',)))


