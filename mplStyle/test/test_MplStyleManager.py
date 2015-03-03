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

"Unit test for the MplStyleManager class."

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
import matplotlib.patches
import matplotlib.text
import matplotlib.pyplot
import os
import os.path
import shutil
import math
import operator
import mplStyle as S

#
# Place all imports before here.
#===========================================================================

#===========================================================================
class TestMplStyleManager( unittest.TestCase ):
   """Test the MplStyleManager class."""

   #-----------------------------------------------------------------------
   @classmethod
   def setUpClass( self ):
      """This method is called before any tests are run."""
      # Save the existing STYLEPATH (if there is one)
      self.outputDir = "output"
      if not os.path.exists( self.outputDir ):
         os.mkdir( self.outputDir )

      self.stylepath = os.environ.get( "STYLEPATH", None )
      os.environ[ "STYLEPATH" ] = self.outputDir

   #-----------------------------------------------------------------------
   @classmethod
   def tearDownClass( self ):
      """This method is called after all tests are run."""
      # You may place finalization code here.
      if self.stylepath is not None:
         os.environ[ "STYLEPATH" ] = self.stylepath

      #if os.path.exists( self.outputDir ):
      #   shutil.rmtree( self.outputDir )

      # Clean up the plot windows
      S.mgr.clear()

   #=======================================================================
   # Add tests methods below.
   # Any method whose name begins with 'test' will be run by the framework.

   #-----------------------------------------------------------------------
   def inputFile( self, fname ):
      return os.path.join( "data-inputs", fname )

   def outputFile( self, fname ):
      return os.path.join( self.outputDir, fname )

   def baselineFile( self, fname ):
      return os.path.join( "baseline", fname )
      
   #-----------------------------------------------------------------------
   def checkPlot( self, testName, fig, msg ):
      fname = "%s.png" % (testName,)
      fig.savefig( self.outputFile( fname ) )

      msg = "%s: Failed -- '%s'" % (testName, msg)
      self.checkImage( self.baselineFile(fname),
                       self.outputFile(fname), 1.0e-3, msg )

   #-----------------------------------------------------------------------
   def checkImage( self, expected, actual, tol, msg ):
      '''Compare two image files.
      = INPUT VARIABLES
      - expected  The filename of the expected image.
      - actual    The filename of the actual image.
      - tol       The tolerance (a unitless float).  This is used to
                  determinte the 'fuzziness' to use when comparing images.
      '''
      from PIL import Image, ImageOps, ImageFilter

      # open the image files and remove the alpha channel (if it exists)
      expectedImage = Image.open( expected ).convert("RGB")
      actualImage = Image.open( actual ).convert("RGB")

      # normalize the images
      expectedImage = ImageOps.autocontrast( expectedImage, 2 )
      actualImage = ImageOps.autocontrast( actualImage, 2 )

      # compare the resulting image histogram functions
      h1 = expectedImage.histogram()
      h2 = actualImage.histogram()
      rms = math.sqrt( reduce( operator.add, map( lambda a,b: ( a - b )**2,
                                                  h1, h2) ) / len( h1 ) )

      diff = rms / 10000.0
      msg += "\nError: Image files did not match.\n" \
             "   RMS Value: %22.15e\n" \
             "   Expected:  %s\n" \
             "   Actual  :  %s\n" \
             "   Tolerance: %22.15e\n" % ( diff, expected, actual, tol )
      self.assertLessEqual( diff, tol, msg )

   #-----------------------------------------------------------------------
   def checkStyleEq( self, testName, desired, expected ):
      desiredProps = desired.propertyNames()
      expectedProps = expected.propertyNames()

      self.assertEqual( desiredProps, expectedProps,
               msg = "%s: desired properties do not match expected " \
                     "properties." % (testName,) )

      for propName in desiredProps:
         desiredValue = getattr( desired, propName )
         expectedValue = getattr( expected, propName )

         if isinstance( desiredValue, S.types.SubStyle ):
            self.checkStyleEq( "%s.%s" % (testName, propName),
                                desiredValue, expectedValue )
         else:
            self.assertEqual( desiredValue, expectedValue,
                     msg = "%s: style values do not match." % (testName,) )

   #-----------------------------------------------------------------------
   def testBasic( self ):
      """A basic test of MplStyleManager."""

      # Setup the plot
      fig, ax = matplotlib.pyplot.subplots()
      patch = mpl.patches.Patch()

      ax.minorticks_on()
      ax.set_title( 'Axes Title' )
      ax.set_xlabel( "X-Axis Label" )
      ax.set_ylabel( "Y-Axis Label" )

      xdata = [1, 1.5,  2, 2.5,  3, 3.5,  4, 4.5,  4.75, 5]
      ydata = [1, 1.75, 2, 2.75, 3, 2.75, 2, 2.25, 2.75, 3]
      line = ax.plot( xdata, ydata, color='blue' )

      axText = ax.text( 4.2, 1.1, "Axes Text" )

      # Get the manager
      mgr = S.mgr

      style1 = mgr.create( 'Style #1' )
      style1.axes.labels.font.size = 8

      style2 = mgr.create( 'Style #2', 
                           { 'figure.bgColor' : 'grey', 
                             'axes.bgColor' : 'white' } )

      style3 = mgr.create( 'Style #3', parent = style1 )
      style3.axes.labels.font.size = 24

      # Resolved 3 with 2
      style4 = S.MplStyle( 'Style #4' )
      style4.axes.labels.font.size = 24
      style4.figure.bgColor = 'grey'
      style4.axes.bgColor = 'yellow'

      # Resolved 3 with 2 and updated 3
      style5 = mgr.create( 'Style #5' )
      mgr[ 'Style #5' ].axes.labels.font.size = 16
      mgr[ 'Style #5' ].figure.bgColor = 'grey'
      mgr[ 'Style #5' ].axes.bgColor = 'yellow'


      # Copy test
      newStyle = mgr.copy( style3, 'NewStyle' )
      self.checkStyleEq( 'Copy - style3', style3, newStyle )

      self.assertRaises( Exception, mgr.copy, 'badName', 'blah',
                   msg = "Failed to raise when copying a non-existant style." )


      self.assertEqual( [], mgr.getElementStyles( fig ),
               msg = "Element styles should be []." )

      mgr.apply( fig, style4 )
      self.checkPlot( "MplStyleManager_testBasic_001", fig,
                       msg = "Apply by style" )

      self.assertEqual( True, mgr.exists(style4),
               msg = "Failed to auto add an applied style." )


      # This should be identical to *_001
      mgr.apply( fig, 'Style #3' )
      self.checkPlot( "MplStyleManager_testBasic_002", fig,
                       msg = "Apply by name" )

      style3.axes.labels.font.size = 16
      mgr.reapply()
      self.checkPlot( "MplStyleManager_testBasic_003", fig,
                       msg = "Re-Apply" )


      mgr.set( fig, 'axes.labels.font.size', 24 )
      self.checkPlot( "MplStyleManager_testBasic_004", fig,
                       msg = "Set by name" )

      mgr.set( fig, { 'axes.labels.font.size' : 16 } )
      self.checkPlot( "MplStyleManager_testBasic_005", fig,
                       msg = "Set by dict" )

      mgr.setElementStyles( ax, [ style2.name ] )
      mgr.reapply()
      self.checkPlot( "MplStyleManager_testBasic_006", fig,
                       msg = "Manually set element styles" )

      tmpStyle = S.MplStyle( "Temp Style" )
      mgr.add( tmpStyle )
      self.assertRaises( Exception, mgr.add, tmpStyle,
                   msg = "Failed to throw on multiple adds." )

      mgr.erase( tmpStyle )
      result = mgr.find( tmpStyle.name )
      self.assertEqual( None, result,
               msg = "Did not remove 'tmpStyle' from the manager." )

      msg = "Failed to throw on multiple removes."
      self.assertRaises( Exception, mgr.erase, tmpStyle, msg = msg )

      mgr.loadFile( self.inputFile( "GoodStyle.mplstyle" ) )
      mgr.apply( fig, "Good Style" )
      self.checkPlot( "MplStyleManager_testBasic_007", fig,
                       msg = "Custom python script" )

      # Check the get/set of the element name
      self.assertEqual( [], mgr.getTags( fig ),
               msg = "Element name should be None" )

      mgr.tag( fig, 'testName' )
      self.assertEqual( ['testName'], mgr.getTags( fig ),
               msg = "Failed to get and set the element name." )

   #-----------------------------------------------------------------------
   def testPersistence( self ):
      """Test reading and writing functionality."""
      mgr = S.MplStyleManager()

      # Setup the style
      style = mgr.create( 'Style_#1' )
      style.bgColor = 'white'
      style.fgColor = 'black'
      # Figure
      style.figure.width = 10
      style.figure.height = 10
      # Axes
      style.axes.axisBelow = True
      style.axes.leftEdge.color = 'magenta'
      style.axes.leftEdge.width = 5
      style.axes.leftEdge.style = '--'
      style.axes.bottomEdge.color = 'magenta'
      style.axes.bottomEdge.width = 5
      style.axes.bottomEdge.style = 'dashed'
      style.axes.topEdge.visible = False
      style.axes.rightEdge.visible = False
      style.axes.title.font.scale = 2.0
      style.axes.title.font.family = 'sans-serif'
      # X-Axis
      style.axes.xAxis.autoscale = True
      style.axes.xAxis.dataMargin = 0.2
      style.axes.xAxis.label.font.scale = 1.2
      style.axes.xAxis.majorTicks.labels.font.scale = 0.75
      style.axes.xAxis.majorTicks.grid.visible = True
      style.axes.xAxis.majorTicks.grid.color = '#B0B0B0'
      style.axes.xAxis.majorTicks.grid.width = 1.5
      style.axes.xAxis.majorTicks.grid.style = ':'
      style.axes.xAxis.majorTicks.length = 15.0
      style.axes.xAxis.majorTicks.width = 1.5
      style.axes.xAxis.minorTicks.grid.visible = True
      style.axes.xAxis.minorTicks.grid.color = '#B0B0B0'
      style.axes.xAxis.minorTicks.grid.width = 0.5
      style.axes.xAxis.minorTicks.grid.style = ':'
      style.axes.xAxis.minorTicks.length = 5.0
      style.axes.xAxis.minorTicks.width = 0.5
      # Y-Axis
      style.axes.yAxis = style.axes.xAxis.copy()
      # Lines
      style.line.color = "blue"
      style.line.style = 'dash-dot'
      style.line.width = 1.5
      style.line.marker.color = 'red'
      style.line.marker.edgeColor = 'green'
      style.line.marker.size = 12
      style.line.marker.style = 'circle'
      style.line.marker.fill = 'bottom'
      # Patches
      style.patch.color = 'gold'
      style.patch.filled = True
      style.patch.edgeColor = 'purple'
      style.patch.edgeWidth = 5
      # Text
      style.text.lineSpacing = 1.0
      style.text.font.size = 12
      style.text.font.family = 'monospace'

      # Save to file
      mgr.save( outdir = self.outputDir )

      self.assertRaises( Exception, mgr.save, outdir=self.outputDir, overwrite=False,
                   msg = "Failed to raise when writing to an existing file." )

      mgr2 = S.MplStyleManager()
      mgr2.load()
      self.checkStyleEq( "Default Load - style", style, mgr2[ style.name ] )

      mgr3 = S.MplStyleManager()
      mgr3.path = [ self.outputDir ]
      mgr3.load()
      self.checkStyleEq( "Load by path - style", style, mgr3[ style.name ] )

      mgr4 = S.MplStyleManager()
      mgr4.path = [ '$STYLEPATH' ]
      mgr4.load()
      self.checkStyleEq( "Load by path STYLEPATH - style",
                          style, mgr4[ style.name ] )

      mgr5 = S.MplStyleManager()
      mgr5.load( self.outputDir )
      self.checkStyleEq( "Load by passed path - style",
                          style, mgr5[ style.name ] )

      os.environ.pop( "STYLEPATH" )
      mgr6 = S.MplStyleManager()
      mgr6.load()

      self.assertEqual( None, mgr6.find( style.name ),
               msg = "There should be not style loaded." )

      p = self.outputFile( 'Style_#1.mplstyle' )
      mgr6.loadFile( p )
      self.assertEqual( True, os.path.exists( p ),
               msg = "Manager failed to write the style file." )

      mgr6.erase( style, delete = True )
      self.assertEqual( False, os.path.exists( p ),
               msg = "Manager failed to remove the style file." )


   #-----------------------------------------------------------------------
   def testErrors( self ):
      """Test error conditions."""
      mgr = S.MplStyleManager()

      self.assertRaises( Exception, mgr.loadFile, "Invalid File",
                   msg = "Failed to throw exception for non-existent file." )

      self.assertRaises( Exception, mgr.loadFile,
                   self.inputFile( "BadStyle1.mplstyle" ),
                   msg = "Failed to throw for missing 'style' in file." )

      self.assertRaises( Exception, mgr.loadFile,
                   self.inputFile( "BadStyle2.mplstyle" ),
                   msg = "Failed to throw for invalid 'style' in file." )

      self.assertRaises( Exception, mgr.loadFile,
                   self.inputFile( "BadCustom.mplstyle" ),
                   msg = "Failed to throw for bad custom file." )

   #-----------------------------------------------------------------------

