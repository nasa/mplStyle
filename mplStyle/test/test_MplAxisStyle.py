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

"Unit test for the MplAxisStyle class."

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
import matplotlib.ticker

from mplStyle import MplAxisStyle
#
# Place all imports before here.
#===========================================================================

#===========================================================================
class TestMplAxisStyle( unittest.TestCase ):
   """Test the MplAxisStyle class."""

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
      """A basic test of MplAxisStyle."""

      xVals = {
         'autoscalex_on' : True,
         'xmargin' : 0.5,
      }

      yVals = {
         'autoscaley_on' : True,
         'ymargin' : 0.5,
      }

      majTickVals = {
         'color' : '#F0F000',
         'markersize' : 15,
         'markeredgewidth' : 3.0,
         'linewidth' : 2,
         'visible' : True
      }

      minTickVals = {
         'color' : '#0F0F00',
         'markersize' : 5,
         'markeredgewidth' : 1.0,
         'linewidth' : 0.5,
         'visible' : True
      }

      majGridVals = {
         'color' : '#B0B0B0',
         'linestyle' : ':',
         'linewidth' : 1,
      }

      minGridVals = {
         'visible' : False,
      }

      fig = mpl.figure.Figure()
      ax = mpl.axes.Axes( fig, [ 0.2, 0.2, 0.6, 0.6 ] )
      ax.xaxis.set_major_locator( matplotlib.ticker.NullLocator() )
      ax.yaxis.set_major_locator( matplotlib.ticker.NullLocator() )

      #----------------------------------------------------------------------
      #MPL-HACK: There is a bug in matplotlib, where they forgot to add this
      #MPL-HACK: method to Axes.  We put this here to make the test work until
      #MPL-HACK: it is updated in matplotlib.
      #FUTURE: Fix this in matplotlib.

      def get_xmargin():
         return ax._xmargin

      ax.get_xmargin = get_xmargin

      def get_ymargin():
         return ax._ymargin

      ax.get_ymargin = get_ymargin
      #----------------------------------------------------------------------

      xStyle = MplAxisStyle(
         autoscale = xVals['autoscalex_on'],
         dataMargin = xVals['xmargin'],
         majorTicks = {
            'grid' : {
               'color' : majGridVals['color'],               
               'style' : majGridVals['linestyle'],
               'width' : majGridVals['linewidth'],
            },
            'length' : majTickVals['markersize'],
            'width' : majTickVals['markeredgewidth'],
            'marks' : {
               'color' : majTickVals['color'],               
               'width' : majTickVals['linewidth'],
               'visible' : majTickVals['visible'],
            },
         },
         minorTicks = {
            'grid' : {
               'visible' : minGridVals['visible'],               
            },
            'length' : minTickVals['markersize'],
            'width' : minTickVals['markeredgewidth'],
            'marks' : {
               'color' : minTickVals['color'],               
               'width' : minTickVals['linewidth'],
               'visible' : minTickVals['visible'],
            },
         },
      )

      yStyle = MplAxisStyle(
         autoscale = yVals['autoscaley_on'],
         dataMargin = yVals['ymargin'],
         majorTicks = {
            'grid' : {
               'color' : majGridVals['color'],               
               'style' : majGridVals['linestyle'],
               'width' : majGridVals['linewidth'],
            },
            'length' : majTickVals['markersize'],
            'width' : majTickVals['markeredgewidth'],
            'marks' : {
               'color' : majTickVals['color'],               
               'width' : majTickVals['linewidth'],
               'visible' : not majTickVals['visible'],
            },
         },
         minorTicks = {
            'grid' : {
               'visible' : minGridVals['visible'],               
            },
            'length' : minTickVals['markersize'],
            'width' : minTickVals['markeredgewidth'],
            'marks' : {
               'color' : minTickVals['color'],               
               'width' : minTickVals['linewidth'],
               'visible' : not minTickVals['visible'],
            },
         },
      )

      xStyle.apply( ax.get_xaxis() )
      yStyle.apply( ax.get_yaxis() )

      self.checkElement( "Apply xAxis", xVals, ax )
      self.checkElement( "Apply yAxis", yVals, ax )

      self.checkElement( "Apply x major ticks", majTickVals,
                          ax.get_xaxis().get_major_ticks()[0].tick1line )
      self.checkElement( "Apply x minor ticks", minTickVals,
                          ax.get_xaxis().get_minor_ticks()[0].tick1line )

      self.checkElement( "Apply x major grid", majGridVals,
                          ax.get_xaxis().get_major_ticks()[0].gridline )
      self.checkElement( "Apply x minor grid", minGridVals,
                          ax.get_xaxis().get_minor_ticks()[0].gridline )


      xStyle.majorTicks.marks.visible = False
      xStyle.minorTicks.marks.visible = False
      xStyle.apply( ax.get_xaxis() )

      self.assertEqual( [], ax.get_xaxis().get_major_ticks(),
               msg = "Failed to disable major ticks" )
      self.assertEqual( [], ax.get_xaxis().get_minor_ticks(),
               msg = "Failed to disable minor ticks" )

      majTickVals[ 'visible' ] = not majTickVals[ 'visible' ]
      minTickVals[ 'visible' ] = not minTickVals[ 'visible' ]
      # Since these are disabled (in the interest of coverage),
      # there is nothing to check.
      #self.checkElement( "Apply y major ticks", majTickVals,
      #                    ax.get_yaxis().get_major_ticks()[0].tick1line )
      #self.checkElement( "Apply y minor ticks", minTickVals,
      #                    ax.get_yaxis().get_minor_ticks()[0].tick1line )

      #self.checkElement( "Apply y major grid", majGridVals,
      #                    ax.get_yaxis().get_major_ticks()[0].gridline )
      #self.checkElement( "Apply y minor grid", minGridVals,
      #                    ax.get_yaxis().get_minor_ticks()[0].gridline )

      self.assertRaises( Exception, xStyle.apply, 'invalid',
                   msg = "Failed to throw on invalid element." )

   #-----------------------------------------------------------------------
   def testError( self ):
      """test of MplAxisStyle error conditions."""

      import matplotlib.axis
      import matplotlib.text

      class MyAxis( matplotlib.axis.Axis ):
         def _get_label( self, *args, **kwargs ):
            return matplotlib.text.Text( x=0, y=0 )
         def _get_offset_text( self, *args, **kwargs ):
            return matplotlib.text.Text( x=0, y=0 )
         def _get_tick( self, *args, **kwargs ):
            return matplotlib.axis.XTick( self.axes, 0, '' )
         def get_view_interval( self, *args, **kwargs ):
            return self.axes.viewLim.intervalx

      fig = mpl.figure.Figure()
      ax = mpl.axes.Axes( fig, [ 0.2, 0.2, 0.6, 0.6 ] )

      # Create neither an x or y axis
      axis = MyAxis( ax )

      xStyle = MplAxisStyle()

      self.assertRaises( Exception, xStyle.apply, axis,
                   msg = "Failed to throw with invalid axis type." )

   #-----------------------------------------------------------------------

