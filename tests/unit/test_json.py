# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0

from __future__ import print_function

import unittest
import _test_aids
import _test_from_file

from _src import sb1288
from sb1288 import rcv
from sb1288 import with_json

import sys
import os
import os.path
import io
import subprocess

PYTHON_2_CMD = 'python'
PYTHON_3_CMD = 'python3'

class TestJson(unittest.TestCase):
  """Test with_json"""

  def setUp(self):
    self.save_maxDiff = self.maxDiff
    self.maxDiff = None

  def tearDown(self):
    self.maxDiff = self.save_maxDiff

  def with_json_other_modes(self, input_file, input_file_name,
        output_file_name):
    input_file.seek(0)
    save_stdout = sys.stdout
    test_stdout = io.StringIO()
    sys.stdout = test_stdout
    try:
      result = with_json.tabulate(input_file, '')
    finally:
      sys.stdout = save_stdout
    test_stdout.seek(0)
    output_str2 = test_stdout.read()
    command_words = [
          PYTHON_2_CMD if sys.version_info.major == 2 else PYTHON_3_CMD,
          '-m', 'sb1288.with_json', input_file_name, output_file_name]
    command_str = ' '.join(command_words)
    os.chdir('..')
    try:
      if os.path.isfile(output_file_name):
        os.remove(output_file_name)
      return_code = subprocess.call(command_str, shell=True)
      self.assertEqual(return_code, 0)
      with open(output_file_name, 'r') as json_result:
        output_str3 = json_result.read()
    finally:
      os.chdir('tests')
    return output_str2, output_str3



  def test_json_001(self):
    input_str = _test_aids.as_unicode(
          '{',
          '  "description": "Simple 3-candidate, 2-winner come-from-behind win"',
          '  ,"nbr_seats_to_fill": 2',
          '  ,"candidates": " A B C"',
          '  ,"ballots": [',
          '        [10, " A B C"],',
          '        [2,  " B C A"],',
          '        [3,  " C A B"]',
          '        ]',
          '  ,"max_ranking_levels": 3',
          '  ,"tie_breaker": " A B C"',
          '  ,"options": {}',
          '}'
          )

    expected_output_str = '''\
{
  "description": "Simple 3-candidate, 2-winner come-from-behind win",
  "elected": ["A", "B"],
  "status": [
    ["A", "elected", 1, 10.0],
    ["B", "elected", 2, 7.0],
    ["C", "defeated", 2, 3.0]
  ],
  "tally": {
    "A": [10.0, 5.0],
    "B": [2.0, 7.0],
    "C": [3.0, 3.0],
    ":Abstentions": [0.0, 0.0],
    ":Other exhausted": [0.0, 0.0],
    ":Overvotes": [0.0, 0.0],
    ":Residual surplus": [0.0, 0.0]
  }
}
'''
    input_file = io.StringIO(input_str)
    output_file = io.StringIO()
    result = with_json.tabulate(input_file, output_file)
    output_file.seek(0)
    output_str = output_file.read()
    self.assertEqual(output_str, expected_output_str)
    output_str2, output_str3 = self.with_json_other_modes(input_file,
          'tests/unit/json-001.json',
          'tests/temp_output/json-001-out.json')
    self.assertEqual(output_str2, expected_output_str)
    self.assertEqual(output_str3, expected_output_str)  
    
  def test_json_002(self):
    input_str = _test_aids.as_unicode(
          '{',
          '  "description": "Simple 4-candidate, from 3rd place to winner"',
          '  ,"nbr_seats_to_fill": 1',
          '  ,"candidates": " A B C D"',
          '  ,"ballots": [',
          '        [15, " A B C"],',
          '        [8, " D C B"],',
          '        [1,  " D"],',
          '        [1,  " D #"],',
          '        [8,  " C D A"],',
          '        [5,  " B C D"]',
          '        ]',
          '  ,"max_ranking_levels": 3',
          '  ,"tie_breaker": " A B C D"',
          '  ,"options": {}',
          '}'
          )

    expected_output_str = '''\
{
  "description": "Simple 4-candidate, from 3rd place to winner",
  "elected": ["C"],
  "status": [
    ["C", "elected", 3, 21],
    ["A", "defeated", 3, 15],
    ["D", "defeated", 2, 10],
    ["B", "defeated", 1, 5]
  ],
  "tally": {
    "C": [8, 13, 21],
    "A": [15, 15, 15],
    "D": [10, 10],
    "B": [5],
    ":Abstentions": [0, 0, 1],
    ":Other exhausted": [0, 0, 0],
    ":Overvotes": [0, 0, 1]
  }
}
'''
    input_file = io.StringIO(input_str)
    output_file = io.StringIO()
    result = with_json.tabulate(input_file, output_file)
    output_file.seek(0)
    output_str = output_file.read()
    self.assertEqual(output_str, expected_output_str)
    output_str2, output_str3 = self.with_json_other_modes(input_file,
          'tests/unit/json-002.json',
          'tests/temp_output/json-002-out.json')
    self.assertEqual(output_str2, expected_output_str)
    self.assertEqual(output_str3, expected_output_str)  

