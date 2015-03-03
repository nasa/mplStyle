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

""": Float property module."""

__version__ = "$Revision: #1 $"

#===========================================================================
from ..StyleProperty import StyleProperty

from .. import convert as cvt
#===========================================================================

__all__ = [ 'Float' ]

#===========================================================================
class Float( StyleProperty ):
   """: A Float style property.
   """

   #-----------------------------------------------------------------------
   def __init__( self, min = None, max = None, default = None, doc = "" ):
      """: Create a new Float object.

      = INPUT VARIABLES
      - min         The minimum float value allowed.
      - max         The maximum float value allowed.
      - default     The default value that instances will be initialized with.
      - doc         The docstring for this property.
      """
      if min is not None:
         doc += "\nThe value must be greater than: %s" % (min,)
      if max is not None:
         doc += "\nThe value must be less than: %s" % (max,)

      validator = cvt.Converter( cvt.toType, float, allowNone=True )

      # These must be defined before calling the base class
      self.min = min
      self.max = max

      StyleProperty.__init__( self, default, validator, doc )

   #-----------------------------------------------------------------------
   def validate( self, value ):
      """: Validate and return a valid value

      = ERROR CONDITIONS
      - Will throw an exception if the specified value is invalid.

      = INPUT VARIABLES
      - value   The value to set the instance of this property to.

      = RETURN VALUE
      - Returns a valid value.
      """
      # First make sure it is a floating point number
      result = StyleProperty.validate( self, value )

      if result is None:
         return result

      msg = ""

      # Now make sure it is in the proper range.
      if self.min is not None:
         if result < self.min:
            msg += "Value must be greater than %s\n" % ( self.min, )

      if self.max is not None:
         if result > self.max:
            msg += "Value must be less than %s\n" % ( self.max, )

      if msg:
         msg = "Error converting the '%s' value.\n%sValue = %s" % \
               ( self.name, msg, value )
         raise Exception( msg )

      return result

   #-----------------------------------------------------------------------

