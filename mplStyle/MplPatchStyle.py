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

""": A class containing patch style information."""

__version__ = "$Revision: #1 $"

#===========================================================================
from . import types as S

from .MplArtistStyle import MplArtistStyle
from .MplBasicLineStyle import MplBasicLineStyle

import matplotlib.patches as mplpatch
#===========================================================================

__all__ = [ 'MplPatchStyle' ]

EDGE_STYLE_MAP = {
   '-' : 'solid',
   '--' : 'dashed',
   '-.' : 'dashdot',
   ':' : 'dotted',
}

#===========================================================================
class MplPatchStyle( MplArtistStyle ):
   """: Style properties for matplotlib Patches.
   """

   antialiased = S.property.Boolean( doc = "Should the item be antialiased." )

   color = S.property.MplColor( doc = "The color value of the item." )

   edgeColor = S.property.Alias( '_edge.color', doc = """\
The color of the edge of the patch.

If this is not set, it will use the 'color' value.
""" )

   edgeWidth = S.property.Alias( '_edge.width', doc = """\
The width (in pixels) of the patch edge line.
""" )

   edgeStyle = S.property.Alias( '_edge.style', doc = """\
The line style for patch edge line.   
""" )

   filled = S.property.Boolean( doc = """\
Fill the Patch.

If set to True, then the patch element will be filled with the 'color' value.
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

      MplArtistStyle.__init__( self, **kwargs )

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
      - This can apply to any matplotlib Patch object.

      = INPUT VARIABLES
      - obj       The object to apply the style to.
      - defaults  Keyword-value dictionary with defaults values to use if a
                  property value is not specified.
      - kwargs    Keyword-value dictionary whose values will supercede
                  any values set by the properties of this sub-style.
      """
      if not isinstance( obj, mplpatch.Patch ):
         msg = "Unable to apply this sub-style to the given element." \
               "Expected a matplotlib 'Patch' and instead received the " \
               "following:\n%s" % (obj,)
         raise Exception( msg )

      # Map the style name to mpl property name
      properties = {
         'antialiased' : 'antialiased',
         'color'       : 'facecolor',
         'filled'      : 'fill',
         'edgeColor'   : 'edgecolor',
         'edgeWidth'   : 'linewidth',
         'edgeStyle'   : 'linestyle',
      }

      # Call the parent class method
      MplArtistStyle.apply( self, obj, defaults, **kwargs )

      kw = {}

      for p in properties:
         mplProp = properties[ p ]

         value = self.getValue( p, defaults, **kwargs )

         if value is not None:
            kw[ mplProp ] = value

      # Set the edgecolor to the same as the facecolor only if
      # the edgecolor is not set and the facecolor is set.
      ec = kw.get( 'edgecolor', None )
      if ec is None:
         ec = kw.get( 'facecolor', None )

      if ec:
         kw[ 'edgecolor' ] = ec

      #MPL-HACK: This is because matplotlib is not consistent in how they
      #MPL-HACK: designate line styles
      #FUTURE: Fix this matplotlib hack.
      if ( 'linestyle' in kw ):
         kw[ 'linestyle' ] = EDGE_STYLE_MAP[ kw['linestyle'] ]

      # Only call update if there is something to update
      if kw:
         obj.update( kw )

   #-----------------------------------------------------------------------

