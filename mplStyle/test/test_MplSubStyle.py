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

"Unit test for the MplSubStyle class."

__version__ = "$Revision: #1 $"

#===========================================================================
# Required imports.  Do not modify these.

import unittest

#===========================================================================
# Place all imports after here.
#

import matplotlib as mpl
import matplotlib.axes
import matplotlib.figure
import matplotlib.patches

from mplStyle import MplSubStyle
#
# Place all imports before here.
#===========================================================================

#===========================================================================
class TestMplSubStyle( unittest.TestCase ):
   """Test the MplSubStyle class."""

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
      """A basic test of MplSubStyle."""

      figVals = {
         'figwidth' : 10,
         'figheight' : 10,
         'dpi' : 100,
      }

      axVals = {
         'axisbelow' : True,
         'frame_on' : False,
      }

      patchVals = {
         'alpha' : 0.95,
         'visible' : False,
         'facecolor' : (1.0, 0.0, 0.0, 0.95),
         'edgecolor' : (1.0, 0.0, 0.0, 0.95),
         'linestyle' : 'dashdot',   # '-.',
         'linewidth' : 2.5,
      }

      fig = mpl.figure.Figure()
      ax = mpl.axes.Axes( fig, [ 0.2, 0.2, 0.6, 0.6 ] )
      element = mpl.patches.Patch()

      style = MplSubStyle(
         figure = {
            'width' : figVals['figwidth'],
            'height' : figVals['figheight'],
            'dpi' : figVals['dpi'],
         },
         axes = {
            'axisBelow' : axVals['axisbelow'],
            'showFrame' : axVals['frame_on'],
         },
         patch = {
            'alpha' : patchVals['alpha'],
            'visible' : patchVals['visible'],
            'color' : patchVals['facecolor'],
            'edgeColor' : patchVals['edgecolor'],
            'edgeStyle' : patchVals['linestyle'],
            'edgeWidth' : patchVals['linewidth'],
         }
      )

      style.apply( fig )
      self.checkElement( "Apply Figure", figVals, fig )

      style.apply( ax )
      self.checkElement( "Apply Axes", axVals, ax )

      style.apply( element )
      self.checkElement( "Apply Patch", patchVals, element )

      self.assertRaises( Exception, style.apply, 'invalid',
                   msg = "Failed to throw on invalid element." )

   #-----------------------------------------------------------------------

