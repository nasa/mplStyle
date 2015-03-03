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

"Unit test for the MplAxesStyle class."

__version__ = "$Revision: #1 $"

#===========================================================================
# Required imports.  Do not modify these.

import unittest

#===========================================================================
# Place all imports after here.
#

import matplotlib as mpl
mpl.use( "Agg" )
import matplotlib.axes
import matplotlib.figure

from mplStyle import MplAxesStyle

#
# Place all imports before here.
#===========================================================================

#===========================================================================
class TestMplAxesStyle( unittest.TestCase ):
   """Test the MplAxesStyle class."""

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
   def testFigure( self ):
      """A basic test of MplAxesStyle using matplotlib.Figure."""

      axVals = {
         'axisbelow' : True,
         'frame_on' : False,
      }

      patchVals = {
         'alpha' : 0.95,
         'visible' : False,
         'zorder' : 5,
         'facecolor' : (1.0, 0.0, 0.0, 0.95),
      }

      edgeVals = {
         'edgecolor' : (0.0, 0.0, 1.0, 0.95),
         'linestyle' : 'dashdot',
         'linewidth' : 2.5,
      }

      titleVals = {
         # Artist Properties
         'alpha' : 0.95,   # None -> resolves to label value
         'clip_on' : True,
         'snap' : True,   # None -> resolves to label value
         'visible' : True,
         'zorder' : 3,
         # Text Properties
         'backgroundcolor' : '#FF0000',
         'color' : '#00FF00',
         'verticalalignment' : 'baseline',
         'horizontalalignment' : 'center',
         'multialignment' : 'right',   # None -> resolves to label value
         'linespacing' : 1.2,
         'rotation' : 0.0,
         'fontsize' : 14.0,
         'fontstyle' : 'normal',
         'fontweight' : 400,
         'fontfamily' : ['sans-serif'],
      }

      labelVals = {
         # Artist Properties
         'alpha' : 0.95,
         'clip_on' : True,
         'snap' : True,
         'visible' : False,
         'zorder' : 5,
         # Text Properties
         'backgroundcolor' : '#FF0000',
         'color' : '#00FF00',
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

      fig = mpl.figure.Figure()
      ax = mpl.axes.Axes( fig, [ 0.2, 0.2, 0.6, 0.6 ] )
      ax.set_title( 'Axes Title' )

      #----------------------------------------------------------------------
      #MPL-HACK: There is a bug in matplotlib, where they forgot to add this
      #MPL-HACK: method to Text.  We put this here to make the test work until
      #MPL-HACK: it is updated in matplotlib.
      #FUTURE: Fix this in matplotlib.

      def get_linespacing():
         return ax.title._linespacing

      ax.title.get_linespacing = get_linespacing

      def get_multialignment():
         return ax.title._multialignment

      ax.title.get_multialignment = get_multialignment

      def get_backgroundcolor():
         if ax.title._bbox is None:
            return None
         else:
            return ax.title._bbox.get( 'facecolor', None )

      ax.title.get_backgroundcolor = get_backgroundcolor

      def get_linespacing():
         return ax.xaxis.label._linespacing

      ax.xaxis.label.get_linespacing = get_linespacing

      def get_multialignment():
         return ax.xaxis.label._multialignment

      ax.xaxis.label.get_multialignment = get_multialignment

      def get_backgroundcolor():
         if ax.xaxis.label._bbox is None:
            return None
         else:
            return ax.xaxis.label._bbox.get( 'facecolor', None )

      ax.xaxis.label.get_backgroundcolor = get_backgroundcolor
      #----------------------------------------------------------------------

      style = MplAxesStyle(
         # Axes Properties
         axisBelow = axVals['axisbelow'],
         showFrame = axVals['frame_on'],
         # Patch Components
         alpha = patchVals['alpha'],
         visible = patchVals['visible'],
         zOrder = patchVals['zorder'],
         bgColor = patchVals['facecolor'],
         # Edge Components
         leftEdge = { 'color' : edgeVals['edgecolor'],
                      'style' : '-.',   # edgeVals['linestyle'],
                      'width' : edgeVals['linewidth'], },
         rightEdge = { 'color' : edgeVals['edgecolor'],
                       'style' : '-.',   # edgeVals['linestyle'],
                       'width' : edgeVals['linewidth'], },
         topEdge = { 'color' : edgeVals['edgecolor'],
                     'style' : edgeVals['linestyle'],
                     'width' : edgeVals['linewidth'], },
         bottomEdge = { 'color' : edgeVals['edgecolor'],
                        'style' : edgeVals['linestyle'],
                        'width' : edgeVals['linewidth'], },
         title = {
            # Artist Properties
            'alpha' : titleVals['alpha'],
            'clip' : titleVals['clip_on'],
            'snap' : titleVals['snap'],
            'visible' : titleVals['visible'],
            'zOrder' : titleVals['zorder'],
            # Line Properties
            'bgColor' : titleVals['backgroundcolor'],
            'fgColor' : '#00FF00',
            'vertAlign' : titleVals['verticalalignment'],
            'horizAlign' : titleVals['horizontalalignment'],
            'multiAlign' : titleVals['multialignment'],
            'lineSpacing' : titleVals['linespacing'],
            'rotation' : titleVals['rotation'],
            'font' : { 'size' : titleVals['fontsize'],
                       'style' : titleVals['fontstyle'],
                       'weight' : titleVals['fontweight'],
                       'family' : titleVals['fontfamily'][0], },
         },
         labels = {
            # Artist Properties
            'alpha' : labelVals['alpha'],
            'clip' : labelVals['clip_on'],
            'snap' : labelVals['snap'],
            'visible' : labelVals['visible'],
            'zOrder' : labelVals['zorder'],
            # Line Properties
            'bgColor' : labelVals['backgroundcolor'],
            'fgColor' : '#00FF00',
            'vertAlign' : labelVals['verticalalignment'],
            'horizAlign' : labelVals['horizontalalignment'],
            'multiAlign' : labelVals['multialignment'],
            'lineSpacing' : labelVals['linespacing'],
            'rotation' : labelVals['rotation'],
            'font' : { 'size' : labelVals['fontsize'],
                       'style' : labelVals['fontstyle'],
                       'weight' : labelVals['fontweight'],
                       'family' : labelVals['fontfamily'][0], },
         },
      )

      style.apply( ax )

      self.checkElement( "Apply", axVals, ax )
      self.checkElement( "Apply: Patch", patchVals, ax.patch )
      self.checkElement( "Apply: Left Edge", edgeVals, ax.spines['left'] )
      self.checkElement( "Apply: Right Edge", edgeVals, ax.spines['right'] )
      self.checkElement( "Apply: Top Edge", edgeVals, ax.spines['top'] )
      self.checkElement( "Apply: Bottom Edge", edgeVals, ax.spines['bottom'] )
      self.checkElement( "Apply: Title", titleVals, ax.title )
      self.checkElement( "Apply: Label", labelVals, ax.xaxis.label )

      self.assertRaises( Exception, style.apply, 'invalid',
                   msg = "Failed to throw on invalid element." )

   #-----------------------------------------------------------------------

