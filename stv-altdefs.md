STV Alternative Defeats for SB 1288 
===================================

# Table of Contents <a id="toc"></a>

  * [Introduction](#introduction)
  * [Shortcuts](#shortcuts)
  * [Integrated into tabulation](#integration)
  * [Conditions](#conditions)

## Introduction <a id="introduction"></a>

The STV alternative defeats option in this reference implementation is
an extension to SB 1288 that allows, under specific conditions, one or
more candidates to be defeated in a single round and allows them to be
defeated even if there is an elected candidate with surplus votes that
have not yet been transferred to other candidates.  When such an
alternative defeat is performed, any votes from the defeated candidates
are transferred, but the transfer of surplus votes is pre-empted and
deferred to a subsequent round or might not need to be transferred at
all.

Defeating more than one candidate in a round, epecially a round other
than the last round, is also known as batch defeats.  Defeating a
candidate instead of transferring available surplus from elected
candidates is also known as deferred surplus transfer.

This STV alternative defeats logic extends the basic SB 1288 STV vote
counting algorithm, which, except for the last round, only allows at
most one candidate to be defeated per round and only if no candidate has
been elected in the round and so that there is no surplus to be
transferred.

The option to perform these alternative defeats were in preliminary versions of
SB 1288, but were later removed and targeted for specification by California
Secretary of State regulations, as authorized by SB 1288.  Use of these
alternative defeats will not result in a different candidate being elected
compared to using the basic defeat logic.

Except in the last round, the basic defeat logic does not allow a
candidate to be defeated if another candidate is elected in that
round.  However, the alternative defeats option may allow some
candidates to be elected and others to be defeated in the same round
that is not the final round.  Nonetheless, it is still the case that in
any given round other than the final round, either votes from defeated
candidates will be transferred or surplus votes from elected candidates
will be transferred.

##Tabulation shortcuts <a id="shortcuts"></a>

The use of alternative defeats can provide vote counting shortcuts for
by using either batch elimination and deferred surplus transfers.  They
can reduce the number of rounds that are needed for an STV tabulation
and reduce the average number of times that a ballot must be examined
during the vote tabulation.  Both are advantages for manual counting of
votes, while the reduced number of rounds can make it easier understand
reported results.

However, there can be situations where using alternative defeats would
increase the number of rounds and the number of times ballots need to be
examined.  It might not always be possible to predict in advance whether
a reduction will occur. 

##Integrated into tabulation <a id="integration"></a>

In the SB 1288 STV vote counting algorithm, the possibility of
performing alternative defeats is checked just before Election Code
subdivision 22101(f), the transfer of surplus.

If any candidates are defeated as alternative defeats, that subdivision
22101(f) and the initial part of subdivision 22101(g), the basic defeat
of a single candidate, are skipped.  That way, any surplus transfers are
deferred to a later round and the additional, basic defeat of a
single, additional candidate is skipped for the round.  However,
paragraphs 22101(g)(1), which checks whether all remaining continuing
candidates can be elected, and, if the tabulation continues,
22101(g)(2), which transfers votes from defeated candidates, are
performed to complete the round.

If no candidates are alternatively defeated, the round continues
normally with subdivision 22101(f).

##Conditions <a id="conditions"></a>

It can be possible that changing the order in which some candidates are
defeated or elected and have their votes or surplus votes transfered to
other candidates, can change which other candidates are subsequently
elected and defeated.  The following set of conditions are sufficient,
but not necessary, to ensure that batch defeats and deferred surplus
transfers will not change who the contest winners are.

The option to use alternative defeats may be exercised on a
round-by-round basis. If the option is exercised, the largest
group of continuing candidates with the fewest votes and which
satisfies all three of the following conditions will be defeated. The
largest group might not have any candidates in it, in which case, the
tabulation proceeds as if the option had not been exercised.

**Condition 1:** The number of candidates elected so far, plus the number
of continuing candidates not in the group is greater than or equal to
the number of seats the contest is allowed to elect.

This condition ensures that defeating the group of candidates will still
leave enough continuing candidates to fill the remaining unfilled
seats.

**Condition 2:** The total votes for all candidates in the defeated group,
plus the total amount of surplus votes for elected candidates is less
than the number of votes for any continuing candidate not in the
defeated group.

This condition ensures that if a continuing candidate is in the
qualifying group, any continuing candidate with fewer or equal votes is
also in the group.  This condition with Condition 1 also ensures that,
using only the basic defeat logic, all of the candidates in the group
will be defeated, none could be elected, and all would be defeated
in some order before any others would be defeated.

**Condition 3:** At least one of the following four conditions is true:

**Condition 3.1:** There is only one remaining unfilled seat.

This condition ensures that the the next elected candidate will be the
last elected candidate, so surplus will not be transferred from that
candidate.

**Condition 3.2:** The number of continuing candidates not in the defeated
group is equal to the number of unfilled seats.

This condition ensures that once the candidates in the defeated group
are next defeated, with or without alternative defeats, there is no
question about which of the other continuing candidates will be
elected.

**Condition 3.3:** The total votes for all candidates in the defeated
group, plus the total amount of surplus votes for elected candidates,
plus the number of votes for a continuing candidate with the most votes
is less than or equal to the threshold.

This condition ensures that transferring all votes from the defeated
candidates and transferring all of the surplus votes can not elect
another candidate.

**Condition 3.4:** Both of the following conditions are true:

**Condition 3.4.1:** There are no surplus votes.

**Condition 3.4.2:** The total votes for all candidates in the defeated
group except for one candidate with the most votes in the defeated
group, plus the number of votes for a continuing candidate with the most
votes is less than or equal to the threshold.

These two conditions ensure that while the basic defeating of all
candidates in the group, one per round, might result in electing one or
more other candidates, no candidate would be elected until after all
candidates in the group had been defeated.

