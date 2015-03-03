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

"Unit test for the Style class."

__version__ = "$Revision: #1 $"

#===========================================================================
# Required imports.  Do not modify these.
import unittest

#===========================================================================
# Place all imports after here.
#
import mplStyle as S

#
# Place all imports before here.
#===========================================================================

#===========================================================================
class MyStyle( S.types.Style ):
   """A Sub-Classed Style."""

   #-----------------------------------------------------------------------
   def __init__( self, name, kw = {}, parent = None, custom = None ):
      self.figure = S.types.Data(
         text = S.types.Data( 
            size = None,
            color = None,
            ),
         bgColor = None,
         fgColor = None,
         )

      self.axes = S.types.Data(
         text = S.types.Data( 
            size = None,
            color = None,
            ),
         bgColor = None,
         fgColor = None,
         )

      # The Style CTOR will attempt to apply the keyword argument values,
      # So we need to call this last.
      S.types.Style.__init__( self, name, kw, parent, custom )

   #-----------------------------------------------------------------------
   def __str__( self ):
      s  = "%s\n" % self.name
      s += "   figure = %s\n" % self.figure
      s += "     axes = %s\n" % self.axes
      return s

   #-----------------------------------------------------------------------
   def copy( self, newName ):
      style = MyStyle( newName, {}, self.parent, self.custom )

      style.figure = self.figure.copy( deep = True )
      style.axes = self.axes.copy( deep = True )

      return style

   #-----------------------------------------------------------------------
   def update( self, style ):
      super( MyStyle, self ).update( style )

      if style.figure.text.size is not None:
         self.figure.text.size = style.figure.text.size

      if style.figure.text.color is not None:
         self.figure.text.color = style.figure.text.color

      if style.figure.bgColor is not None:
         self.figure.bgColor = style.figure.bgColor

      if style.figure.fgColor is not None:
         self.figure.fgColor = style.figure.fgColor

      if style.axes.text.size is not None:
         self.axes.text.size = style.axes.text.size

      if style.axes.text.color is not None:
         self.axes.text.color = style.axes.text.color

      if style.axes.bgColor is not None:
         self.axes.bgColor = style.axes.bgColor

      if style.axes.fgColor is not None:
         self.axes.fgColor = style.axes.fgColor

   #-----------------------------------------------------------------------
   def _applyStyle( self, obj, filter, postProcess ):
      process, recurse = filter( obj )

      if not process:
         return

      if self.figure.text.size is not None:
         obj.figureTextSize = self.figure.text.size

      if self.figure.text.color is not None:
         obj.figureTextColor = self.figure.text.color

      if self.figure.bgColor is not None:
         obj.figureBgColor = self.figure.bgColor

      if self.figure.fgColor is not None:
         obj.figureFgColor = self.figure.fgColor

      if self.axes.text.size is not None:
         obj.axesTextSize = self.axes.text.size

      if self.axes.text.color is not None:
         obj.axesTextColor = self.axes.text.color

      if self.axes.bgColor is not None:
         obj.axesBgColor = self.axes.bgColor

      if self.axes.fgColor is not None:
         obj.axesFgColor = self.axes.fgColor

      postProcess( obj )

#===========================================================================
class TestStyle( unittest.TestCase ):
   """Test the Style class."""

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
   def checkObj( self, name, obj, style ):
      """Check if the object has the style."""
      attrs = {
         'TextSize' : 'text.size',
         'TextColor' : 'text.color',
         'BgColor' : 'bgColor',
         'FgColor' : 'fgColor'
      }

      for key in attrs:
         desired = style.getValue( 'figure.%s' % attrs[key] )
         actual = getattr( obj, 'figure%s' % key )
         msg = "%s: figure %s not properly set." % (name, key)
         self.assertEqual( desired, actual, msg = msg )

         desired = style.getValue( 'axes.%s' % attrs[key] )
         actual = getattr( obj, 'axes%s' % key )
         msg = "%s: axes %s not properly set." % (name, key)
         self.assertEqual( desired, actual, msg = msg )

   #-----------------------------------------------------------------------
   def checkDataEq( self, name, desired, actual ):
      """Check if two Data are equall"""
      if isinstance( desired, S.types.Data ) and \
         isinstance( actual, S.types.Data ):
         self.assertEqual( desired.keys(), actual.keys(),
                  msg = "Data keys are not the same is test '%s'." % (name,) )

         for key in desired:
            self.checkDataEq( '%s:%s' % (name, key), desired[key], actual[key] )
      else:
         self.assertEqual( desired, actual,
                  msg = "Data value wrong in test '%s'" % (name,) )

   #-----------------------------------------------------------------------
   def checkStyleEq( self, name, desired, actual ):
      """Check if two Styles are equall"""
      self.checkDataEq( '%s:figure' % name, desired.figure, actual.figure )
      self.checkDataEq( '%s:axes' % name, desired.axes, actual.axes )

   #-----------------------------------------------------------------------
   def testBasic( self ):
      """A basic test of Style."""

      style1 = MyStyle( 'Style #1' )
      style1.figure.text.size = 12
      style1.axes.text.size = 8

      style2 = MyStyle( 'Style #2' )
      style2.figure.bgColor = 'grey'
      style2.axes.bgColor = 'white'

      style3 = MyStyle( 'Style #3', parent = style1 )
      style3.figure.text.size = 24

      # Resolved 3 with 2
      style4 = MyStyle( 'Style #4' )
      style4.figure.text.size = 24
      style4.axes.text.size = 8
      style4.figure.bgColor = 'grey'
      style4.axes.bgColor = 'white'

      # Update 3 with 2
      style5 = MyStyle( 'Style #5' )
      style5.figure.text.size = 24
      style5.figure.bgColor = 'grey'
      style5.axes.bgColor = 'white'

      # kwarg CTOR
      style6 = MyStyle( 'Style #6',
                        { 'figure.text.size' : 24,
                          'figure.bgColor' : 'grey',
                          'axes.bgColor' : 'white',
                        } )

      style7 = MyStyle( 'Style #7',
                        { 'parent' : style1,
                          'figure.text.size' : 24,
                        } )

      msg = "Incorrect name"
      self.assertEqual( "Style #1", style1.name, msg = msg )

      msg = "Failed direct access: style1.figure.text.size"
      self.assertEqual( 12, style1.figure.text.size, msg = msg )

      msg = "Failed direct access: style3.figure.text.size"
      self.assertEqual( 24, style3.figure.text.size, msg = msg )

      msg = "Failed getValue: style1.figure.text.size"
      self.assertEqual( 12, style1.getValue( 'figure.text.size' ), msg = msg )

      msg = "Failed getValue: style3.figure.text.size"
      self.assertEqual( 24, style3.getValue( 'figure.text.size' ), msg = msg )

      msg = "Failed getValue: style3.axes.text.size"
      self.assertEqual( None, style3.getValue( 'axes.text.size' ), msg = msg )

      msg = "Failed getResolvedValue: style3.axes.text.size"
      self.assertEqual( 8, style3.getResolvedValue( 'axes.text.size' ), msg = msg )

      newStyle = style3.resolve( 'NewStyle', style2 )
      self.checkStyleEq( 'Resolve', style4, newStyle )

      newStyle = style3.copy( 'NewStyle' )
      self.checkStyleEq( 'Copy', style3, newStyle )

      newStyle.update( style2 )
      self.checkStyleEq( 'Update', style5, newStyle )

      self.checkStyleEq( 'kwarg CTOR #1', style5, style6 )
      self.checkStyleEq( 'kwarg CTOR #2', style3, style7 )

      def customFunc( obj ):
         obj.figureBgColor = 'grey'
         obj.axesBgColor = 'white'

      style3.custom = customFunc

      obj = S.types.Data(
         figureTextSize = None,
         figureTextColor = None,
         figureBgColor = None,
         figureFgColor = None,
         axesTextSize = None,
         axesTextColor = None,
         axesBgColor = None,
         axesFgColor = None,
      )

      style3.apply( obj )
      self.checkObj( 'Apply', obj, style4 )

      self.assertEqual( False, style3.canApply( obj ), msg = "Incorrect return value." )

      style1.setValue( 'figure.text.size', 10 )
      msg = "Failed setValue: style1.figure.text.size"
      self.assertEqual( 10, style1.getValue( 'figure.text.size' ), msg = msg )

      newStyle = MyStyle.resolveStyles( None, style1 )
      self.checkStyleEq( 'resolveStyles [01]', style1, newStyle )

      newStyle = MyStyle.resolveStyles( None, [style2, style3] )
      self.checkStyleEq( 'resolveStyles [02]', style4, newStyle )

   #-----------------------------------------------------------------------
   def testMultiParents( self ):
      """A test of multiple parent styles."""

      style1 = MyStyle( 'Style #1' )
      style1.figure.text.size = 12
      style1.figure.text.color = 'black'
      style1.axes.text.size = 8
      style1.axes.text.color = 'darkgray'

      style2 = MyStyle( 'Style #2' )
      style2.figure.bgColor = 'yellow'
      style2.axes.bgColor = 'white'
      style2.axes.text.color = 'gold'

      style3 = MyStyle( 'Style #3', parent = style1 )
      style3.figure.text.size = 24
      style3.figure.fgColor = 'red'

      style4 = MyStyle( 'Style #4', parent = [ style3, style2 ] )
      style4.figure.fgColor = 'green'
      style4.axes.fgColor = 'darkgreen'

      # Resolve 4
      style5 = MyStyle( 'Style #5' )
      style5.figure.text.size = 24
      style5.figure.text.color = 'black'
      style5.figure.bgColor = 'yellow'
      style5.figure.fgColor = 'green'
      style5.axes.text.size = 8
      style5.axes.text.color = 'gold'
      style5.axes.bgColor = 'white'
      style5.axes.fgColor = 'darkgreen'

      newStyle = style4.resolve( 'NewStyle' )
      self.checkStyleEq( 'Resolve Multi Parents', style5, newStyle )

   #-----------------------------------------------------------------------
   def testErrors( self ):
      """A basic test of Style errors."""

      style1 = MyStyle( 'Style #1' )
      style1.figure.text.size = 12
      style1.axes.text.size = 8

      msg = "Bad path failed to error"
      self.assertRaises( Exception, style1.getValue, 'this.is.a.bad.path', msg = msg )

      msg = "Mostly bad get path failed to error"
      self.assertRaises( Exception, style1.getValue, 'figure.text.bogus', msg = msg )

      msg = "Mostly bad set path failed to error"
      self.assertRaises( Exception, style1.setValue, 'figure.text.bogus', 'bad', msg = msg )
