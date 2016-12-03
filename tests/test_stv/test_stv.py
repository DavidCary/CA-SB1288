# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0

import unittest
import _test_aids
import _test_from_file

from _src import sb1288
from sb1288 import rcv


class TestStvFromFiles(unittest.TestCase):
  """Test STV from file-based specs"""

  def setUp(self):
    self.save_maxDiff = self.maxDiff
    self.maxDiff = 800

  def test_stv_001(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-001.json')

  def test_stv_002_1(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-002-1.json')

  def test_stv_002_2(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-002-2.json')

  def test_stv_002_3(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-002-3.json')

  def test_stv_004(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-004.json')

  def test_stv_005(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-005.json')

  def test_stv_005_aa(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-005-aa.json')

  def test_stv_005_oo(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-005-oo.json')

  def test_stv_005_t1(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-005-t1.json')

  def test_stv_005_ta(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-005-ta.json')

  def test_stv_005_to(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-005-to.json')

  def test_stv_006_1(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-006-1.json')

  def test_stv_006_2(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-006-2.json')

  def test_stv_007_1(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-007-1.json')

  def test_stv_007_2(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-007-2.json')

  def test_stv_007_3(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-007-3.json')

  def test_stv_007_4(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-007-4.json')

  def test_stv_008_1(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-008-1.json')

  def test_stv_008_2(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-008-2.json')

  def test_stv_008_3(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-008-3.json')

  def test_stv_008_4(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-008-4.json')

  def test_stv_008_5(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-008-5.json')

  def test_stv_020_1(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-020-1.json')

  def test_stv_020_2(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-020-2.json')

  def test_stv_020_3(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-020-3.json')

  def test_stv_020_4(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-020-4.json')

  def test_stv_020_5(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-020-5.json')

  def test_stv_020_6(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-020-6.json')

  def test_stv_021_1(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-021-1.json')

  def test_stv_021_2(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-021-2.json')

  def test_stv_021_3(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-021-3.json')

  def test_stv_021_4(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-021-4.json')

  def test_stv_021_5(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-021-5.json')

  def test_stv_101_1(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-101-1.json')

  def test_stv_022_1(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-022-1.json')

  def test_stv_022_2(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-022-2.json')

  def test_stv_022_3(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-022-3.json')

  def test_stv_022_4(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-022-4.json')

  def test_stv_023_1(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-023-1.json')

  def test_stv_024_1(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-024-1.json')

  def test_stv_024_2(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-024-2.json')

  def test_stv_024_3(self):
    _test_from_file.run_test_spec(self, 'test_stv/stv-024-3.json')

