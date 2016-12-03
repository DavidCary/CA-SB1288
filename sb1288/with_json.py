# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0
"""Tabulate RCV with JSON files"""

from __future__ import print_function

from sb1288 import rcv
from sb1288 import errors
from sb1288.ballot import Ballot  # this is probably not needed
from sb1288 import status
from sb1288 import validate

import sys
import json
import os.path

# A convenience method for using the rcv.Tabulation class

def tabulate(input_json='', output_json='', default_json=None):
  """
  Tabulate an RCV contest using JSON files for input and output

  Arguments
  ---------
  input_json
    A str name of a file or an opened file that is read to get a JSON
    specification of the tabulation to be performed.  If the value is an
    empty str, standard input is read.  If the value is None, nothing is
    read. The JSON specification should be a JSON object with names
    that correspond to the parameters of rcv.Tabulation() initialization.

    Additional names may be specified.  Some that are recognized
    include:

    description
      A description of the contest being tabulated.

    include
      An array of additional input JSON file names that are read.  The
      name / value pairs in included files are subject to being
      overridden by subsequent file names in the array of included file
      names and also, ultimately, contents of the input_json file.  Any
      include value from an included file is ignored.

  output_json
    A str name of a file or an opened file that is written to with a
    JSON specification of the tabulation results.  If the value is an
    empty str, results are written to standard output.  If the value is
    None, nothing is written.  The JSON specification of the tabulation
    result is a JSON object with the following names:

    elected
      An array of winners, corresponding to the first value returned by
      rcv.Tabulation().tabulate().

    status
      An array of status values, each expressed as an array,
      corresponding to the values of the second value returned by
      rcv.Tabulation().tabulate().  The status values are listed in the
      following order:  candidate, status, nbr_round, votes.  For STV,
      votes are expressed as a real number.

    tally
      An object of tally values, corresponding to the third value
      returned by rcv.Tabulation().tabulate().

    description
      A string value of the input description value, if a non-empty
      description value string was provided.  Otherwise, this name is
      not included in the JSON output.

  default_json
    A str name of a file or an opened file that is read to provide
    default values for input_json specification before that file is
    read.  If the value is an empty string, standard input is read.  If
    the value is None, no attempt to read defaults is made.  If both
    this value and the input_json value are empty strings, this value is
    treated as if it were None.  The include name is recognized from
    this file, but its value may be overridden by an include value
    specified in the input_json file.


  Returns
  -------
  A four-tuple consisting of the three values returned by the
  rcv.Tabulation().tabulate() function, and a dict of the input values
  built from input_json and default_json.


  Raises
  ------
  The same as the rcv.Tabulation().tabulate() method, plus other
  exceptions that might be related to accessing files to build the
  tabulation specification or to store its results.

  """
  tabulate_args, tabulation_spec = build_tabulate_args(
        input_json, default_json)
  try: description = tabulation_spec['description']
  except KeyError: description = None
  elected, status, tally = rcv.Tabulation(*tabulate_args).tabulate()
  json_str = results_to_json(elected, status, tally, description)
  write_file(output_json, s2u(json_str))
  return elected, status, tally, tabulation_spec

def results_to_json(elected, status, tally, description):
  """
  Convert tabulation results to a JSON string

  Arguments
  =========

  elected
    a set or sequence of elected candidates, as given by the first item
    in the return value of the rcv.Tabulation.tabulate() function.

  status
    a dict of sb1288.Status objects keyed by their candidates, as
    given by the second item in the return value of the
    rcv.Tabulation.tabulate() function.

  tally
    a dict of round-by-round vote tallies for each candidate or other
    tabulation category, as given by the third item in the return value
    of the rcv.Tabulation.tabulate() function.

  description
    a string, that is the value of the 'description' key, if it exists,
    from the dictionary of tabulation specification, otherwise None or
    False.
    in the return value of the rcv.Tabulation.tabulate() function.

  Returns
  =======
  a JSON string which represents the function arguments

  Raises
  ======
  May raise various exceptions if the function arguments are not of the
  anticipated structure.

  """
  description_str = ''
  if description is not None:
    description_str = '  "description": ' + json.dumps(description)
    description_str += ',\n'
  elected_str = '  "elected": ' + json.dumps(sorted(elected)) + ',\n'
  status_str = '  "status": [\n'
  for ix, (candidate, cstatus) in enumerate(sorted(status.items(),
        key=lambda item: get_tally_sort_key(item[0], status))):
    status_str += '    ' + json.dumps(cstatus.as_tuple(as_float=True))
    if ix < len(status) - 1:
      status_str += ','
    status_str += '\n'
  status_str += '  ],\n'
  tally_str = '  "tally": {\n'
  tally_sorted = sorted(tally.items(), key=lambda item:
        get_tally_sort_key(item[0], status))
  tally_sorted = [[code, [
        votes if type(votes) == int else float(str(votes))
        for votes in votes_by_round]]
        for code, votes_by_round in tally_sorted]
  for ix, (code, votes_by_round) in enumerate(tally_sorted):
    tally_str += '    "%s": ' % code + json.dumps(votes_by_round)
    if ix < len(tally) - 1:
      tally_str += ','
    tally_str += '\n'
  tally_str += '  }\n'
  json_str = '{\n' + description_str + elected_str
  json_str += status_str + tally_str + '}\n'
  return json_str

def get_tally_sort_key(code, status):
  """
  Get a tally sort key

  The sort key can be used to sort candidates and other tabulation
  categories, for example the status and tally collections returned by
  rcv.Tabulation().tabulate().

  The sort codes will sort candidates before other tabulation
  categories; elected candidates before defeated candidates; elected
  candidates by increasing round of election, then by decreasing votes;
  defeated candidates by decreasing round of election, then by
  decreasing votes; any remaining ties are broken by the sort order of
  candidate names and labels for other tabulation categories.

  Arguments
  =========
  code
    A string representing a candidate name or label of another
    tabulation category.

  status
    A dictionary of tabulation result statuses, as given by the second
    item of the return value from rcv.Tabulation().tabulate().

  Returns
  =======
  A sort key in the form of a tuple of integers and/or strings.

  """
  sort_key = tuple([9, code])
  if code in status:
    nbr_round = status[code].nbr_round
    votes = status[code].votes
    if status[code].status == 'elected':
      sort_key = (1, 1, nbr_round, -votes, code)
    else:
      sort_key = (1, 2, -nbr_round, -votes, code)
  else:
    sort_key = (2, code)
  # print('code =', code, '  sort_key =', sort_key)
  return sort_key

def build_tabulate_args(input_json, default_json):

  """
  From JSON files, build tabulation args and specification

  Arguments
  =========
  See the description of input_json and default_json for this module's
  tabulate() function for details.

  Returns
  =======
  Two values in a tuple:

    + A tuple of tabulation args that can be passed to
      rcv.Tabulation().tabulate()

    + A dict that should specify an RCV tabulation.  Additional
      key/values may be ignored or used for testing.

  Raises
  ======
  Various exceptions may be raised which are related to reading JSON
  files.

  """
  tabulation_spec = read_tabulation_spec(input_json, default_json)
  tabulation_spec['options'] = {u2s(name): u2s(value)
        for name, value in tabulation_spec['options'].items()}
  arg_ballots = tabulation_spec['ballots']
  if 'ballots_more' in tabulation_spec:
    arg_ballots = list(arg_ballots)
    arg_ballots.extend(list(tabulation_spec['ballots_more']))
  tabulate_args = (
        tabulation_spec['nbr_seats_to_fill'],
        tabulation_spec['candidates'],
        arg_ballots,
        tabulation_spec['max_ranking_levels'],
        tabulation_spec['tie_breaker'],
        tabulation_spec['options']
        )
  return tabulate_args, tabulation_spec

def write_file(file_name, text):
  """
  Write text to a file
  """
  if file_name == '':
    sys.stdout.write(text)
  elif type(file_name) != str and hasattr(file_name, 'write'):
    file_name.write(text)
  elif file_name is None:
    pass
  else:
    with open(file_name, 'w') as otfile:
      otfile.write(text)

def read_file(file_name):
  """
  Read text from a file and return as a list of strings
  """
  if file_name == '':
    text = sys.stdin.read()
  elif type(file_name) != str and hasattr(file_name, 'read'):
    text = file_name.read()
  elif file_name is None:
    text = ''
  else:
    with open(file_name, 'r') as infile:
      text = infile.read()
  return text

def read_json(file_name):
  """
  Read JSON data from a text file and return as a python value
  """
  text = read_file(file_name)
  json_result = json.loads(text)
  return json_result

def read_optional_json(file_name):
  """
  Read JSON data if the file exists
  """
  result = {}
  if (file_name == '' or
        (type(file_name) is str and file_name != '' and
        os.path.isfile(file_name)) or
        (type(file_name) is not str and hasattr(file_name, 'read'))
        ):
    file_result = read_json(file_name)
    result.update(file_result)
  return result

def read_tabulation_spec(input_json, default_json):
  """
  Read tabulation specs from primary and default JSON text files

  The order of building test specs, with later values overriding earlier
  values, is:

    * hard-coded default values
    * values in the default JSON file
    * values from the include files in the order listed
    * values from the primary JSON input file

  However, a list include files is only taken from the primary JSON
  file.

  """
  tabulation_spec = {
        'description': 'Test description not provided.',
        'nbr_seats_to_fill': 0,
        'candidates': '',
        'ballots': '',
        'max_ranking_levels': 0,
        'tie_breaker': '',
        'options': {},
        'elected': '',
        'status_codes': [],
        'tally': {},
        }
  if (default_json is not None and
        not (default_json == '' and input_input_json == '')):
    default_spec = read_optional_json(default_json)
    tabulation_spec.update(default_spec)
  primary_spec = read_json(input_json)
  try: include_list = primary_spec['include']
  except KeyError: include_list = []
  for include_input_json in include_list:
    include_spec = read_json(include_input_json)
    tabulation_spec.update(include_spec)
  tabulation_spec.update(primary_spec)
  return tabulation_spec

def s2u(value):
  """conditionally, only for Python 2.x, convert from str to unicode"""
  if sys.version_info[0] == 2 and type(value) == str:
    value = value.decode('ascii')
  return value

def u2s(value):
  """conditionally, only for Python 2.x, convert from unicode to str"""
  if sys.version_info[0] == 2 and type(value) == unicode:
    value = value.encode('ascii')
  return value

if __name__ == '__main__':
  if len(sys.argv) > 2:
    tabulate(sys.argv[1], sys.argv[2])
  elif len(sys.argv) > 1:
    tabulate(sys.argv[1], '')

