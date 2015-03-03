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

""": A class containing text style information."""

__version__ = "$Revision: #1 $"

#===========================================================================

from . import types as S

from .MplArtistStyle import MplArtistStyle
from .MplFontStyle import MplFontStyle

import matplotlib.text as mpltext
#===========================================================================

__all__ = [ 'MplTextStyle' ]

#===========================================================================
class MplTextStyle( MplArtistStyle ):
   """: Style properties for managing matplotlib text elements.
   """

   font = S.property.SubStyle( MplFontStyle, doc = """
The font properties.

= SEE ALSO
- :ref:`MplTextStyle <mplStyle_MplTextStyle>`
""" )

   bgColor = S.property.MplColor( doc = "The color behind the text." )

   color = S.property.MplColor( doc = """
The color value of the text.  This is the same as 'fgColor'.
""" )

   fgColor = S.property.Alias( 'color', isProperty=True, doc = """
The color value of the text.  This is the same as 'color'.
""" )

   vertAlign = S.property.Enum( { 'center' : 'center',
                                  'top' : 'top',
                                  'bottom' : 'bottom',
                                  'baseline' : 'baseline', }, doc = """
The vertical alignment of the text.

Can be one of the following:

   - 'center'
   - 'top'
   - 'bottom'
   - 'baseline'
""" )

   horizAlign = S.property.Enum( { 'center' : 'center',
                                   'left' : 'left',
                                   'right' : 'right', }, doc = """
The horizontal alignment of the text.

Can be one of the following:

   - 'center'
   - 'left'
   - 'right'
""" )

   multiAlign = S.property.Enum( { 'left' : 'left',
                                   'right' : 'right',
                                   'center' : 'center' }, doc = """
The alignment for multiple lines layout.

The layout of the box containing the multiple lines is controlled by
'horizAlign' and 'vertAlign', but the text within the box is controlled by
'multiAlign'.  Can be one of the following:

   - 'left'
   - 'right'
   - 'center'
""" )

   lineSpacing = S.property.Float( min = 0.0, doc = """
The line spacing as a multiple of the font size.
""" )

   rotation = S.property.Float( min = -360.0, max = 360.0, doc = """
The rotation of the text from 0.0 to 360.0 degrees.
""" )

   #-----------------------------------------------------------------------
   def apply( self, obj, defaults = {}, **kwargs ):
      """: Apply this style to the given object using the supplied defaults.

      = NOTE
      - This can apply to any matplotlib Text.

      = INPUT VARIABLES
      - obj       The object to apply the style to.
      - defaults  Keyword-value dictionary with defaults values to use if a
                  property value is not specified.
      - kwargs    Keyword-value dictionary whose values will supercede
                  any values set by the properties of this sub-style.
      """
      if not isinstance( obj, mpltext.Text ):
         msg = "Unable to apply this sub-style to the given element." \
               "Expected a matplotlib 'Text' and instead received " \
               "the following:\n%s" % (obj,)
         raise Exception( msg )

      # Map the style name to mpl property name
      properties = {
         'bgColor'     : 'backgroundcolor',
         'fgColor'     : 'color',
         'vertAlign'   : 'verticalalignment',
         'horizAlign'  : 'horizontalalignment',
         'multiAlign'  : 'multialignment',
         'lineSpacing' : 'linespacing',
         'rotation'    : 'rotation',
      }

      # Apply the font properties
      subKwargs = kwargs.get( 'font', {} )
      subDefaults = S.lib.resolveDefaults( defaults, ['font'] )
      self.font.apply( obj.get_font_properties(), subDefaults, **subKwargs )

      # Call the parent class method
      MplArtistStyle.apply( self, obj, defaults, **kwargs )

      kw = {}

      for p in properties:
         mplProp = properties[ p ]

         value = self.getValue( p, defaults, **kwargs )

         if value is not None:
            kw[ mplProp ] = value

      # Only call update if there is something to update
      if kw:
         obj.update( kw )

   #-----------------------------------------------------------------------

