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

"The ToListOf unit test."

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
class TesttoListOf( unittest.TestCase ):
   """ToListOf module."""

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
   def testToListOf( self ):
      """Test the ToListOf converter."""
      cvtType = cvt.Converter( cvt.toType, float ) 
      converter = cvt.toListOf

      l1 = [ "123", 1234.0, 5 ]
      right = map( float, l1 )
             
      v = converter( l1, cvtType )
      self.assertEqual( right, v, "Incorrect conversion of list." )
      
      v = converter( right, cvtType )
      self.assertEqual( right, v, "Incorrect conversion of floats." )

      v = converter( tuple( l1 ), cvtType )
      self.assertEqual( right, v, "Incorrect conversion of tuples." )
      
      self.assertRaises( Exception, converter, [ "foo bar" ], cvtType,
                         name='value',
                   msg="Invalid string argument should be an error." )
      self.assertRaises( Exception, converter, "foo bar", cvtType, name='value',
                   msg="Invalid non-list argument should be an error." )

   #-----------------------------------------------------------------------
   def testAllowOne( self ):
      """Single item promotion"""
      cvtType = cvt.Converter( cvt.toType, float )
      converter = cvt.toListOf

      l1 = [ "123" ]
      right = map( float, l1 )
             
      v = converter( l1[0], cvtType, allowOne=True )
      self.assertEqual( right, v, "Incorrect conversion of single item." )
      
   #-----------------------------------------------------------------------
   def testAllowNone( self ):
      """None item promotion"""
      cvtType = cvt.Converter( cvt.toType, float ) 
      converter = cvt.toListOf

      v = converter( None, cvtType, allowNone=True )
      self.assertEqual( None, v, "Incorrect conversion of none item." )
      
#===========================================================================
