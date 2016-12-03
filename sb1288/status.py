# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0
"""RCV classes and functions that are shared between IRV and STV"""

from sb1288 import constants as K
from sb1288 import errors

class Status(object):
  """
  RCV tabulation status for a candidate

  Attributes
  ----------
  The following attributes are directly accessible and setable.  Their
  intended usage is also described.

  candidate
    The name of the candidate.

  status
    A string showing whether the candidate is a continuing candidate, is
    elected, or is defeated.

  nbr_round
    For a continuing candidate, None.  Otherwise, the 1-based number of
    the round in which the candidate was elected or defeated.

  votes
    The number of votes a candidate had at the time the candidate was
    elected or defeated.  The votes for a continuing candidate is set to
    the votes tallied for the candidate at the beginning of the round.

    Votes for an IRV tabulation are integers.  Votes for an STV
    tabulation are objects of the special, fixed decimal class Decimal5,
    a.k.a Decimal.

  """
  def __init__(self, candidate, votes=0, nbr_round=None,
        status=K.STATUS_CONTINUING):
    """
    Initialize a Status object

    If candidate is a dictionary, set the properties to the values of
    the corresponding keys.  Otherwise, set the properties to the
    corresponding arguments.

    Arguments
    ---------
    candidate
      The name of the candidate.

    votes
      The number of votes for the candidate.
      Default value: 0

    nbr_round
      The 1-based number of the round for which this status applies or
      first began to apply.
      Default value: None

    status
      A string value indicating the status of the candidate.
      Default value: K.STATUS_CONTINUING

    """
    if type(candidate) == dict:
      self.candidate = candidate['candidate']
      self.votes = candidate['votes']
      self.nbr_round = candidate['nbr_round']
      self.status = candidate['status']
    else:
      self.candidate = candidate
      self.votes = votes
      self.nbr_round = nbr_round
      self.status = status

  def as_dict(self):
    """
    Create a corresponding dictionary

    Returns
    -------
    A dictionary that has keys and values corresponding to the
    properties of this object.

    """
    result = {'candidate': self.candidate, 'votes': self.votes,
          'nbr_round': self.nbr_round, 'status': self.status}
    return result

  def as_tuple(self, as_float=False):
    """
    Create a corresponding tuple

    Arguments
    ---------
    as_float
      if evaluates to True, convert non-integer value (Decimal5
      objects) to float, via a conversion to string.

    Returns
    -------
    A tuple showing the values in order of:
      (candidate, status, nbr_round, votes)

    """
    result = (self.candidate, self.status, self.nbr_round,
        self.votes if type(self.votes) == int
        else float(str(self.votes)))
    return result

  def __str__(self):
    result = '{'
    result += 'candidate: ' + repr(self.candidate)
    result += ', status: ' + repr(self.status)
    result += ', nbr_round: ' + str(self.nbr_round)
    result += ', votes: ' + str(self.votes) + '}'
    return result


  def __eq__(self, other):
    """
    Is self equal to other?

    Equality is based on self's attributes for candidate, votes,
    nbr_round, and status.  The argument other may have correspondingly
    named attributes or indexable keys.  Attributes of other take
    precedence over indexable keys.

    """
    is_equal = True
    try:
      if ((hasattr(other, 'candidate') and
            self.candidate == other.candidate) or
            (hasattr(other, '__getitem__') and
            self.candidate == other['candidate'])):
        pass
      else:
        return False
      if ((hasattr(other, 'status') and
            self.status == other.status) or
            (hasattr(other, '__getitem__') and
            self.status == other['status'])):
        pass
      else:
        return False
      if ((hasattr(other, 'nbr_round') and
            self.nbr_round == other.nbr_round) or
            (hasattr(other, '__getitem__') and
            self.nbr_round == other['nbr_round'])):
        pass
      else:
        return False
      if ((hasattr(other, 'votes') and
            self.votes == other.votes) or
            (hasattr(other, '__getitem__') and
            self.votes == other['votes'])):
        pass
      else:
        return False
    except Exception as exc:
      is_equal = False
    return is_equal

  def __ne__(self, other):
    """negation of __eq__"""
    return not self.__eq__(other)


