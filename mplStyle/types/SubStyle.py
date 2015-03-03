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

""": SubStyle module.

This implements a system similar to Enthought traits, but much, much simpler.
"""

__version__ = "$Revision: #1 $"

#===========================================================================

import inspect

from copy import copy

from .StyleProperty import StyleProperty
#===========================================================================

__all__ = [ 'SubStyle' ]

#===========================================================================
class _SubStyleFactory( type ):
   """: Allow us to create/validate instance attributes.

   This will instantiate any attributes in the derived classes.

   The calling sequence is as follows:

      Upon loading the SubStyle class definition:

         # Allocate the class definition as an object
         _SubStyleFactory.__new__

         # Initialize the class definition instance
         _SubStyleFactory.__init__

      Upon instancing SubStyle:

         # Create an instance of SubStyle by calling __new__ and __init__
         _SubStyleFactory.__call__

            # Allocate the SubStyle instance
            SubStyle.__new__

            # Initialize the SubStyle instance
            SubStyle.__init__
   """

   #-----------------------------------------------------------------------
   def __new__( meta, name, bases, members ):
      """: Create a new SubStyle class.

      This will instantiate all attributes that inherit from 'StyleProperty'
      as new instance members.

      = INPUT VARIABLES
      - meta     An instance of this meta class (_SubStyleMeta).
      - name     The name of the class being created (ie 'SubStyle')
      - bases    A tuple of base classes for the class instance being created.
      - members  A dictionary of class members indexed by name.

      = RETURN VALUE
      - Returns a new instance of SubStyle.
      """
      properties = []
      # Search for any members that are instances of or sub-types of
      # StyleProperty and add the instance into the dictionary of attributes
      # used to create the SubStyle class.
      for key in members:
         value = members[ key ]

         if isinstance( value, StyleProperty ):
            # It is already instanced, so just set the name
            # Each instance of StyleProperty likes to know what it's name is.
            value._name = key
            properties.append( key )

      # Call the parent class new -- makes a new class type
      return type.__new__( meta, name, bases, members )

   #-----------------------------------------------------------------------
   def __init__( cls, name, bases, members ):
      """: Initialize a new SubStyle class.

      This is called *before* SubStyle.__init__

      = INPUT VARIABLES
      - cls      The SubStyle class.
      - name     The name of the class being created (ie 'SubStyle')
      - bases    A tuple of base classes for the class instance being created.
      - members  A dictionary of class members indexed by name.
      """
      # Delay load to avoid circular imports
      from .property import Alias

      # Each SubStyle derived class needs to track the aliases it contains
      cls._aliases = {}

      # Each SubStyle derived class has a cache of property names
      cls._propertyNames = []

      # Let each property member know what class it belongs to
      # We do this here instead of in SubStyle.__new__ because:
      #   1) It only needs to be done once for any particular SubStyle derived
      #      class.  __new__ will be called every time a SubStyle derived class
      #      is instanced.
      #   2) The _owner value might be needed for error messages or
      #      documentation introspection without any SubStyle derived classes
      #      being instanced.
      for key in members:
         value = members[ key ]

         if isinstance( value, StyleProperty ):
            value._owner = cls

         if isinstance( value, Alias ):
            # Keep track of aliases
            propName = value.alias
            if propName not in cls._aliases:
               cls._aliases[ propName ] = []

            if key not in cls._aliases[ propName ]:
               cls._aliases[ propName ].append( key )

      # Call the base class init method
      type.__init__( cls, name, bases, members )

      # Pre-cache the names of all properties.
      #NOTE: We do this here so that all levels of derived class
      #      definitions have been initialized.
      for name in dir( cls ):
         value = getattr( cls, name )
         if isinstance( value, StyleProperty ):
            cls._propertyNames.append( name )

      cls._propertyNames.sort()

   #-----------------------------------------------------------------------
   def __call__( cls, *args, **kwargs ):
      """: Construct an instance of SubStyle class.

      This is called *before* SubStyle.__new__

      = INPUT VARIABLES
      - cls      The SubStyle class.
      - args     The arguments that will be passed to the ctor.
      - kwargs   The keyword arguments that will be passed to the ctor.
      """
      # create and initialize an instance of the class
      instance = type.__call__( cls, *args, **kwargs )

      # Set the restricted setattr flag for the instance
      instance._restricted_setattr = True

      # Return the newly created and initialized instance
      return instance

#===========================================================================
class SubStyle( object ):
   """: A class that enforces type checking on data attributes.

   This is used with the Style system for enforcing type-correctness on 
   data attributes.
   """

   # Define a wrapper for how this class (and its derivatives) are created.
   __metaclass__ = _SubStyleFactory

   # When set to True this flag prevents setting attributes on instances of
   # this class that do not already exist in the class.  We need a flag because
   # in order to create the attributes in the first place we need to have it
   # disabled.  This flag will be flipped by the metaclass 'call' method.
   _restricted_setattr = False

   _propertyNames = []

   #-----------------------------------------------------------------------
   def __new__( cls, **kwargs ):
      """: Initialize the StyleProperty instances to their defaults.

      = INPUT VARIABLES
      - cls     The class type being created.
      - kwargs  The keyword arguments passed into the constructor.
      """
      # Call the base class new
      instance = object.__new__( cls, **kwargs )

      # For each class member that is a StyleProperty, set to default
      for memberName in dir( cls ):
         member = getattr( cls, memberName )
         if isinstance( member, StyleProperty ):
            # Set the value for this instance to the default value
            member.initialize( instance, memberName, kwargs )

      # Return the newly created instance
      return instance

   #-----------------------------------------------------------------------
   def __init__( self, **kwargs ):
      """: Create a new SubStyle object.

      = INPUT VARIABLES
      - kwargs  A dictionary of keywords mapping style properties to their
                values.
      """
      for key in kwargs:
         # Only set keywords that were defined as properties.
         fullKey = key
         if '.' in key:
            idx = key.find( '.' )
            key = key[ :idx ]

         if key not in self.__dict__:
            msg  = "SubStyle was given a property name that it does not "
            msg += "recognize.\n"
            msg += "   Invalid keyword '%s' = %s\n" % (key, kwargs[key])
            msg += "   Valid Keywords are:\n"
            propertyList = self.propertyNames()
            for property in propertyList:
               msg += "   * '%s'\n" % (property,)
            raise Exception( msg )
         else:
            setattr( self, fullKey, kwargs[ fullKey ] )

   #-----------------------------------------------------------------------
   def __setattr__( self, name, value ):
      """: Set the named attribute to the specified value.

      = ERROR CONDITIONS
      - This will throw an error if attempting to set an attribute that does
        not already exist.

      = INPUT VARIABLES
      - name     The name of the attribute to set.
      - value    The value to give to the named attribute.
      """
      properties = self.propertyNames()

      subName = ''
      if '.' in name:
         idx = name.find( '.' )
         subName = name[ idx+1: ]
         name = name[ :idx ]

      if hasattr( self, name ) or ( name in properties ) or \
         ( not self._restricted_setattr ):
         if subName:
            obj = getattr( self, name )
            setattr( obj, subName, value )
         else:
            object.__setattr__( self, name, value )
      else:
         msg = "Unable to set the property '%s' to the specified value.  " \
               "No property with that name exists.  Valid properties are:" \
               "\n" % name

         for p in properties:
            msg += " * %s\n" % p

         raise Exception( msg )

   #-----------------------------------------------------------------------
   def __str__( self ):
      """: Get a string representation of this instance.

      = RETURN VALUE
      - Returns a string represnetation of this property.
      """
      return self.format()

   #-----------------------------------------------------------------------
   def format( self, indent = 0, indentFirstLine = True ):
      """: Format as a string representation of this instance.

      = INPUT VARIABLE
      - indent     The number of spaces to indent the resultant string.

      = RETURN VALUE
      - Returns a string represnetation of this property.
      """
      kw = self.kwargs()

      indentStr = ' '
      if indentFirstLine:
         indentStr = ' ' * indent

      s = "%s%s:" % ( indentStr, self.__class__.__name__ )

      keywords = kw.keys()
      keywords.sort()
      for key in keywords:
         value = kw[ key ]
         if isinstance( value, SubStyle ):
            if value.hasAnySet():
               valueStr = value.format( indent + 3, False )
            else:
               continue
         else:
            valueStr = str( value )

         s += "\n%s   * %s = %s" % ( ' ' * indent, key, valueStr )

      return s


   #-----------------------------------------------------------------------
   @classmethod
   def propertyNames( cls ):
      """: Get a list of all of the properties belonging to this class.

      = RETURN VALUES
      - A sorted list of the name of all defined properties for this class
        and its parents.
      """
      return cls._propertyNames

   #-----------------------------------------------------------------------
   def getPropertyType( self, name ):
      """ Get the type of the named property.

      = INPUT VARIABLE
      - name    The name of the property whose type we want.

      = RETURN VALUE
      - Returns the type of the named property.  If the property does not
        exist, then this returns None.
      """
      # Delay load to avoid circular imports
      from .property import Alias

      prop = None

      cls = self.__class__
      if hasattr( cls, name ):
         prop = getattr( cls, name )

         if isinstance( prop, Alias ):
            prop = prop.getType( self )

      return prop.__class__

   #-----------------------------------------------------------------------
   def hasAnySet( self ):
      """: Determine if there is any property or sub-property set.

      = RETURN VALUE
      - Returns True if this SubStyle has any property values set.
      """
      properties = self.propertyNames()

      for p in properties:
         value = getattr( self, p )
         if value is not None:
            if isinstance( value, SubStyle ):
               result = value.hasAnySet()
               if result:
                  return True
            else:
               return True

      return False

   #-----------------------------------------------------------------------
   def getValue( self, name, defaults = {}, **kwargs ):
      """Get the value of the named property.

      What this does is, given a name of a property, it will:

         1) If the named property is passed in as a keyword argument and it is
            not None, then the keyword value will be returned.

         2) If the named property is set for this instance (i.e. not None),
            then that value is used.

         3) If the named property is in the default dictionary, then tha value
            will be returned.

         4) None is returned

      = NOTE
      - This does *NOT* check to see if the named property exists first as
        this is a private method only called for properties we know exist.

      = INPUT VARIABLES
      - name      The name of the property to retrieve.
      - defaults  The default value dictionary to use.
      - kwargs    A dictionary of values that supercede all else

      = RETURN VALUE
      - Return the value of the named property, resolving any value set in
        the defaults (as necessary).
      """
      subName = ""

      if '.' in name:
         idx = name.find( '.' )
         subName = name[ idx + 1: ]
         name = name[ 0: idx ]

      # First check the kwargs
      value = kwargs.get( name, None )

      # Check for aliases in the kwargs
      if (value is None) and (name in self._aliases):
         for alias in self._aliases[ name ]:
            value = kwargs.get( alias, None )
            if value is not None:
               break

      if value is None:
         value = getattr( self, name, value )

      if subName and value is not None:
         # We need to recurse into a sub-property
         value = value.getValue( subName, defaults, **kwargs )

      if value is None:
         # The value is unset, so check the defaults we were given
         value = defaults.get( name, None )

      # Check for aliases in the defaults
      if (value is None) and (name in self._aliases):
         for alias in self._aliases[ name ]:
            value = defaults.get( alias, None )
            if value is not None:
               break

      return value

   #-----------------------------------------------------------------------
   def update( self, subStyle ):
      """: Update this with the values specified in the other sub-style.

      = INPUT VARIABLES
      - subStyle    The sub-style whose values we are going to use to update
                    this sub-style.
      """
      if subStyle is None:
         return

      properties = self.propertyNames()

      for p in properties:
         # Only if the sub-style has the property
         if hasattr( subStyle, p ):
            v1 = getattr( self, p )
            v2 = getattr( subStyle, p )

            # Only if the sub-style property is set
            if v2 is not None:
               if isinstance( v1, SubStyle ):
                  # If this is a sub-sub-style
                  v1.update( v2 )
               else:
                  # Otherwise just set the value
                  setattr( self, p, v2 )

   #-----------------------------------------------------------------------
   def kwargs( self, recursive = False ):
      """ Get this sub-style as keyword arguments.

      = RETURN VALUE
      - Returns this sub-style as a series of keyword-arguments.
      """
      properties = self.propertyNames()

      kw = {}

      for p in properties:
         value = getattr( self, p )
         if value != getattr( self.__class__, p ).default:
         #if value is not None:
            if isinstance( value, SubStyle ):
               if recursive:
                  kw[ p ] = value.kwargs( recursive )
               else:
                  kw[ p ] = value.copy()
            else:
               kw[ p ] = value

      return kw

   #-----------------------------------------------------------------------
   def __copy__( self ):
      """: Get a copy of this object.

      This is provided so that the python copy method will work.

      = RETURN VALUE
      - Return  a copy of this class type
      """
      result = self.__class__( **self.kwargs() )
      return result

   def copy( self ):
      """: Get a copy of this object.

      = RETURN VALUE
      - Return  a copy of this class type
      """
      return self.__copy__()

