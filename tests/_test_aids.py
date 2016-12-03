# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0
"""Functions that support testing """

import sys

from _src import sb1288
from sb1288 import constants as K
from sb1288 import with_json

u2s = with_json.u2s


def assertRaises_with_message(test_case, expected_exception, expected_message,
      raising_callable, args):
  """Run a test case that is expected to raise an exception"""
  print_message = False
  verify_message = False
  exception_message = None

  try:
    raising_callable(*args)
  except Exception as exc:
    
    if ((type(expected_exception) == str and
          str(type(exc)).split("'")[1].split('.')[-1] == expected_exception)
          or
          type(exc) == expected_exception):
      if print_message:
        print()
        print('Exception, {}, raised with message:'.
              format(str(type(exc))))
        print(str(exc))
      exception_message = str(exc).split('\n')[0]
      verify_message = True
    else:
      raise
  else:
    test_case.fail('An expected exception of type {} was not raised.'. 
          format(str(expected_exception)))
  if verify_message:
    if type(expected_message) == str: 
      test_case.assertEqual(exception_message, expected_message)
    else:
      test_case.assertIn(exception_message, expected_message)

def build_expected_status(status_codes):
  """Build an expected status, given an iterable of status codes"""
  result = {u2s(candidate): {'candidate': u2s(candidate),
        'status': u2s(status), 'nbr_round': nbr_round,
        'votes': K.Decimal(votes) if type(votes) == float else votes}
        for candidate, status, nbr_round, votes in status_codes}
  return result

def build_stv_tally(tally):
  """Build an STV tally, converting votes totals to Decimal"""
  result = {u2s(category):
        [K.Decimal(vote_total)
        for vote_total in votes]  
        for category, votes in tally.items()}
  return result

def as_unicode(*lines):
  result = '' if sys.version_info[0] > 2 else ''.decode('ascii')
  for ix, line in enumerate(lines):
    if ix < len(lines) - 1:
      line += '\n'
    result += line if sys.version_info[0] > 2 else line.decode('ascii')
  return result

