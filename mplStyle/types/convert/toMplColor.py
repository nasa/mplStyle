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

""": type conversion utilities.

This module contains utilities used to convert data into a specific type.
"""

__version__ = "$Revision: #1 $"

#===========================================================================
#===========================================================================

#===========================================================================
def toMplColor( value, allowNone=False, name="" ):
   """: Convert a value to a matplotlib color object.

   = INPUT VARIABLES
   - value       The input value to convert.
   - allowNone   If true, then the Python variable None is allowed as
                 an input.  The user is responsible for handling the
                 usage and conversion of this parameter then.
   - name        A name to give to this converter instance. Used in making
                 error messages easier to understand.

   = RETURN VALUE
   - Returns a matplotlib color object.
   """
   # Delay load GUI code
   from PyQt4 import QtGui
   import matplotlib.colors as MplColors

   if value is None and allowNone:
      return None

   if name:
      name = " '%s'" % name

   result = 'none'
   origValue = value

   try:
      if isinstance( value, str ):
         value = value.lower()
         if value in MplColors.ColorConverter.colors:
            value = MplColors.ColorConverter.colors[ value ]
            return toMplColor( value, allowNone, name )
         if value == 'none':
            return result
         value = QtGui.QColor( value )
      elif isinstance( value, list ) or isinstance( value, tuple ):
         c = QtGui.QColor()
         if len(value) >= 3:
            # Red
            if isinstance( value[0], float ):
               c.setRedF( value[0] )
            else:
               c.setRed( value[0] )

            # Green
            if isinstance( value[1], float ):
               c.setGreenF( value[1] )
            else:
               c.setGreen( value[1] )

            # Blue
            if isinstance( value[2], float ):
               c.setBlueF( value[2] )
            else:
               c.setBlue( value[2] )

         if len( value ) == 4:
            # Alpha
            if isinstance( value[3], float ):
               c.setAlphaF( value[3] )
            else:
               c.setAlpha( value[3] )

         value = c

      if isinstance( value, QtGui.QColor ):
         if value.isValid():
            result = str( value.name() ).upper()
         else:
            msg = "Invalid color value: %s" % (origValue,)
            raise Exception( msg )

      if value is None:
            msg = "Invalid color value: %s" % (origValue,)
            raise Exception( msg )
   except Exception, e:
      msg = "%s\nError trying to convert an input to a matplotlib color " \
            "object.\nInput%s: %s" % ( e, name, value )
      raise Exception( msg )

   return result

#===========================================================================
