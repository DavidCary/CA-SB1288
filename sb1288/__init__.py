# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0
"""
A reference implementation for tabulating RCV per California SB 1288
"""

import sys

from .rcv import tabulate
from .with_json import tabulate as tabulate_with_json
from .status import Status

