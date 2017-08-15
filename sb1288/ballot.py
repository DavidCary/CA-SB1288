# -*- encoding=utf-8 -*-
# Copyright 2016-2017 David Cary; licensed under the Apache License,
#       Version 2.0
"""Support a ballot during RCV tabulation"""

from __future__ import print_function

from sb1288 import errors
import sb1288.constants as K
from sb1288.constants import Decimal

class Ballot(object):
  """A class representing a ballot during RCV tabulation """

  _multiple = 0
  _rankings = tuple()
  _transfer_value = K.ONE
  _current_index = 0

  def __init__(self, multiple, rankings):
    """
    Initialize an RCV tabulation ballot

    The ballot class represents a group of ballots, all of
    which have the same rankings.

    The requirements for the arguments are the same as for a ballot
    group in the ballots argument for the rcv.tabulate() function.  The
    arguments should already have been processed by an appropriate
    validation and formatting routine.

    Arguments
    ---------
    multiple
      The number of ballots in the ballot group.

    rankings
      The candidate rankings for the ballot group.

    """

    self._multiple = multiple
    self._rankings = rankings

  def get_hrcc(self,
        continuing_candidates, max_ranking_levels):
    """
    Get the highest-ranked continuing candidate

    If such a candidate does not exist, get the appropriate label
    indicating how the ballot should be counted.

    Arguments
    ---------
    continuing_candidates
      A list, set, or dictionary of the continuing candidate names.

    max_nbr_rankings
      The maximum number of candidates that a voter may rank on a ballot.

    Returns
    -------
    A candidate name or other tabulation label for which the ballot next
    counts.


    This method assumes that for a specific ballot object, the collection of
    continuing candidates is a subset of the collection given in any previous
    calls.

    """

    for ix, ranking_code in enumerate(self._rankings[self._current_index:]):
      if ranking_code == K.RANKING_CODE_OVERVOTE:
        self._current_index = ix
        return K.LABEL_OVERVOTES
      if ranking_code in continuing_candidates:
        self._current_index = ix
        return ranking_code
    else:
      self._current_index = len(self._rankings)
      if max_ranking_levels > len(set(
            [ranking_code for ranking_code in self._rankings
            if ranking_code != K.RANKING_CODE_SKIPPED and
            ranking_code != K.RANKING_CODE_OVERVOTE])):
        return K.LABEL_ABSTENTIONS
      else:
        return K.LABEL_OTHER_EXHAUSTED

  def total_votes(self):
    """Get the number of total votes for this ballot group"""
    return self.get_transfer_value() * self.get_multiple()

  def get_multiple(self):
    """Get the number of ballots in this ballot group"""
    return self._multiple

  def get_transfer_value(self):
    """Get the current transfer value"""
    return self._transfer_value

  def update_transfer_value(self, surplus_factor):
    """Update the transfer value with the surplus factor

    The new transfer value is the surplus_factor times the current
    transfer value, rounding down (truncating for positive values).

    The new transfer value is returned.

    Arguments:
    ----------
    surplus_factor
    A Decimal value between 0 and 1 inclusive.

    Returns:
    --------
    The new transfer value.

    """

    self._transfer_value *= surplus_factor
    return self._transfer_value

  def __repr__(self):
    """Convert ballot to a string that shows the transfer value"""
    result = '({}, {}, {})'.format(self._multiple, self._transfer_value,
        self._rankings)
    return result

  def __str__(self):
    """Convert ballot to a string that does not show the transfer value"""
    result = '({}, {})'.format(self._multiple, self._rankings)
    return result

  def as_tuple(self):
    result = (self._multiple, self._transfer_value, self._rankings)
    return result

  def __eq__(self, other):
    """
    Is self equal to other?

    Equality is based on self's attributes for _multiple, rankings, and
    _transfer_value.  The argument other may have correspondingly named
    attributes or indexable keys.  Attributes of other take precedence
    over indexable keys.

    """
    is_equal = True
    try:
      if ((hasattr(other, '_multiple') and
            self._multiple == other._multiple) or
            (hasattr(other, '__getitem__') and
            self._multiple == other['_multiple'])):
        pass
      else:
        return False
      if ((hasattr(other, '_rankings') and
            self._rankings == other._rankings) or
            (hasattr(other, '__getitem__') and
            self._rankings == other['_rankings'])):
        pass
      else:
        return False
      if ((hasattr(other, '_transfer_value') and
            self._transfer_value == other._transfer_value) or
            (hasattr(other, '__getitem__') and
            self._transfer_value == other['_transfer_value'])):
        pass
      else:
        return False
    except Exception as exc:
      is_equal = False
    return is_equal

  def __ne__(self, other):
    """negation of __eq__"""
    return not self.__eq__(other)


