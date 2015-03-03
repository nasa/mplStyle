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

"Unit test for the MplStyle class."

__version__ = "$Revision: #1 $"

#===========================================================================
# Required imports.  Do not modify these.

import unittest

#===========================================================================
# Place all imports after here.
#
import matplotlib as mpl
mpl.use( "Agg" )

import matplotlib.pyplot
import matplotlib.axes
import matplotlib.figure
import matplotlib.patches
import matplotlib.text
import os, os.path
import shutil
import math, operator

import mplStyle as S

#
# Place all imports before here.
#===========================================================================

#===========================================================================
def doNothing( element ):
   pass

#===========================================================================
class TestMplStyle( unittest.TestCase ):
   """Test the MplStyle class."""

   #-----------------------------------------------------------------------
   @classmethod
   def setUpClass( self ):
      """This method is called before any tests are run."""
      self.outputDir = "output"
      if not os.path.exists( self.outputDir ):
         os.mkdir( self.outputDir )

   #-----------------------------------------------------------------------
   @classmethod
   def tearDownClass( self ):
      """This method is called after all tests are run."""
      if os.path.exists( self.outputDir ):
         shutil.rmtree( self.outputDir )

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
   def testBasic( self ):
      """A basic test of MplStyle."""

      # Setup the plot
      fig, ax = matplotlib.pyplot.subplots()
      patch = mpl.patches.Patch()

      ax.set_title( 'Axes Title' )
      ax.set_xlabel( "X-Axis Label" )
      ax.set_ylabel( "Y-Axis Label" )

      xdata = [1, 1.5,  2, 2.5,  3, 3.5,  4, 4.5,  4.75, 5]
      ydata = [1, 1.75, 2, 2.75, 3, 2.75, 2, 2.25, 2.75, 3]
      line = ax.plot( xdata, ydata )
      # There is only one line returned
      line = line[0]

      rect = mpl.patches.Rectangle( (2.8, 1.0), 0.4, 1.2 )
      ax.add_patch( rect )

      axText = ax.text( 4.2, 1.1, "Axes Text" )

      figText = fig.text( 0.0, 0.0, "Figure Text" )
      figLine = mpl.lines.Line2D( [0.5, 0.5], [0.0, 1.0], color='red' )
      fig._set_artist_props( figLine )
      fig.lines.append( figLine )
      figRect = mpl.patches.Rectangle( (0.25, 0.25), 0.5, 0.5,
                                       facecolor='lightgreen',
                                       edgecolor='lightgreen',
                                       alpha=0.25 )
      fig._set_artist_props( figRect )
      fig.patches.append( figRect )

      # Setup the style
      style = S.MplStyle( "Test Style" )
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
      style.axes.xAxis.majorTicks.marks.visible = True
      style.axes.xAxis.majorTicks.grid.visible = True
      style.axes.xAxis.majorTicks.grid.color = '#B0B0B0'
      style.axes.xAxis.majorTicks.grid.width = 1.5
      style.axes.xAxis.majorTicks.grid.style = ':'
      style.axes.xAxis.majorTicks.length = 15.0
      style.axes.xAxis.majorTicks.width = 1.5
      style.axes.xAxis.minorTicks.marks.visible = True
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

      # Check the dir function
      expected = [ '__class__', '__delattr__', '__dict__', '__doc__',
                   '__format__', '__getattribute__', '__hash__', '__init__',
                   '__metaclass__', '__module__', '__new__', '__reduce__',
                   '__reduce_ex__',
                   '__repr__', '__setattr__', '__sizeof__', '__str__',
                   '__subclasshook__', '__weakref__', '_aliases',
                   '_applyStyle', '_completed_init', '_getParentOfProperty',
                   '_name', '_propertyNames', '_restricted_setattr',
                   '_subStyle', 'apply', 'axes', 'bgColor', 'canApply', 'copy',
                   'custom', 'fgColor', 'figure', 'format', 'getPropertyType',
                   'getResolvedValue', 'getValue', 'hasAnySet', 'kwargs',
                   'line', 'name', 'parent', 'patch', 'propertyNames',
                   'resolve', 'resolveStyles', 'setValue', 'text', 'update' ]
      self.assertEqual( expected, dir(style), msg = "Invalid 'dir' result." )

      # Check the str function
      style2 = S.MplStyle( "Test Style #2" )
      style2.update( {
         'bgColor' : 'white',
         'fgColor' : 'black',
         'figure.width' : 10,
         'figure.height' : 10,
      } )
      expected = """MplSubStyle:
   * bgColor = #FFFFFF
   * fgColor = #000000
   * figure =  MplFigureStyle:
      * height = 10.0
      * width = 10.0"""
      self.assertEqual( expected, str(style2), msg = "Invalid 'str' result." )

      # Check Property types
      self.assertEqual( S.types.property.MplColor,
                        style.getPropertyType( 'fgColor' ),
                        msg = "Invalid property type for 'fgColor'" )

      self.assertEqual( S.types.property.SubStyle,
                        style.getPropertyType( 'patch' ),
                        msg = "Invalid property type for 'patch'" )

      # Check 'canApply'
      self.assertEqual( True, style.canApply( fig ),
               msg = "Invalid 'canApply' for Figure" )
      self.assertEqual( True, style.canApply( ax ),
               msg = "Invalid 'canApply' for Axes" )
      self.assertEqual( True, style.canApply( line ),
               msg = "Invalid 'canApply' for Line2D" )
      self.assertEqual( True, style.canApply( rect ),
               msg = "Invalid 'canApply' for Patch" )
      self.assertEqual( True, style.canApply( axText ),
               msg = "Invalid 'canApply' for Text" )
      self.assertEqual( False, style.canApply( 1.23 ),
               msg = "Invalid 'canApply' for Float" )

      # Write to a file
      fname = "MplStyle_testBasic_001.png"
      fig.savefig( self.outputFile( fname ) )

      msg = "Failed initial image plot check"
      self.checkImage( self.baselineFile(fname),
                       self.outputFile(fname), 1.0e-3, msg )


      # Apply the styles
      style.apply( fig, postProcess = doNothing )

      # Write to a file
      fname = "MplStyle_testBasic_002.png"
      fig.savefig( self.outputFile( fname ) )

      msg = "Error formatting the plot properly."
      self.checkImage( self.baselineFile(fname),
                       self.outputFile(fname), 1.0e-3, msg )

      # Copy the style
      styleCopy = style.copy( "Original Style" )

      # Update the x-axis only
      style.axes.xAxis.dataMargin = 0.5
      style.axes.xAxis.majorTicks.labels.rotation = -30.0
      style.axes.yAxis.majorTicks.labels.rotation = -90.0
      style.apply( ax.get_xaxis(), postProcess = doNothing )
      style.apply( ax.get_yaxis(), postProcess = doNothing )

      fname = "MplStyle_testBasic_003.png"
      fig.savefig( self.outputFile( fname ) )
      self.checkImage( self.baselineFile(fname),
                       self.outputFile(fname), 1.0e-3, 
                       msg = "axis is not correct" )

      # Update the font properties
      style.text.font.size = 16
      style.apply( ax.title.get_fontproperties(), postProcess = doNothing )

      fname = "MplStyle_testBasic_004.png"
      fig.savefig( self.outputFile( fname ) )
      self.checkImage( self.baselineFile(fname),
                       self.outputFile(fname), 1.0e-3, 
                       msg = "axes text is not correct" )

      # Apply the new style to the entire figure
      style.apply( fig, postProcess = doNothing )

      fname = "MplStyle_testBasic_005.png"
      fig.savefig( self.outputFile( fname ) )
      self.checkImage( self.baselineFile(fname),
                       self.outputFile(fname), 1.0e-3, 
                       msg = "modified Style is not correct" )

      # apply the copied style
      styleCopy.apply( fig, postProcess = doNothing )

      # This is almost identical to #002 -- the x-axis labels should be rotated
      fname = "MplStyle_testBasic_006.png"
      fig.savefig( self.outputFile(fname) )
      self.checkImage( self.baselineFile(fname),
                       self.outputFile(fname), 1.0e-3, 
                       msg = "Copied Style is not correct" )

      # Make a new style
      invertedStyle = S.MplStyle( "Inverted Style" )
      invertedStyle.bgColor = 'black'
      invertedStyle.fgColor = 'white'

      styleCopy.update( invertedStyle )
      styleCopy.apply( ax, postProcess = doNothing )

      fname = "MplStyle_testBasic_007.png"
      fig.savefig( self.outputFile( fname ) )
      self.checkImage( self.baselineFile(fname),
                       self.outputFile(fname), 1.0e-3, 
                       msg = "Updated Style is not correct" )

   #-----------------------------------------------------------------------
   def testErrors( self ):
      """A test of MplStyle error conditions."""

      # Setup the style
      style = S.MplStyle( "Test Errors Style" )

      self.assertRaises( Exception, style.apply, "bogusObject",
                   msg = "Failed to throw on invalid apply object." )

      try:
         style.bogus
      except:
         pass
      else:
         fail( "Failed to throw on accessing an invalid property." )

      style._subStyle = None
      try:
         style.bogus = "invalid"
      except:
         pass
      else:
         fail( "Failed to throw on setting an invalid property." )


      class MplDerivedStyle( S.MplStyle ):
         def __init__( self, *args, **kwargs ):
            S.MplStyle.__init__( self, *args, **kwargs )
            self.bgColor = 'white'
            self.fgColor = 'black'
            self.newProperty = None

      # Make sure that construction doesn't throw
      tmpStyle = MplDerivedStyle( "tmpStyle" )

   #-----------------------------------------------------------------------
   def testDefaults( self ):
      """Test that MplStyle falls through to defaults properly."""
      fig, ax = matplotlib.pyplot.subplots()
      ax.set_title( "This is the Title" )
      line = ax.plot( [1, 2, 3, 4], [2, 4, 6, 8] )

      style = S.MplStyle( "Big Title" )
      #style.axes.title.font.family = "sans-serif"

      fname = "MplStyle_testDefaults_001.png"
      fig.savefig( self.outputFile( fname ) )
      self.checkImage( self.baselineFile(fname),
                  self.outputFile(fname), 1.0e-3, 
                  msg = "Original plot is not correct" )

      style.apply( fig )

      fname = "MplStyle_testDefaults_002.png"
      fig.savefig( self.outputFile( fname ) )
      self.checkImage( self.baselineFile(fname),
                  self.outputFile(fname), 1.0e-3, 
                  msg = "Styled plot is not correct" )

   #-----------------------------------------------------------------------

