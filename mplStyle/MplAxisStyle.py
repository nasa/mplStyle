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

""": A class containing axis style information."""

__version__ = "$Revision: #1 $"

#===========================================================================

from . import types as S

from .MplTickStyle import MplTickStyle
from .MplTextStyle import MplTextStyle

import matplotlib.axis as mplaxis
import matplotlib.ticker as mticker
#===========================================================================

__all__ = [ 'MplAxisStyle' ]

#===========================================================================
class MplAxisStyle( S.SubStyle ):
   """: Style properties for matplotlib Axis objects.
   """

   autoscale = S.property.Boolean( doc = """
Automatically scale the axis bounds.

If this is True, then the axis this applies to will be automatically
scaled to fit the data.
""" )

   dataMargin = S.property.Float( doc = """
The pad between the axis bounds and the data.

If autoscaling is turned on, then this will be the pad 
between the last data element and the extrema of the axis.

This value is multiplied by the span of the data in the Axis
direction and added onto the Axis limits on both ends.
""" )

   majorTicks = S.property.SubStyle( MplTickStyle, doc = """
The style regulating the major ticks for this axis.

= SEE ALSO
- :ref:`MplTickStyle <mplStyle_MplTickStyle>`
""" )

   minorTicks = S.property.SubStyle( MplTickStyle, doc = """
The style regulating the minor ticks for this axis.

= SEE ALSO
- :ref:`MplTickStyle <mplStyle_MplTickStyle>`
""" )

   label = S.property.SubStyle( MplTextStyle, doc = """
The style regulating how axis labels are formatted.

= SEE ALSO
- :ref:`MplTextStyle <mplStyle_MplTextStyle>`
""" )

   offsetText = S.property.SubStyle( MplTextStyle, doc = """
The style properties for "offset" text for this axis.

The "offset" text is sometimes used by the tick formatter to specify an offset
value for all of the tick labels.

= SEE ALSO
- :ref:`MplTextStyle <mplStyle_MplTextStyle>`
""" )

   #-----------------------------------------------------------------------
   def apply( self, obj, defaults = {}, **kwargs ):
      """: Apply this style to the given object using the supplied defaults.

      = NOTE
      - This can be applied to any matplotlib Axis object.

      = INPUT VARIABLES
      - obj       The object to apply the style to.
      - defaults  Keyword-value dictionary with defaults values to use if a
                  property value is not specified.
      - kwargs    Keyword-value dictionary whose values will supercede
                  any values set by the properties of this sub-style.
      """
      if not isinstance( obj, mplaxis.Axis ):
         msg = "Unable to apply this sub-style to the given element." \
               "Expected a matplotlib 'Axis' and instead received the " \
               "following:\n%s" % (obj,)
         raise Exception( msg )


      # Major Ticks
      subKwargs = kwargs.get( 'majorTicks', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['majorTicks'] )

      #---
      #MPL-HACK: Once tick stores 'major', we can remove this to MplTickStyle.
      # Activate the grids as appropriate
      value = self.majorTicks.grid.getValue( 'visible',
                                              subDefaults, **subKwargs )
      if value is not None:
         obj.grid( value, which = 'major' )

      # Activate the ticks as appropriate
      majorOn = self.majorTicks.marks.getValue( 'visible',
                                                subDefaults, **subKwargs )
      majorOn2 = self.majorTicks.secondaryMarks.getValue( 'visible',
                                                subDefaults, **subKwargs )

      if majorOn or majorOn2:
         if isinstance(obj.get_major_locator(), mticker.NullLocator):
            obj.set_major_locator( mticker.AutoLocator() )
      elif (majorOn is not None) or (majorOn2 is not None):
         if not isinstance(obj.get_major_locator(), mticker.NullLocator):
            obj.set_major_locator( mticker.NullLocator() )
      #---

      majorTicks = obj.get_major_ticks()
      for tick in majorTicks:
         self.majorTicks.apply( tick, subDefaults, **subKwargs )


      # Minor Ticks
      subKwargs = kwargs.get( 'minorTicks', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['minorTicks'] )

      #---
      #MPL-HACK: Once tick stores 'minor', we can remove this to MplTickStyle.
      # Activate the grids as appropriate
      value = self.minorTicks.grid.getValue( 'visible',
                                              subDefaults, **subKwargs )
      if value is not None:
         obj.grid( value, which = 'minor' )

      minorOn = self.minorTicks.marks.getValue( 'visible',
                                                subDefaults, **subKwargs )
      minorOn2 = self.minorTicks.secondaryMarks.getValue( 'visible',
                                                subDefaults, **subKwargs )
      if minorOn or minorOn2:
         if isinstance(obj.get_minor_locator(), mticker.NullLocator):
            obj.set_minor_locator( mticker.AutoMinorLocator() )
      elif (minorOn is not None) or (minorOn2 is not None):
         if not isinstance(obj.get_minor_locator(), mticker.NullLocator):
            obj.set_minor_locator( mticker.NullLocator() )
      #---

      minorTicks = obj.get_minor_ticks()
      for tick in minorTicks:
         self.minorTicks.apply( tick, subDefaults, **subKwargs )


      # Label
      subKwargs = kwargs.get( 'label', {} )
      subDefaults = S.lib.resolveDefaults( defaults,
                                           ['text', 'labels', 'label'] )
      self.label.apply( obj.get_label(), subDefaults, **subKwargs )

      # Offset Text
      subKwargs = kwargs.get( 'offsetText', {} )
      subDefaults = S.lib.resolveDefaults( defaults,
                                           ['text', 'labels', 'offsetText'] )
      self.offsetText.apply( obj.get_offset_text(), subDefaults, **subKwargs )

      # Get the axes
      axes = obj.axes

      if isinstance( obj, mplaxis.XAxis ):
         # This is the x-axis
         # Autoscale
         autoOn = self.getValue( 'autoscale', defaults, **kwargs )
         if autoOn is not None:
            axes.set_autoscalex_on( autoOn )

         # Margin
         value = self.getValue( 'dataMargin', defaults, **kwargs )
         if value is not None:
            axes.set_xmargin( value )

         # The axis needs to be told to update
         axes.autoscale( enable = autoOn, axis='x' )
      elif isinstance( obj, mplaxis.YAxis ):
         # This is the y-axis
         # Autoscale
         autoOn = self.getValue( 'autoscale', defaults, **kwargs )
         if autoOn is not None:
            axes.set_autoscaley_on( autoOn )

         # Margin
         value = self.getValue( 'dataMargin', defaults, **kwargs )
         if value is not None:
            axes.set_ymargin( value )

         # The axis needs to be told to update
         axes.autoscale( enable = autoOn, axis='y' )
      else:
         # Sanity check, we should never get here
         msg = "An error happened while applying Axis style properties " \
               "to the object '%s'.  If this error happens it is a result " \
               "of a coding error and should be reported immediately." % (obj,)
         raise Exception( msg )

   #-----------------------------------------------------------------------

