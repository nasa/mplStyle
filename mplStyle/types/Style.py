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

""": A class for containing style information."""

__version__ = "$Revision: #1 $"

#===========================================================================
#===========================================================================

__all__ = [ 'Style' ]

#===========================================================================
class _StyleFactory( type ):
   """: Allow us to create/validate instance attributes.

   This is here to allow us to have restricted access styles if desired.

   The calling sequence is as follows:

      Upon loading the Style class definition:

         # Allocate the class definition as an object
         _StyleFactory.__new__

         # Initialize the class definition instance
         _StyleFactory.__init__

      Upon instancing Style:

         # Create an instance of Style by calling __new__ and __init__
         _StyleFactory.__call__

            # Allocate the Style instance
            Style.__new__

            # Initialize the Style instance
            Style.__init__
   """

   #-----------------------------------------------------------------------
   def __call__( cls, *args, **kwargs ):
      """: Construct an instance of Style class.

      This is called *before* Style.__new__

      = INPUT VARIABLES
      - cls      The Style class.
      - args     The arguments that will be passed to the ctor.
      - kwargs   The keyword arguments that will be passed to the ctor.
      """
      # create and initialize an instance of the class
      instance = type.__call__( cls, *args, **kwargs )

      # Set the flag for the instance indicating init has finished.
      instance._completed_init = True

      # Return the newly created and initialized instance
      return instance

#===========================================================================
class Style( object ):
   """: An object used to contain style information.

   When using this class it is best to sub-class and overloard the following
   methods:

      * copy
        The base Style class cannot know about the derived class CTOR
        calling sequence or values, therefor the derived class needs to
        construct and create the copy.

      * update
        The base Style class cannot differentiate between properties and any
        'other' members of the derived class in order to perform an update. 
        The base Style class has no way of knowing into what members it needs
        to recurse into in order to properly update.

      * applyStyle
        This is a static method that is specific to the derived class.  This
        is what applies the derived style to an instance of the object type
        it was defined for.
   """

   # Define a wrapper for how this class (and its derivatives) are created.
   __metaclass__ = _StyleFactory

   # Can be used by derived classes to test if a class instance has
   # finished constructing.   Some derived classes might use this to
   # restrict setattr access after __init__ has completed.
   _completed_init = False

   #-----------------------------------------------------------------------
   def __init__( self, name, initialValues = {}, parent = None, custom = None ):
      """: Create a new Style object.

      If this style has a parent, then it will use the values set by
      the parent if that value is not set in this style.

      = INPUT VARIABLES
      - name      The name to give this style.
      - initialValues  A dictionary of keyword-value pairs that (if present)
                       will set the appropriate style property with the
                       specified value.
      - parent    The parent style of this style.
      - custom    A callable object or function that will be passed the object
                  that needs styling.
      """

      # This cannot be changed after creating.
      self._name = name

      # All Styles can have a parent style for resolving values
      if isinstance( parent, Style ):
         parent = [ parent ]

      self.parent = parent

      # Custom style function.
      self.custom = custom

      # initialize any specified properties
      for key in initialValues:
         self.setValue( key, initialValues[ key ] )

   #-----------------------------------------------------------------------
   def _getParentOfProperty( self, property ):
      """: Get the parent of the specified property.

      = INPUT VARIABLES
      - property   A string name of the property to retrieve.  If the property
                   is nested in other data objects, then each accessor is
                   named and concatenated together with '.'  Eg 'a.b.property'

      = RETURN VALUES
      - Returns the parent object that has the property and the single name of
        the property without any parent objects.
      """
      objectNames = property.split( '.' )

      currentObject = self
      currentName = self.__class__.__name__
      currentPath = "%s" % currentName

      nextName = objectNames.pop( 0 )

      while len( objectNames ):
         if hasattr( currentObject, nextName ):
            currentObject = getattr( currentObject, nextName )
            currentName = nextName
            currentPath = '%s.%s' % (currentPath, currentName)
            nextName = objectNames.pop( 0 )
         else:
            msg  = "Invalid Property '%s'\n" % property
            msg += "%s does not have a property named '%s'.  " % \
                   (currentPath, nextName)
            msg += "Valid values are:\n"

            propertyList = dir( currentObject )
            propertyList.sort()

            for name in propertyList:
               if name.startswith( '_' ):
                  continue
               msg += "   * %s\n" % name

            raise Exception( msg )

      return currentObject, nextName

   #-----------------------------------------------------------------------
   def getResolvedValue( self, property ):
      """: Get the value of the specified property.

      If the specified property is not set by this style, then this will
      return the result of calling 'getResolvedValue' on the parent style
      (if any).

      = ERROR CONDITIONS
      - Will throw an exception if the requested property does not exist.

      = INPUT VARIABLES
      - property   The style property whose value you wish to get.

      = RETURN VALUE
      - Returns the resolved value of the requested property.  Will return
        None if not set.
      """
      value = self.getValue( property )

      if ( value is None ) and self.parent:
         for p in self.parent:
            value = p.getResolvedValue( property )
            if value is not None:
               break

      return value

   #-----------------------------------------------------------------------
   def getValue( self, property, default = None ):
      """: Get the value of the specified property.

      This will get the value of the specified property as set by this style.

      = ERROR CONDITIONS
      - Will throw an exception if the requested property does not exist.

      = INPUT VARIABLES
      - property   The style property whose value you wish to get.

      = RETURN VALUE
      - Returns the value of the requested property.  Will return
        None if not set.
      """
      # Split and traverse the style heirarchy
      parent, itemName = self._getParentOfProperty( property )

      if not hasattr( parent, itemName ):
         msg  = "Could not get the value '%s'\n" % property
         msg += "Valid values are:\n"

         propertyList = dir( parent )
         propertyList.sort()

         for name in propertyList:
            if name.startswith( '_' ):
               continue
            msg += "   * %s" % name

         raise Exception( msg )

      # return the value
      result = getattr( parent, itemName )

      if result is None:
         result = default

      return result

   #-----------------------------------------------------------------------
   def setValue( self, property, value ):
      """: Set the value of the specified property.

      This will traverse the style heirarchy to set the specified property
      with the given value.  Nested property values can be specified by
      concatenating them with '.'  Eg: :code:`'style.figure.text.size'`.

      = ERROR CONDITIONS
      - Will throw an exception if the requested property does not exist.

      = INPUT VARIABLES
      - property   The style property whose value you wish to set.
      - value      The value to give to the specified property.
      """
      # Split and traverse the style heirarchy
      parent, itemName = self._getParentOfProperty( property )

      if not hasattr( parent, itemName ):
         msg  = "Could not set the value '%s'\n" % property
         msg += "Valid values are:\n"

         propertyList = dir( parent )
         propertyList.sort()

         for name in propertyList:
            if name.startswith( '_' ):
               continue
            msg += "   * %s" % name

         raise Exception( msg )

      # set the value
      setattr( parent, itemName, value )

   #-----------------------------------------------------------------------
   def resolve( self, name, style = None ):
      """: Resolve all properties into a single Style.

      This will return a new unnamed style that has as many property
      values set as possible.  This will use the result of the resolved parent,
      apply any values set by this style, then finally any values set by the
      optional style passed into this function.

      = NOTE
      This will not take into account any custom defined formatter functions.

      = INPUT VARIABLES
      - name     The name to give to the new resolved style.
      - style    If specified, this is a style whose property values
                 supercede any values set by this style.  Only the values
                 set by 'style' will be used.  This function will *not*
                 resolve 'style' first, if that is the desired, then you
                 must call 'resolve' on 'style' before passing it into
                 this function. 

      = RETURN VALUE
      - Returns a single style with all properties resolved to a value
        (where possible).
      """
      if self.parent:
         newStyle = self.parent[0].resolve( name )

         for p in self.parent[1:]:
            newStyle.update( p.resolve(None) )

         newStyle.update( self )
      else:
         newStyle = self.copy( name )
         newStyle.parent = None
         newStyle.custom = None

      if ( style ):
         newStyle.update( style )

      return newStyle

   #-----------------------------------------------------------------------
   def copy( self, newName ):
      """: Make a copy of this Style and give it the specified name.

      When making a copy of a style with a parent, the new style will
      have the same parent.

      When making a copy of a style with a custom formatter, the new style
      will have the same formatter.

      = INPUT VARIABLES
      - newName    The name to give to the new style.

      = RETURN VALUE
      - Return a new Style with the given name that is a copy of this style.
      """
      from copy import copy

      # Specialize in derived class.
      return Style( newName, parent = copy(self.parent), custom = self.custom )

   #-----------------------------------------------------------------------
   def update( self, style ):
      """: Update this style with the values in the given style.

      This will *not* update this style's parent with that of the given style.

      = INPUT VARIABLES
      - style     Will use to set this style's values.
      """
      # Nothing to do here -- Specialize in derived class.
      pass

   #-----------------------------------------------------------------------
   def apply( self, obj, recursive = True, filter = None, postProcess = None ):
      """Resolve this style and apply its values to the given object.

      = INPUT VARIABLES
      - obj          The object to apply the style to.
      - recursive    If True, then, when appropriate, the style will recursively
                     apply itself to child objects.
      - filter       A filter function for determining what should have this
                     style applied to it.  The function will be passed the
                     element as a parameter and should return two bool values. 
                     The first determines whether or not the style should be
                     applied to the current element and the second value
                     determines whether or not the apply function should keep
                     going (recursively) or not.
      - postProcess  A function that is called after applying a style to an
                     element.  It is passed the element as a parameter.  This
                     will be called recursively on child elements (where
                     applicable).
      """
      # Lets always define it
      if filter is None:
         filter = lambda x: (True, recursive)

      if postProcess is None:
         postProcess = lambda x: None

      # Apply the parent styles first
      if self.parent:
         for p in self.parent:
            # No need to post-process yet, as we are not done processing.
            p.apply( obj, recursive, filter )

      # apply this style
      self._applyStyle( obj, filter = filter, 
                        postProcess = postProcess )

      # apply any custom functions
      if self.custom:
         self.custom( obj )

   #-----------------------------------------------------------------------
   def _applyStyle( self, obj, filter, postProcess ):
      """: Apply the style to the object.

      This is the workhorse of each style.  This is where the magic happens.

      = INPUT VARIABLES
      - obj          The object to apply to.
      - filter       A filter function for determining what should have this
                     style applied to it.  The function will be passed the
                     element as a parameter and should return two bool values. 
                     The first determines whether or not the style should be
                     applied to the current element and the second value
                     determines whether or not the apply function should keep
                     going (recursively) or not.
      - postProcess  A function that is called after applying a style to an
                     element.  It is passed the element as a parameter.  This
                     will be called recursively on child elements (where
                     applicable).
      """
      # Nothing to do here -- Specialize in derived class.
      pass

   #-----------------------------------------------------------------------
   # Static Functions

   #-----------------------------------------------------------------------
   @classmethod
   def resolveStyles( cls, name, styles ):
      """: Resolve a list of styles into a single named style.

      = INPUT VARIABLES
      - name    The name of the newly generated style.
      - styles  A list of one or more styles.

      = RETURN VALUE
      - Returns a newly created style with the given name that is a result
        of resolving all of the styles listed.
      """
      if isinstance( styles, Style ):
         styles = [ styles ]

      newStyle = cls( name )

      for s in styles:
         if s:
            newStyle.update( s.resolve(None) )

      return newStyle

   #-----------------------------------------------------------------------
   @staticmethod
   def canApply( obj ):
      """: Check if this style type can apply to the given object.

      = INPUT VARIABLES
      - obj    The object to check if it can use this style.

      = RETURN VALUE
      - Will return True if this style type can be applied to the given object.
      """
      # Specialize in derived class.
      return False

   #-----------------------------------------------------------------------
   # Class Properties

   #-----------------------------------------------------------------------
   @property
   def name( self ):
      """The name of this style.
      """
      return self._name

   # name is a read-only property, so there is only a getter
   # @name.setter
   # def name( self, value ):

   #-----------------------------------------------------------------------

