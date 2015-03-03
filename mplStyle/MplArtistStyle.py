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

""": A class containing artist style information."""

__version__ = "$Revision: #1 $"

#===========================================================================
from . import types as S
#===========================================================================

__all__ = [ 'MplArtistStyle' ]

#===========================================================================
class MplArtistStyle( S.SubStyle ):
   """: Style properties for matplotlib Artists.
   """

   alpha = S.property.Float( min = 0.0, max = 1.0, doc = "The alpha value" )

   clip = S.property.Boolean( doc = """
Should this be clipped by the axes boundaries?

If this is False, then the element will be draw outside the axes where
appropriate.
""" )

   snap = S.property.Boolean(
          doc = "If True, then snap vertices to the nearest pixel center." )

   visible = S.property.Boolean( doc = "Is this drawn or not." )

   zOrder = S.property.Float( doc = """
The z-value of the item.

The z-value is used for depth sorting of elements.  Higher z-order value items
will be drawn over items with a lower z-order value.  Typically the default is
best and there is no need to change this.
""" )

   #-----------------------------------------------------------------------
   def apply( self, obj, defaults = {}, **kwargs ):
      """: Apply this style to the given object.

      = NOTE
      - This applies to any matplotlib artist

      = INPUT VARIABLES
      - obj       The object to apply the style to.
      - defaults  Keyword-value dictionary with defaults values to use if a
                  property value is not specified.
      - kwargs    Keyword-value dictionary whose values will supercede
                  any values set by the properties of this sub-style.
      """
      # Map the style name to mpl property name
      properties = {
         'alpha'   : 'alpha',
         'clip'    : 'clip_on',
         'snap'    : 'snap',
         'visible' : 'visible',
         'zOrder'  : 'zorder',
      }

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

