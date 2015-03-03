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

"Unit test for the SubStyle class."

__version__ = "$Revision: #1 $"

#===========================================================================
# Required imports.  Do not modify these.
import unittest

#===========================================================================
# Place all imports after here.
#
import mplStyle as S
import mplStyle.types.convert as cvt
#
# Place all imports before here.
#===========================================================================

#===========================================================================
class MySubSubSubStyle( S.types.SubStyle ):
   """A Sub-Classed Style."""

   prop = S.types.StyleProperty( default = 0.0, validator = \
                                 cvt.Converter( cvt.toType, float,
                                                allowNone=True ) )

   value = S.types.StyleProperty( default = None )

   #-----------------------------------------------------------------------
   def __init__( self, **kwargs ):
      S.types.SubStyle.__init__( self, **kwargs )

#===========================================================================
class MySubSubStyle( S.types.SubStyle ):
   """A Sub-Classed Style."""

   prop = S.types.SubStyle( MySubSubSubStyle )

   value = S.types.StyleProperty( default = None )

   #-----------------------------------------------------------------------
   def __init__( self, **kwargs ):
      S.types.SubStyle.__init__( self, **kwargs )

#===========================================================================
class MySubStyle( S.types.SubStyle ):
   """A Sub-Classed Style."""

   prop = S.types.StyleProperty( default = 0.0, validator = \
                                 cvt.Converter( cvt.toType, float,
                                                allowNone=True ) )
   myProp = S.types.property.Alias( 'prop', isProperty = True )

   value = S.types.StyleProperty( default = None )

   sstyle = S.types.SubStyle( MySubSubStyle )

   #-----------------------------------------------------------------------
   def __init__( self, **kwargs ):
      SubStyle.__init__( self, **kwargs )

#===========================================================================
class TestSubStyle( unittest.TestCase ):
   """Test the SubStyle class."""

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
   def testBasic( self ):
      """A basic test of SubStyle."""

      # Check the available property names
      expected = [ 'myProp', 'prop', 'sstyle', 'value' ]
      actual = MySubStyle.propertyNames()
      self.assertEqual( expected, actual, msg = "Incorrect property names." )

      # Default initialize
      s1 = MySubStyle()
      self.assertEqual( True, s1.hasAnySet(),
               msg = "Reporting values set, when none are set." )

      self.assertEqual( 0.0, MySubStyle.prop.default,
               msg = "Class default value for 'prop' wrong" )
      self.assertEqual( None, MySubStyle.value.default,
               msg = "Class default value for 'value' wrong" )

      self.assertEqual( 0.0, s1.prop,
               msg = "Instance default value for 's1.prop' wrong" )
      self.assertEqual( None, s1.value,
               msg = "Instance default value for 's1.value' wrong" )

      # Change the local copy
      s1.prop = 1
      s1.value = "abc"

      self.assertEqual( 0.0, MySubStyle.prop.default,
               msg = "1) Class default value for 'prop' changed" )
      self.assertEqual( None, MySubStyle.value.default,
               msg = "1) Class default value for 'value' changed" )

      self.assertEqual( 1.0, s1.prop,
               msg = "1) Instance local value for 's1.prop' wrong" )
      self.assertEqual( 'abc', s1.value,
               msg = "1) Instance local value for 's1.value' wrong" )

      # Make a new instance
      s2 = MySubStyle( prop = 9.0, value = 'xyz' )
      setattr( s2, 'sstyle.value', 'ijk' )
      setattr( s2, 'sstyle.prop.value', '123' )

      self.assertEqual( 0.0, MySubStyle.prop.default,
               msg = "2) Class default value for 'prop' changed" )
      self.assertEqual( None, MySubStyle.value.default,
               msg = "2) Class default value for 'value' changed" )

      self.assertEqual( 1.0, s1.prop,
               msg = "2) Instance local value for 's1.prop' wrong" )
      self.assertEqual( 'abc', s1.value,
               msg = "2) Instance local value for 's1.value' wrong" )

      self.assertEqual( 9.0, s2.prop,
               msg = "Instance local value for 's2.prop' wrong" )
      self.assertEqual( 'xyz', s2.value,
               msg = "Instance local value for 's2.value' wrong" )

      # Test update
      s1.update( None )
      self.assertEqual( 1.0, s1.prop,
               msg = "3) Instance local value for 's1.prop' wrong" )
      self.assertEqual( 'abc', s1.value,
               msg = "3) Instance local value for 's1.value' wrong" )


      s1.update( s2 )
      self.assertEqual( 9.0, s1.prop,
               msg = "4) Instance local value for 's1.prop' wrong" )
      self.assertEqual( 'xyz', s1.value,
               msg = "4) Instance local value for 's1.value' wrong" )

      self.assertEqual( 9.0, s2.prop,
               msg = "4) Instance local value for 's2.prop' wrong" )
      self.assertEqual( 'xyz', s2.value,
               msg = "4) Instance local value for 's2.value' wrong" )

      s3 = s1.copy()
      self.assertEqual( 9.0, s1.prop,
               msg = "5) Instance local value for 's1.prop' wrong" )
      self.assertEqual( 'xyz', s1.value,
               msg = "5) Instance local value for 's1.value' wrong" )

      self.assertEqual( 9.0, s2.prop,
               msg = "5) Instance local value for 's2.prop' wrong" )
      self.assertEqual( 'xyz', s2.value,
               msg = "5) Instance local value for 's2.value' wrong" )

      self.assertEqual( 9.0, s3.prop,
               msg = "5) Instance local value for 's3.prop' wrong" )
      self.assertEqual( 'xyz', s3.value,
               msg = "5) Instance local value for 's3.value' wrong" )

      # Test kwargs
      kw = s2.sstyle.prop.kwargs()
      expected = { 'value' : '123' }
      self.assertEqual( expected, kw, msg = "Incorrect keyword-arguments." )


      txt = """MySubStyle:
   * myProp = 9.0
   * prop = 9.0
   * sstyle =  MySubSubStyle:
      * prop =  MySubSubSubStyle:
         * value = 123
      * value = ijk
   * value = xyz"""
      self.assertEqual( txt, str(s2), msg = "Incorrect string representation." )

      # Error condition
      msg = "Failed to raise on invalid keyword."
      self.assertRaises( Exception, MySubStyle, garbage='bad', msg = msg )

      try:
         s2.badProperty = "garbage"
      except:
         pass
      else:
         msg = "Failed to raise on setting of invalid property."
         self.fail( msg )

      # Test property Type
      self.assertEqual( StyleProperty, s1.getPropertyType( 'prop' ),
               msg = "Invalid type for property 'prop'" )

      self.assertEqual( StyleProperty, s1.getPropertyType( 'myProp' ),
               msg = "Invalid type for alias property 'myProp'" )

   #-----------------------------------------------------------------------
   def testGetValue( self ):
      """Test the getValue method."""

      # Test getValue
      s1 = MySubStyle( prop = 2.5 )
      defaults = { 'prop' : 1.5, 'value' : 'rst' }

      msg = "Wrong value for getValue('prop') with no defaults and no kwargs."
      self.assertEqual( 2.5, s1.getValue( 'prop' ), msg = msg )
      msg = "Wrong value for getValue('value') with no defaults and no kwargs."
      self.assertEqual( None, s1.getValue( 'value' ), msg = msg )

      msg = "Wrong value for getValue('prop') with defaults and no kwargs."
      self.assertEqual( 2.5, s1.getValue( 'prop', defaults ), msg = msg )
      msg = "Wrong value for getValue('value') with defaults and no kwargs."
      self.assertEqual( 'rst', s1.getValue( 'value', defaults ), msg = msg )

      msg = "Wrong value for getValue('prop') with no defaults and kwargs."
      self.assertEqual( 4.5, s1.getValue( 'prop', prop=4.5 ), msg = msg )
      msg = "Wrong value for getValue('value') with no defaults and kwargs."
      self.assertEqual( 'ijk', s1.getValue( 'value', value='ijk' ), msg = msg )

      msg = "Wrong value for getValue('prop') with defaults and kwargs."
      self.assertEqual( 4.5, s1.getValue( 'prop', defaults, prop=4.5 ), msg = msg )
      msg = "Wrong value for getValue('value') with defaults and kwargs."
      self.assertEqual( 'ijk', s1.getValue( 'value', defaults, value='ijk' ), msg = msg )

      # Test aliasing
      s1.prop = None
      self.assertEqual( 5.0, s1.getValue( 'prop', myProp = 5, prop = None ),
               msg = "Failed to retrieve aliased value from kwargs." )
      self.assertEqual( 7.0, s1.getValue( 'prop', { 'myProp' : 7 } ),
               msg = "Failed to retrieve aliased value from defaults." )

   #-----------------------------------------------------------------------
   def testNestedSubStyle( self ):
      """Test for nested sub-style functionality."""

      # Test getValue
      s1 = MySubStyle( value = MySubStyle( prop = 1.1 ), prop = 1 )
      s2 = MySubStyle( value = MySubStyle( prop = 2.1 ), prop = 2 )
      s3 = MySubStyle( value = MySubStyle( prop = None,
                                           value = MySubStyle( prop = None ) ),
                       prop = 3 )
      s4 = MySubStyle( value = 5, prop = 1 )

      s1.update( s2 )

      self.assertEqual( 2, s1.prop, msg = "Incorrect value for 's1.prop'" )
      self.assertEqual( 2.1, s1.value.prop, msg = "Incorrect value for 's1.value.prop'" )

      self.assertEqual( 2.1, s1.getValue( 'value.prop' ),
               msg = "Incorrect value for s1.getValue('value.prop')" )


      txt = """MySubStyle:
   * myProp = 2.0
   * prop = 2.0
   * sstyle =  MySubSubStyle:
      * prop =  MySubSubSubStyle:
   * value =  MySubStyle:
      * myProp = 2.1
      * prop = 2.1
      * sstyle =  MySubSubStyle:
         * prop =  MySubSubSubStyle:"""
      self.assertEqual( txt, str(s2), msg = "Incorrect string representation (s2)." )

      self.assertEqual( True, s3.hasAnySet(), msg = "Wrong value for 'hasAnySet'" )

      txt = """MySubStyle:
   * myProp = 3.0
   * prop = 3.0
   * sstyle =  MySubSubStyle:
      * prop =  MySubSubSubStyle:
   * value =  MySubStyle:
      * prop = None
      * sstyle =  MySubSubStyle:
         * prop =  MySubSubSubStyle:
      * value =  MySubStyle:
         * prop = None
         * sstyle =  MySubSubStyle:
            * prop =  MySubSubSubStyle:"""
      s3.value.prop = None
      self.assertEqual( txt, str(s3), msg = "Incorrect string representation (s3)." )

      kw = s4.kwargs( recursive = True )
      expected = { 'value' : 5, 'sstyle' : { 'prop': {}},
                   'prop' : 1.0, 'myProp' : 1.0 }
      self.assertEqual( expected, kw, msg = "Incorrect nested keyword-arguments." )

