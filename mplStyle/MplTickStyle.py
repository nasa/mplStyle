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

""": A class containing tick mark style information."""

__version__ = "$Revision: #1 $"

#===========================================================================

from . import types as S

from .MplBasicLineStyle import MplBasicLineStyle
from .MplTextStyle import MplTextStyle

import matplotlib.axis as mplaxis
#===========================================================================

__all__ = [ 'MplTickStyle' ]

#===========================================================================
class MplTickStyle( S.SubStyle ):
   """: Style properties for managing matplotlib axis tick elements.
   """

   labels = S.property.SubStyle( MplTextStyle, doc = """
The style properties for any text labels placed at tick marks along the
primary axis edge.

If this is on the X-Axis, then the primary edge is the bottom.
If this is on the Y-Axis, then the primary edge is the left.

= SEE ALSO
- :ref:`MplTextStyle <mplStyle_MplTextStyle>`
""" )

   secondaryLabels = S.property.SubStyle( MplTextStyle, doc = """
The style properties for any text labels placed at tick marks along the
secondary axis edge.

If this is on the X-Axis, then the secondary edge is the top.
If this is on the Y-Axis, then the secondary edge is the right.

= SEE ALSO
- :ref:`MplTextStyle <mplStyle_MplTextStyle>`
""" )

   marks = S.property.SubStyle( MplBasicLineStyle, doc = """
The style properties for the tick marks along the primary axis edge.

If this is on the X-Axis, then the primary edge is the bottom.
If this is on the Y-Axis, then the primary edge is the left.

= SEE ALSO
- :ref:`MplBasicLineStyle <mplStyle_MplBasicLineStyle>`
""" )

   secondaryMarks = S.property.SubStyle( MplBasicLineStyle, doc = """
The style properties for the tick marks along the secondary axis edge.

If this is on the X-Axis, then the secondary edge is the top.
If this is on the Y-Axis, then the secondary edge is the right.

= SEE ALSO
- :ref:`MplBasicLineStyle <mplStyle_MplBasicLineStyle>`
""" )

   grid = S.property.SubStyle( MplBasicLineStyle, doc = """
The style properties for the grid lines.

Grid lines are present for each tick mark.  This means that if there is no
tick locator for an axis, then there are no ticks to use for grid lines. 
Setting the visibility of the tick marks to True will ensure that a tick
locator is present to use for generating grid lines.

= SEE ALSO
- :ref:`MplBasicLineStyle <mplStyle_MplBasicLineStyle>`
""" )

   length = S.property.Float( min = 0.0, doc = """
The length of the ticks (in points).
""" )

   width = S.property.Float( min = 0.0, doc = """
The width of the ticks (in points).
""" )

   pad = S.property.Float( doc = """
The spacing between the ticks and their labels (in points).
""" )

   #-----------------------------------------------------------------------
   def apply( self, obj, defaults = {}, **kwargs ):
      """: Apply this style to the given object using the supplied defaults.

      = NOTE
      - This can apply to any matplotlib Tick.

      = INPUT VARIABLES
      - obj       The object to apply the style to.
      - defaults  Keyword-value dictionary with defaults values to use if a
                  property value is not specified.
      - kwargs    Keyword-value dictionary whose values will supercede
                  any values set by the properties of this sub-style.
      """
      if not isinstance( obj, mplaxis.Tick ):
         msg = "Unable to apply this sub-style to the given element." \
               "Expected a matplotlib 'Tick' and instead received the " \
               "following:\n%s" % (obj,)
         raise Exception( msg )

      # Labels
      subKwargs = kwargs.get( 'labels', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['text', 'labels'] )
      self.labels.apply( obj.label1, subDefaults, **subKwargs )

      value = self.labels.getValue( 'visible', subDefaults, **subKwargs )
      if value is not None:
         obj.label1On = value

      # Secondary Labels
      subKwargs = kwargs.get( 'secondaryLabels', {} )
      subDefaults = S.lib.resolveDefaults( defaults,
                                         ['text', 'labels', 'secondaryLabels'] )
      self.secondaryLabels.apply( obj.label2, subDefaults, **subKwargs )

      value = self.secondaryLabels.getValue( 'visible',
                                              subDefaults, **subKwargs )
      if value is not None:
         obj.label2On = value

      # marks
      subKwargs = kwargs.get( 'marks', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['marks'] )
      self.marks.apply( obj.tick1line, subDefaults, **subKwargs )

      value = self.marks.getValue( 'visible', subDefaults, **subKwargs )
      if value is not None:
         obj.tick1On = value

      # Secondary Marks
      subKwargs = kwargs.get( 'secondaryMarks', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['secondaryMarks'] )
      self.secondaryMarks.apply( obj.tick2line, subDefaults, **subKwargs )

      value = self.secondaryMarks.getValue( 'visible',
                                             subDefaults, **subKwargs )
      if value is not None:
         obj.tick2On = value

      # Grid
      subKwargs = kwargs.get( 'grid', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['grid'] )
      self.grid.apply( obj.gridline, subDefaults, **subKwargs )

      value = self.grid.getValue( 'visible', subDefaults, **subKwargs )
      if value is not None:
         obj.gridOn = value

      # Activate the grid as appropriate
      #FUTURE: This should be here using Tick.major, but matplotlib
      #FUTURE: needs to be fixed first.
      #FUTURE obj.grid( self.grid.visible )
      #FUTURE: Setup minor tick locators (as necessary)

      # Length
      value = self.getValue( 'length', defaults, **kwargs )
      if value is not None:
         obj._size = value
         obj.tick1line.set_markersize( obj._size )
         obj.tick2line.set_markersize( obj._size )

      # Width
      value = self.getValue( 'width', defaults, **kwargs )
      if value is not None:
         obj._width = value
         obj.tick1line.set_markeredgewidth( obj._width )
         obj.tick2line.set_markeredgewidth( obj._width )

      # Pad 
      value = self.getValue( 'pad', defaults, **kwargs )
      if value is not None:
         obj.set_pad( value )

   #-----------------------------------------------------------------------

