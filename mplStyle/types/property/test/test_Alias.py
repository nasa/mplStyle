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

"The Alias unit test."

__version__ = "$Revision: #1 $"

#===========================================================================
# Reqmtypes.ed imports.  Do not modify these.
import unittest


#===========================================================================
# Place all imports after here.
#
import os

import mplStyle.types as S
#
# Place all imports before here.
#===========================================================================

#===========================================================================
class MySubSubStyle( S.SubStyle ):
   """A Sub-Classed Style."""

   value = S.property.Float( min = 0.0, max = 10.0 )

   #-----------------------------------------------------------------------

#===========================================================================
class MySubStyle( S.SubStyle ):
   """A Sub-Classed Style."""

   # Test a member variable
   prop = S.property.Alias( '_subValue' )
   ssprop = S.property.Alias( '_subSubValue.value' )

   # Test a property of this class
   otherProp = S.property.Float( min = 0.0, max = 10.0 )
   prop2 = S.property.Alias( 'otherProp', isProperty=True )

   # Test a nested property
   subProp = S.property.SubStyle( MySubSubStyle )
   prop3 = S.property.Alias( 'subProp.value', isProperty=True )

   # Test a class attribute
   clsProp = None
   prop4 = S.property.Alias( 'clsProp' )

   # Test a non-existant property
   badProp = S.property.Alias( 'bad.property' )

   #-----------------------------------------------------------------------
   def __init__( self, **kwargs ):
      # Must define *before* SubStyle CTOR since SubStyle CTOR might init the
      # Aliased value, which will need to resolve this value
      self._subValue = S.property.Float( min = 0.0, max = 10.0 )
      self._subSubValue = MySubSubStyle()

      S.SubStyle.__init__( self, **kwargs )

   #-----------------------------------------------------------------------

#===========================================================================
class MyBadSubStyle( S.SubStyle ):
   """A Sub-Classed Style."""

   # Test a member variable
   prop = S.property.Alias( 'Bad' )

   #-----------------------------------------------------------------------

#===========================================================================
class TestAlias( unittest.TestCase ):
   """Alias module."""

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
   #=======================================================================
   def testAlias( self ):
      """Test Alias style property."""
      # Default initialize
      style = MySubStyle()
      self.assertEqual( None, MySubStyle.prop.default,
               msg = "Class default value for 'prop' wrong" )
      self.assertEqual( None, style.prop,
               msg = "Instance default value for 'style.prop' wrong" )
      self.assertEqual( None, style.otherProp,
               msg = "Instance default value for 'style.otherProp' wrong" )
      self.assertEqual( None, style.prop2,
               msg = "Instance default value for 'style.prop2' wrong" )
      self.assertEqual( None, style.subProp.value,
               msg = "Instance default value for 'style.subProp.value' wrong" )
      self.assertEqual( None, style.prop3,
               msg = "Instance default value for 'style.prop3' wrong" )
      self.assertEqual( None, style.prop4,
               msg = "Instance default value for 'style.prop4' wrong" )

      # Change the local copy
      style.prop = 5.0
      self.assertEqual( None, MySubStyle.prop.default,
               msg = "1) Class default value for 'prop' changed" )
      self.assertEqual( 5.0, style.prop,
               msg = "1) Instance value for 'style.prop' wrong" )

      style.otherProp = 5.5
      self.assertEqual( 5.5, style.otherProp,
               msg = "1) Instance value for 'style.otherProp' wrong" )
      self.assertEqual( 5.5, style.prop2,
               msg = "1) Instance value for 'style.prop2' wrong" )

      style.subProp.value = 5.75
      self.assertEqual( 5.75, style.subProp.value,
               msg = "1) Instance value for 'style.subProp.value' wrong" )
      self.assertEqual( 5.75, style.prop3,
               msg = "1) Instance value for 'style.prop3' wrong" )

      style.prop3 = 5.25
      self.assertEqual( 5.25, style.subProp.value,
               msg = "1) Instance value for 'style.subProp.value' wrong" )
      self.assertEqual( 5.25, style.prop3,
               msg = "1) Instance value for 'style.prop3' wrong" )

      MySubStyle.clsProp = 'abc'
      self.assertEqual( 'abc', style.prop4,
               msg = "1) Instance value for 'style.prop4' wrong" )


      # Make a new instance
      newStyle = MySubStyle( prop = 3.0, prop2 = 3.5, prop3 = 3.75 )
      self.assertEqual( None, MySubStyle.prop.default,
               msg = "2) Class default value for 'prop' changed" )
      self.assertEqual( 5.0, style.prop,
               msg = "2) Instance value for 'style.prop' wrong" )
      self.assertEqual( 3.0, newStyle.prop,
               msg = "2) Instance value for 'newStyle.prop' wrong" )

      self.assertEqual( 5.5, style.otherProp,
               msg = "2) Instance value for 'style.otherProp' wrong" )
      self.assertEqual( 5.5, style.prop2,
               msg = "2) Instance value for 'style.prop2' wrong" )
      self.assertEqual( 3.5, newStyle.otherProp,
               msg = "2) Instance value for 'newStyle.otherProp' wrong" )
      self.assertEqual( 3.5, newStyle.prop2,
               msg = "2) Instance value for 'newStyle.prop2' wrong" )

      self.assertEqual( 5.25, style.subProp.value,
               msg = "2) Instance value for 'style.subProp.value' wrong" )
      self.assertEqual( 5.25, style.prop3,
               msg = "2) Instance value for 'style.prop3' wrong" )
      self.assertEqual( 3.75, newStyle.subProp.value,
               msg = "2) Instance value for 'newStyle.subProp.value' wrong" )
      self.assertEqual( 3.75, newStyle.prop3,
               msg = "2) Instance value for 'newStyle.prop3' wrong" )
      self.assertEqual( 'abc', newStyle.prop4,
               msg = "2) Instance value for 'style.prop4' wrong" )

      # Check error case
      try:
         invalid = MyBadStyle( prop = 0 )
      except:
         pass
      else:
         self.fail( "Invalid property failed to throw an exception." )

      # String check
      s = 'Float: MySubStyle.prop'
      self.assertEqual( s, str(MySubStyle.prop),
               msg = "Incorrect string value for 'prop'" )

      s = 'Float: MySubStyle.otherProp'
      self.assertEqual( s, str(MySubStyle.otherProp),
               msg = "Incorrect string value for 'otherProp'" )

      s = 'Float: MySubStyle.prop2'
      self.assertEqual( s, str(MySubStyle.prop2),
               msg = "Incorrect string value for 'prop2'" )

      s = 'str: MySubStyle.prop4'
      self.assertEqual( s, str(MySubStyle.prop4),
               msg = "Incorrect string value for 'prop4'" )

      prop = S.property.Alias( 'something' )
      s = 'Unknown'
      self.assertEqual( s, str(prop),
               msg = "Incorrect string value for 'free' property." )

      prop._name = "FreeProp"
      s = 'Unknown: FreeProp'
      self.assertEqual( s, str(prop),
               msg = "Incorrect string value for 'free' property." )

      # Check bad alias
      try:
         s = str( style.badProp )
      except:
         pass
      else:
         self.fail( "Failed to throw on invalid alias." )

      self.assertEqual( S.property.Float, style.getPropertyType( 'prop2' ),
               msg = "Invalid type for aliased property in style" )

      self.assertEqual( S.property.Float, style.getPropertyType( 'prop' ),
               msg = "Invalid type for aliased member data in style" )

      self.assertEqual( S.property.Float, style.getPropertyType( 'ssprop' ),
               msg = "Invalid type for aliased member sub-data in style" )

      self.assertEqual( S.property.Float, MySubStyle.prop2.getType(),
               msg = "Invalid type for aliased property" )

      self.assertEqual( None, MySubStyle.prop.getType(),
               msg = "Invalid type for aliased member data" )

#=======================================================================

