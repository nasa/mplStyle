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

"The ToFileList unit test."

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
class TesttoFileList( unittest.TestCase ):
   """ToFileList module."""

   #-----------------------------------------------------------------------
   def setUp( self ):
      """This method is called before any tests are run."""
      
      # You may place initialization code here.


   #-----------------------------------------------------------------------
   def tearDown( self ):
      """This method is called after all tests are run."""
      
      # You may place finalization code here.
      if os.path.exists( "convert-temp1.txt" ):
         os.remove( "convert-temp1.txt" )
      if os.path.exists( "convert-temp2.txt" ):
         os.remove( "convert-temp2.txt" )
      if os.path.exists( "convert-temp3.txt" ):
         os.remove( "convert-temp3.txt" )

   #=======================================================================
   # Add tests methods below.
   # Any method whose name begins with 'test' will be run by the framework.
   #=======================================================================
   def testNew( self ):
      """For new files."""
      converter = cvt.toFileList

      l = [ "a.boa",
            "b.boa",
            "c.boa" ]
      v = converter( l, mode = "New" )
      self.assertEqual( l, v, "Incorrect conversion of basic inputs." )

      l = [ "$HOME/a.boa",
            "$HOME/b.boa",
            "$HOME/c.boa" ]

      h = os.environ[ "HOME" ]
      r = [ "%s/a.boa" % h,
            "%s/b.boa" % h,
            "%s/c.boa" % h ]
      v = converter( l, mode = "New" )
      self.assertEqual( r, v, "Incorrect conversion of env variables." )

   #-----------------------------------------------------------------------
   def testExist( self ):
      """For existing files."""
      open( "convert-temp1.txt", "w" ).write( "asdf" )
      open( "convert-temp2.txt", "w" ).write( "asdf" )
      open( "convert-temp3.txt", "w" ).write( "asdf" )
      
      l = [ "./convert-*.txt" ]
      r = [ "./convert-temp1.txt",
            "./convert-temp2.txt",
            "./convert-temp3.txt", ]

      converter = cvt.toFileList
      v = converter( l, mode = "Exist" )
      self.assertEqual( r, v, "Incorrect conversion of wildcards variables." )

      l = [ "convert-temp1.txt" ]
      r = l
      v = converter( l, mode = "Exist" )
      self.assertEqual( r, v, "Incorrect conversion of simple file." )

      self.assertRaises( Exception, converter, "xxx.txt", mode = "Exist",
                         name='value', msg = "Input not a list didn't error." )

      self.assertRaises( Exception, converter, [ "xxx.txt" ], mode = "Exist",
                         name='value', msg = "Invalid input file didn't error." )

      self.assertRaises( Exception, converter, 123, mode = "Exist",
                         name='value', msg = "Input not a list didn't error." )

   #-----------------------------------------------------------------------
   def testNone( self ):
      """Allow none."""
      converter = cvt.toFileList
      v = converter( None, mode="New", allowNone=True )
      self.assertEqual( None, v, "Incorrect conversion of none." )

      self.assertRaises( Exception, cvt.toFileList, "invalid", mode = "XXX",
                   msg = "Invalid mode didn't error." )

#=======================================================================
