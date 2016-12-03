# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0
"""Run test cases based on JSON files """

from __future__ import print_function

import _test_aids

from _src import sb1288
from sb1288 import with_json
from sb1288 import rcv
from sb1288 import validate
from sb1288 import constants as K

import json
import os.path

u2s = with_json.u2s

def run_test_spec(test_case, input_json):
  """
  Run a test case using test specs from a JSON text file
  """
  tabulate_args, test_spec = with_json.build_tabulate_args(
        input_json, 'all-tests-spec.json')
  if 'maxDiff' in test_spec:
    maxDiff = test_spec['maxDiff']
    if maxDiff is None:
      test_case.maxDiff = None
    if type(maxDiff) == int and maxDiff >= 0:
      test_case.maxDiff = maxDiff

  try: print_description = test_spec['print_description']
  except KeyError: print_description = False
  if print_description:
    print('\n  """' + test_spec['description'] + '"""')

  if 'exception' in test_spec:
    exception_type, exception_message = test_spec['exception']
    _test_aids.assertRaises_with_message(test_case,
          u2s(exception_type),
          u2s(exception_message),
          rcv.tabulate, tabulate_args)
  else:
    expected_elected = validate.str_tuple(test_spec['elected'])
    expected_status = _test_aids.build_expected_status(
          test_spec['status_codes'])
    expected_tally = {_test_aids.u2s(candidate): 
          [K.Decimal(vote_total) if test_spec['nbr_seats_to_fill'] > 1
              else vote_total
          for vote_total in votes]
          for candidate, votes in test_spec['tally'].items()}
    elected, status, tally = rcv.Tabulation(*tabulate_args).tabulate()
    if 'print_results' in test_spec and test_spec['print_results']:
      print_elected(elected)
      print_status(status)
      print_tally(tally)
      try: description = test_spec['description']
      except KeyError: description = None
      jason_str = with_json.results_to_json(elected, status, tally,
            description)
      print(jason_str)
    status_dict = {candidate: status.as_dict()
          for candidate, status in status.items()}
    test_case.assertEqual(tally, expected_tally)
    test_case.assertEqual(status_dict, expected_status)
    test_case.assertEqual(set(elected), set(expected_elected))

# The following are convenience debugging methods

def print_elected(elected):
  """
  Print a list of elected candidates; for debugging
  """
  print("elected:", sorted(elected))

def print_status(status):
  """
  Print a dictionary of candidate status; for debugging
  """
  print("status:")
  sorted_status = sorted(status.items())
  for candidate, cand_status in sorted_status:
    print("%5s: %s" % (candidate, str(cand_status)))

def print_tally(tally):
  """
  Print a dictionary of tabulation vote totals by round; for debugging
  """
  print("tally:")
  sorted_tally = sorted(tally.items())
  for tally_key, tally_votes in sorted_tally:
    print("%20s: " % tally_key, end="")
    for votes in tally_votes:
      print("%9s " % votes, end="")
    print()

