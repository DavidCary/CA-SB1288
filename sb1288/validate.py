# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0
"""Validate and reformat RCV data"""

from __future__ import print_function

from sb1288 import errors
from sb1288 import constants as K
from sb1288.ballot import Ballot

import sys

# Convenience functions to use the Validator class
def nbr_seats_to_fill(nbr_seats_to_fill):
  """
  Validate the number of seats to fill, using the Validator class

  This is a convenience function for using the Validator class.

  """
  return Validator().nbr_seats_to_fill(nbr_seats_to_fill)

def candidates(candidates):
  """
  Validate a sequence of candidates, using the Validator class

  This is a convenience function for using the Validator class.

  """
  return Validator().candidates(candidates)

def ballots(ballots, candidates, max_ranking_levels):
  """
  Validate a sequence of candidates, using the Validator class

  This is a convenience function for using the Validator class.

  """
  return Validator().ballots(ballots, candidates, max_ranking_levels)

def max_ranking_levels(max_ranking_levels):
  """
  Validate the max number of ranking levels, using the Validator class

  This is a convenience function for using the Validator class.

  """
  return Validator().max_ranking_levels(max_ranking_levels)

def tie_breaker(tie_breaker, candidates):
  """
  Validate a tie breaker specification, using the Validator class

  This is a convenience function for using the Validator class.

  """
  return Validator().tie_breaker(tie_breaker, candidates)

def options(options):
  """
  Validate RCV tabulation options, using the Validator class

  This is a convenience function for using the Validator class.

  """
  return Validator().options(options)

def str_tuple(value):
  """
  Produce a tuple of strings

  Arguments
  ---------
  value
    A string, a list of strings, or a tuple of strings.

    For Python 2, where a string type is allowed, a unicode type may
    also be used, but must be strictly convertible to an ASCII string.

  Returns
  -------
  A tuple of zero or more strings.

  If value is a tuple of strings, that tuple is returned.

  If value is a list of strings, it is converted to a tuple of the same
  strings.

  If value is a string, then the string is split by its first character,
  whatever that is, and a tuple is created from the resulting list.  If
  value is an empty string or consists of a single charater, an empty
  tuple is returned.

  Raises
  ------
  TypeError
    If value is not as described above.

  """
  if sys.version_info[0] == 2 and type(value) == unicode:
    value = value.encode('utf-8')
  if type(value) == str:
    if value:
      result = tuple(value[1:].split(value[0]))
    else:
      result = tuple()
  elif type(value) == list or type(value) == tuple:
    result = []
    for item in value:
      if sys.version_info[0] == 2 and type(item) == unicode:
        item = item.encode('utf-8')
      if type(item) != str:
        value_type = str(type(value)).split("'")[1]
        raise TypeError('Item in {} is not a str:'.format(value_type)
              + '\n  {:25}=  {}'.format('item type', str(type(item)))
              + '\n  {:25}=  {}'.format('item value', repr(item)))
      result.append(item)
    result = tuple(result)
  else:
    raise TypeError('Can not make a str_tuple from a {}.'.
          format(str(type(value))))
  return result

class Validator(object):
  """
  A collection of validation and reformatting methods for RCV data
  """

  def nbr_seats_to_fill(self, nbr_seats_to_fill):
    """Validate the number of seats to fill

    Arguments
    ---------
    nbr_seats_to_fill
      Must be a positive int

    Returns
    -------
    nbr_seats_to_fill if it meets requirements.

    Raises
    ------
    RcvValueError
      If nbr_seats_to_fill does not meet requirements.

    """
    if type(nbr_seats_to_fill) != int:
      raise errors.RcvValueError('nbr_seats_to_fill not an int:', (
            ('type(nbr_seats_to_fill)', type(nbr_seats_to_fill)),
            ))
    if nbr_seats_to_fill <= 0:
      raise errors.RcvValueError('nbr_seats_to_fill not >= 1:', (
            ('nbr_seats_to_fill', nbr_seats_to_fill),
            ))
    return nbr_seats_to_fill

  def candidates(self, candidates):
    """
    Validate a specification of candidates names

    Arguments
    ---------
    candidates
      An ordered collection of strings, each a unique candidate name,
      which meets the requirements for rcv.tabulate().

    Returns
    -------
    A tuple of the candidate names, in the same order, if they meet
    requirements.

    Raises
    ------
    RcvValueError
      If the candidate names do not meet requirements.

    """
    try:
      candidates = str_tuple(candidates)
    except TypeError as exc:
      raise errors.RcvValueError('Invalid candidates type:', (), exc)
    for ix, name in enumerate(candidates):
      if name in K.RANKING_CODES_NOT_A_CANDIDATE or name[0] == ':':
        raise errors.RcvValueError('Invalid candidate name:', (
              ('candidate name', name),
              ('candidate name index', ix),
              ))
    if len(set(candidates)) != len(candidates):
      raise errors.RcvValueError('Candidate names are not unique.')
    return candidates

  def tie_breaker(self, tie_breaker, candidates):
    """
    Validate and convert a specification of a tie_breaker

    Arguments
    ---------
    tie_breaker
      An ordered collection of strings which meets the rcv.tabulate
      requirements for a tie_breaker.

    candidates
      A tuple of the names of all candidates.

    Returns
    -------
    A tie_breaker as a dictionary keyed by candidate names with the
    ordering indexes as values, if the tie_breaker argument meets
    requirements.

    Raises
    ------
    RcvValueError
      If the tie_breaker argument does not meet requirements.

    """
    try:
      tie_breaker = str_tuple(tie_breaker)
    except TypeError as exc:
      raise errors.RcvValueError('Invalid tie_breaker type:', (), exc)
    for ix, name in enumerate(tie_breaker):
      if name not in candidates:
        raise errors.RcvValueError('Invalid candidate name in tie_breaker:', (
              ('candidate name', name),
              ('tie_breaker index', ix),
              ))
    result = {candidate: index
          for index, candidate in enumerate(tie_breaker)}
    if len(result) != len(tie_breaker):
      raise errors.RcvValueError(
            'Candidate names in tie_breaker are not unique.')
    return result

  def ballots(self, ballots, candidates, max_ranking_levels):
    """
    Validate a specification of ballots

    Arguments
    ---------
    ballots
      A valid specification of ballots that meet the requirements of
      the rcv.tabulate function.

    candidates
      A tuple of all the names of all candidates.

    max_ranking_levels
      The maximum length of a ballot's rankings, possibly None.

    Returns
    -------
    A tuple of the ballots, each converted to a Ballot object, in the same
    order as ballots, if ballots meets requirements.

    Raises
    ------
    RcvValueError
      If the ballots do not meet requirements.

    """
    result = []
    if type(ballots) not in (list, tuple):
      raise errors.RcvValueError('ballots is not a list or tuple:', (
            ('type(ballots)', type(ballots)),
            ))
    for ix, ballot in enumerate(ballots):
      if type(ballot) not in (list, tuple):
        raise errors.RcvValueError('A ballot is not a list or tuple:', (
              ('type(ballot)', type(ballot)),
              ('ballot index', ix),
              ))
      if len(ballot) != 2:
        raise errors.RcvValueError('A ballot is not a pair of values:', (
              ('len(ballot)', len(ballot)),
              ('ballot index', ix),
              ))
      multiple = ballot[0]
      if type(multiple) != int:
        raise errors.RcvValueError('A ballot multiple is not an int:', (
              ('type(multiple)', type(multiple)),
              ('ballot index', ix),
              ))
      if multiple < 1:
        raise errors.RcvValueError('A ballot multiple is zero or less:', (
              ('multiple', multiple),
              ('ballot index', ix),
              ))
      try:
        rankings = str_tuple(ballot[1])
      except TypeError as exc:
        raise errors.RcvValueError('Invalid ballot rankings type:', (
              ('ballot index', ix),
              ), exc)
      if (max_ranking_levels is not None and
            len(rankings) > max_ranking_levels):
        raise errors.RcvValueError('Ballot rankings is too long:', (
              ('len(rankings)', len(rankings)),
              ('max_ranking_levels', max_ranking_levels),
              ('ballot index', ix),
              ))
      for rix, ranking_code in enumerate(rankings):
        if (ranking_code not in candidates and
              ranking_code not in K.RANKING_CODES_NOT_A_CANDIDATE):
          raise errors.RcvValueError('Invalid ballot ranking code:', (
                ('ranking code', ranking_code),
                ('ballot index', ix),
                ('ranking code index', rix),
                ))
      internal_ballot = Ballot(multiple, rankings)
      result.append(internal_ballot)
    result = tuple(result)
    return result

  def max_ranking_levels(self, max_ranking_levels):
    """Validate the maximum number of candidates that can be ranked

    Arguments
    ---------
    max_ranking_levels
      Must be None or an int that is at least three.

    Returns
    -------
    max_ranking_levels if it meets requirements.

    Raises
    ------
    RcvValueError
      If max_ranking_levels does not meet requirements.

    """
    if max_ranking_levels is None:
      return max_ranking_levels
    if type(max_ranking_levels) != int:
      raise errors.RcvValueError('max_ranking_levels not an int:', (
            ('type(max_ranking_levels)', type(max_ranking_levels)),
            ))
    if max_ranking_levels < K.MIN_RANKINGS_SUPPORTED:
      raise errors.RcvValueError('max_ranking_levels is less than {}:'.
            format(K.MIN_RANKINGS_SUPPORTED), (
            ('max_ranking_levels', max_ranking_levels),
            ))
    return max_ranking_levels

  def options(self, options):
    """Validate a dictionary of rcv.tabulate options

    Arguments
    ---------
    options
      A dictionary of options that are valid for the the rcv.tabulate
      function. An option is valid even if it might not be used.

    Returns
    -------
    An options dictionary, if the options argument meets requirements.

    Raises
    ------
    RcvValueError
      If options does not meet requirements.

    """
    result = {}
    if type(options) != dict:
      raise errors.RcvValueError('options is not a dict:', (
            ('type(options)', type(options)),
            ))
    for name, value in options.items():
      if type(name) != str:
        raise errors.RcvValueError('An option name is not a str:', (
              ('option name', name),
              ))
      if name == K.OPTION_STOP_AT_MAJORITY:
        if value is not True and value is not False:
          raise errors.RcvValueError('The option {} must be True or False.'.
                format(repr(K.OPTION_STOP_AT_MAJORITY)))
        result[K.OPTION_STOP_AT_MAJORITY] = value
      elif name == K.OPTION_ALTERNATIVE_DEFEATS:
        if (type(value) == str and value.upper() in
              K.OPTION_ALTERNATIVE_DEFEATS_VALUE_SET):
          value = value.upper()
        else:
          try:
            value = str_tuple(value)
          except TypeError as exc:
            raise errors.RcvValueError(
                  'Invalid option value type:', (
                  ('option name', K.OPTION_ALTERNATIVE_DEFEATS),
                  ), exc)
          for ix, per_round_value in enumerate(value):
            if (per_round_value.upper() not in
                  K.OPTION_ALTERNATIVE_DEFEATS_VALUE_SET):
              raise errors.RcvValueError('Invalid per-round option value:', (
                    ('per-round value', per_round_value),
                    ('index', ix),
                    ('for round', ix + 1),
                    ('option name', K.OPTION_ALTERNATIVE_DEFEATS),
                    ))
          value = tuple([per_round_value.upper() for per_round_value in value])
        result[K.OPTION_ALTERNATIVE_DEFEATS] = value
      else:
        raise errors.RcvValueError('Invalid option name:', (
          ('option name', name),
          ))
    return result

