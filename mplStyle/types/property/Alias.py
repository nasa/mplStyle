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

""": Alias property module."""

__version__ = "$Revision: #1 $"

#===========================================================================
from ..StyleProperty import StyleProperty
#===========================================================================

__all__ = [ 'Alias' ]

#===========================================================================
class Alias( StyleProperty ):
   """: A Alias style property.
   """

   #-----------------------------------------------------------------------
   def __init__( self, alias, isProperty = False, doc = "" ):
      """: Create a new Alias object.

      This will alias a values stored elsewhere in the class this property
      belongs to.

      = INPUT VARIABLES
      - alias      The name of the property this is an alias to.
      - isProperty If True, then this is an alias to another property (or 
                   sub-property) otherwise it is an alias to a data member
                   of the class this Alias is in.
      - doc        The docstring for this property.
      """
      # These must be defined before calling the base class
      self.alias = alias
      self.isProperty = isProperty
      self.typeName = "Unknown"

      StyleProperty.__init__( self, None, doc = doc )

   #-----------------------------------------------------------------------
   def _getParentOfProperty( self, instance ):
      """: Get the parent of the specified property.

      = INPUT VARIABLES
      - instance   The instance of the class this is a property in.

      = RETURN VALUES
      - Returns the parent object that has the property and the single name of
        the property without any parent objects.
      """
      objectNames = self.alias.split( '.' )

      if isinstance( instance, type(object) ):
         currentObject = instance
         currentName = instance.__name__
         currentPath = "%s" % currentName
      else:
         currentObject = instance
         currentName = instance.__class__.__name__
         currentPath = "%s" % currentName

      nextName = objectNames.pop( 0 )

      while len( objectNames ):
         attrs = dir( currentObject )
         if hasattr( currentObject, nextName ):
            currentObject = getattr( currentObject, nextName )
            currentName = nextName
            currentPath = '%s.%s' % (currentPath, currentName)
            nextName = objectNames.pop( 0 )
         elif nextName in attrs:
            # If we get here then we are probably looking for a property that
            # has not been initialized yet, so just return None
            return None, None
         else:
            msg  = "Invalid Property '%s'\n" % self.alias
            msg += "%s does not have a property named '%s'.  " % \
                   (currentPath, nextName)
            msg += "Valid values are:\n"

            propertyList = dir( currentObject )
            propertyList.sort()

            for name in propertyList:
               if name.startswith( '__' ):
                  continue
               msg += "   * %s\n" % name

            raise Exception( msg )

      return currentObject, nextName

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
         # Get the parent object and the property name
         parent, name = self._getParentOfProperty( instance )

         if parent is None:
            value = None
         elif self.isProperty:
            value = getattr( parent, name )
            subProperty = getattr( parent.__class__, name )
            self.typeName = subProperty.__class__.__name__
         else:
            if hasattr( parent, name ):
               # We are aliased to an instance member variable
               subProperty = getattr( parent, name )
               self.typeName = subProperty.__class__.__name__
            else:
               subProperty = getattr( instance, name )

            if isinstance( subProperty, StyleProperty ):
               # Make sure the sub-property is using our name
               subProperty._name = self.name
               value = subProperty.__get__( parent, parent.__class__ )
            else:
               value = subProperty

         # we set the value in the local dictionary to help with introspection
         instance.__dict__[ self.name ] = value

         # return the value
         return value
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
      # Avoid circular imports
      from ..SubStyle import SubStyle

      # Get the parent object and the property name
      parent, name = self._getParentOfProperty( instance )
      if parent:
         if self.isProperty:
            setattr( parent, name, value )
            # Get the validated value, so we can store it locally
            value = getattr( parent, name )
            subProperty = getattr( parent.__class__, name )
            self.typeName = subProperty.__class__.__name__
         elif isinstance( parent, SubStyle ) and parent is not instance:
            # The parent handle the getting / setting
            setattr( parent, name, value )
            value = getattr( parent, name )
         elif hasattr( parent, name ):
            # We are aliased to an instance member variable
            subProperty = getattr( parent, name )
            self.typeName = subProperty.__class__.__name__

            if isinstance( subProperty, StyleProperty ):
               subProperty._name = self.name
               subProperty.__set__( parent, value )

               # Get the validated value, so we can store it locally
               value = subProperty.__get__( parent, None )
            else:
               setattr( parent, name, value )
         else:
            setattr( parent, name, value )

      # we set the value in the local dictionary to help with introspection
      instance.__dict__[ self.name ] = value

   #-----------------------------------------------------------------------
   def __str__( self ):
      """: Get a string representation of this instance.

      = RETURN VALUE
      - Returns a string represnetation of this property.
      """
      try:
         subType = self.getType()
      except:
         subType = None

      if subType:
         typeName = subType.__name__
      else:
         typeName = self.typeName

      if self.owner:
         return "%s: %s.%s" % (self.typeName, self.owner.__name__, self.name)
      elif self.name:
         return "%s: %s" % (self.typeName, self.name)
      else:
         return self.typeName

   #-----------------------------------------------------------------------
   def initialize( self, instance, memberName, kwargs ):
      """: Set the named property to the default value.

      = INPUT VARIABLES
      - instance    The class instance that contains the property to be set.
      - memberName  The name of the member to be set to the default value.
      - kwargs      A dictionary of possible initial values.  This is ignored
                    for this class.
      """
      # Alias does nothing on initialization.  Whatever it points to
      # handles this when it is initialized.
      assert( self.name == memberName )
      instance.__dict__[ memberName ] = None

   #-----------------------------------------------------------------------
   def getType( self, instance = None ):
      """: Get the type this alias points to.

      = INPUT VARIABLES
      - instance   The SubStyle instance this Alias is a property of.

      = RETURN VALUE
      - Returns the type this alias points to.
      """
      # Import here to prevent circular imports
      from ..SubStyle import SubStyle

      result = None

      if instance:
         owner = instance
      else:
         owner = self.owner

      parent, name = self._getParentOfProperty( owner )

      if parent:
         if self.isProperty:
            if instance:
               result = getattr( parent.__class__, name )
            else:
               result = getattr( parent, name ).__class__
         elif instance:
            if isinstance( parent, SubStyle ) and \
               parent.__class__ is not self.owner:
               if hasattr( parent.__class__, name ):
                  # We are aliased to an instance member variable
                  result = getattr( parent.__class__, name )
            elif hasattr( parent, name ):
               # We are aliased to a member variable
               result = getattr( parent, name )
         elif hasattr( parent, name ):
            # get the attribute
            result = getattr( parent, name ).__class__
         else:
            # Not a property and no instance means we cannot determine the type
            result = None

      return result

   #-----------------------------------------------------------------------

