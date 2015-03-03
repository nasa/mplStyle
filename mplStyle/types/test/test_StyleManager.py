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

"Unit test for the StyleManager class."

__version__ = "$Revision: #1 $"

#===========================================================================
# Required imports.  Do not modify these.
import unittest

#===========================================================================
# Place all imports after here.
#
import mplStyle as S
import os
import shutil
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
class MyStyleManager( S.types.StyleManager ):
   """A Sub-Classed Style."""

   #-----------------------------------------------------------------------
   def __init__( self ):
      S.types.StyleManager.__init__( self, MyStyle, 'testyle', 'TEST' )

   #-----------------------------------------------------------------------
   def _loadFromFile( self, fname ):
      name = fname.namebase
      style = MyStyle( name )

      with open( fname, 'r' ) as fin:
         s = fin.readline()
         style.figure.__dict__ = eval( s )

         d = style.figure.text
         style.figure.text = Data()
         style.figure.text.__dict__ = d

         s = fin.readline()
         style.axes.__dict__ = eval( s )

         d = style.axes.text
         style.axes.text = Data()
         style.axes.text.__dict__ = d

      return style

   #-----------------------------------------------------------------------
   def _saveToFile( self, style, fname ):
      with open( fname, 'w' ) as fout:
         fout.write( "%s\n" % style.figure )
         fout.write( "%s\n" % style.axes )

   #-----------------------------------------------------------------------
   def _deleteStyleFile( self, fname ):
      fname.remove()

#===========================================================================
class TestStyleManager( unittest.TestCase ):
   """Test the StyleManager class."""

   #-----------------------------------------------------------------------
   def setUp( self ):
      """This method is called before any tests are run."""
      # Save the existing STYLEPATH (if there is one)
      self.outputDir = "output"
      self.stylepath = os.environ.get( "STYLEPATH", None )
      os.environ[ "STYLEPATH" ] = self.outputDir

      if not os.path.exists( self.outputDir ):
         os.mkdir( self.outputDir )

   #-----------------------------------------------------------------------
   def tearDown( self ):
      """This method is called after all tests are run."""
      # You may place finalization code here.
      if self.stylepath is not None:
         os.environ[ "STYLEPATH" ] = self.stylepath

      if os.path.exists( self.outputDir ):
         shutil.rmtree( self.outputDir )

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

      style = style.resolve(None)

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
      """A basic test of StyleManager."""

      mgr = MyStyleManager()

      style1 = mgr.create( 'Style #1' )
      style1.figure.text.size = 12
      style1.axes.text.size = 8

      style2 = mgr.create( 'Style #2', 
                           { 'figure.bgColor' : 'grey', 
                             'axes.bgColor' : 'white' } )
      style2.figure.bgColor = 'grey'
      style2.axes.bgColor = 'white'

      style3 = mgr.create( 'Style #3', parent = style1 )
      style3.figure.text.size = 24

      # Resolved 3 with 2
      style4 = MyStyle( 'Style #4' )
      style4.figure.text.size = 24
      style4.axes.text.size = 8
      style4.figure.bgColor = 'grey'
      style4.axes.bgColor = 'white'

      # Resolved 3 with 2 and updated 3
      style5 = mgr.create( 'Style #5' )
      mgr[ 'Style #5' ].figure.text.size = 16
      mgr[ 'Style #5' ].axes.text.size = 8
      mgr[ 'Style #5' ].figure.bgColor = 'grey'
      mgr[ 'Style #5' ].axes.bgColor = 'white'

      style6 = mgr.create( 'Style #6', parent='Style #5' )
      style6.figure.text.color = 'orange'
      style6.axes.text.color = 'purple'

      # Copy tests
      newStyle = mgr.copy( style3, 'NewStyle1' )
      self.checkStyleEq( 'Copy by style', style3, newStyle )

      newStyle = mgr.copy( 'Style #3', 'NewStyle2' )
      self.checkStyleEq( 'Copy by name', style3, newStyle )

      self.assertRaises( Exception, mgr.copy, 'badName', 'blah',
                   msg = "Failed to raise when copying a non-existant style." )

      # Test Resolve
      resolvedStyle = mgr.resolve( "Resolved Style #1", 'Style #2' )
      self.checkStyleEq( 'Resolve by name', style2, resolvedStyle )
      mgr.erase( resolvedStyle )

      resolvedStyle = mgr.resolve( "Resolved Style #2",
                                   ['Style #2', style3, 'blah'],
                                   ignoreNotFound = True )
      self.checkStyleEq( 'Resolve by list', style4, resolvedStyle )
      mgr.erase( resolvedStyle )

      self.assertRaises( Exception, mgr.resolve, None, 'does not exist',
                   msg = "Resolve failed to throw on invalid style." )

      # Apply testing
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

      mgr.apply( obj, style4 )
      self.checkObj( 'Apply by style', obj, style4 )
      self.assertEqual( True, mgr.exists(style4),
               msg = "Failed to auto add an applied style." )

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

      self.assertRaises( Exception, mgr.apply, obj, 'invalidName',
                   msg = "Failed to raise on applying a bad style." )

      self.assertEqual( [], mgr.getElementStyles( obj ),
               msg = "Element styles should be []." )

      mgr.apply( obj, 'Style #3' )
      self.checkObj( 'Apply by name', obj, style4 )

      style3.figure.text.size = 16
      mgr.reapply()
      self.checkObj( 'Re-Apply', obj, style5 )

      mgr.set( obj, 'figure.text.size', 24 )
      self.checkObj( 'Set by name', obj, style4 )

      mgr.set( obj, { 'figure.text.size' : 16 } )
      self.checkObj( 'Set by dict', obj, style5 )

      self.assertRaises( Exception, mgr.set, obj, { 'foo' : 1 }, 1,
                   msg = "Failed to throw with invalid 'set' parameters." )

      # Check the get/set of the element tag
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
      mgr.apply( obj, style5 )

      self.assertEqual( [], mgr.getTags( obj ),
               msg = "Element name should be None" )

      mgr.untag( obj, 'testTag' )
      self.assertEqual( False, mgr.hasTag( obj, 'testTag' ),
               msg = "Incorrect result for hasTag (when nothing set)." )
      mgr.tag( obj, 'testTag' )
      self.assertEqual( ['testTag'], mgr.getTags( obj ),
               msg = "Set/get tag failed for obj" )
      self.assertEqual( True, mgr.hasTag( obj, 'testTag' ),
               msg = "Incorrect result for hasTag (when it has it)" )
      mgr.untag( obj, 'testTag' )
      self.assertEqual( False, mgr.hasTag( obj, 'testTag' ),
               msg = "Incorrect result for hasTag (when it doesn't have it)" )
      mgr.tag( obj, 'testTag' )

      tagStyle = MyStyle( 'TagStyle' )
      tagStyle.figure.text.color = 'orange'
      tagStyle.axes.text.color = 'purple'

      mgr.apply( obj, tagStyle, tag = "OtherTag" )
      self.checkObj( 'Set by incorrect tag', obj, style5 )

      mgr.apply( obj, tagStyle, tag = "testTag" )
      self.checkObj( 'Set by correct tag', obj, style6 )

      # Check apply by tag only
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
      mgr.tag( obj, 'applyTestTag' )
      mgr.apply( None, style6, tag = 'applyTestTag' )
      self.checkObj( 'Apply by tag', obj, style6 )

      # Verify that the new style will be added when resolve is called
      tmpStyle1 = MyStyle( 'TmpStyle #1' )
      mgr.resolve( None, tmpStyle1 )

      # Verify that the new style will be added when create is called
      tmpStyle2 = MyStyle( 'TmpStyle #2' )
      mgr.create( None, parent = tmpStyle2 )

      # check loading / clearing styles
      expected = [ 'NewStyle1', 'NewStyle2', 'Style #1', 'Style #2',
                   'Style #3', 'Style #4', 'Style #5', 'Style #6',
                   'TagStyle', 'TmpStyle #1', 'TmpStyle #2' ]
      self.assertEqual( expected, mgr.getAll(),
               msg = "Invalid list of loaded styles." )

      tmpfile = open( os.path.join( self.outputDir, "warning-output.log" ),
                      'w' )
      mgr.apply( obj, [ style1, 'Style #3' ] )
      mgr.erase( style3 )
      mgr.reapply()
      tmpfile.close()

      mgr.clear()
      expected = []
      self.assertEqual( expected, mgr.getAll(),
               msg = "mgr shows styles loaded, when should be empty." )

      tmpStyle = MyStyle( "Temp Style" )
      mgr.add( tmpStyle )
      self.assertRaises( Exception, mgr.add, tmpStyle,
                   msg = "Failed to throw on multiple adds." )

      mgr.erase( tmpStyle )
      result = mgr.find( tmpStyle.name )
      self.assertEqual( None, result,
               msg = "Did not remove 'tmpStyle' from the manager." )

      msg = "Failed to throw on multiple removes."
      self.assertRaises( Exception, mgr.erase, tmpStyle, msg = msg )

      msg = "Failed to throw with invalid parent"
      self.assertRaises( Exception, mgr.create, 'Bad Parent', parent = "Bogus", msg = msg )

   #-----------------------------------------------------------------------
   def testPersistence( self ):
      """Test reading and writing functionality."""

      mgr = MyStyleManager()

      style1 = mgr.create( 'Style_#1' )
      style1.figure.text.size = 12
      style1.axes.text.size = 8

      mgr.save( outdir = self.outputDir )

      self.assertRaises( Exception, mgr.save, outdir=self.outputDir, overwrite=False,
                   msg = "Failed to raise when writing to an existing file." )

      mgr2 = MyStyleManager()
      mgr2.load()
      self.checkStyleEq( "Default Load", style1, mgr2[ style1.name ] )

      mgr3 = MyStyleManager()
      mgr3.path = [ self.outputDir ]
      mgr3.load()
      self.checkStyleEq( "Load by path", style1, mgr3[ style1.name ] )

      mgr4 = MyStyleManager()
      mgr4.path = [ '$STYLEPATH' ]
      mgr4.load()
      self.checkStyleEq( "Load by path STYLEPATH", style1, mgr4[ style1.name ] )

      mgr5 = MyStyleManager()
      mgr5.load( self.outputDir )
      self.checkStyleEq( "Load by passed path", style1, mgr5[ style1.name ] )

      os.environ.pop( "STYLEPATH" )
      mgr6 = MyStyleManager()
      mgr6.load()

      self.assertEqual( None, mgr6.find( style1.name ),
               msg = "There should be not style loaded." )

      p = path( self.outputFile( 'Style_#1.testyle' ) )
      self.assertEqual( True, p.exists(),
               msg = "Manager failed to write the style file." )

      mgr.erase( style1, delete = True )
      self.assertEqual( False, p.exists(),
               msg = "Manager failed to remove the style file." )

   #-----------------------------------------------------------------------
   def testErrors( self ):
      """Test error conditions."""

      mgr = MyStyleManager()
      style = MyStyle( "Dummy" )

      self.assertRaises( Exception, S.types.StyleManager._loadFromFile,
                         mgr, "Dummy", "Bogus",
                   msg = "Failed to throw on call to '_loadFromFile'." )

      self.assertRaises( Exception, S.types.StyleManager._saveToFile, mgr,
                         style, "Bogus",
                   msg = "Failed to throw on call to '_saveToFile'." )

      self.assertRaises( Exception, S.types.StyleManager._deleteStyleFile,
                         mgr, "Bogus",
                   msg = "Failed to throw on call to '_deleteStyleFile'." )

   #-----------------------------------------------------------------------

