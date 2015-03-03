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

""": A class for style font information."""

__version__ = "$Revision: #1 $"

#===========================================================================

from . import types as S

from matplotlib import font_manager as mplfont
#===========================================================================

__all__ = [ 'MplFontStyle' ]

#===========================================================================
class MplFontStyle( S.SubStyle ):
   """: Style properties for managing matplotlib fonts.
   """

   size = S.property.Float( min = 1.0, doc = """
The size, in points, of the font.
""" )

   scale = S.property.OneOf( [ S.property.Float( min = 0 ),
                               S.property.Enum( mplfont.font_scalings ) ],
                             doc = """
The scale factor to apply to the font size.

The scale factor is multiplied by the size of the font to determine the actual
size to use for the font.

The scale can be a float or one of the following:

   - 'xx-small'
   - 'x-small'
   - 'small'
   - 'medium'
   - 'large'
   - 'x-large'
   - 'xx-large'
   - 'larger'
   - 'smaller'
""" )

   style = S.property.Enum( { 'normal' : 'normal',
                              'italic' : 'italic',
                              'oblique' : 'oblique' },
                            doc = """
The font 'slant' style. Can be one of the following:

   - 'normal'
   - 'italic'
   - 'oblique'
""" )

   weight = S.property.OneOf( [ S.property.Float( min = 0, max = 1000 ),
                                S.property.Enum( mplfont.weight_dict ) ],
                             doc = """
The weight of the font.

Can be a float or one of the following:

   - 'ultralight'
   - 'light'
   - 'normal'
   - 'regular'
   - 'book'
   - 'medium'
   - 'roman'
   - 'semibold'
   - 'demibold'
   - 'demi'
   - 'bold'
   - 'heavy'
   - 'extra bold'
   - 'black'
""" )

   family = S.property.String( doc = """
The name of the font to use.

Can be any valid font name that can be found
by the 'fontconfig' package.  Can also be a font family such as:

   - 'serif'
   - 'sans-serif'
   - 'cursive'
   - 'fantasy'
   - 'monospace'
   - etc...
""" )

   #-----------------------------------------------------------------------
   def apply( self, obj, defaults = {}, **kwargs ):
      """: Apply this style to the given object.

      = NOTE
      - This applies to any matplotlib FontProperties object

      = INPUT VARIABLES
      - obj       The object to apply the style to.
      - defaults  Keyword-value dictionary with defaults values to use if a
                  property value is not specified.
      - kwargs    Keyword-value dictionary whose values will supercede
                  any values set by the properties of this sub-style.
      """
      if not isinstance( obj, mplfont.FontProperties ):
         msg = "Unable to apply this sub-style to the given element." \
               "Expected a matplotlib 'FontProperties' and instead received " \
               "the following:\n%s" % (obj,)
         raise Exception( msg )

      # Size
      size = self.getValue( 'size', defaults, **kwargs )
      scale = self.getValue( 'scale', defaults, **kwargs )

      if scale is not None:
         # If there is a scale value, we need to apply it to size
         if size is None:
            # Which means we *really* need a value for size.
            # If we get here and there was never any size specified, then
            # just do what matplotlib will do to determine the default size.
            size = mplfont.FontManager.get_default_size()
         size *= scale

      if size is not None:
         obj.set_size( size )

      # Family
      value = self.getValue( 'family', defaults, **kwargs )

      if value is not None:
         obj.set_family( value )

      # Style
      value = self.getValue( 'style', defaults, **kwargs )

      if value is not None:
         obj.set_style( value )

      # Weight
      value = self.getValue( 'weight', defaults, **kwargs )

      if value is not None:
         obj.set_weight( value )

   #-----------------------------------------------------------------------

