#===========================================================================
#
# Copyright (c) 2014, California Institute of Technology.
# U.S. Government Sponsorship under NASA Contract NAS7-03001 is
# acknowledged.  All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#===========================================================================

""": type conversion utilities.

This module contains utilities used to convert data into a specific type.
"""

__version__ = "$Revision: #1 $"

#===========================================================================
import re
#===========================================================================

#===========================================================================
def _typeList( enums ):
   """: Return a list of allowed types for this converter."""
   pat = re.compile( "<type '([\w]+)'>" )

   foundTypes = []
   
   allowed = [ ]
   for v in enums:

      # Strip the Python formatted type string to give a better
      # string for built in types.  This changes things like
      # "<type bool'>" to "bool".
      typeStr = str( type( v ) )
      m = pat.match( typeStr )
      if m:
         typeStr = m.group( 1 )

      # Only add the type string if we haven't seen it before.
      if typeStr not in foundTypes:
         foundTypes.append( typeStr )
         allowed.append( typeStr )
      
   return allowed

#===========================================================================
def toEnum( value, enumDict, allowNone=False, caseInsens=False, name="" ):
   """: Convert a value to an enumeration.

   This converter will use the dictionary input to the constructor to
   convert a user input into an enumerated value.

   This works with C++ promoted enumerations as the mapped value.

   = EXAMPLE

   To convert from boolean flags to an enumeration do this:

   #   import style.types as stypes
   #
   #   value = True
   #   stypes.convert.toEnum( value, { True : "SOME_TRUE_VALUE",
   #                                   False : "SOME_FALSE_VALUE" } )

   = INPUT VARIABLES
   - value       The input value to convert.
   - enumDict    The conversion dictionary.
   - allowNone   If true, then the Python variable None is allowed as
                 an input.  The user is responsible for handling the
                 usage and conversion of this parameter then.
   - caseInsens  If true, then the string is case insensitive.
   - name        A name to give to this converter instance. Used in making
                 error messages easier to understand.

   = RETURN VALUE
   - Returns a Enum object.
   """
   if value is None and allowNone:
      return None
   
   if name:
      name = " '%s'" % name

   # Convert everything to upper case for case insensitivity.
   enums = enumDict
   if caseInsens:
      if isinstance( value, str ):
         value = value.upper()
      enums = { key.upper(): value for ( key, value ) in enumDict.iteritems() }

   try:
      # Return the dictionary value for the input.
      if value in enums:
         return enums[value]

      # See if the value is already one of the dictionary values.
      for v in enums.itervalues():
         if value == v:
            return value

      # See if the value is a string that can be converted to the correct
      # type.
      allowed = _typeList( enumDict )
      if isinstance( value, str ) and 'str' not in allowed:
         value = eval( value )
         return enums[value]
      
   except:
      # Fall through to error below.  This blanket except is used
      # because some callers do OneOf w/ an enum which means this
      # needs to support weird inputs like a list for the value input
      # which will fail with python exception.
      pass
   
   msg = "Error trying to convert the input argument.  The input is not " \
         "valid.\n   Input%s: %s\n   Valid inputs are: " % ( name, value )
   for v in enumDict:
      msg += "%s, " % repr( v )
   raise Exception( msg )
   

#===========================================================================
