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

""": A class containing sub-style information."""

__version__ = "$Revision: #1 $"

#===========================================================================

from . import types as S

from .MplAxesStyle import MplAxesStyle
#FUTURE from .MplBarStyle import MplBarStyle
from .MplFigureStyle import MplFigureStyle
from .MplLineStyle import MplLineStyle
from .MplPatchStyle import MplPatchStyle
from .MplTextStyle import MplTextStyle

import matplotlib.axes as mplaxes
import matplotlib.figure as mplfig
import matplotlib.lines as mpllines
import matplotlib.patches as mplpatch
import matplotlib.text as mpltext
#===========================================================================

__all__ = [ 'MplSubStyle' ]

MPL_TYPE_MAP = {
   mplaxes.Axes : 'axes',
   mplfig.Figure : 'figure',
   mpllines.Line2D : 'line',
   mplpatch.Patch : 'patch',
   mpltext.Text : 'text',
}

#===========================================================================
class MplSubStyle( S.SubStyle ):
   """: Manages style properties for matplotlib elements.
   """

   figure = S.property.SubStyle( MplFigureStyle, doc = """
The style properties for matplotlib figures.

= SEE ALSO
- :ref:`MplFigureStyle <mplStyle_MplFigureStyle>`
""" )

   axes = S.property.SubStyle( MplAxesStyle, doc = """
The style properties for matplotlib axes.

= SEE ALSO
- :ref:`MplAxesStyle <mplStyle_MplAxesStyle>`
""" )

   #FUTURE legend = property.SubStyle( MplLegendStyle, doc = """ """ )

   fgColor = S.property.MplColor( doc = """
A default foreground color.

If specified, this will be used as the foreground color anywhere the 'fgColor'
property is used, unless that property is explicitly set.
""" )

   bgColor = S.property.MplColor( doc = """
A default foreground color.

If specified, this will be used as the background color anywhere the 'bgColor'
property is used, unless that property is explicitly set.
""" )

   text = S.property.SubStyle( MplTextStyle, doc = """
The set of style properties used for formatting plotted text.

If specified this will also be used as the text properties anywhere the text
property is needed, unless that property is explicitly set.

= SEE ALSO
- :ref:`MplTextStyle <mplStyle_MplTextStyle>`
""" )

   line = S.property.SubStyle( MplLineStyle, doc = """
The set of style properties used for formatting lines.

= SEE ALSO
- :ref:`MplLineStyle <mplStyle_MplLineStyle>`
""" )

   patch = S.property.SubStyle( MplPatchStyle, doc = """
The set of style properties used for formatting patches.

= SEE ALSO
- :ref:`MplPatchStyle <mplStyle_MplPatchStyle>`
""" )

   #FUTURE bar = S.property.SubStyle( MplBarStyle, doc = """
   #FUTURE The set of style properties used for formatting bars.
   #FUTURE """ )

   #FUTURE contour = S.property.SubStyle( MplContourStyle, doc = """
   #FUTURE The set of style properties used for formatting contours.
   #FUTURE  """ )

   #FUTURE errorBar = S.property.SubStyle( MplErrorBarStyle, doc = """
   #FUTURE The set of properties used for formatting error bars.
   #FUTURE """ )

   #-----------------------------------------------------------------------
   def apply( self, obj, defaults = {}, **kwargs ):
      """: Apply this style to the given object using the supplied defaults.

      = NOTE
      - This applies to any matplotlib Axes, Figure, Line2D, Patch, or Text
        object.

      = INPUT VARIABLES
      - obj       The object to apply the style to.
      - defaults  Keyword-value dictionary with defaults values to use if a
                  property value is not specified.
      - kwargs    Keyword-value dictionary whose values will supercede
                  any values set by the properties of this sub-style.
      """
      # First update the defaults for all children components
      defaults = S.lib.resolveDefaults( defaults,
                                        bgColor = self.bgColor,
                                        fgColor = self.fgColor,
                                        text = self.text )

      didApply = False

      for cls in MPL_TYPE_MAP:
         if isinstance( obj, cls ):
            name = MPL_TYPE_MAP[ cls ]
            subKwargs = kwargs.get( name, {} )
            subDefaults = S.lib.resolveDefaults( defaults, [ name ] )

            attr = getattr( self, name )
            attr.apply( obj, subDefaults, **subKwargs )

            didApply = True
            break
         
      if not didApply:
         msg = "Unable to apply this sub-style to the given element.\n" \
               "Expected one of the following matplotlib objects:\n"

         for cls in MPL_TYPE_MAP:
            msg += "   - %s\n" % (cls.__name__,)
   
         msg += "Instead was given the following:\n%s" % (obj,)
         raise Exception( msg )

   #-----------------------------------------------------------------------

