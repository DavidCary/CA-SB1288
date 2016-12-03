# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0
"""Support for fast decimals with five decimal places

This class provides defined behavior, relatively free from external
influences.

"""

import sys

_NBR_DECIMAL_PLACES = 5
_FACTOR = pow(10, _NBR_DECIMAL_PLACES)


class Decimal5Error(Exception):
  """An Exception error for the Decimal5 module """
  pass

class Decimal5(object):
  """An immutable class for expressing numbers to five decimal places

  This is useful for counting votes in STV tabulations

  """

  _value_as_integer = 0

  def __init__(self, value=None, exponent_of_10=0):
    """Initialize a Decimal5 object

    Creates a numeric quantity with a value of:

      value * 10 ^ exponent_of_10

    truncated to five decimal places.

    Arguments:
    ----------
    value
    A numeric value, which is either a float, int, or another Decimal5
    object.

    exponent_of_10
    A numeric value representing a exponent of 10.  The value should be
    an int value or a value that can be rounded to a integral value and
    then converted to an int.

    Raises:
    -------
    Decimal5Error
    If value or exponent_of_10 is not a supported type.

    """

    try:
      exponent_of_10 = int(round(exponent_of_10))
    except Exception as exc:
      raise Decimal5Error('exponent_of_10 is not a supported type:'
            + '\n  {:25}=  {}'.format('type', str(type(exponent_of_10)))
            + '\n  {:25}=  {}'.format('repr(exponent_of_10)',
            repr(exponent_of_10)))
    if value is None:
      self._value_as_integer = 0
      return
    if isinstance(value, float):
      multiplier = pow(10, exponent_of_10 + _NBR_DECIMAL_PLACES)
      adjusted_value = value * multiplier
      self._value_as_integer = int(round(adjusted_value, 0))
      return
    if isinstance(value, Decimal5):
      multiplier = pow(10, exponent_of_10)
      adjusted_value = value._value_as_integer * multiplier
      self._value_as_integer = int(round(adjusted_value, 0))
      return
    if type(value) != int and (
          sys.version_info[0] > 2 or type(value) != long):
      raise Decimal5Error('Value is not a supported type:'
            + '\n  {:25}=  {}'.format('type', str(type(value)))
            + '\n  {:25}=  {}'.format('repr(value)', repr(value)))
    add_decimal_places = _NBR_DECIMAL_PLACES + exponent_of_10
    multiplier = pow(10, abs(add_decimal_places))
    if add_decimal_places >= 0:
      adjusted_value = value * multiplier
    else:
      adjusted_value = div_to_int(value, multiplier)
    self._value_as_integer = int(adjusted_value)

  def _get_value(self):
    """Get the integer value used to store the Decimal5 value."""
    return self._value_as_integer

  def __repr__(self):
    """Get a string representation of the value, same as __str__()."""
    return self.__str__()

  def __str__(self):
    """Convert the value to a string, showing all decimal places."""
    if self._value_as_integer >= 0:
      sign = ''
      (int_part, fraction_part) = divmod(self._value_as_integer, _FACTOR)
    else:
      sign = '-'
      (int_part, fraction_part) = divmod(-self._value_as_integer, _FACTOR)
    fraction_str = str(fraction_part)
    fraction_pad = '0' * (_NBR_DECIMAL_PLACES - len(fraction_str))
    result = sign + str(int_part) + '.' + fraction_pad + fraction_str
    return result

  #def __cmp__(self, value):
  #    result = long(self._value_as_integer).__cmp__(
  #            long(value._value_as_integer))
  #    return result


  def __lt__(self, value):
    """Compare less than with another Decimal5 value"""
    _confirm_types(value, Decimal5)
    result = self._value_as_integer < value._value_as_integer
    return result

  def __le__(self, value):
    """Compare less than or equal with another Decimal5 value"""
    _confirm_types(value, Decimal5)
    result = self._value_as_integer <= value._value_as_integer
    return result

  def __eq__(self, value):
    """Compare equal with another Decimal5 value"""
    # allowing comparison to None avoids a bug in help() and inspect
    _confirm_types(value, Decimal5, type(None))
    if type(value) != Decimal5:
      return False
    result = self._value_as_integer == value._value_as_integer
    return result

  def __ne__(self, value):
    """Compare not equal with another Decimal5 value"""
    result = not self.__eq__(value)
    return result

  def __ge__(self, value):
    """Compare greater than or equal with another Decimal5 value"""
    _confirm_types(value, Decimal5)
    result = self._value_as_integer >= value._value_as_integer
    return result

  def __gt__(self, value):
    """Compare greater than with another Decimal5 value"""
    _confirm_types(value, Decimal5)
    result = self._value_as_integer > value._value_as_integer
    return result

  def __add__(self, value):
    """Add with another Decimal5 value"""
    _confirm_types(value, Decimal5)
    result = Decimal5()
    result._value_as_integer = self._value_as_integer + value._value_as_integer
    return result

  def __sub__(self, value):
    """Subtract another Decimal5 value from this one"""
    _confirm_types(value, Decimal5)
    result = Decimal5()
    result._value_as_integer = self._value_as_integer - value._value_as_integer
    return result

  def __neg__(self):
    """Negate this Decimal5 value"""
    result = Decimal5()
    result._value_as_integer = - self._value_as_integer
    return result

  def __mul__(self, value):
    """Multiply with another Decimal5 value, truncating result"""
    _confirm_types(value, Decimal5, int)
    if isinstance(value, int):
      multiplier = value * _FACTOR
    else:
      multiplier = value._value_as_integer
    result = Decimal5(self._value_as_integer * multiplier,
          -2 * _NBR_DECIMAL_PLACES)
    return result

  def __div__(self, value, round_away=False):
    """Divide by another Decimal5 value

    By default the result is truncated to five decimal places, but if
    round_away evaluates to true, the result is rounded away from
    zero.

    """
    _confirm_types(value, Decimal5, int)
    result = Decimal5()
    numerator = self._value_as_integer * _FACTOR
    if type(value) == int:
      denominator = value * _FACTOR
    else:
      denominator = value._value_as_integer
    quotient = div_to_int(numerator, denominator, round_away)
    result._value_as_integer = quotient
    return result

  def __truediv__(self,value, round_away=False):
    """Divide by another Decimal5, same as __div__"""
    return self.__div__(value, round_away=round_away)

  def divide_by(self, value, round_away=False):
    """Divide by another Decimal5, same as __div__"""
    return self.__div__(value, round_away=round_away)


class Decimal5Total(Decimal5):
  """A mutable subclass of Decimal5 for accumulating totals

  Totals can be accumulated through standard addition and subtraction
  operations.

  """

  def __init__(self):
    """Always initialize to zero"""
    self._value_as_integer = 0

  def __add__(self, value):
    """Add another Decimal5 value to this one"""
    _confirm_types(value, Decimal5)
    self._value_as_integer += value._value_as_integer
    return self

  def __sub__(self, value):
    """Subtract another Decimal5 value from this one"""
    _confirm_types(value, Decimal5)
    self._value_as_integer -= value._value_as_integer
    return self


def _confirm_types(value, *required_types):
  """Raise an Decimal5Error if value is not an instance of the
  required type
  """
  for required_type in required_types:
    if isinstance(value, required_type):
      break
  else:
    raise Decimal5Error(
          'Value is not an instance of the required type:'
          + '\n  {:25}=  {}'.format('value type', str(type(value)))
          + '\n  {:25}=  {}'.format('repr(value)', repr(value))
          + '\n  {:25}=  {}'.format('required types', repr(required_types)))
  return True

def div_to_int(int_numerator, int_denominator, round_away=False):
  """Integer division with truncation or rounding away.

  If round_away evaluates as True, the quotient is rounded away from
  zero, otherwise the quotient is truncated.

  """

  is_numerator_negative = False
  if int_numerator < 0:
    int_numerator = -int_numerator
    is_numerator_negative = True
  is_denominator_negative = False
  if int_denominator < 0:
    int_denominator = - int_denominator
    is_denominator_negative = True
  quotient, remainder = divmod(int_numerator, int_denominator)
  if round_away and remainder > 0:
    quotient += 1
  if is_numerator_negative != is_denominator_negative:
    quotient = -quotient
  return quotient


