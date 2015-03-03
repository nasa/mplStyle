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

""": OneOf property module."""

__version__ = "$Revision: #1 $"

#===========================================================================
from ..StyleProperty import StyleProperty

from .. import convert as cvt
#===========================================================================

__all__ = [ 'OneOf' ]

#===========================================================================
class OneOf( StyleProperty ):
   """: A OneOf style property.
   """

   #-----------------------------------------------------------------------
   def __init__( self, converters, default = None, doc = None ):
      """: Create a new OneOf object.

      = INPUT VARIABLES
      - default     The default value that instances will be initialized with.
      - doc         The docstring for this property.
      """
      if doc is None:
         doc = "\nThe value must satisfy one of the following converters:"
         for c in converters:
            doc += "   + '%s'\n" % ( c, )
         doc += "\n"

      self.converters = converters

      validator = cvt.Converter( cvt.toOneOf, converters )
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
      # Since we know that the converters list is the first argument we are
      # passing into the Converter CTOR up in __init__, we can reference it
      # directly here.  We need to make sure that the children types all
      # have the 'name' set so the error messages don't get confusing.  We
      # Do this here instead of in the CTOR because the 'name' gets set just
      # after __init__ finishes.
      for cvtType in self.validator.args[0]:
         if isinstance( cvtType, StyleProperty ):
            cvtType._name = self.name

      # Call the base class validate method
      result = StyleProperty.validate( self, value )

      return result

   #-----------------------------------------------------------------------

