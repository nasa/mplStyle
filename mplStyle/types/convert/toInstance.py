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
#===========================================================================

#===========================================================================
def toInstance( value, classType, allowNone=False, name="" ):
   """: Convert a value to an instance of a type

   = INPUT VARIABLES
   - value       The input value to convert.
   - classType   The type of class the input must be.
   - allowNone   If true, then the Python variable None is allowed as
                 an input.  The user is responsible for handling the
                 usage and conversion of this parameter then.
   - name        A name to give to this converter instance. Used in making
                 error messages easier to understand.

   = RETURN VALUE
   - Returns a Instance object.
   """
   isBool = ( classType == bool )
   isFloat = ( classType == float )
   isComplex = ( classType == complex )

   if value is None and allowNone:
      return None
   
   if name:
      name = " '%s'" % name

   if not isinstance( value, classType ):
      # Convert an input string to the specified class type.  It is
      # normally used by the command line. We evaluate the value first
      # then check the type.
      if isinstance( value, str ):
         try:
            value = eval( value )
            if isinstance( value, classType ):
               return value
         except:
            s = "Error trying to convert an input string to the type of " \
                "%s.  The input is not the right type.\n" \
                "Input%s: %s" % ( classType, name, value )
            raise Exception( s )

      # For floats, allow an int
      # conversion before throwing an error.
      if isFloat:
         try:
            v = float( value )
            return v
         except:
            # Fall through to the error message below.
            pass

      if isComplex:
         try:
            v = complex( value, 0 )
            return v
         except:
            pass

      if isBool and value is not None:
         v = bool( value )
         return v

      s = "Error trying to convert an input to the type of %s.  " \
          "The input is not the right type.\n" \
          "Input%s: %s" % ( classType, name, value )
      raise Exception( s )

   return value



#===========================================================================
