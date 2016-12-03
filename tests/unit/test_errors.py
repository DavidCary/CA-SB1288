# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0

import unittest
import _test_aids

from _src import sb1288
from sb1288 import errors

import sys
import re

class TestErrors(unittest.TestCase):
  """Test Errors"""

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

  def test_indent_message(self):
    self.assertEqual(errors.indent_message('Hello'), '  Hello')
    self.assertEqual(errors.indent_message('Hello\n'), '  Hello\n')
    self.assertEqual(errors.indent_message('Hello\nagain'), '  Hello\n  again')
    self.assertEqual(errors.indent_message(
          'Hello\nagain\n'), '  Hello\n  again\n')
    self.assertEqual(errors.indent_message(
          'Hello\n  again\n'), '  Hello\n    again\n')
    self.assertEqual(errors.indent_message(
          'Hello\n\nagain\n'), '  Hello\n  \n  again\n')
    self.assertEqual(errors.indent_message(''), '  ')
    self.assertEqual(errors.indent_message('Hello', indent_by=4), '    Hello')
    self.assertEqual(errors.indent_message(
          'Hello\n', indent_by=4), '    Hello\n')
    self.assertEqual(errors.indent_message(
          'Hello\nagain', indent_by=4), '    Hello\n    again')
    if False:
      _test_aids.assertRaises_with_message(self,
          decimal5.Decimal5Error,
          'Value is not a supported type: type=\'<class \'str\'>\', ' +
          'str(value)=\'2.8\'',
          D5, ('2.8',))

  def test_describe_exc(self):
    self.maxDiff = 4096
    message = None
    try:
      raise ValueError('This is a test ValueError', 7)
    except ValueError as exc:
      message = str(exc)
      description = errors.describe_exc(exc)
    self.assertEqual(message, '(\'This is a test ValueError\', 7)')
    #print(); print(description)
    qualifier = 'exceptions.' if sys.version_info.major == 2 else ''
    match = re.match('^Exception description:\n' +
          '  ' + qualifier + 'ValueError:\n' +
          '    \\(\'This is a test ValueError\', 7\\)\n' +
          '  Raised at:\n    File[^\n]*\n' +
          '      raise ValueError\\(\'This is a test ValueError\', 7\\)\n' +
          '  Caught at:\n    File[^\n]*\n' +
          '      description = errors.describe_exc\\(exc\\)\n' +
          '  Stack before try:\n(    File[^\n]*\n      [^\n]*\n)+' +
          '  Stack after try:\n(    File[^\n]*\n      [^\n]*\n)+' +
          'END Exception description$', 
        description)
    self.assertTrue(match)

  def test_RcvValueError_message(self):
    self.maxDiff = 4096
    self.assertEqual(self.get_exception_message(errors.RcvValueError, (
          'This is a test RcvValueError error.',
          )),
          'This is a test RcvValueError error.')

  def test_RcvValueError_message2(self):
    self.maxDiff = 4096
    self.assertEqual(self.get_exception_message(errors.RcvValueError, (
          'This is a test RcvValueError error.',
          'more info',
          )),
          'This is a test RcvValueError error.'
          + '\n  \'more info\'')
    self.assertEqual(self.get_exception_message(errors.RcvValueError, (
          'This is a test RcvValueError error.',
          ['more info:', ('problem index', 17),
          ('expected value', 'Fred')],
          )),
          'This is a test RcvValueError error.'
          + '\n  \'more info:\''
          + '\n  problem index            =  17'
          + '\n  expected value           =  \'Fred\'')

  def test_RcvImplementationError_message(self):
    self.maxDiff = 4096
    message = None
    try:
      raise ValueError('Testing: String is too long.')
    except ValueError as exc:
       message = self.get_exception_message(errors.RcvImplementationError, (
             'Testing: unexpected exception:', (), exc
             ))
    #print(message)
    qualifier = 'exceptions.' if sys.version_info.major == 2 else ''
    match = re.match('^' +
          'Testing: unexpected exception:\n' +
          '  Exception description:\n' +
          '    ' + qualifier + 'ValueError:\n' +
          '      Testing: String is too long.\n' +
          '    Raised at:\n      File[^\n]*\n' +
          '        raise ValueError\\(\'Testing: String is too long.\'\\)\n' +
          '    Caught at:\n      File[^\n]*\n' +
          '        self\\.base_exception_description =' +
          ' describe_exc\\(self\\.base_exception\\)\n' +
          '    Stack before try:\n(      File[^\n]*\n        [^\n]*\n)+' +
          '    Stack after try:\n(      File[^\n]*\n        [^\n]*\n)+' +
          # '([^\n]*\n)*' +
          '  END Exception description$', 
          message)
    self.assertTrue(match)
 
