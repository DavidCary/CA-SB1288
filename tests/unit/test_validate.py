# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0

import sys

import unittest
import _test_aids

from _src import sb1288
from sb1288 import validate
from sb1288 import errors
from sb1288.constants import Decimal
ONE = Decimal(1)

import re

def sample_options_function(parms, result):
  return 'Y'

class TestValidate(unittest.TestCase):
  """Test the validate module"""

  def test_str_tuple_from_str(self):
    self.assertEqual(validate.str_tuple(''), tuple())
    self.assertEqual(validate.str_tuple(' '), ('',))
    self.assertEqual(validate.str_tuple('#'), ('',))
    self.assertEqual(validate.str_tuple(' A'), ('A',))
    self.assertEqual(validate.str_tuple(' AA'), ('AA',))
    self.assertEqual(validate.str_tuple(' A B'), ('A', 'B'))
    self.assertEqual(validate.str_tuple(' A  B'), ('A', '', 'B'))
    self.assertEqual(validate.str_tuple('|A|B'), ('A', 'B'))

  def test_str_tuple_from_list(self):
    self.assertEqual(validate.str_tuple([]), tuple())
    self.assertEqual(validate.str_tuple(['']), ('',))
    self.assertEqual(validate.str_tuple(['#']), ('#',))
    self.assertEqual(validate.str_tuple(['AA']), ('AA',))
    self.assertEqual(validate.str_tuple(['A', 'B']), ('A', 'B'))
    self.assertEqual(validate.str_tuple(['A', '', 'B']), ('A', '', 'B'))
    _test_aids.assertRaises_with_message(self, TypeError,
          'Item in list is not a str:',
          validate.str_tuple, (['A', 7, 'B'],))

  def test_str_tuple_from_tuple(self):
    self.assertEqual(validate.str_tuple(tuple()), tuple())
    self.assertEqual(validate.str_tuple(('',)), ('',))
    self.assertEqual(validate.str_tuple(('#',)), ('#',))
    self.assertEqual(validate.str_tuple(('AA',)), ('AA',))
    self.assertEqual(validate.str_tuple(('A', 'B')), ('A', 'B'))
    self.assertEqual(validate.str_tuple(('A', '', 'B')), ('A', '', 'B'))
    _test_aids.assertRaises_with_message(self, TypeError,
          'Item in tuple is not a str:',
          validate.str_tuple, (('A', 7, 'B'),))

  def test_str_tuple_from_other(self):
    type_type = 'type' if sys.version_info.major == 2 else 'class'
    _test_aids.assertRaises_with_message(self, TypeError,
          'Can not make a str_tuple from a <' + type_type + ' \'set\'>.',
          validate.str_tuple, (set(('A', 7, 'B')),))

  def test_nbr_seats_to_fill_valid(self):
    self.assertEqual(validate.nbr_seats_to_fill(1), 1)
    self.assertEqual(validate.nbr_seats_to_fill(2), 2)
    self.assertEqual(validate.nbr_seats_to_fill(3), 3)
    self.assertEqual(validate.nbr_seats_to_fill(4), 4)
    self.assertEqual(validate.nbr_seats_to_fill(5), 5)
    self.assertEqual(validate.nbr_seats_to_fill(1020), 1020)

  def test_nbr_seats_to_fill_invalid(self):
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'nbr_seats_to_fill not an int:',
          validate.nbr_seats_to_fill, ('two',))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'nbr_seats_to_fill not >= 1:',
          validate.nbr_seats_to_fill, (0,))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'nbr_seats_to_fill not >= 1:',
          validate.nbr_seats_to_fill, (-1,))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'nbr_seats_to_fill not >= 1:',
          validate.nbr_seats_to_fill, (-2,))

  def test_candidates_valid(self):
    self.assertEqual(validate.candidates(()), ())
    self.assertEqual(validate.candidates([]), ())
    self.assertEqual(validate.candidates(''), ())
    self.assertEqual(validate.candidates(('A',)), ('A',))
    self.assertEqual(validate.candidates(('B', 'A')), ('B', 'A'))
    self.assertEqual(validate.candidates(('B', 'C', 'A')), ('B', 'C', 'A'))
    self.assertEqual(validate.candidates(
          ('B', 'C', 'A', 'I', 'H', 'G', 'F', 'E', 'D', 'J', 'K', 'L')),
          ('B', 'C', 'A', 'I', 'H', 'G', 'F', 'E', 'D', 'J', 'K', 'L'))
    self.assertEqual(validate.candidates(['A']), ('A',))
    self.assertEqual(validate.candidates(['B', 'A']), ('B', 'A'))
    self.assertEqual(validate.candidates(['B', 'C', 'A']), ('B', 'C', 'A'))
    self.assertEqual(validate.candidates(
          ['B', 'C', 'A', 'I', 'H', 'G', 'F', 'E', 'D', 'J', 'K', 'L']),
          ('B', 'C', 'A', 'I', 'H', 'G', 'F', 'E', 'D', 'J', 'K', 'L'))
    self.assertEqual(validate.candidates(' A'), ('A',))
    self.assertEqual(validate.candidates(' B A'), ('B', 'A'))
    self.assertEqual(validate.candidates(' B C A'), ('B', 'C', 'A'))
    self.assertEqual(validate.candidates(
          ' B C A I H G F E D J K L'),
          ('B', 'C', 'A', 'I', 'H', 'G', 'F', 'E', 'D', 'J', 'K', 'L'))
    self.assertEqual(validate.candidates(
          ',Joe Smith,John Doe'),
          ('Joe Smith', 'John Doe'))
    self.assertEqual(validate.candidates(
          ';Smith, Joe;Doe, John'),
          ('Smith, Joe', 'Doe, John'))

  def test_candidates_invalid(self):
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid candidates type:',
          validate.candidates, (17,))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid candidate name:',
          validate.candidates, (('A', ''),))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid candidate name:',
          validate.candidates, (('A', '#'),))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid candidate name:',
          validate.candidates, (('A', ':who'),))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Candidate names are not unique.',
          validate.candidates, (('A', 'B', 'A'),))

  def test_tie_breaker_valid(self):
    candidates = ('B', 'C', 'A', 'I', 'H', 'G', 'F', 'E', 'D', 'J', 'K', 'L',
          'Joe Smith', 'John Doe', 'Smith, Joe', 'Doe, John')
    self.assertEqual(validate.tie_breaker((), candidates), {})
    self.assertEqual(validate.tie_breaker([], candidates), {})
    self.assertEqual(validate.tie_breaker('', candidates), {})
    self.assertEqual(validate.tie_breaker(('A',), candidates), {'A': 0})
    self.assertEqual(validate.tie_breaker(
          ('B', 'A'), candidates),
          {'B': 0, 'A': 1})
    self.assertEqual(validate.tie_breaker(
          ('B', 'C', 'A'), candidates),
          {'B': 0, 'C': 1, 'A': 2})
    self.assertEqual(validate.tie_breaker(
          ('B', 'C', 'A', 'I', 'H', 'G', 'F', 'E', 'D', 'J', 'K', 'L'),
          candidates),
          {'B': 0, 'C': 1, 'A': 2, 'I': 3, 'H': 4, 'G': 5, 'F': 6, 'E': 7,
          'D': 8, 'J': 9, 'K': 10, 'L': 11})
    self.assertEqual(validate.tie_breaker(['A'], candidates), {'A': 0})
    self.assertEqual(validate.tie_breaker(
          ['B', 'A'], candidates),
          {'B': 0, 'A': 1})
    self.assertEqual(validate.tie_breaker(
          ['B', 'C', 'A'], candidates),
          {'B': 0, 'C': 1, 'A': 2})
    self.assertEqual(validate.tie_breaker(
          ['B', 'C', 'A', 'I', 'H', 'G', 'F', 'E', 'D', 'J', 'K', 'L'],
          candidates),
          {'B': 0, 'C': 1, 'A': 2, 'I': 3, 'H': 4, 'G': 5, 'F': 6, 'E': 7,
          'D': 8, 'J': 9, 'K': 10, 'L': 11})
    self.assertEqual(validate.tie_breaker(' A', candidates), {'A': 0})
    self.assertEqual(validate.tie_breaker(' B A', candidates),
          {'B': 0, 'A': 1})
    self.assertEqual(validate.tie_breaker(' B C A', candidates),
          {'B': 0, 'C': 1, 'A': 2})
    self.assertEqual(validate.tie_breaker(
          ' B C A I H G F E D J K L', candidates),
          {'B': 0, 'C': 1, 'A': 2, 'I': 3, 'H': 4, 'G': 5, 'F': 6, 'E': 7,
          'D': 8, 'J': 9, 'K': 10, 'L': 11})
    self.assertEqual(validate.tie_breaker(
          ',Joe Smith,John Doe', candidates),
          {'Joe Smith': 0, 'John Doe': 1})
    self.assertEqual(validate.tie_breaker(
          ';Smith, Joe;Doe, John', candidates),
          {'Smith, Joe': 0, 'Doe, John': 1})

  def test_tie_breaker_invalid(self):
    candidates = ('A', 'C')
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid tie_breaker type:',
          validate.tie_breaker, (17, candidates))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid candidate name in tie_breaker:',
          validate.tie_breaker, (('A', 'B'), candidates))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid candidate name in tie_breaker:',
          validate.tie_breaker, (('A', ''), candidates))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid candidate name in tie_breaker:',
          validate.tie_breaker, (('A', '#'), candidates))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid candidate name in tie_breaker:',
          validate.tie_breaker, (('A', ':who'), candidates))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Candidate names in tie_breaker are not unique.',
          validate.tie_breaker, (('A', 'C', 'A'), candidates))

  def test_ballots_valid(self):
    candidates = validate.str_tuple(' A B C D E F G H I J K L')
    self.assertEqual(validate.ballots((), candidates, 3), ())
    self.assertEqual(validate.ballots([], candidates, 3), ())
    self.assertEqual(repr(validate.ballots(
          ((5, ('A',)),), candidates, 3)),
          "((5, 1.00000, ('A',)),)")
    self.assertEqual(repr(validate.ballots(
          [[5, ['A',]],], candidates, 3)),
          "((5, 1.00000, ('A',)),)")
    self.assertEqual(repr(validate.ballots(
          [[5, ' A'],], candidates, 3)),
          "((5, 1.00000, ('A',)),)")
    self.assertEqual(repr(validate.ballots(
          [(3, ' A B'), (5, ' B A'),], candidates, 3)),
          "((3, 1.00000, ('A', 'B')), (5, 1.00000, ('B', 'A')))")
    self.assertEqual(repr(validate.ballots(
          [(3, ' A  B'), (5, ' B # A'),], candidates, 3)),
          "((3, 1.00000, ('A', '', 'B')), (5, 1.00000, ('B', '#', 'A')))")
    self.assertEqual(repr(validate.ballots(
          [(3, ' A   B'), (5, '   A'),], candidates, 4)),
          "((3, 1.00000, ('A', '', '', 'B')), (5, 1.00000, ('', '', 'A')))")
    self.assertEqual(repr(validate.ballots(
          [(3, ' A   B'), (5, '   A'),], candidates, None)),
          "((3, 1.00000, ('A', '', '', 'B')), (5, 1.00000, ('', '', 'A')))")
    self.assertEqual(repr(validate.ballots(
          [(3, ''), (5, ' #'),], candidates, 3)),
          "((3, 1.00000, ()), (5, 1.00000, ('#',)))")
    self.assertEqual(repr(validate.ballots(
          [(3, ' A B C D E F G H I J K L'),
          (5, ' L K J I H G F E D C B A'),], candidates, 12)),
          "((3, 1.00000, ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'" +
          ", 'J', 'K', 'L'))," +
          " (5, 1.00000, ('L', 'K', 'J', 'I', 'H', 'G', 'F', 'E', 'D'" +
          ", 'C', 'B', 'A')))")
    self.assertEqual(repr(validate.ballots(
          [(3, ' A B C D E F G H I J K L'),
          (5, ' L K J I H G F E D C B A'),], candidates, None)),
          "((3, 1.00000, ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'" +
          ", 'J', 'K', 'L'))," +
          " (5, 1.00000, ('L', 'K', 'J', 'I', 'H', 'G', 'F', 'E', 'D'" +
          ", 'C', 'B', 'A')))")

  def test_ballots_invalid(self):
    candidates = validate.str_tuple(' A B C D E F G H I J K L')
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'ballots is not a list or tuple:',
          validate.ballots, (' A B', candidates, 3))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'A ballot is not a list or tuple:',
          validate.ballots, ((' A B',), candidates, 3))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'A ballot is not a pair of values:',
          validate.ballots, ([('A', 'B', 'C')], candidates, 3))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'A ballot multiple is not an int:',
          validate.ballots, ([(0.12,' A B C')], candidates, 3))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'A ballot multiple is zero or less:',
          validate.ballots, ([(-1,' A B C')], candidates, 3))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'A ballot multiple is zero or less:',
          validate.ballots, ([(0,' A B C')], candidates, 3))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid ballot rankings type:',
          validate.ballots, ([(1, 77)], candidates, 3))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid ballot rankings type:',
          validate.ballots, ([(2, ('A', 77))], candidates, 3))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Ballot rankings is too long:',
          validate.ballots, ([(2, ' A B C D')], candidates, 3))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid ballot ranking code:',
          validate.ballots, ([(2, ('A', 'Z'))], candidates, 3))

  def test_max_ranking_levels_valid(self):
    self.assertEqual(validate.max_ranking_levels(3), 3)
    self.assertEqual(validate.max_ranking_levels(4), 4)
    self.assertEqual(validate.max_ranking_levels(5), 5)
    self.assertEqual(validate.max_ranking_levels(1020), 1020)
    self.assertEqual(validate.max_ranking_levels(None), None)

  def test_max_ranking_levels_invalid(self):
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'max_ranking_levels not an int:',
          validate.max_ranking_levels, ('two',))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'max_ranking_levels is less than 3:',
          validate.max_ranking_levels, (2,))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'max_ranking_levels is less than 3:',
          validate.max_ranking_levels, (1,))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'max_ranking_levels is less than 3:',
          validate.max_ranking_levels, (0,))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'max_ranking_levels is less than 3:',
          validate.max_ranking_levels, (-1,))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'max_ranking_levels is less than 3:',
          validate.max_ranking_levels, (-2,))

  def test_options_valid(self):
    self.assertEqual(validate.options({}), {})
    self.assertEqual(validate.options(
          {'stop_at_majority': True}),
          {'stop_at_majority': True})
    self.assertEqual(validate.options(
          {'stop_at_majority': False}),
          {'stop_at_majority': False})
    self.assertEqual(validate.options(
          {'alternative_defeats': 'Y'}),
          {'alternative_defeats': 'Y'})
    self.assertEqual(validate.options(
          {'alternative_defeats': 'y'}),
          {'alternative_defeats': 'Y'})
    self.assertEqual(validate.options(
          {'alternative_defeats': 'N'}),
          {'alternative_defeats': 'N'})
    self.assertEqual(validate.options(
          {'alternative_defeats': ('y', 'n', 'y', 'Y')}),
          {'alternative_defeats': ('Y', 'N', 'Y', 'Y')})
    self.assertEqual(validate.options(
          {'alternative_defeats': ['y', 'n', 'N']}),
          {'alternative_defeats': ('Y', 'N', 'N')})
    self.assertEqual(validate.options(
          {'alternative_defeats': ' y n N Y'}),
          {'alternative_defeats': ('Y', 'N', 'N', 'Y')})

  def test_options_invalid(self):
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'options is not a dict:',
          validate.options, (7,))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'An option name is not a str:',
          validate.options, ({('junk',): True},))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'The option \'stop_at_majority\' must be True or False.',
          validate.options, ({'stop_at_majority': 1},))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid option value type:',
          validate.options, ({'alternative_defeats': True},))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid per-round option value:',
          validate.options, ({'alternative_defeats': ('Z',)},))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid per-round option value:',
          validate.options, ({'alternative_defeats': ['Z']},))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid per-round option value:',
          validate.options, ({'alternative_defeats': ' Z'},))
    _test_aids.assertRaises_with_message(self, errors.RcvValueError,
          'Invalid option name:',
          validate.options, ({'no_skipped_rankings': True},))

