# -*- encoding=utf-8 -*-
# Copyright 2016 David Cary; licensed under the Apache License, Version 2.0
"""RCV related classes and functions for exceptions and errors
"""

import sys
import traceback



class _RcvError(Exception):
  """A base class for Exceptions related to RCV

  This class is not intended for direct use, just used as a base class
  for other exceptions.

  """

  def __init__(self, message, other_values=[], base_exception=None):
    """Initialize with a base message, other values, and an exception

    Arguments:
    ----------
    message
    A string identifying the general nature of the error.

    other_values
    A list or tuple of typically tuple pairs, usually each pair consists
    of a label and a value.  The list or tuple may contain items that
    are not tuple pairs.
    Default value: an empty list

    base_exception
    An exception is subsumed by this one.
    Default value: None

    """
    Exception.__init__(self, message)
    self.message = str(message)
    self.other_values = other_values
    self.base_exception = base_exception
    self.base_exception_description = ''
    if (self.base_exception is not None and
          isinstance(self.base_exception, Exception)):
      self.base_exception_description = describe_exc(self.base_exception)

  def _show_base_exception(self):
    """Select what to show about the base_exception"""
    return str(self.base_exception)

  def __str__(self):
    """Convert to a string"""
    result = [self.message]
    if self.other_values:
      result.append(self._other_values_as_str(self.other_values))
    if self.base_exception:
      result.append(indent_message(self._show_base_exception()))
    result = '\n'.join(result)
    return result

  def _other_values_as_str(self, other_values, indent_by=2):
    result = []
    if type(other_values) in (list, tuple):
      for value_item in other_values:
        if type(value_item) in (list, tuple) and len(value_item) == 2:
          value = value_item[1]
          result.append('{:25}=  {}'.
                format(str(value_item[0]), repr(value)))
        else:
          result.append(repr(value_item))
    else:
      result.append(repr(other_values))
    result = '\n'.join(result)
    result = indent_message(result, indent_by)
    return result


class RcvValueError(_RcvError):
  """An exception class to identify invalid argument data.

  Used for argument data that is normally supplied from outside the
  package.

  """

  def __init__(self, message, other_values=[], base_exception=None):
    """Initialize with a base message, other values, and an exception

    See base class for a description of the arguments.  Default value
    for other_values is [], for base_exception is None.
    """
    _RcvError.__init__(self, message, other_values, base_exception)


class RcvImplementationError(_RcvError):
  """An error class for possible RCV implementation errors"""

  def __init__(self, message, other_values=[], base_exception=None):
    """Initialize with a base message, other values, and an exception

    See base class for a description of the arguments.  Default value
    for other_values is [], for base_exception is None.

    """
    _RcvError.__init__(self, message, other_values, base_exception)

  def _show_base_exception(self):
    """Select what to show about the base_exception"""
    return str(self.base_exception_description)


def describe_exc(exc):
  """Create a multi-line description of an exception and its traceback"""
  parts = []
  parts.append('Exception description:')
  ex_type, ex_value, ex_tb = sys.exc_info()
  parts.append('  %s:' % str(ex_type).split('\'')[1])
  parts.append(indent_message(str(exc), 4))
  formatted_tb = traceback.format_tb(ex_tb)
  parts.append('Raised at:')
  parts.append(formatted_tb[-1][:-1])
  parts.append('Caught at:')
  formatted_stack = traceback.format_stack()
  parts.append(formatted_stack[-2][:-1])
  parts.append('Stack before try:')
  parts.append(''.join(traceback.format_stack()[:-2])[:-1])
  parts.append('Stack after try:')
  parts.append(''.join(formatted_tb)[:-1])
  del ex_tb
  parts.append('END Exception description')
  indented_parts = (parts[:3] +
        [indent_message(part) for part in parts[3:-1]] +
        [parts[-1]])
  result = "\n".join(indented_parts)
  return result

def indent_message(message, indent_by=2):
  indent_str = ' ' * indent_by
  if message and message[-1] == '\n':
    tail = '\n'
    main_message = message[:-1]
  else:
    tail = ''
    main_message = message
  new_message = (indent_str + main_message.replace('\n', '\n' + indent_str) +
        tail)
  return new_message
