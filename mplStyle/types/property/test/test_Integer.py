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

"The Integer unit test."

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
class MySubStyle( S.SubStyle ):
   """A Sub-Classed Style."""

   prop = S.property.Integer( 0, 10, default = None )

   #-----------------------------------------------------------------------

#===========================================================================
class TestInteger( unittest.TestCase ):
   """Integer module."""

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
   def testInteger( self ):
      """Test Integer style property."""
      # Default initialize
      style = MySubStyle()
      self.assertEqual( None, MySubStyle.prop.default,
               msg = "Class default value for 'prop' wrong" )
      self.assertEqual( None, style.prop,
               msg = "Instance default value for 'style.prop' wrong" )

      # Change the local copy
      style.prop = 5
      self.assertEqual( None, MySubStyle.prop.default,
               msg = "1) Class default value for 'prop' changed" )
      self.assertEqual( 5, style.prop,
               msg = "1) Instance value for 'style.prop' wrong" )

      # Make a new instance
      newStyle = MySubStyle( prop = 3 )
      self.assertEqual( None, MySubStyle.prop.default,
               msg = "2) Class default value for 'prop' changed" )
      self.assertEqual( 5, style.prop,
               msg = "2) Instance value for 'style.prop' wrong" )
      self.assertEqual( 3, newStyle.prop,
               msg = "2) Instance value for 'newStyle.prop' wrong" )

      # Check converter
      newStyle.prop = "9"
      self.assertEqual( None, MySubStyle.prop.default,
               msg = "3) Class default value for 'prop' changed" )
      self.assertEqual( 5, style.prop,
               msg = "3) Instance value for 'style.prop' wrong" )
      self.assertEqual( 9, newStyle.prop,
               msg = "3) Instance value for 'newStyle.prop' wrong" )

      # Error condition
      msg = "Failed to raise on invalid value."
      self.assertRaises( Exception, MySubStyle, prop='bad', msg = msg )

      msg = "Failed to raise on low value."
      self.assertRaises( Exception, MySubStyle, prop=-1, msg = msg )

      msg = "Failed to raise on high value."
      self.assertRaises( Exception, MySubStyle, prop=100, msg = msg )

      # String check
      s = 'Integer: MySubStyle.prop'
      self.assertEqual( s, str(MySubStyle.prop), msg = "Incorrect string value" )

#=======================================================================

