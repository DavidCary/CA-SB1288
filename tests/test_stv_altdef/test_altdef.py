# -*- encoding=utf-8 -*-
# Copyright 2016-2017 David Cary; licensed under the Apache License,
#       Version 2.0

import unittest
import _test_aids
import _test_from_file

from _src import sb1288
from sb1288 import rcv


class TestStvAltDefeatsFromFiles(unittest.TestCase):
  """Test STV from file-based specs for alternative defeats"""

  def setUp(self):
    self.save_maxDiff = self.maxDiff
    self.maxDiff = 800

  def test_altdef_000_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-000-1.json')

  def test_altdef_000_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-000-2.json')

  def test_altdef_001_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-001-1.json')

  def test_altdef_001_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-001-2.json')

  def test_altdef_002_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-002-1.json')

  def test_altdef_002_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-002-2.json')

  def test_altdef_003_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-003-1.json')

  def test_altdef_003_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-003-2.json')

  def test_altdef_004_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-004-1.json')

  def test_altdef_004_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-004-2.json')

  def test_altdef_005_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-005-1.json')

  def test_altdef_005_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-005-2.json')

  def test_altdef_011_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-011-1.json')

  def test_altdef_011_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-011-2.json')

  def test_altdef_012_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-012-1.json')

  def test_altdef_012_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-012-2.json')

  def test_altdef_013_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-013-1.json')

  def test_altdef_013_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-013-2.json')

  def test_altdef_014_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-014-1.json')

  def test_altdef_014_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-014-2.json')

  def test_altdef_015_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-015-1.json')

  def test_altdef_015_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-015-2.json')

  def test_altdef_016_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-016-1.json')

  def test_altdef_016_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-016-2.json')

  def test_altdef_017_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-017-1.json')

  def test_altdef_017_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-017-2.json')

  # for test conditions for test_altdef_018*, see altdef test 13

  def test_altdef_019_1(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-019-1.json')

  def test_altdef_019_2(self):
    _test_from_file.run_test_spec(self, 'test_stv_altdef/altdef-019-2.json')

