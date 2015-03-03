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

""": A class containing figure style information."""

__version__ = "$Revision: #1 $"

#===========================================================================

from . import types as S

from .MplAxisStyle import MplAxisStyle
from .MplPatchStyle import MplPatchStyle
from .MplTextStyle import MplTextStyle

import matplotlib.figure as mplfig
#===========================================================================

__all__ = [ 'MplFigureStyle' ]

#===========================================================================
class MplFigureStyle( S.SubStyle ):
   """: Style properties for matplotlib Figure objects.
   """

   width = S.property.Float( min = 0.1, doc = """
The width of the figure (in inches).

Combined with the dpi this value determines the width (in pixels)
of the figure.
""" )

   height = S.property.Float( min = 0.1, doc = """
The height of the figure (in inches).

Combined with the dpi this value determines the height (in pixels)
of the figure.
""" )

   dpi = S.property.Integer( min = 1, doc = """
The resolution of the figure (in dots-per-inch).

Combined with the width and height, this value determines the pixel dimensions
of the figure.
""" )

   bgColor = S.property.Alias( '_patch.color',
                             doc = "The background color of the figure." )

   edgeColor = S.property.Alias( '_patch.edgeColor', doc = """
The color of the figure border (edge).
""" )

   edgeStyle = S.property.Alias( '_patch.edgeStyle', doc = """
The line style of the figure border (edge).
""" )

   edgeWidth = S.property.Alias( '_patch.edgeWidth', doc = """
The line width (in pixels) of the figure border (edge).
""" )

   leftMargin = S.property.Float( min = 0.0, max = 1.0, doc = """
The left-hand side margin of the figure.

The margin must be between 0.0 and 1.0, such that 0.0 is the left-most
side and 1.0 is the right-most side.  A value of 0.5 would be the center
of the figure.
""" )

   rightMargin = S.property.Float( min = 0.0, max = 1.0, doc = """
The right-hand side margin of the figure.

The margin must be between 0.0 and 1.0, such that 0.0 is the right-most
side and 1.0 is the left-most side.  A value of 0.5 would be the center
of the figure.
""" )

   topMargin = S.property.Float( min = 0.0, max = 1.0, doc = """
The top margin of the figure.

The margin must be between 0.0 and 1.0, such that 0.0 is the top-most
side and 1.0 is the bottom-most side.  A value of 0.5 would be the center
of the figure.
""" )

   bottomMargin = S.property.Float( min = 0.0, max = 1.0, doc = """
The bottom margin of the figure.

The margin must be between 0.0 and 1.0, such that 0.0 is the bottom-most
side and 1.0 is the top-most side.  A value of 0.5 would be the center
of the figure.
""" )

   axesPadX = S.property.Float( min = 0.0, max = 1.0, doc = """
Pad between Axes in the x-direction.

The amount of padding to put between axes in the x-direction when automatically
determining postion of axes in the figure.  This must be between 0.0 and 1.0.
A value of 0.0 means that there is no padding, whereas a value of 1.0 means
that they will be seperated by the width of the figure.
""" )

   axesPadY = S.property.Float( min = 0.0, max = 1.0, doc = """
Pad between Axes in the y-direction.

The amount of padding to put between axes in the y-direction when automatically
determining postion of axes in the figure.  This must be between 0.0 and 1.0.
A value of 0.0 means that there is no padding, whereas a value of 1.0 means
that they will be seperated by the width of the figure.
""" )

   #-----------------------------------------------------------------------
   def __init__( self, **kwargs ):
      """: Create a new SubStyle object.

      = INPUT VARIABLES
      - kwargs  A dictionary of keywords mapping style properties to their
                values.
      """
      # This must be defined *before* calling SubStyle.__init__ so that
      # the aliases into _patch can find what they need.
      self._patch = MplPatchStyle()

      S.SubStyle.__init__( self, **kwargs )

   #-----------------------------------------------------------------------
   def __copy__( self ):
      """: Get a copy of this object.

      This is provided so that the python copy method will work.

      = RETURN VALUE
      - Return  a copy of this class type
      """
      result = S.SubStyle.__copy__( self )
      result._patch = self._patch.copy()
      return result

   #-----------------------------------------------------------------------
   def apply( self, obj, defaults = {}, **kwargs ):
      """: Apply this style to the given object using the supplied defaults.

      = NOTE
      - This applies to any matplotlib Figure object.

      = INPUT VARIABLES
      - obj       The object to apply the style to.
      - defaults  Keyword-value dictionary with defaults values to use if a
                  property value is not specified.
      - kwargs    Keyword-value dictionary whose values will supercede
                  any values set by the properties of this sub-style.
      """
      if not isinstance( obj, mplfig.Figure ):
         msg = "Unable to apply this sub-style to the given element." \
               "Expected a matplotlib 'Figure' and instead received " \
               "the following:\n%s" % (obj,)
         raise Exception( msg )

      # First update the defaults for all children components
      defaults = S.lib.resolveDefaults( defaults, bgColor = self.bgColor )

      # Background patch
      subKwargs = kwargs.get( 'frame', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['frame'] )

      bgColor = self.getValue( 'bgColor', defaults, **kwargs )
      if ( ('color' in subKwargs) and (subKwargs[ 'color' ] is None) ) or \
           ('color' not in subKwargs):
         subKwargs[ 'color' ] = kwargs.get( 'bgColor', bgColor )

      self._patch.apply( obj.patch, subDefaults, **subKwargs )

      # Subplot spacing
      subDefaults = S.lib.resolveDefaults( defaults,
                                      leftMargin = obj.subplotpars.left,
                                      rightMargin = 1.0 - obj.subplotpars.right,
                                      topMargin = 1.0 - obj.subplotpars.top,
                                      bottomMargin = obj.subplotpars.bottom,
                                      axesPadX = obj.subplotpars.wspace,
                                      axesPadY = obj.subplotpars.hspace )
      l = self.getValue( 'leftMargin', subDefaults, **kwargs )
      r = self.getValue( 'rightMargin', subDefaults, **kwargs )
      t = self.getValue( 'topMargin', subDefaults, **kwargs )
      b = self.getValue( 'bottomMargin', subDefaults, **kwargs )
      x = self.getValue( 'axesPadX', subDefaults, **kwargs )
      y = self.getValue( 'axesPadY', subDefaults, **kwargs )

      obj.subplots_adjust( left = l, right = 1.0 - r,
                           top = 1.0 - t, bottom = b,
                           wspace = x, hspace = y )


      # Width
      width = self.getValue( 'width', defaults, **kwargs )
      if width is None:
         width = obj.get_figwidth()

      # Height
      height = self.getValue( 'height', defaults, **kwargs )
      if height is None:
         height = obj.get_figheight()

      # Make sure to physically resize the canvas containing the figure
      obj.set_size_inches( width, height, forward = True )

      # DPI
      value = self.getValue( 'dpi', defaults, **kwargs )
      if value is not None:
         obj.set_dpi( value )

   #-----------------------------------------------------------------------

