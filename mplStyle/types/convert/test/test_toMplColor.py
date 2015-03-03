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

"The ToMplColor unit test."

__version__ = "$Revision: #1 $"

#===========================================================================
# Reqmtypes.ed imports.  Do not modify these.
import unittest

#===========================================================================
# Place all imports after here.
#
import os
import mplStyle.types.convert as cvt

from PyQt4 import QtGui
#
# Place all imports before here.
#===========================================================================

#===========================================================================
class TesttoMplColor( unittest.TestCase ):
   """ToMplColor module."""

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
   def testToMplColor( self ):
      """Test the ToMplColor converter."""
      converter = cvt.toMplColor

      t = converter( 'red' )
      self.assertEqual( '#FF0000', t, "Incorrect conversion of a string." )

      t = converter( QtGui.QColor( 0, 255, 0 ) )
      self.assertEqual( '#00FF00', t, "Incorrect conversion of a QColor." )

      t = converter( 'None' )
      self.assertEqual( 'none', t, "Incorrect conversion of a GlColor." )

      t = converter( (1.0, 0.0, 0.0, 1.0), )
      self.assertEqual( '#FF0000', t, "Incorrect conversion of a float tuple." )

      t = converter( [0, 255, 0, 1], )
      self.assertEqual( '#00FF00', t, "Incorrect conversion of an int list." )

      t = converter( 'r' )
      self.assertEqual( '#FF0000', t, "Incorrect conversion of 'r'." )

      t = converter( 'g' )
      self.assertEqual( '#008000', t, "Incorrect conversion of 'g'." )

      t = converter( 'b' )
      self.assertEqual( '#0000FF', t, "Incorrect conversion of 'b'." )

      t = converter( 'k' )
      self.assertEqual( '#000000', t, "Incorrect conversion of 'k'." )

      t = converter( 'w' )
      self.assertEqual( '#FFFFFF', t, "Incorrect conversion of 'w'." )

      self.assertRaises( Exception, converter, None, name='value',
                   msg="None argument should be an error." )
      self.assertRaises( Exception, converter, "foo bar", name='value',
                   msg="String argument should be an error." )

      # Try w/ allowNone
      t = converter( None, allowNone=True )
      self.assertEqual( None, t, "Incorrect conversion of None." )

#=======================================================================
