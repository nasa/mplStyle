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

"Unit test for the MplMarkerStyle class."

__version__ = "$Revision: #1 $"

#===========================================================================
# Required imports.  Do not modify these.

import unittest

#===========================================================================
# Place all imports after here.
#

import matplotlib as mpl
import matplotlib.lines

from mplStyle import MplMarkerStyle
#
# Place all imports before here.
#===========================================================================

#===========================================================================
class TestMplMarkerStyle( unittest.TestCase ):
   """Test the MplMarkerStyle class."""

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
      """A basic test of MplMarkerStyle."""

      values = {
         # Marker Properties
         'markerfacecolor' : '#00FF00',
         'markeredgecolor' : '#0000FF',
         'markeredgewidth' : 0.5,
         'markersize' : 8,
         'marker' : 'o',
         'fillstyle' : 'bottom',
      }

      element = mpl.lines.Line2D( [1, 2, 3], [3, 2, 1] )

      style = MplMarkerStyle(
         # Marker Properties
         color = values['markerfacecolor'],
         edgeColor = values['markeredgecolor'],
         edgeWidth = values['markeredgewidth'],
         size = values['markersize'],
         style = values['marker'],
         fill = values['fillstyle'],
      )

      style.apply( element )

      self.checkElement( "Apply", values, element )

      self.assertRaises( Exception, style.apply, 'invalid',
                   msg = "Failed to throw on invalid element." )

   #-----------------------------------------------------------------------

