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

"The ToEnum unit test."

__version__ = "$Revision: #1 $"

#===========================================================================
# Reqmtypes.ed imports.  Do not modify these.
import unittest

#===========================================================================
# Place all imports after here.
#
import os
import mplStyle.types.convert as cvt
#
# Place all imports before here.
#===========================================================================

#===========================================================================
class TesttoEnum( unittest.TestCase ):
   """ToEnum module."""

   #-----------------------------------------------------------------------
   def setUp( self ):
      """This method is called before any tests are run."""
      
      # You may place initialization code here.


   #-----------------------------------------------------------------------
   def tearDown( self ):
      """This method is called after all tests are run."""
      pass
   #=======================================================================
   # Add tests methods below.
   # Any method whose name begins with 'test' will be run by the framework.
   #=======================================================================
   def testToEnum( self ):
      """Test the ToEnum converter."""
      converter = cvt.toEnum
      enums = { True : "TRUE", False : "FALSE" }

      v = converter( True, enums )
      self.assertEqual( "TRUE", v, "Incorrect conversion of True." )
      
      v = converter( False, enums )
      self.assertEqual( "FALSE", v, "Incorrect conversion of False." )

      v = converter( "TRUE", enums )
      self.assertEqual( "TRUE", v, "Incorrect value of 'TRUE'." )

      v = converter( "True", enums )
      self.assertEqual( "TRUE", v, "Incorrect string conversion of 'TRUE'." )

      self.assertRaises( Exception, converter, "ABC", enums, name='value',
                   msg="Invalid string argument should be an error." )
      self.assertRaises( Exception, converter, 123, enums, name='value',
                   msg="Invalid argument should be an error." )
      self.assertRaises( Exception, converter, None, enums, name='value',
                   msg="None argument should be an error." )

      # Test string case insensitive
      enums= { 'One' : 1, 'Two' : 2 }

      v = converter( 'ONE', enums, caseInsens=True )
      self.assertEqual( 1, v, "Incorrect conversion of 'ONE'." )
      
      v = converter( 'one', enums, caseInsens=True )
      self.assertEqual( 1, v, "Incorrect conversion of 'one'." )
      
      v = converter( 'TWO', enums, caseInsens=True )
      self.assertEqual( 2, v, "Incorrect conversion of 'TWO'." )

      v = converter( 'two', enums, caseInsens=True )
      self.assertEqual( 2, v, "Incorrect conversion of 'two'." )

   #-----------------------------------------------------------------------
   def testToNone( self ):
      """Test the converter w/ None."""
      converter = cvt.toEnum
      enums = { True : "TRUE", False : "FALSE" }

      right = None
      v = converter( None, enums, allowNone=True )
      self.assertEqual( right, v, "Incorrect conversion of None." )

#=======================================================================
