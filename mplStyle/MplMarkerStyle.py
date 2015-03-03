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

""": A class containing marker style information."""

__version__ = "$Revision: #1 $"

#===========================================================================

from . import types as S

from .MplBasicLineStyle import MplBasicLineStyle

from matplotlib import markers as mplmarker
from matplotlib import path as mplpath
import matplotlib.lines as mpllines
#===========================================================================

__all__ = [ 'MplMarkerStyle' ]

MARKER_DICT = {}
for key in mplmarker.MarkerStyle.markers:
   if key in [ None, ' ' ]:
      continue
   MARKER_DICT[ key ] = key
   MARKER_DICT[ mplmarker.MarkerStyle.markers[key] ] = key

#===========================================================================
class MplMarkerStyle( S.SubStyle ):
   """: Style properties for managing matplotlib markers.
   """

   color = S.property.MplColor( doc = "The color of the marker." )

   edgeColor = S.property.Alias( '_edge.color', doc = """
The color of the edge of the marker.

If this is not set, it will use the 'color' value.
""" )

   edgeWidth = S.property.Alias( '_edge.width', doc = """
The width (in pixels) of the marker edge line.
""" )

   size = S.property.Float( min = 0.0, doc = """
The size (in pixels) of the marker.
""" )

   style = S.property.OneOf( [ S.property.Enum( MARKER_DICT ),
                               S.property.Instance( mplpath.Path ),
                               S.property.String( "^\$.+?\$$" ), ],
                             doc = """
The marker Style.

Can be one of the following:

   - '.' or 'point'
   - ',' or 'pixel'
   - 'o' or 'circle'
   - 'v' or 'triangle_down'
   - '^' or 'triangle_up'
   - '<' or 'triangle_left'
   - '>' or 'triangle_right'
   - '1' or 'tri_down'
   - '2' or 'ti_up'
   - '3' or 'tri_left'
   - '4' or 'tri_right'
   - '8' or 'octagon'
   - 's' or 'square'
   - 'p' or 'pentagon'
   - '*' or 'star'
   - 'h' or 'hexagon1'
   - 'H' or 'hexagon2'
   - '+' or 'plus'
   - 'x'
   - 'D' or 'diamond'
   - 'd' or 'thin_diamond'
   - '|' or 'vline'
   - '_' or 'hline'
   - 0 or 'tickleft'
   - 1 or 'tickright'
   - 2 or 'tickup'
   - 3 or 'tickdown'
   - 4 or 'caretleft'
   - 5 or 'caretright'
   - 6 or 'caretup'
   - 7 or 'caretdown'
   - '' or 'None'
   - A matplotlib Path instance
   - A string of the form '$...$' which will be rendered using mathtext.
""" )

   fill = S.property.Enum( { 'full' : 'full',
                             'left' : 'left',
                             'right' : 'right',
                             'top' : 'top',
                             'bottom' : 'bottom',
                             'none' : 'none' }, doc = """
For marker styles that can be filled this specifies a fill pattern.

How the marker should be filled.  This only applies to the marker styles that
can be filled.  Can be one of the following:

= VALUES
- full     The entire marker will be filled (if it can be).
- left     The left half of the marker will be filled.
- right    The right half of the marker will be filled.
- top      The top half of the marker will be filled.
- bottom   The bottom half of the marker will be filled.
- none     The marker will not be filled.
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
      self._edge = MplBasicLineStyle()

      S.SubStyle.__init__( self, **kwargs )

   #-----------------------------------------------------------------------
   def __copy__( self ):
      """: Get a copy of this object.

      This is provided so that the python copy method will work.

      = RETURN VALUE
      - Return  a copy of this class type
      """
      result = S.SubStyle.__copy__( self )
      result._edge = self._edge.copy()
      return result

   #-----------------------------------------------------------------------
   def apply( self, obj, defaults = {}, **kwargs ):
      """: Apply this style to the given object using the supplied defaults.

      = NOTE
      - This can apply to any matplotlib Line2D.

      = INPUT VARIABLES
      - obj       The object to apply the style to.
      - defaults  Keyword-value dictionary with defaults values to use if a
                  property value is not specified.
      - kwargs    Keyword-value dictionary whose values will supercede
                  any values set by the properties of this sub-style.
      """
      # Currently matplotlib only uses markers on Line2D objects and for
      # scatter plots.  Scatter plots uses the marker properties only during
      # the initiali scatter call, where the created markers are turned into
      # paths and stuffed into a PathCollection.

      if not isinstance( obj, mpllines.Line2D ):
         msg = "Unable to apply this sub-style to the given element." \
               "Expected a matplotlib 'Line2D' and instead received the " \
               "following:\n%s" % (obj,)
         raise Exception( msg )

      # Map the style name to mpl property name
      properties = {
         'color'     : 'markerfacecolor',
         'edgeColor' : 'markeredgecolor',
         'edgeWidth' : 'markeredgewidth',
         'size'      : 'markersize',
         'style'     : 'marker',
         'fill'      : 'fillstyle',
      }

      kw = {}

      for p in properties:
         mplProp = properties[ p ]

         value = self.getValue( p, defaults, **kwargs )

         if value is not None:
            kw[ mplProp ] = value

      # Set the edgecolor to the same as the facecolor only if
      # the edgecolor is not set and the facecolor is set.
      ec = kw.get( 'markeredgecolor', None )
      if ec is None:
         ec = kw.get( 'markerfacecolor', None )

      if ec:
         kw[ 'markeredgecolor' ] = ec

      # Only call update if there is something to update
      if kw:
         obj.update( kw )

   #-----------------------------------------------------------------------

