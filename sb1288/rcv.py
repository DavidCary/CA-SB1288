# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0
"""Tabulate ranked choice voting (RCV) per California SB 1288"""

from __future__ import print_function

from sb1288 import constants as K
from sb1288 import errors
from sb1288.ballot import Ballot  # this is probably not needed
from sb1288 import status
from sb1288 import validate

# A convenience method to the RcvTabulation class

def tabulate(nbr_seats_to_fill, candidates, ballots,
      max_ranking_levels, tie_breaker, options={}):
  """
  Tabulate an RCV contest per California SB 1288

  This is a convenience function for accessing the Tabulation class.

  Create an instance of the Tabulation class, using the supplied
  arguments, then call the instance's tabulate() method, returning the
  results from that method.

  Arguments
  ---------
  The same as the __init__ method of the Tabulation class.

  Returns
  -------
  The same as the tabulate method of the Tabulation class.

  Raises
  ------
  The same as the tabulate method of the Tabulation class.

  """
  return Tabulation(nbr_seats_to_fill, candidates, ballots,
      max_ranking_levels, tie_breaker, options
      ).tabulate()

class Tabulation(object):
  """
  A class for RCV tabulations per California SB 1288.

  Demonstrate the core tabulation logic for RCV.  Both instant runoff
  voting (IRV) and single transferable vote (STV) tabulations can be
  performed.

  Typical use of this class is to instantiate it and then run its
  tabulate() method to get the results.

  """


  def __init__(self, nbr_seats_to_fill, candidates, ballots,
        max_ranking_levels, tie_breaker, options={}):
    """
    Initialize a tabulation for an RCV contest per California SB 1288

    Terminology
    -----------

    Several arguments or parts of an argument, namely candidates,
    rankings in a ballot, tie_breaker, and the value of the
    'alternative_defeats' option, are or may be an ordered collection of
    string values.

    An ordered collection of string values may be represented as one of
    the following:

      - a tuple of strings
      - a list of strings
      - a string that is either the empty string, representing an empty
        tuple, or a delimiter separated list of string values where the
        first character of the string is the delimiter.  The delimiter
        character may not be part of any of the component string
        values.

    The following Python expressions specify equivalent ordered
    collections of string values::

      ('A', 'B', '', 'C', '#', 'D')
      ['A', 'B', '', 'C', '#', 'D']
      ' A B  C # D'
      '|A|B||C|#|D'


    Arguments
    ---------
    nbr_seats_to_fill
      The number of seats to fill, an integer that is at least one (also
      referred to as the number of winners or the number of candidates
      to elect).

    candidates
      An ordered collection of strings, each representing a unique
      candidate.  Candidate names may not begin with a colon (':'), may
      not be the empty string, and may not be the string '#'.

    ballots
      A list or tuple of ballot groups.  A ballot group represents a
      number of ballots with the same rankings.  A ballot group is a
      list or tuple of length two with the following values:

        multiple
          A positive integer indicating how many individual ballots are
          summarized into this ballot group.

        rankings
          An ordered collection of strings, each of which is a candidate
          name or other ranking code, ordered from most preferred first
          to least preferred last.

          Other ranking codes are:
            - the empty string, indicating a skipped ranking
            - the string '#', indicating an overvote ranking

          Trailing and skipped ranking codes do not have to be
          specified.

          Note: This representation of candidate rankings relies on an
          implicit numerical ranking equal to the index of the
          ennumeration of a candidate name and use of the special string
          '#' to indicate an overvote.


    max_ranking_levels
      The maximum number of candidates that each voter is allowed to
      rank on a ballot, i.e. the maximum length of a ballot's rankings,
      when expressed as a tuple. The value for max_ranking_levels must
      be None or an integer that is at least three.  If it is None,
      there is no restriction on the length of a ballot's rankings.

    tie_breaker
      A specification of candidate names.  When two or more
      candidates are tied to be defeated, the earlier candidate is
      chosen to be defeated.

      The tie_breaker represents a random ordering of the candidates,
      determined by lot conducted in public with notice.  This is a
      sufficient tie breaking procedure which is allowed by SB 1288,
      although other procedures are also allowed.

    options
      A dictionary of tabulation options, containing zero or more of the
      following keys and values.
      Default value: a dictionary with each option's default value.

        'stop_at_majority'
          A boolean value indicating that an IRV tabulation should stop
          in the first round that demonstrates a candidate with a
          majority of votes, even if there are more than two continuing
          candidates.
          Default value: False

        'alternative_defeats'
          A value indicating when the option to perform alternative
          defeats should be exercised if they are allowed.  The value
          may be a string or an ordered collection of string values.
          Default value: 'N'

          Performing alternative defeats for IRV consists of defeating
          multiple candidates in a round and is an option explicitly
          permitted by SB 1288.  Alternate defeats for STV are not
          explicitly permitted by SB 1288 but could be a modification to
          the STV vote counting rules that the California Secretary of
          State could authorize.  The option is currently ignored for
          multi-seat contests.

          The value for this option may be one of the following
          case-insensitive string values, indicating when to do
          alternative defeats, if they are allowed:

            'Y' yes, always

            'N' no, never

          The value for this option may also be an ordered collection of
          string values, each string equal to one of the values listed
          above, one for each round of the tabulation.  Extra values in
          the tuple are allowed and are ignored.

          SB 1288 allows greater flexibility in choosing for which
          rounds the alternative defeats option is exercised.  Any
          sequence of round-by-round choices may be replicated with this
          option.

    Raises
    ------
    Same as for Tabulation.tabulate()

    """
    try:
      self.nbr_seats_to_fill = nbr_seats_to_fill
      self.candidates = candidates
      self.ballots = ballots
      self.max_ranking_levels = max_ranking_levels
      self.tie_breaker = tie_breaker
      self.options = options
      validator = validate.Validator()
      self.nbr_seats_to_fill = validator.nbr_seats_to_fill(
            self.nbr_seats_to_fill)
      self.candidates = validator.candidates(self.candidates)
      self.max_ranking_levels = validator.max_ranking_levels(
            self.max_ranking_levels)
      self.ballots = validator.ballots(self.ballots,
            self.candidates, self.max_ranking_levels)
      self.tie_breaker = validator.tie_breaker(self.tie_breaker,
            self.candidates)
      options_validated = validator.options(self.options)
      self.options = {K.OPTION_STOP_AT_MAJORITY: False,
          K.OPTION_ALTERNATIVE_DEFEATS:
          K.OPTION_ALTERNATIVE_DEFEATS_NEVER,
            }
      self.options.update(options_validated)
    except (errors.RcvValueError, errors.RcvImplementationError):
      raise
    except (MemoryError, SystemError):
      raise
    except Exception as exc:
      raise errors.RcvImplementationError(
            'Possible RCV implementation error:', (), exc)

  def tabulate(self, **kwargs):
    """
    Perform a tabulation of an RCV contest per SB 1288

    Arguments
    ---------
    Normally this method is called with no arguments.  However to
    facilitate unit testing, the following arguments may be provided as
    keyword arguments to artificially stop the tabulation at various
    points in a given round.  Values of None mean the tabulation is not
    artificially stopped.

    stop_at_begin
      The number of a round; stop at the beginning of that round.
      Default value: None

    stop_after_status_update
      The number of a round; stop after the vote tally and status tally
      update for that round.
      Default value: None

    stop_at_end
      The number of a round; stop at the end of that round.
      Default value: None

    Returns
    -------
    A tuple with the following values in order:

      elected
        A set of candidate names that have been elected by the
        tabulation

      status
        A dictionary keyed by candidate name for every candidate, each
        with a value that is an status.Status object, which has the
        following attributes:

          candidate
            The candidate's name.

          status
            A string indicating the candidate's status: 'elected' or
            'defeated'.

          nbr_round
            The 1-based number of the round in which the candidate is
            elected or defeated.

          votes
            The number of votes the candidate had when elected or
            defeated.

      tally
        A dictionary, keyed by candidate names and labels for other
        tabulation categories, of tuples of round-by-round vote totals.
        A vote total for the kth round is accessed with an index of k-1.
        A candidate has a vote total only for those rounds which started
        with the candidate as a continuing or elected candidate.

        In addition to candidates, there are vote totals for all rounds
        for each of the following keys / tabulation categories::
          ':Overvote'
          ':Abstention'
          ':Other exhausted'
          ':Residual Surplus'   (only for STV tabulations)


    Raises
    ------
    RcvValueError
      If any values passed to this function do not pass validation
      checks.

    RcvImplementationError
      If an inconsistency is detected during the tabulation that is not
      attributable to invalid arguments, resource constraints, resource
      availability, or other external interventions.  If this exception
      is raised, it might be because this Python package contains a
      logic error.

    Other exceptions:
      Other exceptions defined by Python and its standard libraries can
      be raised, for example as a result of unavailable or insufficient
      resources.

      This function does not otherwise impose restrictions on the size
      of the tabulation, including, the number of seats to be elected,
      the number of candidates, the number of ballots or ballot groups,
      the number of rankings per ballot, or the length of candidate
      names.  The size of a tabulation that can be performed is
      primarily dependent on the resources on the hardware and software
      configuration on which the function runs.

    The RcvValueError and RcvImplementationError classes are subclasses
    of the Exception class and neither is a subclass of the other,
    directly or indirectly.

    """
    try:
      self.testing = {'stop_at_begin': None, 'stop_after_status_update': None,
            'stop_at_end': None}
      self.testing.update(kwargs)
      if self.is_irv():
        elected, status, tally = self._tabulate_irv()
      else:
        elected, status, tally = self._tabulate_stv()
    except (errors.RcvValueError, errors.RcvImplementationError):
      raise
    except (MemoryError, SystemError):
      raise
    except Exception as exc:
      raise errors.RcvImplementationError(
            'Possible RCV implementation error:', (), exc)
    return elected, status, tally

  def is_irv(self):
    return self.nbr_seats_to_fill == 1

  def zero_votes(self):
    return 0 if self.is_irv() else K.ZERO

  def ballot_votes(self, ballot):
    return ballot.get_multiple() if self.is_irv() else ballot.total_votes()

  def other_categories(self):
    result = {other_label: [] for other_label in K.OTHER_LABELS_LIST}
    if self.is_irv():
      del result[K.LABEL_RESIDUAL_SURPLUS]
    return result

  def votes_for_previously_elected(self, tab_code_tally):
    """
    Vote total for candidate after being elected
    """
    return tab_code_tally if self.is_irv() else K.Decimal(self.threshold)

  def _tabulate_irv(self):
    """
    Tabulate an IRV contest.

    This method is for internal use only.

    """
    self._tabulate_setup()
    while self._process_an_irv_round():
      if self.testing['stop_at_end'] == self.nbr_round:
        break
    return self.elected(), self.status, self.tallies

  def _tabulate_stv(self):
    """
    Tabulate an STV contest.

    This method is for internal use only.

    """
    self._tabulate_setup()
    self.total_residual_surplus = self.zero_votes()
    while self._process_an_stv_round():
      if self.testing['stop_at_end'] == self.nbr_round:
        break
    return self.elected(), self.status, self.tallies

  def _tabulate_setup(self):
    """
    Create instance values needed to tabulate IRV or STV
    """
    self.tallies = {candidate: [] for candidate in self.candidates}
    self.tallies.update(self.other_categories())
    self.ballots_for = {tab_code: [] for tab_code in self.tallies}
    self.status = {candidate: status.Status(candidate, self.zero_votes())
          for candidate in self.candidates}
    self.nbr_round = 0

  def _process_an_irv_round(self):
    """
    Process vote counting for an IRV round

    Return a boolean indicating whether to continue with another round.

    """
    self.nbr_round += 1
    if self.testing['stop_at_begin'] == self.nbr_round:
      return False
    # print()
    # print('nbr_round =', self.nbr_round)
    if self.nbr_round == 1:
      # initial assignment to highest ranked continuing candidate (hrcc)
      self.assign_ballots(self.ballots)
    self.tally_votes_for_assigned_ballots()
    self.update_candidate_status_tally()
    if self.testing['stop_after_status_update'] == self.nbr_round:
      return False
    # print('tallies =', self.tallies)
    # print('ballots_for =', self.ballots_for)
    # print('status =', {candidate: status2.as_dict()
    #       for candidate, status2 in self.status.items()})

    # check for special cases of few candidates
    if self.nbr_round == 1:
      if len(self.candidates) == 0:
        return False
      if len(self.candidates) == 1:
        self.elect_candidates(set(self.candidates))
        return False
    # prepare for defeating candidates
    defeated_this_round = set()
    # check for having just two continuing candidates, the finalists
    if len(self.continuing()) == 2:
      defeated_this_round = self.get_single_defeat_candidate()
      self.defeat_candidates(defeated_this_round)
      self.elect_candidates(set(self.continuing()))
      return False
    # determine / collect important vote totals
    continuing_votes = self.continuing_votes()
    total_continuing_votes = sum(
          [votes for votes in continuing_votes.values()])
    max_continuing_votes = max(
          [votes for votes in continuing_votes.values()])
    leading_candidates = set([candidate
          for candidate, votes in continuing_votes.items()
          if votes == max_continuing_votes])
    # check for stopping with a majority winner
    if 2 * max_continuing_votes > total_continuing_votes:
      if self.options[K.OPTION_STOP_AT_MAJORITY]:
        self.elect_candidates(leading_candidates)
        self.defeat_candidates(set(self.continuing()))
        return False
    # check for alternative defeats (a.k.a batch elimination)
    alt_defeats_option = self.get_alt_defeats_option()
    if alt_defeats_option ==  K.OPTION_ALTERNATIVE_DEFEATS_YES:
      # do alternative defeats
      defeated_this_round = self.get_irv_alternative_defeats(
            self.continuing_votes())
      self.defeat_candidates(defeated_this_round)
    if not defeated_this_round:
      # do regular, single-candidate defeat, after resolving any ties
      defeated_this_round = self.get_single_defeat_candidate()
      self.defeat_candidates(defeated_this_round)
    #print('defeats =', defeats)
    self.transfer_from_defeated(defeated_this_round)
    return True

  def _process_an_stv_round(self):
    """
    Process vote counting for an STV round

    Return a boolean indicating whether to continue with another round.

    """
    self.nbr_round += 1
    if self.testing['stop_at_begin'] == self.nbr_round:
      return False
    # print()
    # print('nbr_round =', self.nbr_round)
    if self.nbr_round == 1:
      # initial assignment to highest ranked continuing candidate (hrcc)
      self.assign_ballots(self.ballots)
      self.threshold = self.total_votes_for_candidates().__div__(
            self.nbr_seats_to_fill + 1, True)
      # print('threshold =', self.threshold)
    self.tally_votes_for_assigned_ballots()
    self.update_candidate_status_tally()
    if self.testing['stop_after_status_update'] == self.nbr_round:
      return False
    # print('tallies =', self.tallies)
    # print('ballots_for =', self.ballots_for)
    # print('status =', {candidate: status2.as_dict()
    #       for candidate, status2 in self.status.items()})

    # check for electing all continuing candidates
    if (self.nbr_round == 1 and
          len(self.continuing()) <= self.nbr_seats_to_fill):
      self.elect_candidates(self.continuing())
      return False
    # candidates with more than a threshold of votes are elected
    candidates_with_surplus = self.get_candidates_with_surplus()
    # print('candidates_with_surplus =', candidates_with_surplus)
    self.elect_candidates(set(candidates_with_surplus) - self.elected())
    # print('status =', {candidate: status2.as_dict()
    #       for candidate, status2 in self.status.items()})
    # if enough candidates are elected, defeat all continuing candidates
    if len(self.elected()) == self.nbr_seats_to_fill:
      self.defeat_candidates(self.continuing())
      return False
    # check for surplus to be transferred
    if candidates_with_surplus:
      # transfer surplus
      self.transfer_surplus(candidates_with_surplus)
    # if no candidates had surplus transferred
    #   defeat a candidate with the fewest votes
    defeated_this_round = set()
    if not candidates_with_surplus:
      # do regular, single-candidate defeat, after resolving any ties
      defeated_this_round = self.get_single_defeat_candidate()
      self.defeat_candidates(defeated_this_round)
    #print('defeated_this_round =', defeated_this_round)
    # check if all continuing candidates will be elected
    if (len(self.continuing()) + len(self.elected())
          == self.nbr_seats_to_fill):
      self.elect_candidates(self.continuing())
      return False
    # transfer ballots from all defeated candidates
    self.transfer_from_defeated(defeated_this_round)
    return True

  def assign_ballots(self, ballot_list):
    """
    Assign ballots from the ballot list
    """
    for ballot in ballot_list:
      self.ballots_for[ballot.get_hrcc(self.continuing(),
            self.max_ranking_levels)].append(ballot)

  def tally_votes_for_assigned_ballots(self):
    """
    Tally the votes for a round
    """
    for tab_code in self.ballots_for:
      if (tab_code in self.status and
            self.status[tab_code].status == K.STATUS_DEFEATED):
        continue
      if tab_code == K.LABEL_RESIDUAL_SURPLUS:
        tab_code_tally = self.total_residual_surplus
      else:
        tab_code_tally = sum([
              self.ballot_votes(ballot)
              for ballot in self.ballots_for[tab_code]], self.zero_votes())
        if (tab_code in self.status and
              self.status[tab_code].status == K.STATUS_ELECTED and
              tab_code_tally == self.zero_votes()):
          tab_code_tally = self.votes_for_previously_elected(tab_code_tally)
      # print('tab_code =', tab_code, ', tally =', tab_code_tally)
      self.tallies[tab_code].append(tab_code_tally)

  def update_candidate_status_tally(self):
    index_round = self.nbr_round - 1
    for candidate, candidate_status in self.status.items():
      if candidate_status.status == K.STATUS_CONTINUING:
        candidate_status.nbr_round = self.nbr_round
        candidate_status.votes = self.tallies[candidate][index_round]

  def elected(self):
    """
    Provide a set of the elected candidates
    """
    index_round = self.nbr_round - 1
    elected_candidates = set([candidate
          for candidate in self.status
          if self.status[candidate].status == K.STATUS_ELECTED])
    return elected_candidates

  def continuing(self):
    """
    Provide a set of the continuing candidates
    """
    index_round = self.nbr_round - 1
    continuing_candidates = set([candidate
          for candidate in self.status
          if self.status[candidate].status == K.STATUS_CONTINUING])
    return continuing_candidates

  def continuing_votes(self):
    """
    Get a dict of continuing candidates and their vote totals
    """
    continuing_votes = {candidate: self.status[candidate].votes
          for candidate in self.status
          if self.status[candidate].status == K.STATUS_CONTINUING}
    return continuing_votes

  def defeat_candidates(self, candidates):
    """
    Defeat the collection of candidates
    """
    for candidate in candidates:
      if self.status[candidate].status == K.STATUS_CONTINUING:
        self.status[candidate].status = K.STATUS_DEFEATED
      else:
        raise errors.RcvImplementationError(
              'Attempting to defeat a candidate that is not continuing.', [
              ('candidate', candidate),
              ('status', self.status[candidate].status),
              ('round', self.nbr_round)
              ])

  def elect_candidates(self, candidates):
    """
    Update the status of each candidate in the list
    """
    for candidate in candidates:
      if self.status[candidate].status == K.STATUS_CONTINUING:
        self.status[candidate].status = K.STATUS_ELECTED
      else:
        raise errors.RcvImplementationError(
              'Attempting to elect a candidate that is not continuing.', [
              ('candidate', candidate),
              ('status', self.status[candidate].status),
              ('round', self.nbr_round)
              ])

  def transfer_from_defeated(self, defeated):
    """
    Transfer ballots from defeated candidates
    """
    for defeated_candidate in defeated:
      self.assign_ballots(self.ballots_for[defeated_candidate])
      self.ballots_for[defeated_candidate] = []

  def get_single_defeat_candidate(self):
    """
    Get the candidate with the fewest votes, after resolving any tie

    Returns
    -------
    A singleton set of the candidate with the fewest votes, after
    resolving any tie.

    Raises
    ------
    RcvValueError
      If there is a tied candidate not in self.tie_breaker.

    """
    continuing_votes = self.continuing_votes()
    min_votes = min(continuing_votes.values())
    trailing_candidates = set([candidate
          for candidate, votes in continuing_votes.items()
          if votes == min_votes])
    defeat_candidate = self.resolve_tie(trailing_candidates)
    return set([defeat_candidate])

  def resolve_tie(self, tied_candidates):
    """
    Select the tied candidate that is earliest in the tie_breaker.

    Arguments
    ---------
    tied_candidates
      A set of one or more candidates that are tied.

    Returns
    -------
    The candidate name with the lowest tie_breaker index.

    Raises
    ------
    RcvValueError
      If there is a tied candidate not in self.tie_breaker.

    """
    if len(tied_candidates) <= 1:
      return list(tied_candidates)[0]
    not_in_tie_breaker = tied_candidates.difference(set(self.tie_breaker))
    if not_in_tie_breaker:
      raise errors.RcvValueError('Tied candidate not in tie_breaker:', (
            ('candidate', not_in_tie_breaker.pop()),
            ('round', self.nbr_round),
            ('tied_candidates', tied_candidates),
            ('tie_breaker', self.tie_breaker),
            ))
    tied_candidates_by_index = {index: candidate
        for candidate, index in self.tie_breaker.items()
        if candidate in tied_candidates}
    selected_candidate = tied_candidates_by_index[
          min(tied_candidates_by_index)]
    return selected_candidate


  def get_alt_defeats_option(self):
    """
    Get the value for alternative defeats for the current round

    Returns
    -------
    A string that is the option for alternative defeats in the round

    Raises
    ------
    RcvValueError
      If the option is stored as a tuple of strings, one per round, but
      the tuple is too short.

    """
    options_value = self.options[K.OPTION_ALTERNATIVE_DEFEATS]
    if type(options_value) == str:
      alt_defeats_option = options_value
    else:
      try:
        alt_defeats_option = options_value[self.nbr_round - 1]
      except IndexError:
        raise errors.RcvValueError(
              'Alternative defeats option tuple too short.', (
              ('nbr_round', nbr_round),
              ('len(options_value)', len(options_value)),
              ))
    return alt_defeats_option

  def get_irv_alternative_defeats(self, continuing_votes):
    """
    Get largest set of IRV candidates that can be defeated this round

    Arguments
    ---------
    continuing_votes
      A dictionary keyed by name of continuing candidates with values
      equal to current vote totals.

    Returns
    -------
    The largest possible set of candidates that satisfy the criteria for
    being defeated in a single round.

    """
    by_votes = sorted(continuing_votes.items(),
          key=lambda item: item[1], reverse=True)
    total_lesser_votes = sum(continuing_votes.values())
    candidates_to_defeat = set(continuing_votes)
    for ix, (candidate, votes) in enumerate(by_votes):
      total_lesser_votes -= votes
      candidates_to_defeat.remove(candidate)
      if ix > 0 and total_lesser_votes < votes:
        break
    return candidates_to_defeat

  def total_votes_for_candidates(self):
    """
    Calculate the total votes for candidates
    """
    result = sum([sum([self.ballot_votes(ballot)
          for ballot in self.ballots_for[candidate]], self.zero_votes())
          for candidate in self.candidates], self.zero_votes())
    return result

  def get_candidates_with_surplus(self):
    """
    Get a dict of candidates with surplus and their vote totals
    """
    index_round = self.nbr_round - 1
    candidates_with_surplus = {
          candidate: self.tallies[candidate][index_round]
          for candidate in self.status
          if (index_round < len(self.tallies[candidate]) and
                self.tallies[candidate][index_round] > self.threshold)}
    return candidates_with_surplus

  def transfer_surplus(self, candidates_with_surplus):
    """
    Transfer surplus from candidates with surplus
    """
    for candidate, candidate_votes in candidates_with_surplus.items():
      surplus_votes = candidate_votes - self.threshold
      surplus_factor = surplus_votes / candidate_votes
      transferred_votes = K.ZERO
      for ballot in self.ballots_for[candidate]:
        ballot.update_transfer_value(surplus_factor)
        transferred_votes += ballot.total_votes()
      self.assign_ballots(self.ballots_for[candidate])
      self.ballots_for[candidate] = []
      self.total_residual_surplus += surplus_votes - transferred_votes



