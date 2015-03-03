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

"The SubStyle unit test."

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

   prop = S.property.SubStyle( MySubSubStyle )

   #-----------------------------------------------------------------------

#===========================================================================
class TestSubStyle( unittest.TestCase ):
   """SubStyle module."""

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
   def testSubStyle( self ):
      """Test SubStyle style property."""
      # Default initialize
      style = MySubStyle()
      self.assertEqual( None, MySubSubStyle.value.default,
               msg = "Class default value for 'value' wrong" )
      self.assertEqual( None, MySubStyle.prop.default.value,
               msg = "Class default value for 'prop.value' wrong" )
      self.assertEqual( None, style.prop.value,
               msg = "Instance default value for 'style.prop' wrong" )

      # Change the local copy
      style.prop.value = 5.0
      self.assertEqual( None, MySubSubStyle.value.default,
               msg = "1) Class default value for 'value' changed" )
      self.assertEqual( 5.0, style.prop.value,
               msg = "1) Instance value for 'style.prop.value' wrong" )

      # Make a new instance
      newStyle = MySubStyle( prop = { 'value': 3.0 } )
      self.assertEqual( None, MySubSubStyle.value.default,
               msg = "2) Class default value for 'value' changed" )
      self.assertEqual( 5.0, style.prop.value,
               msg = "2) Instance value for 'style.prop.value' wrong" )
      self.assertEqual( 3.0, newStyle.prop.value,
               msg = "2) Instance value for 'newStyle.prop.value' wrong" )

      # Check Data assignment
      newStyle.prop = S.Data( value = 5.0 ) # TODO: why does this fail?
      self.assertEqual( 5.0, newStyle.prop.value,
               msg = "3) Instance value for 'newStyle.prop.value' wrong" )

      # String check
      s = "MySubSubStyle: MySubStyle.prop"
      self.assertEqual( s, str(MySubStyle.prop),
                        msg = "Incorrect string value" )

      prop = S.property.SubStyle( MySubSubStyle )
      s = "MySubSubStyle"
      self.assertEqual( s, str(prop),
               msg = "Incorrect standalone string value" )

      prop._name = "prop"
      s = "MySubSubStyle: prop"
      self.assertEqual( s, str(prop),
               msg = "Incorrect standalone string value" )

#=======================================================================

