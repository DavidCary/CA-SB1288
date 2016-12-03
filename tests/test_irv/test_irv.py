# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0

import unittest
import _test_aids
import _test_from_file

from _src import sb1288
from sb1288 import rcv


class TestIrvFromFiles(unittest.TestCase):
  """Test IRV from file-based specs"""

  def setUp(self):
    self.save_maxDiff = self.maxDiff
    self.maxDiff = 800

  def test_irv_001(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-001.json')


  def test_irv_002(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-002.json')

  def test_irv_003(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-003.json')

  def test_irv_004(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-004.json')

  def test_irv_005(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-005.json')

  def test_irv_005_aa(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-005-aa.json')

  def test_irv_005_oo(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-005-oo.json')

  def test_irv_005_ta(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-005-ta.json')

  def test_irv_005_to(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-005-to.json')

  def test_irv_005_t1(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-005-t1.json')

  def test_irv_006_1(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-006-1.json')

  def test_irv_006_2(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-006-2.json')

  def test_irv_007_1(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-007-1.json')

  def test_irv_007_2(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-007-2.json')

  def test_irv_007_3(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-007-3.json')

  def test_irv_007_4(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-007-4.json')

  def test_irv_008_1(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-008-1.json')

  def test_irv_008_2(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-008-2.json')

  def test_irv_008_3(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-008-3.json')

  def test_irv_008_4(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-008-4.json')

  def test_irv_009(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-009.json')

  def test_irv_010_1(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-010-1.json')

  def test_irv_010_2(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-010-2.json')

  def test_irv_010_3(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-010-3.json')

  def test_irv_010_4(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-010-4.json')

  def test_irv_011_1(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-011-1.json')

  def test_irv_011_2(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-011-2.json')

  def test_irv_011_3(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-011-3.json')

  def test_irv_011_4(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-011-4.json')

  def test_irv_012_1(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-012-1.json')

  def test_irv_012_2(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-012-2.json')

  def test_irv_012_3(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-012-3.json')

  def test_irv_012_4(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-012-4.json')

  def test_irv_012_5(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-012-5.json')

  def test_irv_013_1(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-013-1.json')

  def test_irv_013_2(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-013-2.json')

  def test_irv_013_3(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-013-3.json')

  def test_irv_013_4(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-013-4.json')

  def test_irv_014_1(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-014-1.json')

  def test_irv_014_2(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-014-2.json')

  def test_irv_014_3(self):
    _test_from_file.run_test_spec(self, 'test_irv/irv-014-3.json')

