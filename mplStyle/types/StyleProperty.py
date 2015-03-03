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

""": StyleProperty module."""

__version__ = "$Revision: #1 $"

#===========================================================================
from . import util
import weakref
from copy import copy
#===========================================================================

__all__ = [ 'StyleProperty' ]

#===========================================================================
class StyleProperty( object ):
   """: The base class of all style types.

   Derivations of this class should overload the 'validate' method to
   determine what is a valid value for that Style property type.
   """

   #-----------------------------------------------------------------------
   def __init__( self, default, validator = None, doc = "" ):
      """: Create a new Style object.

      = INPUT VARIABLES
      - default     The default value that instances will be initialized with.
      """
      # The default value for the class instance
      self._default = None

      # The name of the property.  This will be set by the class creator.
      self._name = None

      # The class this property is associated with
      self._owner = None

      # An optional callable object that will validate an object assigned
      # to this property.
      self.validator = validator

      # Set the docstring for this property.
      self.__doc__ = doc

      # Set and validate the default value
      self.default = default

   #-----------------------------------------------------------------------
   @property
   def name( self ):
      """: The name of the instance of this property type.
      """
      # We really-really do not want anybody changing the name of each property
      # instance, so we make this read-only.
      return self._name

   #-----------------------------------------------------------------------
   @property
   def owner( self ):
      """: The class that owns this property instance.
      """
      # We really-really do not want anybody changing the this of each property
      # instance, so we make this read-only.
      return self._owner

   #-----------------------------------------------------------------------
   @property
   def default( self ):
      """: The default value for instances of this property type.
      """
      return self._default

   @default.setter
   def default( self, value ):
      """: Validate and set the default value.

      = INPUT VARIABLES
      - value   The value to use for the default.
      """
      self._default = self.validate( value )

   #-----------------------------------------------------------------------
   def initialize( self, instance, memberName, kwargs ):
      """: Set the named property to the default value.

      = INPUT VARIABLES
      - instance    The class instance that contains the property to be set.
      - memberName  The name of the member to be set to the default value.
      - kwargs      A dictionary of possible initial values to search for an
                    initial value to use for this property.  If a value is
                    found for this property, it will be removed from the
                    dictionary.
      """
      # Determine the initial value
      if memberName in kwargs:
         value = kwargs.pop( memberName )
      else:
         # We must create a copy of the default value, otherwise we
         # might accidentally change the default value.  This is
         # particularly true if the default is a container object.
         value = copy( self.default )

      # Set the new copy as an instance member.
      # This will end up calling __set__.
      setattr( instance, memberName, value )

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
      if self.validator:
         try:
            result = self.validator( value )
            return result
         except Exception, e:
            name = self.name
            if self.owner:
               name = "%s.%s" % ( self.owner.__name__, name )
            msg = "Error trying to validate the '%s' property." % name
            raise util.mergeExceptions( e, msg )
      else:
         # accept whatever it is given.
         return value

   #-----------------------------------------------------------------------
   def __call__( self, value ):
      """: This will perform validation of the value

      = ERROR CONDITIONS
      - Will throw an exception if the specified value is invalid.

      = INPUT VARIABLES
      - value   The value to set the instance of this property to.

      = RETURN VALUE
      - Returns a valid value.
      """
      return self.validate( value )

   #-----------------------------------------------------------------------
   def __str__( self ):
      """: Get a string representation of this instance.

      = RETURN VALUE
      - Returns a string represnetation of this property.
      """
      if self.owner:
         return "%s: %s.%s" % \
                ( self.__class__.__name__,
                  self.owner.__name__,
                  self.name )
      elif self.name:
         return "%s: %s" % ( self.__class__.__name__, self.name )
      else:
         return "%s" % ( self.__class__.__name__ )

   #-----------------------------------------------------------------------
   def __get__( self, instance, owner ):
      """: Get the value stored for the instance of this class.

      The presence of the __get__ and __set__ methods let python know that
      this is a 'descriptor' class.  This allows us to control how 
      instances of this class act when being get and/or set.

      The actual value is stored in the instance's __dict__

      = INPUT VARIABLES
      - instance    The class (or container) instance that owns an instance
                    of this class.  Since the StyleProperty class is only used
                    to define style properties in sub-classes of SubStyle,
                    we can assume that the instance is a sub-class of SubStyle.
      - owner       The class type of the instance that owns an instance of
                    this class.

      = RETURN VALUE
      - Returns the value for this stype type instance.
      """
      if instance:
         # Return the value stored in the class instance
         return instance.__dict__[ self.name ]

      else:
         # We are getting the value from the class and not from the
         # class instance.
         return self

   #-----------------------------------------------------------------------
   def __set__( self, instance, value ):
      """: Set the value stored for the instance of this class.

      The presence of the __get__ and __set__ methods let python know that
      this is a 'descriptor' class.  This allows us to control how 
      instances of this class act when being get and/or set.

      Oddly enough, when we call 'setattr' on the class instance that cotains
      this instance, this function is called and the value is never set in 
      the instance class' __dict__. So we store the actual value in the
      instance's __dict__

      = INPUT VARIABLES
      - instance    The class (or container) instance that owns an instance
                    of this class.  Since the StyleProperty class is only used
                    to define style properties in sub-classes of SubStyle,
                    we can assume that the instance is a sub-class of SubStyle.
      - value       The value to set.  This will be validated first.

      """
      instance.__dict__[ self.name ] = self.validate( value )

   #-----------------------------------------------------------------------

