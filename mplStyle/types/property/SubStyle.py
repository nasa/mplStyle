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

""": SubStyle property module."""

__version__ = "$Revision: #1 $"

#===========================================================================
from ..StyleProperty import StyleProperty
from copy import copy
from .. import convert as cvt
#===========================================================================

__all__ = [ 'SubStyle' ]

#===========================================================================
class SubStyle( StyleProperty ):
   """: A SubStyle style property.
   """

   #-----------------------------------------------------------------------
   def __init__( self, styleClass, **kwargs ):
      """: Create a new SubStyle object.

      This is a property that is an instance of a SubStyle type.

      = INPUT VARIABLES
      - styleClass   The class of the sub style type.
      - kwargs       Keyword argument values used when constructing an instance
                     of styleClass.
      """
      validator = cvt.Converter( cvt.toInstance, styleClass, allowNone=False )
      doc = kwargs.pop( 'doc', None )

      if doc is None:
         doc = "The value must be an instance of class '%s'." % \
               ( styleClass.__name__, )

      # Create an instance of the SubStyle -- this becomes the default value
      self.styleClass = styleClass
      self.kwargs = kwargs
      style = self.styleClass( **self.kwargs )

      StyleProperty.__init__( self, style, validator, doc )

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
      # If this is a dictionary, then convert it
      if isinstance( value, dict ):
         kw = {}
         kw.update( self.kwargs )
         kw.update( value )
         value = self.styleClass( **kw )

      # Now validate as before
      return StyleProperty.validate( self, value )

   #-----------------------------------------------------------------------
   def __str__( self ):
      """: Get a string representation of this instance.

      = RETURN VALUE
      - Returns a string represnetation of this property.
      """
      if self.owner:
         return "%s: %s.%s" % \
                ( self.styleClass.__name__,
                  self.owner.__name__,
                  self.name )
      elif self.name:
         return "%s: %s" % ( self.styleClass.__name__, self.name )
      else:
         return "%s" % ( self.styleClass.__name__ )

   #-----------------------------------------------------------------------

