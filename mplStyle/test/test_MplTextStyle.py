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

"Unit test for the MplTextStyle class."

__version__ = "$Revision: #1 $"

#===========================================================================
# Required imports.  Do not modify these.

import unittest

#===========================================================================
# Place all imports after here.
#

import matplotlib as mpl
import matplotlib.text

from mplStyle import MplTextStyle
#
# Place all imports before here.
#===========================================================================

#===========================================================================
class TestMplTextStyle( unittest.TestCase ):
   """Test the MplTextStyle class."""

   #-----------------------------------------------------------------------
   def setUp( self ):
      """This method is called before any tests are run."""
      pass

   #-----------------------------------------------------------------------
   def tearDown( self ):
      """This method is called after all tests are run."""
      pass

   #=======================================================================
   # Add tests methods below.
   # Any method whose name begins with 'test' will be run by the framework.

   #-----------------------------------------------------------------------
   def checkElement( self, testName, values, element ):
      for property in values:
         expected = values[ property ]
         msg = "%s: Incorrect value for property: %s" % (testName, property)
         getFunc = getattr( element, 'get_%s' % property )
         self.assertEqual( expected, getFunc(), msg = msg )

   #-----------------------------------------------------------------------
   def testBasic( self ):
      """A basic test of MplTextStyle."""

      values = {
         # Artist Properties
         'alpha' : 0.95,
         'clip_on' : True,
         'snap' : True,
         'visible' : False,
         'zorder' : 5,
         # Text Properties
         'backgroundcolor' : '#FF0000',
         'color' : '#0000FF',
         'verticalalignment' : 'center',
         'horizontalalignment' : 'left',
         'multialignment' : 'right',
         'linespacing' : 2.0,
         'rotation' : 15.0,
         'fontsize' : 24.0,
         'fontstyle' : 'italic',
         'fontweight' : 700,
         'fontfamily' : ['serif'],
      }

      element = mpl.text.Text()

      #----------------------------------------------------------------------
      #MPL-HACK: There is a bug in matplotlib, where they forgot to add this
      #MPL-HACK: method to Text.  We put this here to make the test work until
      #MPL-HACK: it is updated in matplotlib.
      #FUTURE: Fix this in matplotlib.

      def get_linespacing():
         return element._linespacing

      element.get_linespacing = get_linespacing

      def get_multialignment():
         return element._multialignment

      element.get_multialignment = get_multialignment

      def get_backgroundcolor():
         if element._bbox is None:
            return None
         else:
            return element._bbox.get( 'facecolor', None )

      element.get_backgroundcolor = get_backgroundcolor
      #----------------------------------------------------------------------

      style = MplTextStyle(
         # Artist Properties
         alpha = values['alpha'],
         clip = values['clip_on'],
         snap = values['snap'],
         visible = values['visible'],
         zOrder = values['zorder'],
         # Line Properties
         bgColor = values['backgroundcolor'],
         fgColor = values['color'],
         vertAlign = values['verticalalignment'],
         horizAlign = values['horizontalalignment'],
         multiAlign = values['multialignment'],
         lineSpacing = values['linespacing'],
         rotation = values['rotation'],
         font = { 'size' : values['fontsize'],
                  'style' : values['fontstyle'],
                  'weight' : values['fontweight'],
                  'family' : values['fontfamily'][0], },
      )

      style.apply( element )

      self.checkElement( "Apply", values, element )

      self.assertRaises( Exception, style.apply, 'invalid',
                   msg = "Failed to throw on invalid element." )

   #-----------------------------------------------------------------------

