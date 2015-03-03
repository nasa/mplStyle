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

""": A class for managing styles."""

__version__ = "$Revision: #1 $"

#===========================================================================
import logging
import weakref
import os
import os.path
import glob
from .Style import Style
from .StyleData import StyleData
from .lib import stylePath, cleanupFilename
#===========================================================================

__all__ = [ 'StyleManager' ]

DEFAULT_ENVVAR = "$STYLEPATH"

# The prefix will be added later
ELEMENT_TAG_PROPERTY = "_mpl_style_%s_tag"
ELEMENT_STYLES_PROPERTY = "_mpl_style_%s_styles"

#===========================================================================
def iterable( value, excludeStrings = False ):
   """: Determine if the value is iterable.

   = INPUT VARIABLE
   - value            The value to determine the iterability of.
   - excludeStrings   If set to True, then strings will fail this test.

   = RETURN VALUE
   - Returns True if the value can be iterated over.
   """
   if excludeStrings and ( isinstance( value, str ) or \
                           isinstance( value, unicode ) ):
      return False

   try:
      len( value )
   except:
      return False
   else:
      return True

#===========================================================================
class StyleManager( object ):
   """: An object used to manage one or more Style classes.

   """

   #-----------------------------------------------------------------------
   def __init__( self, styleClass, extension, prefix ):
      """: Create a new StyleManager object.
      """
      # The path to use when searching for styles
      self.path = []

      # The style class this manager manages
      self.styleClass = styleClass

      # The persistent file extension.
      self.extension = extension

      # The prefix used to track elements
      self.prefix = prefix

      # The styles variable is a dictionary of dictionaries.  It contains
      # references to style objects, organized by the type of style.
      # Styles can be accessed in the following way:
      # self._styles[NAME], where NAME is the name of the individual style.
      #  Key: Name
      #  Value: StyleData
      self._styles = {}

      # This is a dictionary mapping tags to elements
      self._tags = {}

   #-----------------------------------------------------------------------
   def loadFile( self, fname, ignoreIfExists = False ):
      """: Load the specified style file.

      = INPUT VARIABLES
      - fname    The name of the style file to load.
      - ignoreIfExists   If set to True, then if a style with the name of the
                         newly loaded style is already loaded, then the newly
                         loaded style will be discarded.

      = RETURN VALUE
      - Returns the loaded style.
      """
      fname = os.path.normpath( os.path.expanduser \
                                ( os.path.expandvars( fname ) ) )

      # call the implementation specific "load" function
      style = self._loadFromFile( fname )

      if not ( self.exists( style.name ) and ignoreIfExists ):
         # Add the style to the manager
         self.add( style )

      # Save the filename with the style
      self._styles[ style.name ].filename = fname

      # Return the newly loaded style.
      return style

   #-----------------------------------------------------------------------
   def load( self, path = None ):
      """: Load all the styles available.

      This will load all styles found in the path as determined by
      'StyleManager.path'.  If this is empty, then it will be assumed to 
      be '$STYLEPATH'.  If that too is not specified, then it will default
      to be [ '.', '~/.matplotlib/styles' ]

      = INPUT VARIABLES
      - path   If specified, then this path will be used to search for
               style files.
      """
      # Get the directories to search
      dirs = self._searchPath( path )

      for d in dirs:
         if os.path.exists( d ):
            files = glob.glob( os.path.join( d, '*.%s' % (self.extension) ) )
            for f in files:
               if os.path.isfile( f ):
                  self.loadFile( f, ignoreIfExists = True )

   #-----------------------------------------------------------------------
   def save( self, outdir = '~/.matplotlib/styles', overwrite = True ):
      """: Save the styles to persistent file.

      If a style was not loaded from a file, then it will be written to
      a file placed in the directory specified by 'outdir'.

      = INPUT VARIABLES
      - outdir      The directory to write styles to that have not yet
                    been written to persistent store.
      - overwrite   If the style already has a file, then it will be
                    overwritten if this is set to True.
      """
      errorMessage = ""
      outdir = os.path.normpath( os.path.expanduser \
                                 ( os.path.expandvars( outdir ) ) )
      if not os.path.exists( outdir ):
         os.makedirs( outdir )

      for styleName in self._styles:
         style = self._styles[ styleName ]
         fname = style.filename

         if fname is None:
            # No filename yet, so create one
            fname = cleanupFilename( styleName )
            fname = os.path.join( outdir, "%s.%s" % (fname, self.extension) )
            # Save the new filename back to the style meta-data
            style.filename = fname

         if os.path.exists( fname ) and not overwrite:
            msg = "Error saving '%s' to file '%s'.  A file with that name" \
                  "already exists.\n" % (styleName, fname)
            errorMessage += msg
            continue

         self._saveToFile( style.style, fname )

      if errorMessage:
         raise Exception( msg )

   #-----------------------------------------------------------------------
   def find( self, name ):
      """: Find a style with the given name.

      = INPUT VARIABLES
      - name    The name of the style to find.

      = RETURN VALUE
      - Will return the named style.  If the named style does not exist,
        then this will return None.
      """
      try:
         return self.__getitem__( name )
      except:
         return None

   #-----------------------------------------------------------------------
   def exists( self, name ):
      """: Check if the named style exists in the manager.

      = INPUT VARIABLES
      - name    The name of the style to look for.

      = RETURN VALUES
      - Will return True if the style is being managed by this manager,
        False otherwise.
      """
      # Make sure we have a name
      if isinstance( name, Style ):
         name = name.name

      return name in self._styles

   #-----------------------------------------------------------------------
   def getAll( self ):
      """: Get a list of the loaded styles.

      = RETURN VALUE
      - This will return a list of the names of the loaded styles.
      """
      names = self._styles.keys()
      names.sort()
      return names

   #-----------------------------------------------------------------------
   def resolve( self, name, styles, ignoreNotFound = False ):
      """: Resolve a list of styles into a new named style.

      = INPUT VARIABLES 
      - name     The name to give to the new style.
      - styles   One or more style instances or names of styles.  Can be
                 a single value if there is only one.
      - ignoreNotFound  If set to True, then if a named style is not
                        found it will be ignored (skipped).

      = RETURN VALUE
      - Returns a newly named style that is a result of resolving all styles
        passed in.  The styles are resolved in the order they appear in the
        list.  This means that a property value set by a later style will
        supercede a property value set by an earlier style.
      """
      # Make sure we have a list
      if isinstance( styles, Style ) or isinstance( styles, str ):
         styles = [ styles ]

      # Create a new style with the given name
      newStyle = self.create( name )

      # Determine the actual styles to use
      for styleName in styles:
         if isinstance( styleName, Style ):
            # We were given a Style instance
            if styleName.name and not self.exists( styleName.name ):
               # we were given a style not in the manager, so add it
               self.add( styleName )

            newStyle.update( styleName.resolve(None) )
         else:
            # we have the name of a style
            s = self.find( styleName )

            if s:
               newStyle.update( s.resolve(None) )
            elif not ignoreNotFound:
               msg = "Could not resolve the style named '%s'.  There is no " \
                     "loaded style with that name.\nLoaded Styles:\n" \
                     % styleName

               for n in self._styles:
                  msg += "   * %s\n" % n

               raise Exception( msg )

      # Return the new style
      return newStyle

   #-----------------------------------------------------------------------
   def apply( self, element, style, tag = None, recurse = True ):
      """: Apply a style or list of styles to an element.

      Will apply a style or list of styles to the specified element.  If a
      style is given that is not managed by this manager, then it will be
      added first.

      = INPUT VARIABLES
      - element   The object or list of objects to apply the style(s) to.
      - style     Can be a Style instance, the name of a managed style or a
                  list of either.  This will determine the style(s) to apply
                  to the element.
      - tag       If specified, then the manager will apply the style(s) only
                  to the element if it is tagged with the given tag value.  If
                  apply is working recursively, then it will additionally only
                  apply to those sub-elements that have been tagged with the
                  specified tag value.
      - recurse   If True and the element has sub-elements that can be handled
                  by the styles, then those sub-elements will also have the
                  specified style(s) applied.
      """
      # Make sure we have lists.  Can't use iterable() for elements
      # because of the way the test cases are set up.
      if not iterable( style, excludeStrings=True ):
         style = [ style ]

      if element is None and tag:
         # Apply to all elements for the given tag
         if tag in self._tags:
            element = [ ref() for ref in self._tags[ tag ] ]

      if not ( isinstance( element, list ) or isinstance( element, tuple ) ):
         element = [ element ]

      # Determine the actual styles to use
      styleList = []
      for name in style:
         s = None

         if isinstance( name, Style ):
            if name.name:
               if not self.exists( name.name ):
                  # we were given a style not in the manager, so add it
                  self.add( name )
            else:
               s = name

            # we only want the name of the style
            name = name.name

         #FUTURE: resolve the styles as much as possible before applying them.
         def filterFunc( e ):
            if tag:
               return bool( tag in self.getTags( e ) ), recurse
            else:
               return True, recurse

         if s:
            for e in element:
               s.apply( e, recursive = recurse, filter = filterFunc )

         elif self.exists( name ):
            s = self._styles[ name ]

            def postApply( e ):
               # Add a reference to the element in the style data
               ref = weakref.ref( e )
               if ref not in s.elements:
                  s.elements.append( ref )

               # Save the list of styles to the element
               self.setElementStyles( e, styleList )

            for e in element:
               s.style.apply( e, recursive = recurse, filter = filterFunc,
                              postProcess = postApply )

         else:
            msg = "Unable to apply the style '%s' to the element %s.  " \
                  "No style with that name could be found." % (name, element)
            raise Exception( msg )

         styleList.append( name )

   #-----------------------------------------------------------------------
   def reapply( self ):
      """: Re-Apply styles to the elements they were applied to.

      Whenever a style is applied to an element it is tracked.  Calling
      'reapply' will reapply the styles set to the tracked elements.
      """
      # First build up a list of elements to update
      elements = []

      for name in self._styles:
         style = self._styles[ name ]

         updatedElementList = []
         for ref in style.elements:
            # Check to see if the reference is still valid
            e = ref()
            if e is not None:
               # Then we will keep the reference
               updatedElementList.append( ref )

               # Add the element to the list (if it is not already there)
               if e not in elements:
                  elements.append( e )

         # Update the element list with references that are still valid
         style.elements = updatedElementList

      # Iterate over the elements and update them
      for e in elements:
         elementStyles = self.getElementStyles( e )

         styles = []
         # check for invalid styles
         for name in elementStyles:
            if self.exists( name ):
               styles.append( name )
            else:
               msg = "MplStyle: Unable to re-apply the style '%s' to the " \
                     "element %s.  No style with that name could be found." \
                     % (name, e)
               logging.warning( msg )

         self.apply( e, styles, recurse = False )


   #-----------------------------------------------------------------------
   def add( self, style, replace = False ):
      """: Add a style to the manager.

      = ERROR CONDITIONS
      - An error will be thrown if a style of the same name and category
        already exists in the manager (unless the 'replace' flag is set
        to True).

      = INPUT VARIABLES
      - style     A named style to add to the manager.
      - replace   If a style of the same name and categroy exist, then 
                  replace the existing style with this style only is this
                  is set to True.
      """
      if self.exists( style.name ) and not replace:
         msg = "Unable to add the style '%s' to the style manager.  " \
               "A style with that name already exists." % (style.name,)
         raise Exception( msg )

      self._styles[ style.name ] = StyleData( style )

   #-----------------------------------------------------------------------
   def erase( self, name, delete = True ):
      """: Remove the named style from the manager.

      = INPUT VARIABLES
      - name    The name of the style to remove.
      - delete  If set to true, then this will also delete any persistent
                files associated with the style.
      """
      if isinstance( name, Style ):
         name = name.name

      if self.exists( name ):
         s = self._styles.pop( name )

         if delete and s.filename:
            self._deleteStyleFile( s.filename )
      else:
         msg = "Unable to remove the style '%s' as it cannot be found." \
               % (name,)
         raise Exception( msg )

   #-----------------------------------------------------------------------
   def clear( self, delete = False ):
      """: Remove all loaded styles.

      = INPUT VARIABLES
      - delete    If set to True, then this will also delete any persistent
                  files associated with any of the loaded styles.  
                  By default this is set to False.

      = NOTE
      - If you set `delete` to True, then **all** loaded styles that have
        any persistent files will be deleted.  Use with caution!
      """
      styleNames = self.getAll()
      for name in styleNames:
         self.erase( name, delete )

   #-----------------------------------------------------------------------
   def copy( self, name, newName ):
      """: Copy the named style.

      This will create a copy of the named style giving it the specified
      new name.

      = INPUT VARIABLES
      - name     The name of the style to copy.
      - newName  The name to give to the newly created copy.

      = RETURN VALUE
      - Returns the newly created copy.
      """
      if isinstance( name, Style ):
         originalStyle = name
         name = originalStyle.name
      else:
         originalStyle = self.find( name )

      if originalStyle is None:
         msg = "Unable to make a copy of style '%s' as no style with that " \
               "name could be found." % (name,)
         raise Exception( msg )

      # Create the new copy
      newStyle = originalStyle.copy( newName ) 

      # Add the new copy to the manager
      if newName:
         self.add( newStyle )

      # Return the copy
      return newStyle

   #-----------------------------------------------------------------------
   def create( self, name, properties = {},
               parent = None, custom = None, **kwargs ):
      """: Create a new style with the given name.

      = INPUT VARIABLES
      - name        The name to give to the newly created style.
      - properties  Initial property values to set in the newly created style.
      - parent      The name of an existing style to use as the parent of the
                    newly created style.
      - custom      A callable object or function that will be passed the object
                    that needs styling.
      - kwargs      Any extra keyword arguments are passed into the style
                    constructor.

      = RETURN VALUE
      - Returns the newly created style instance.
      """
      parentList = []
      if parent:
         # Turn parent into a list
         if not iterable( parent, excludeStrings = True ):
            parent = [ parent ]

         # If parent is specified by string, get the actual style
         for p in parent:
            if isinstance( p, Style ):
               # we were given a style instance
               if p.name and not self.exists( p.name ):
                  # we were given a style not in the manager, so add it
                  self.add( p )
               parentList.append( p )
            else:
               # we were given the name of a style
               tmp = self.find( p )
               if tmp:
                  parentList.append( tmp )
               else:
                  msg = "Error creating a style named '%s' with a parent " \
                        "named '%s'.  No existing style with that name could " \
                        "be found." % (name, p)
                  raise Exception( msg )

      # Create the new style
      style = self._create( name, properties, parentList, custom, **kwargs )

      # Automatically add it to the manager
      if name:
         self.add( style )

      return style

   #-----------------------------------------------------------------------
   def set( self, element, property, value = None, tag = None ):
      """: Set the specified property on the given element.

      = ERROR CONDITIONS
      - An exception will be thrown if property is a dictionary of values
        and 'value' is not None.

      = INPUT VARIABLES
      - element    The element to set the property for.
      - property   This can either be the name of a property to set in the form
                   of 'a.b.c', or it can be a dictionary of properties and their
                   values.  If this is a dictioanry, then do not pass in
                   something for 'value'
      - value      The value to give to the specified property.  This should be
                   set to None if a dictionary of property-values is passed in
                   for 'property'.
      - tag        If specified, then the manager will apply the style(s) only
                   to the element if it is tagged with the given tag value.  If
                   apply is working recursively, then it will additionally only
                   apply to those sub-elements that have been tagged with the
                   specified tag value.
      """
      # Create an anonymous empty style
      style = self._create( None, {}, None, None )

      # Determine the property dictionary
      properties = {}

      if isinstance( property, dict ):
         if value is not None:
            msg = "Attempting to set a dictionary of properties to the " \
                  "object %s and a value was specified.  Can only specify " \
                  "a dictionary of property/values or a single property " \
                  "and value." % (element,)
            raise Exception( msg )

         properties = property
      else:
         properties[ property ] = value

      # Set the properties
      for p in properties:
         style.setValue( p, properties[p] )

      # Apply the values to the object
      self.apply( element, style, tag = tag )

   #-----------------------------------------------------------------------
   def getTags( self, element ):
      """: Get the tags of the specified element.

      The element tag is a "label" given to the element as used by the style
      system.  The meaning of the tag is up to the individual applications.

      = INPUT VARIABLES
      - element   The element whose tag we wish to get.

      = RETURN VALUE
      - Returns the list of tags of the element as set by 'tag'.  Will return
        [] if no tag has been set.
      """
      if hasattr( element, ELEMENT_TAG_PROPERTY % self.prefix ):
         return getattr( element, ELEMENT_TAG_PROPERTY % self.prefix )
      else:
         return []

   #-----------------------------------------------------------------------
   def tag( self, element, label ):
      """: Set the tag of the specified element.

      The element tag is a label given to the element as used by the style
      system.  The meaning of the tag is up to the individual applications.

      = INPUT VARIABLES
      - element   The element (or list of elements) whose name we wish to set.
      - label     The label (or list of labels) to tag the specified element(s)
                  with.
      """
      # We cannot us 'iterable' here, because element might in fact be
      # a single iterable object, we really need to know if this is a
      # list or tuple of elements.
      if not ( isinstance(element, list) or isinstance(element, tuple) ):
         element = [ element ]

      if not iterable( label, excludeStrings = True ):
         label = [ label ]

      tagPropName = ELEMENT_TAG_PROPERTY % self.prefix

      for e in element:
         if not hasattr( e, tagPropName  ):
            setattr( e, tagPropName, [] )

         tagAttr = getattr( e, tagPropName )

         for lbl in label:
            if lbl not in tagAttr:
               tagAttr.append( lbl )

               # Add the element to the tag map
               if lbl not in self._tags:
                  self._tags[ lbl ] = []

               ref = weakref.ref( e )
               if ref not in self._tags[ lbl ]:
                  self._tags[ lbl ].append( ref )

   #-----------------------------------------------------------------------
   def untag( self, element, label ):
      """: Remove the tag of the specified element.

      = INPUT VARIABLES
      - element   The element (or list of elements) whose name we wish to untag.
      - label     The label (or list of labels) to remove from the specified
                  element(s).
      """
      # We cannot us 'iterable' here, because element might in fact be
      # a single iterable object, we really need to know if this is a
      # list or tuple of elements.
      if not ( isinstance(element, list) or isinstance(element, tuple) ):
         element = [ element ]

      if not iterable( label, excludeStrings = True ):
         label = [ label ]

      tagPropName = ELEMENT_TAG_PROPERTY % self.prefix

      for e in element:
         if not hasattr( e, tagPropName  ):
            continue

         tagAttr = getattr( e, tagPropName )

         for lbl in label:
            while lbl in tagAttr:
               tagAttr.remove( lbl )

            if lbl in self._tags:
               ref = weakref.ref( e )
               while ref in self._tags[ lbl ]:
                  self._tags[ lbl ].remove( ref )

   #-----------------------------------------------------------------------
   def hasTag( self, element, label ):
      """: Check if the specified element has the specified tag.

      = INPUT VARIABLES
      - element   The element to check.
      - label     The label to check the element for.

      = RETURN VALUE
      - Returns True if the element has been tagged with the given label.
        False otherwise.
      """
      tagPropName = ELEMENT_TAG_PROPERTY % self.prefix

      if hasattr( element, tagPropName ):
         tagAttr = getattr( element, tagPropName )
         return label in tagAttr
      else:
         return False

   #-----------------------------------------------------------------------
   def getElementStyles( self, element ):
      """: Get the styles applied to the given element.

      When using a managed set of styles, then each element has a list of styles
      that have been applied to it.  This will get that list of styles.

      = INPUT VARIABLES
      - element   The element whose styles we wish to get.

      = RETURN VALUE
      - Returns the list of the names of the styles that have been applied to
        the given element via a StyleManager.  This will be an empty list if
        no styles have been set.
      """
      if hasattr( element, ELEMENT_STYLES_PROPERTY % self.prefix ):
         return getattr( element, ELEMENT_STYLES_PROPERTY % self.prefix )
      else:
         return []

   #-----------------------------------------------------------------------
   def setElementStyles( self, element, styles ):
      """: Set the styles applied to the given element.

      When using a managed set of styles, then each element has a list of styles
      that have been applied to it.  This will set that list of styles.

      = INPUT VARIABLES
      - element   The element whose styles we wish to get.
      - styles    A list of style names that are to be assiciated with the
                  specified element.
      """
      setattr( element, ELEMENT_STYLES_PROPERTY % self.prefix, styles )

   #-----------------------------------------------------------------------
   def _searchPath( self, dirs ):
      """: Determine the actual search path.

      = RETURN VALUE
      - A List of paths to search.
      """

      actualPaths = []

      if dirs is None:
         dirs = self.path
      elif isinstance( dirs, str ):
         dirs = [ dirs ]

      for directory in dirs:
         if directory.upper() == DEFAULT_ENVVAR:
            p = stylePath( DEFAULT_ENVVAR )
            actualPaths += p
         else:
            p = os.path.normpath( os.path.expanduser \
                                  ( os.path.expandvars( directory ) ) )
            actualPaths.append( p )

      if not actualPaths:
         # self.path gave us nothing, so look for '$STYLEPATH'
         actualPaths = stylePath( DEFAULT_ENVVAR )

      if not actualPaths:
         # Still do not have anything, so go with the defaults
         defaults = [ '.', '~/.matplotlib/styles' ]
         for directory in defaults:
            p = os.path.normpath( os.path.expanduser \
                                  ( os.path.expandvars( directory ) ) )
            actualPaths.append( p )

      return actualPaths

   #-----------------------------------------------------------------------
   def _loadFromFile( self, name, fname ):
      """: Load the specified style file.

      = INPUT VARIABLES
      - name     The name to give to the newly created style.
      - fname    The path of the file to load.

      = RETURN VALUE
      - Returns the new style that results from loading from the specified file.
      """
      msg = "Unable to load style from '%s'.  This method should not be " \
            "called directly, rather it should be called on a sub-class of " \
            "StyleManager." % (fname,)
      raise Exception( msg )

   #-----------------------------------------------------------------------
   def _saveToFile( self, style, fname ):
      """: Save the style to persistent file.

      This will write the given style to the named file overwriting the file if
      it already exists.

      = INPUT VARIABLES
      - style     The style to save to a file.
      - fname     The name of the file to save the style to.
      """
      msg = "Unable to save style '%s' to '%s'.  This method should not be " \
            "called directly, rather it should be called on a sub-class of " \
            "StyleManager." % (style.name, fname)
      raise Exception( msg )

   #-----------------------------------------------------------------------
   def __getitem__( self, name ):
      """: Get a style with the given name.

      = ERROR CONDITIONS
      - This will throw a python 'KeyError' if the named style does not exist.

      = INPUT VARIABLES
      - name    The name of the style to retrieve.

      = RETURN VALUE
      - Will return the style with the given name.
      """
      if name in self._styles:
         return self._styles[ name ].style
      else:
         msg = "Invalid style '%s'.  Valid values are:\n" % (name)
         for name in self._styles:
            msg += "   * %s\n" % name

         raise Exception( msg )

   #-----------------------------------------------------------------------
   def _deleteStyleFile( self, fname ):
      """: Delete the persistent files for a style.

      = INPUT VARIABLES
      - fname    The name of the style file to delete.
      """
      msg = "Unable to delete style file '%s'.  This method should not be " \
            "called directly, rather it should be called on a sub-class of " \
            "StyleManager." % fname
      raise Exception( msg )

   #-----------------------------------------------------------------------
   def _create( self, name, properties, parent, custom, **kwargs ):
      """: Create a new style with the given name.

      = INPUT VARIABLES
      - name        The name to give to the newly created style.
      - properties  Initial property values to set in the newly created style.
      - parent      The name of an existing style to use as the parent of the
                    newly created style.
      - custom      A callable object or function that will be passed the object
                    that needs styling.
      - kwargs      Any extra keyword arguments are passed into the style
                    constructor.
      """
      return self.styleClass( name, properties, parent, custom, **kwargs )

   #-----------------------------------------------------------------------

