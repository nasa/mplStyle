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

""": A class containing axes style information."""

__version__ = "$Revision: #1 $"

#===========================================================================

from . import types as S
from .MplAxisStyle import MplAxisStyle
from .MplBasicLineStyle import MplBasicLineStyle
from .MplPatchStyle import MplPatchStyle
from .MplTextStyle import MplTextStyle

import matplotlib.axes as mplaxes
#===========================================================================

__all__ = [ 'MplAxesStyle' ]

#===========================================================================
class MplAxesStyle( S.SubStyle ):
   """: Style properties for matplotlib Axes.
   """

   alpha = S.property.Alias( '_patch.alpha', doc = """
The transparency value of an Axes

Setting this value should affect all sub-components comprising the the axes
(i.e. the xAxis, yAxis, etc) that do not explicitly set their own alpha value.
""" )

   visible = S.property.Alias( '_patch.visible', doc = """
Is the Axes drawn or not.

Setting this value should affect all sub-components comprising the the axes
(i.e. the xAxis, yAxis, etc) that do not explicitly set their own visiblility
value.
""" )

   zOrder = S.property.Alias( '_patch.zOrder', doc = """
The z-value of the item.  Higher value items will be drawn
over items with a lower zOrder value.
""" )

   bgColor = S.property.Alias( '_patch.color',
                             doc = "The background color of the axes." )

   fgColor = S.property.MplColor( doc = """
The foreground color for axes components.

This will set the color value to use for all axes components that have a
fgColor property that is unset.  This is components like axis lines, ticks,
gridlines, etc.
""" )

   showFrame = S.property.Boolean( doc = """
The visiblility of the axes frame.

If set to True, then the Axes frame will be visible, unless overriden
by the 'visible' property for each of the individual edges.
""" )

   frameWidth = S.property.Float( min = 0.0, doc = """
The width to use for the axes frame edges.

This value is only used if not set by the individual edges.
""" )

   axisBelow = S.property.Boolean( doc = """
Should the axis lines be below the plot elements.

If set to True, then the axis ticks and gridlines will be below
the artists on the plot.

= NOTE
- This will have no effect on items where the zOrder is manually set.
""" )

   xAxis = S.property.SubStyle( MplAxisStyle, doc = """
The style properties for the x-axis.

This controls how the x-axis is styled for a given Axes.  This is where you
would control the properties of the tick marks and grid lines along the
independant axis of an axes.

= SEE ALSO
- :ref:`MplAxisStyle <mplStyle_MplAxisStyle>`
""" )

   yAxis = S.property.SubStyle( MplAxisStyle, doc = """
The style properties for the y-axis.

This controls how the y-axis is styled for a given Axes.  This is where you
would control the properties of the tick marks and grid lines along the
dependant axis of an axes.
""" )

   leftEdge = S.property.SubStyle( MplBasicLineStyle, patchStyle = True,
                                   doc = """
The style properties for the left edge of the axes.

= SEE ALSO
- :ref:`MplBasicLineStyle <mplStyle_MplBasicLineStyle>`
""" )

   rightEdge = S.property.SubStyle( MplBasicLineStyle, patchStyle = True,
                                    doc = """
The style properties for the right edge of the axes.

= SEE ALSO
- :ref:`MplBasicLineStyle <mplStyle_MplBasicLineStyle>`
""" )

   topEdge = S.property.SubStyle( MplBasicLineStyle, patchStyle = True,
                                  doc = """
The style properties for the top edge of the axes.

= SEE ALSO
- :ref:`MplBasicLineStyle <mplStyle_MplBasicLineStyle>`
""" )

   bottomEdge = S.property.SubStyle( MplBasicLineStyle, patchStyle = True,
                                     doc = """
The style properties for the bottom edge of the axes.

= SEE ALSO
- :ref:`MplBasicLineStyle <mplStyle_MplBasicLineStyle>`
""" )

   title = S.property.SubStyle( MplTextStyle, doc = """
The style properties to use with title text placed onto the axes.

= SEE ALSO
- :ref:`MplTextStyle <mplStyle_MplTextStyle>`
""" )

   labels = S.property.SubStyle( MplTextStyle, doc = """
The style properties to use with axes labels.

Although an Axes does not have any labels directly, some of it's components do.
 This can be tick labels, axis labels, etc.  Any values set here will affect
any sub-component's labels only if they do not have any property values set.

= SEE ALSO
- :ref:`MplTextStyle <mplStyle_MplTextStyle>`
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
      - This applies to any matplotlib Axes object.

      = INPUT VARIABLES
      - obj       The object to apply the style to.
      - defaults  Keyword-value dictionary with defaults values to use if a
                  property value is not specified.
      - kwargs    Keyword-value dictionary whose values will supercede
                  any values set by the properties of this sub-style.
      """
      if not isinstance( obj, mplaxes.Axes ):
         msg = "Unable to apply this sub-style to the given element." \
               "Expected a matplotlib 'Axes' and instead received " \
               "the following:\n%s" % (obj,)
         raise Exception( msg )

      # First update the defaults for all children components
      defaults = S.lib.resolveDefaults( defaults,
                                        bgColor = self.bgColor,
                                        fgColor = self.fgColor,
                                        labels = self.labels )

      # Set the bg patch properties
      self._patch.apply( obj.patch, defaults,
                         alpha = kwargs.get( 'alpha', None ),
                         color = kwargs.get( 'bgColor', None ),
                         visible = kwargs.get( 'visible', None ),
                         zOrder = kwargs.get( 'zOrder', None ) )
      value = self.getValue( 'zOrder', defaults, **kwargs )
      if value is not None:
         obj.set_zorder( value )

      # axisBelow
      value = self.getValue( 'axisBelow', defaults, **kwargs )
      if value is not None:
         obj.set_axisbelow( value )

      # bgColor
      value = self.getValue( 'bgColor', defaults, **kwargs )
      if value is not None:
         obj.set_axis_bgcolor( value )

      # showFrame
      value = self.getValue( 'showFrame', defaults, **kwargs )
      if value is not None:
         obj.set_frame_on( value )

      # X-Axis
      subKwargs = kwargs.get( 'xAxis', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['xAxis'] )
      self.xAxis.apply( obj.get_xaxis(), subDefaults, **subKwargs )

      # Y-Axis
      subKwargs = kwargs.get( 'yAxis', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['yAxis'] )
      self.yAxis.apply( obj.get_yaxis(), subDefaults, **subKwargs )

      # Title text
      subKwargs = kwargs.get( 'title', {} )
      subDefaults = S.lib.resolveDefaults( defaults,
                                           ['text', 'labels', 'title'] )
      self.title.apply( obj.title, subDefaults, **subKwargs )

      # Edges
      defaults = S.lib.resolveDefaults( defaults, width = self.frameWidth,
                                                  alpha = self.alpha )

      subKwargs = kwargs.get( 'leftEdge', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['leftEdge'] )
      self.leftEdge.apply( obj.spines[ 'left' ], subDefaults, **subKwargs )

      subKwargs = kwargs.get( 'rightEdge', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['rightEdge'] )
      self.rightEdge.apply( obj.spines[ 'right' ], subDefaults, **subKwargs )

      subKwargs = kwargs.get( 'topEdge', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['topEdge'] )
      self.topEdge.apply( obj.spines[ 'top' ], subDefaults, **subKwargs )

      subKwargs = kwargs.get( 'bottomEdge', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['bottomEdge'] )
      self.bottomEdge.apply( obj.spines[ 'bottom' ], subDefaults, **subKwargs )

   #-----------------------------------------------------------------------

