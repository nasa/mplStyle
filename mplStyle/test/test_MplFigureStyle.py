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

"Unit test for the MplFigureStyle class."

__version__ = "$Revision: #1 $"

#===========================================================================
# Required imports.  Do not modify these.

import unittest

#===========================================================================
# Place all imports after here.
#

import matplotlib as mpl
mpl.use( "Agg" )
import matplotlib.figure
import matplotlib.pyplot
import mplStyle as S
import os, os.path
import math, operator
import shutil
#
# Place all imports before here.
#===========================================================================

#===========================================================================
class TestMplFigureStyle( unittest.TestCase ):
   """Test the MplFigureStyle class."""

   #-----------------------------------------------------------------------
   @classmethod
   def setUp( self ):
      """This method is called before any tests are run."""
      self.outputDir = "output"
      if not os.path.exists( self.outputDir ):
         os.mkdir( self.outputDir )

   #-----------------------------------------------------------------------
   @classmethod
   def tearDown( self ):
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
   def checkElement( self, testName, values, element ):
      for property in values:
         expected = values[ property ]
         msg = "%s: Incorrect value for property: %s" % (testName, property)
         getFunc = getattr( element, 'get_%s' % property )
         self.assertEqual( expected, getFunc(), msg = msg )

   #-----------------------------------------------------------------------
   def testFigure( self ):
      """A basic test of MplFigureStyle using matplotlib.Figure."""

      values = {
         'figwidth' : 10.0,
         'figheight' : 10.0,
         'dpi' : 100,
      }

      patchVals = {
         'facecolor' : (0.0, 1.0, 0.0, 1.0),
         'edgecolor' : (0.0, 0.0, 1.0, 1.0),
         'linestyle' : 'dashed',
         'linewidth' : 1.5,
      }

      subplotVals = {
         'left' : 0.2,
         'right' : 0.98,
         'bottom' : 0.2,
         'top' : 0.98,
         'wspace' : 0.2,
         'hspace' : 0.2,
      }

      element, ax = matplotlib.pyplot.subplots()

      style = S.MplFigureStyle(
         width = values['figwidth'],
         height = values['figheight'],
         dpi = values['dpi'],
         bgColor = patchVals['facecolor'],
         edgeColor = patchVals['edgecolor'],
         edgeStyle = '--',   #   patchVals['linestyle'],
         edgeWidth = patchVals['linewidth'],
         leftMargin = subplotVals['left'],
         rightMargin = 1.0 - subplotVals['right'],
         topMargin = 1.0 - subplotVals['top'],
         bottomMargin = subplotVals['bottom'],
         axesPadX = subplotVals['wspace'],
         axesPadY = subplotVals['hspace'],
      )

      style.apply( element )

      # Check the image
      fname = "MplFigureStyle_testFigure_001.png"
      element.savefig( self.outputFile( fname ) )

      msg = "Incorrect styled Figure plot."
      self.checkImage( self.baselineFile(fname),
                       self.outputFile(fname), 1.0e-3, msg )

      self.checkElement( "Apply", values, element )
      self.checkElement( "Apply Patch", patchVals, element.patch )

      subplotParams = element.subplotpars
      for name in subplotVals:
         self.assertEqual( subplotVals[name], getattr( subplotParams, name ),
                  msg = "Incorrect subplot-param '%s'" % name )

      self.assertRaises( Exception, style.apply, 'invalid',
                   msg = "Failed to throw on invalid element." )

   #-----------------------------------------------------------------------

