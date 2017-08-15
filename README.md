CA-SB1288
=========

A reference implementation for counting votes with ranked
choice voting (RCV).

# Table of Contents <a id="toc"></a>

  * [Introduction](#introduction)
  * [Repository Structure](#repository-structure)
  * [Use examples](#use-examples)
  * [Testing](#testing)
  * [Limitations](#limitations)
  * [Extension](#extension)
  * [Licensing](#licensing)


## Introduction <a id="introduction"></a>

This is a reference implementation in Python of the core vote counting
algorithms for ranked choice voting (RCV) as specified by
[California Senate Bill 1288 (2016)](
http://leginfo.legislature.ca.gov\
/faces/billNavClient.xhtml?bill_id=201520160SB1288 "SB-1288").

SB 1288 was passed by the California Legislature but was vetoed by 
Governor Jerry Brown.  Though it did not become law, it still serves 
as a useful reference as an RCV specification.

The legal language describing the RCV vote counting algorithms was
developed with an emphasis on being clear, consistent, and complete,
with the goal that any two conforming implementations would produce the
same results for a given set of equivalent inputs and tabulation
parameters.  The legal language describing the vote counting was proposed
in a new Division 22 of the California Elections Code, Chapters 1 and
2.

This reference implementation is intended to supplement that legal
language as an additional means to document the intended intepretation,
clarify any ambiguities, and avoid misunderstandings.

As a reference implementation, the programs and test cases can be used
as a starting point for conformance testing of other implementations.


## Repository Structure <a id="repository-structure"></a>

The __`sb1288`__ directory contains a Python package with the
reference implementation programs.  The __`tests`__ directory contains
test programs and data that document the intended behavior and which in
some regards are as important as the Python programs in the
__`sb1288`__ directory for documenting the intent of the legal
language.

The vote counting algorithms in this reference implementation cover both
single-winner RCV, also known as instant runoff voting (IRV), and
multi-winner RCV, also known as single transferable vote (STV).

For multi-winner RCV, SB 1288 specifies a version of the weighted
inclusive Gregory method, so that when a winner's surplus is distributed
to other candidates, all ballots counting for that winner are
transferred, but each ballot is transferred at a reduced transfer value
representing that ballot's share of the winner's surplus as a portion of
the winner's total vote count.  The winner retains a vote total equal to
the threshold.  As a result, a ballot can subsequently count for a
subsequent candidate as only a fraction of a whole vote.

Both single- and multi-winner algorithms can be invoked with the
__`sb1288.tabulate()`__ function, which takes as a first argument the
number of seats to be elected.  That function resides in the
__`sb1288/rcv.py`__ file.  That file contains additional documentation
about the __`tabulate()`__ function.


## Use Examples <a id="use-examples"></a>

Three ways to run an RCV tabulation are:

  * [Caller gives data directly](#caller-data)
  * [Caller gives data in JSON files](#caller-json)
  * [Command line using JSON files](#command-line)

### Caller gives data directly <a id="caller-data"></a>

After importing the __`sb1288`__ package with:

    import sb1288

tabulation of RCV votes can be accomplished by calling the
__`sb1288.tabulate()`__ function, which is defined as:

    def tabulate(nbr_seats_to_fill, candidates, ballots,
          max_ranking_levels, tie_breaker, options={}):

For example:

    elected, status, tally = sb1288.tabulate(1, " A B C", [
          [4, ' A B C'],
          [3, ' B A C'],
          [2, ' C B A']
          ],
          3, ' C A B', {})

will tabulate a contest that:

  * produces one winner, i.e. uses the IRV algorithm
  * has three candidates (A, B, and C)
  * has nine ballots, two of which rank C first, B second, and A third
  * allows a voter to rank up to three candidates
  * uses a tie breaker ranking for resolving ties, picking for
    elimination the earliest ranked candidate of any tied candidates; so
    C is picked for elimination if tied with A or B (or both) and A is
    picked for elimination if tied only with B
  * does not specify any special tabulation options

The above example uses a short cut for specifying a sequence of strings
by writing them in a single, delimiter-separated string with the first
character specifying what the delimiter is.

The result of the function is a three-tuple consisting of:

  * elected, a set of winners
  * status, a dict showing the status of each candidate
    * whether the candidate was elected or defeated
    * the round in which the candidate was elected or defeated
    * the candidate's vote total when elected or defeated -- the
      candidates largest vote total in any round
  * tally, a dict showing the essential round-by-round vote totals of
    the tabulation

In this particular case, the results would be as if the following
assignments had occured:

    elected = ('B',)
    status = {
          'A': sb1288.Status('A', 'defeated', 2, 4),
          'B': sb1288.Status('B', 'elected',  2, 5),
          'C': sb1288.Status('C', 'defeated', 1, 2)
          }
    tally = {
          'A': (4, 4),
          'B': (3, 5),
          'C': (2,),
          ':Overvotes': (0, 0),
          ':Abstentions': (0, 0),
          ':Other exhausted': (0, 0)
          }

### Caller gives data in JSON files <a id="caller-json"></a>

An alternative way to run a tabulation is with the
__`sb1288.tabulate_with_json()`__ function which reads the tabulation
input from a named JSON file and by default prints the results.

For example, the previous example can be tabulated using a file named
__`example.json`__ with the following content:

    {
      "description": "An example RCV contest"
      ,"nbr_seats_to_fill": 1
      ,"candidates": " A B C"
      ,"ballots": [
        [4, " A B C"],
        [3, " B A C"],
        [2, " C B A"]
        ]
      ,"max_ranking_levels": 3
      ,"tie_breaker": " C A B"
      ,"options": {}
    }

and then executing the Python statement:

    elected, status, tally, tab_spec = sb1288.tabulate_with_json(
          'example.json', 'example-results.json')

which writes a file __`example-results.json`__ with the following
content:

    {
      "description": "An example RCV contest",
      "elected": ["B"],
      "status": [
        ["B", "elected", 2, 5],
        ["A", "defeated", 2, 4],
        ["C", "defeated", 1, 2]
      ],
      "tally": {
        "B": [3, 5],
        "A": [4, 4],
        "C": [2],
        ":Abstentions": [0, 0],
        ":Other exhausted": [0, 0],
        ":Overvotes": [0, 0]
      }
    }
 
If the second argument is omitted or set to the empty string, the JSON
output is printed to __`stdout`__ rather than being written to a file.

The first three return values are the same as are returned using the
__`sb1288.tabulate()`__ function.  The fourth return value is a dict
of tabulation specifications reflecting the net result of what was found
in the input JSON file and any included files.  The input JSON file can
have an 'include' property with a value that is a list of JSON file
names from which other property/values are included, but which can be
overridden by corresponding property/values in the primary input JSON
file.

### Command line using JSON files <a id="command-line"></a>

A third way to run an RCV tabulation is from the command line.  The
previous example could be run as:

> python -m sb1288.with_json example.json example-results.json

Depending on the configuration of your computer, other command names
might be used, for example __`python3`__ instead of __`python`__ when
running a Python version 3.x.

If the __`example-results.json`__ argument is omitted or given as an
empty string, the JSON results are printed to __`stdout`__ rather than
being written to the file. 


## Testing <a id="testing"></a>

Tests can be run using the Python unittest module.  For example in a
local copy of this repository, change the working directory to the
__`tests`__ directory and run one of the following commands:

> python -m unittest discover

> python3 -m unittest discover

That should run 182 tests, all without errors, typically in less than a
second, though speeds vary depending on the type of computer being used.

There are two kinds of tests in the __`tests`__ directory tree:

  * traditional unittest tests specified in
    __`tests/unittest/test\*.py`__
    files and which are typically dependent on the internal design and
    implementation of this reference implementation

  * tests with inputs and expected results that are specified in JSON
    files and which are designed to be typically applicable to other
    conforming implementations of the California RCV vote counting
    algorithms

The JSON-based tests are typically run from a test\*.py file in the same
directory as the JSON files specifying the test.  A group of related
tests are specified in similarly named JSON files, sometimes sharing a
base JSON file for common data.  For example, files __`abc-007-1.json`__
and __`abc-007-2.json`__ might specify two related tests and reference
(include and possibly override) a common __`abc-007-base.json`__ file.

The JSON files specify a JSON object which is convertible to a
Python dict and which includes a __`"description"`__ name / key.

Global parameters for the JSON-based test cases may be set in the file
__`tests/all-tests-spec.json`__.

The programs have been written and tested for Python versions 2.7.x,
beginning with 2.7, and versions 3.x, beginning with 3.2.  The unit tests
for the command line interface assume that the Python command name is
__`python`__ for versions 2.7.x and __`python3`__ for versions 3.x.
Change the values for __`PYTHON_2_CMD`__ and __`PYTHON_3_CMD`__ in
__`tests/unit/test_json.py`__ if your computer uses different commands.


## Limitations <a id="limitations"></a>

This reference implementation focuses on the core vote counting
algorithms and does not offer all of the functionality that a voting
system would need to provide to support a California RCV election.  For
example, it does not provide all of the information needed for
reporting.  Specifically, it does not support any information about
precincts.

There are several areas where the legal language allows some leeway in
the specifics of how RCV vote counting is
performed.  They include:

  * resolution of ties for which candidate should be eliminated in a
    round
  * decisions about whether an IRV tabulation should continue once a
    majority winner has been identified
  * the manner in which ballot rankings are expressed

This reference implementation provides some features to support that
functionality, but other implementations that conform to the legal
language can provide other modes of support.

California RCV vote counting algorithms may be modified by California
Secretary of State regulations provided those modifications do not
change who is elected.  This reference implementation does not currently
reflect any such proposed or adopted regulations.

Neither the programs nor the test cases enforce specific maximum
limitations on the sizes of input to an RCV tabulation.  Sizes of
contests that can be tabulated generally depend on the amount of
resources, especially memory, available to the software.

For a reference implementation written in Python, optimizing the amount
of memory, CPU time, or elapsed time to tabulate votes was generally not
a priority.  Instead, there has been some preference for writing the
programs so that they more closely parallel the provisions of the
legal language.

Running the automated tests in Python 3 requires at least version 3.2.

In order to focus on issues of core RCV functionality and to allow
programs to run under different versions of Python, all test data has
been limited to using ASCII characters.  Non-ASCII characters are not
supported.

## Extension <a id="extension"></a>

This reference implementation includes an extension to the STV
tabulation logic that provides for alternative conditions for defeating
candidates: batch defeats of multiple candidates and deferred
distribution of surplus.  These features were part of SB 1288 when it
was introduced, but later removed and identified for specification as
California Secretary of State regulations, as authorized by SB 1288.

For more information about these features, please read this [additional
description](stv-altdefs.html).

## Licensing <a id="licensing"></a>

This project is licensed under the Apache License, Version 2.0 (the
"License"); you may not use contents of this repository except in
compliance with the License.  A copy of the License is in the LICENSE
file and may also be obtained at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Copyright 2016 David Cary; licensed under Apache License, Version 2.0
