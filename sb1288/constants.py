# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0
"""Constants for an RCV tabulation"""

from sb1288.decimal5 import Decimal5 as Decimal
from sb1288.decimal5 import Decimal5Total as DecimalTotal

ZERO = Decimal(0)
ONE = Decimal(1)

MIN_RANKINGS_SUPPORTED = 3

RANKING_CODE_SKIPPED = ''
RANKING_CODE_OVERVOTE = '#'
RANKING_CODES_NOT_A_CANDIDATE = set((
      RANKING_CODE_SKIPPED,
      RANKING_CODE_OVERVOTE))

LABEL_OVERVOTES = ':Overvotes'
LABEL_ABSTENTIONS = ':Abstentions'
LABEL_OTHER_EXHAUSTED = ':Other exhausted'
LABEL_RESIDUAL_SURPLUS = ':Residual surplus'

OTHER_LABELS_LIST = [
      LABEL_OVERVOTES, LABEL_ABSTENTIONS, LABEL_OTHER_EXHAUSTED,
      LABEL_RESIDUAL_SURPLUS]

OPTION_STOP_AT_MAJORITY = 'stop_at_majority'
OPTION_ALTERNATIVE_DEFEATS = 'alternative_defeats'
OPTION_KEY_SET = set([
      OPTION_STOP_AT_MAJORITY,
      OPTION_ALTERNATIVE_DEFEATS,
      ])
OPTION_ALTERNATIVE_DEFEATS_YES = 'Y'
OPTION_ALTERNATIVE_DEFEATS_NEVER = 'N'
OPTION_ALTERNATIVE_DEFEATS_VALUE_SET = set([
      OPTION_ALTERNATIVE_DEFEATS_YES,
      OPTION_ALTERNATIVE_DEFEATS_NEVER,
      ])

STATUS_CONTINUING = 'continuing'
STATUS_DEFEATED = 'defeated'
STATUS_ELECTED = 'elected'
