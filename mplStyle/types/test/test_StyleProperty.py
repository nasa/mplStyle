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

"Unit test for the StyleProperty class."

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
def floatValidator( v ):
   return float( v )

#===========================================================================
class MySubStyle( S.types.SubStyle ):
   """A Sub-Classed Style."""

   prop = S.types.StyleProperty( default = 0.0, validator = float )

   time = S.types.StyleProperty( default = 1.2, 
                                 validator = floatValidator )

   value = S.types.StyleProperty( default = None )

   #-----------------------------------------------------------------------

#===========================================================================
class TestSubProperty( unittest.TestCase ):
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
      """A basic test of StyleProperty."""

      s1 = MySubStyle()

      try:
         s1.prop = "abc"
      except:
         pass
      else:
         self.fail( "Did not raise exception on invalid float." )

      try:
         s1.time = "abc"
      except:
         pass
      else:
         self.fail( "Did not raise exception on invalid Epoch." )

      s = "StyleProperty: MySubStyle.prop"
      self.assertEqual( s, str(MySubStyle.prop),
               msg = "Invalid string representation #1" )

      prop1 = S.types.StyleProperty( default = 0.0, validator = float )
      prop1._name = 'FreeProp'
      s = "StyleProperty: FreeProp"
      self.assertEqual( s, str(prop1),
               msg = "Invalid string representation #2" )

      prop2 = S.types.StyleProperty( default = 0.0, validator = int )
      s = "StyleProperty"
      self.assertEqual( s, str(prop2),
               msg = "Invalid string representation #3" )

      self.assertEqual( 2, prop2( 2.1 ), msg = "Failed to validate." )

