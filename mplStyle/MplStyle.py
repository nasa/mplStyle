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

""": Base class for style information."""

__version__ = "$Revision: #1 $"

#===========================================================================

from . import types as S
from .MplSubStyle import MplSubStyle

from collections import OrderedDict

import matplotlib
import matplotlib.figure
import matplotlib.axes
import matplotlib.axis
import matplotlib.font_manager
import matplotlib.lines
import matplotlib.text
import matplotlib.patches
#===========================================================================

__all__ = [ 'MplStyle' ]

# We need this to be ordered so that Artist will always resolve last
MPL_TYPE_MAP = OrderedDict( [
   ( matplotlib.figure.Figure, '_applyToFigure' ),
   ( matplotlib.axes.Axes, '_applyToAxes' ),
   ( matplotlib.axis.Axis, '_applyToAxis' ),
   ( matplotlib.font_manager.FontProperties, '_applyToFont' ),
   ( matplotlib.lines.Line2D, '_applyToLine' ),
   ( matplotlib.text.Text, '_applyToText' ),
   ( matplotlib.patches.Patch, '_applyToPatch' ),
] )

#===========================================================================
class MplStyle( S.Style ):
   """: An object used to contain matplotlib style properties.

   This class has the same methods and properties as
   :ref:`MplSubStyle <mplStyle_MplSubStyle>`.
   """

   #-----------------------------------------------------------------------
   def __init__( self, name, initialValues = {}, parent = None, custom = None ):
      """: Create a new matplotlib style object.

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
      self._subStyle = MplSubStyle()

      # Since the Style CTOR will attempt to init the style with any values
      # found in 'initialValues', we need to have this classes data structures
      # ready to to accept any values specified, so we call this last.
      S.Style.__init__( self, name, initialValues, parent, custom )

   #-----------------------------------------------------------------------
   def __str__( self ):
      """: Get a tring representation of the instance.
      """
      return str( self._subStyle )

   #-----------------------------------------------------------------------
   def __getattribute__( self, name ):
      """: Get the spcified attribute of this class.

      This method is provided so that the subStyle members can be directly
      accessed as members of this class.

      = INPUT VARIABLES
      - name    The name of the attribute to get.

      = RETURN VALUE
      - return the requested attribute.
      """
      if ( name.startswith( '__' ) ):
         # If we want a double-underscore item, then just give it
         return object.__getattribute__( self, name )

      subStyle = object.__getattribute__( self, "_subStyle" )
      selfdict = object.__getattribute__( self, "__dict__" )
      c = object.__getattribute__( self, "__class__" )
      classdict = c.__dict__
      classdir = dir( c )

      if ( (name in selfdict) or (name in classdict) or (name in classdir) ):
         # If the requested attribute is part of the class
         # or the instance, then give it.
         return object.__getattribute__( self, name )
      elif ( hasattr(subStyle, name) ):
         # If the requested attribute is part of the subStyle,
         # then give it.
         return getattr( subStyle, name )
      else:
         # Otherwise fall through with regular attribute accessor
         return object.__getattribute__( self, name )

   #-----------------------------------------------------------------------
   def __setattr__( self, name, value ):
      """: Set the attribute value

      This is provided so that, top-level _substyle values are not superceded.

      = INPUT VARIABLES
      - name    The name of the attribute to set.
      - value   The value to give the named attribute.
      """
      if name.startswith( '_' ):
         subStyle = None
      else:
         subStyle = object.__getattribute__( self, "_subStyle" )

      if object.__getattribute__( self, '_completed_init' ):
         selfdict = object.__getattribute__( self, "__dict__" )
         c = object.__getattribute__( self, "__class__" )
         classdict = c.__dict__
         classdir = dir( c )

         if ( (name in selfdict) or (name in classdict) or (name in classdir) ):
            S.Style.__setattr__( self, name, value )
         elif subStyle:
            setattr( subStyle, name, value )
         else:
            msg = "Unable to set the property '%s' to the specified value.  " \
                  "No property with that name exists." % name
            raise Exception( msg )
      else:
         if subStyle and hasattr( subStyle, name ):
            setattr( subStyle, name, value )
         else:
            S.Style.__setattr__( self, name, value )

   #-----------------------------------------------------------------------
   def __dir__( self ):
      """: This allows dir to report the subStyle's attributes.

      = RETURN VALUE
      - Returns a list of this classes attributes.
      """
      result = self.__dict__.keys()

      bases = self.__class__.__bases__
      for b in bases:
         d = dir( b )
         for item in d:
            if item not in result:
               result.append( item )

      subStyle = object.__getattribute__( self, "_subStyle" )
      subdir = dir( subStyle )

      for item in subdir:
         if item.startswith( '__' ):
            continue

         if item not in result:
            result.append( item )

      result.sort()
      return result

   #-----------------------------------------------------------------------
   def getPropertyType( self, name ):
      """ Get the type of the named property.

      = INPUT VARIABLE
      - name    The name of the property whose type we want.

      = RETURN VALUE
      - Returns the type of the named property.  If the property does not
        exist, then this returns None.
      """
      return self._subStyle.getPropertyType( name )

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

      result = MplStyle( newName, {},
                         parent = copy( self.parent ),
                         custom = self.custom )

      result._subStyle = self._subStyle.copy()
      return result

   #-----------------------------------------------------------------------
   def update( self, style ):
      """: Update this style with the values in the given style.

      This will *not* update this style's parent with that of the given style.

      = INPUT VARIABLES
      - style     Will use to set this style's values.
      """
      # Specialized from base class
      if not isinstance( style, MplStyle ):
         style = MplStyle( None, style )

      self._subStyle.update( style._subStyle )

   #-----------------------------------------------------------------------
   def _getFigure( self, obj ):
      """: Determine the figure the object is associated with.

      This is used when ininteractive mode to get the figure and refresh it.
      """
      if isinstance( obj, matplotlib.figure.Figure ):
         return obj
      elif hasattr( obj, 'get_figure' ):
         return obj.get_figure()
      else:
         return None

   #-----------------------------------------------------------------------
   # Apply methods

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
      # Get the name of the apply method
      func = self._getApplyFunc( obj )

      if func is None:
         msg = "Unable to apply a style to a given object:\n" \
               "   Style: %s\n" \
               "   Object: %s\n" % (self.name, obj)
         raise Exception( msg )

      # Get a handle to the apply method
      func = getattr( self, func )

      # call the appropriate apply method
      func( obj, filter, postProcess,
            bgColor = self.bgColor,
            fgColor = self.fgColor,
            text = self.text )


      # redraw the figure (if interactive and applicable)
      if matplotlib.is_interactive():
         fig = self._getFigure( obj )
         if fig and fig.canvas:
            fig.canvas.draw()

   #-----------------------------------------------------------------------
   def _applyToAxes( self, obj, filter, postProcess, **defaults ):
      """: Apply the style to a figure object.
      """
      process, recursive = filter( obj )

      defaults = S.lib.resolveDefaults( defaults, [ 'axes' ] )

      if process:
         self.axes.apply( obj, defaults )
         if postProcess:
            postProcess( obj )

      if recursive:
         defaults = S.lib.resolveDefaults( defaults,
                                           bgColor = self.axes.bgColor,
                                           fgColor = self.axes.fgColor,
                                           labels = self.axes.labels )

         # Collections -- axes.collections
         #FUTURE: Implement

         # Patches -- axes.patches
         for item in obj.patches:
            self._applyToPatch( item, filter, postProcess, **defaults )

         # Lines -- axes.lines
         for item in obj.lines:
            self._applyToLine( item, filter, postProcess, **defaults )

         # Text -- axes.texts
         for item in obj.texts:
            self._applyToText( item, filter, postProcess, **defaults )

         # Artists -- axes.artists
         #FUTURE: Implement

         # Legend -- axes.legend_
         #FUTURE: Implement

         # Tables -- axes.tables
         #FUTURE: Implement

         # Images -- axes.images
         #FUTURE: Implement

   #-----------------------------------------------------------------------
   def _applyToAxis( self, obj, filter, postProcess, **defaults ):
      """: Apply the style to a figure object.
      """
      process, recursive = filter( obj )

      defaults = S.lib.resolveDefaults( defaults, [ 'axis' ] )

      if process:
         if isinstance( obj, matplotlib.axis.XAxis ):
            self.axes.xAxis.apply( obj, defaults )
         elif isinstance( obj, matplotlib.axis.YAxis ):
            self.axes.yAxis.apply( obj, defaults )

         if postProcess:
            postProcess( obj )

   #-----------------------------------------------------------------------
   def _applyToFigure( self, obj, filter, postProcess, **defaults ):
      """: Apply the style to a figure object.
      """
      process, recursive = filter( obj )

      defaults = S.lib.resolveDefaults( defaults, [ 'figure' ] )

      if process:
         self.figure.apply( obj, defaults )
         if postProcess:
            postProcess( obj )

      if recursive:
         defaults = S.lib.resolveDefaults( defaults, bgColor = self.bgColor )

         # Axes -- figure axes
         for item in obj.axes:
            self._applyToAxes( item, filter, postProcess, **defaults )

         # Patches -- figure.patches
         for item in obj.patches:
            self._applyToPatch( item, filter, postProcess, **defaults )

         # Lines -- figure.lines
         for item in obj.lines:
            self._applyToLine( item, filter, postProcess, **defaults )

         # Artists -- figure.artists
         #FUTURE: Implement

         # Images -- figure.images
         #FUTURE: Implement

         # Text -- figure.texts
         for item in obj.texts:
            self._applyToText( item, filter, postProcess, **defaults )

         # Legends -- figure.legends
         #FUTURE: Implement

   #-----------------------------------------------------------------------
   def _applyToFont( self, obj, filter, postProcess, **defaults ):
      """: Apply the style to a figure object.
      """
      process, recursive = filter( obj )

      # This will pull up any 'text' values to the top, including any 'font'
      # parameters
      defaults = S.lib.resolveDefaults( defaults, [ 'text' ] )

      # This will take any 'font' parameters and merge them into any that
      # already exist at the top-level.
      defaults = S.lib.resolveDefaults( defaults, [ 'font' ] )

      if process:
         self.text.font.apply( obj, defaults )
         if postProcess:
            postProcess( obj )

   #-----------------------------------------------------------------------
   def _applyToLine( self, obj, filter, postProcess, **defaults ):
      """: Apply the style to a figure object.
      """
      process, recursive = filter( obj )

      defaults = S.lib.resolveDefaults( defaults, [ 'line' ] )

      if process:
         self.line.apply( obj, defaults )
         if postProcess:
            postProcess( obj )

   #-----------------------------------------------------------------------
   def _applyToPatch( self, obj, filter, postProcess, **defaults ):
      """: Apply the style to a figure object.
      """
      process, recursive = filter( obj )

      defaults = S.lib.resolveDefaults( defaults, [ 'patch' ] )

      if process:
         self.patch.apply( obj, defaults )
         if postProcess:
            postProcess( obj )

   #-----------------------------------------------------------------------
   def _applyToText( self, obj, filter, postProcess, **defaults ):
      """: Apply the style to a figure object.
      """
      process, recursive = filter( obj )

      defaults = S.lib.resolveDefaults( defaults, [ 'text' ] )

      if process:
         self.text.apply( obj, defaults )
         if postProcess:
            postProcess( obj )

   #-----------------------------------------------------------------------
   # Static Functions

   #-----------------------------------------------------------------------
   @staticmethod
   def _getApplyFunc( obj ):
      """: Get the apply function to use for the given type.

      = INPUT VARIABLES
      - obj    The object to check if it can use this style.

      = RETURN VALUE
      - Will return the name of the appropriate apply method to use, or None.
      """
      # Specialized from base class
      if obj.__class__ in MPL_TYPE_MAP:
         return MPL_TYPE_MAP[ obj.__class__ ]

      for cls in MPL_TYPE_MAP:
         if isinstance( obj, cls ):
            return MPL_TYPE_MAP[ cls ]

      return None

   #-----------------------------------------------------------------------
   @staticmethod
   def canApply( obj ):
      """: Check if this style type can apply to the given object.

      = INPUT VARIABLES
      - obj    The object to check if it can use this style.

      = RETURN VALUE
      - Will return True if this style type can be applied to the given object.
      """
      return bool( MplStyle._getApplyFunc( obj ) )

   #-----------------------------------------------------------------------

