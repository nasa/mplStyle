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

"The ToType unit test."

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
class TesttoType( unittest.TestCase ):
   """ToType module."""

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
   def testToBool( self ):
      """Boolean values."""
      cvtType = bool
      converter = cvt.toType

      self.assertRaises( Exception, converter, None, cvtType, name='value',
                   msg = "None when allowNone=false didn't throw." )

      t = converter( 1, cvtType )
      self.assertEqual( True, t, "Incorrect conversion of 1 to a bool." )

      t = converter( 0, cvtType )
      self.assertEqual( False, t, "Incorrect conversion of 0 to a bool." )

      t = converter( 1.1234, cvtType )
      self.assertEqual( True, t, "Incorrect conversion of a float to a bool." )

      t = converter( "1.1234", cvtType )
      self.assertEqual( True, t,
               "Incorrect conversion of a bool represented by a string." )

   #-----------------------------------------------------------------------
   def testToType( self ):
      """Floating point."""
      cvtType = float
      converter = cvt.toType

      self.assertRaises( Exception, converter, None, cvtType, name='value',
                   msg = "None when allowNone=false didn't throw." )

      t = converter( 1, cvtType )
      self.assertEqual( 1.0, t, "Incorrect conversion of an integer." )

      t = converter( 1.1234, cvtType )
      self.assertEqual( 1.1234, t, "Incorrect conversion of a float." )

      t = converter( "1.1234", cvtType )
      self.assertEqual( 1.1234, t,
               "Incorrect conversion of a float represented by a string." )

      self.assertRaises( Exception, converter, "foo bar", cvtType, name='value',
                   msg="String argument should be an error." )
      self.assertRaises( Exception, converter, [ 1, 2, 3 ], cvtType,
                         name='value', msg="List argument should be an error." )

   #-----------------------------------------------------------------------
   def testToComplex( self ):
      """Complex point."""
      cvtType = complex
      converter = cvt.toType

      self.assertRaises( Exception, converter, None, cvtType, name='value',
                   msg = "None when allowNone=false didn't throw." )

      t = converter( 1, cvtType )
      self.assertEqual( complex( 1.0 ), t,
                        msg="Incorrect conversion of an integer." )

      t = converter( 1.1234, cvtType )
      self.assertEqual( complex( 1.1234 ), t,
                        msg="Incorrect conversion of a float." )

      t = converter( "1.1234", cvtType )
      self.assertEqual( complex( 1.1234 ), t,
               "Incorrect conversion of a float represented by a string." )

      t = converter( complex( 1, 2 ), cvtType )
      self.assertEqual( complex( 1, 2 ), t,
               "Incorrect conversion of a float represented by a string." )

      self.assertRaises( Exception, converter, "foo bar", cvtType, name='value',
                   msg="String argument should be an error." )
      self.assertRaises( Exception, converter, [ 1, 2, 3 ], cvtType,
                         name='value', msg="List argument should be an error." )


   #-----------------------------------------------------------------------
   def testNone( self ):
      """Allow none."""
      # Check w/ allowNone
      cvtType = float
      converter = cvt.toType
      right = None
      t = converter( right, cvtType, allowNone=True )
      self.assertEqual( right, t, "Incorrect conversion of None." )

#=======================================================================
