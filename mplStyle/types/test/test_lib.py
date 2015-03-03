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

"Unit test for the lib utility functions."

__version__ = "$Revision: #1 $"

#===========================================================================
# Required imports.  Do not modify these.

import unittest

#===========================================================================
# Place all imports after here.
#
import os
import mplStyle as S

#
# Place all imports before here.
#===========================================================================

#===========================================================================
class MySubStyle( S.types.SubStyle ):
   """A Sub-Classed Style."""

   prop = S.types.StyleProperty( default = 0.0, validator = float )

   value = S.types.StyleProperty( default = None )

   #-----------------------------------------------------------------------

#===========================================================================
class Testlib( unittest.TestCase ):
   """Test the SubStyle class."""

   #-----------------------------------------------------------------------
   def setUp( self ):
      """This method is called before any tests are run."""

      # Save the existing STYLEPATH (if there is one)
      self.stylepath = os.environ.get( "STYLEPATH", None )

   #-----------------------------------------------------------------------
   def tearDown( self ):
      """This method is called after all tests are run."""
      
      # You may place finalization code here.
      if self.stylepath is not None:
         os.environ[ "STYLEPATH" ] = self.stylepath


   #=======================================================================
   # Add tests methods below.
   # Any method whose name begins with 'test' will be run by the framework.

   #-----------------------------------------------------------------------
   def testResolveDefaults( self ):
      """A basic test of 'resolveDefaults' utility function."""

      s1 = MySubStyle( value = MySubStyle( prop=1.1 ) )
      s2 = MySubStyle( value = MySubStyle( prop=2.1, value={1: 'a', 2:'b'} ),
                       prop=2 )
      s3 = MySubStyle( prop = 3, value = \
                       MySubStyle( prop=3.1, value = \
                          MySubStyle( prop = 3.2, value = 'abc' ) ) )

      kw1 = s1.kwargs( recursive=True )
      kw2 = s2.kwargs( recursive=True )
      kw3 = s3.kwargs( recursive=False )


      expected = { 'value': { 'prop': 1.1 } }
      actual = S.types.lib.resolveDefaults( kw1 )
      msg = "Invalid results of resolveDefaults with no subNames and no kwargs."
      self.assertEqual( expected, actual, msg = msg )

      expected = { 'value': { 'prop': 1.1 }, 'prop': 9.0 }
      actual = S.types.lib.resolveDefaults( kw1, prop=9, value = None )
      msg = "Invalid results of resolveDefaults with no subNames and kwargs."
      self.assertEqual( expected, actual, msg = msg )

      expected = { 'value': { 'prop': 1.1 }, 'prop': 1.1 }
      actual = S.types.lib.resolveDefaults( kw1, ['value'] )
      msg = "Invalid results of resolveDefaults with subNames and no kwargs."
      self.assertEqual( expected, actual, msg = msg )

      expected = { 'value': { 'prop': 1.1 }, 'prop': 1.1 }
      actual = S.types.lib.resolveDefaults( kw1, ['value'], prop=9.0 )
      msg = "Invalid results of resolveDefaults with subNames and kwargs."
      self.assertEqual( expected, actual, msg = msg )

      expected = { 'value': { 'value': 'abc', 'prop': 5.0 }, 'prop': 2.0 }
      actual = S.types.lib.resolveDefaults( kw2, value = { 'prop': 5.0,
                                                           'value': 'abc' } )
      msg = "Invalid results of resolveDefaults with dict kwarg."
      self.assertEqual( expected, actual, msg = msg )

      expected = { 'value': { 'value': {1:'a', 2:'b', 3:'c'},
                              'prop': 5.0 }, 'prop': 2.0 }
      actual = S.types.lib.resolveDefaults( kw2,
                                    value={ 'prop': 5.0, 'value': {3:'c'} } )
      msg = "Invalid results of resolveDefaults with nested dict kwarg."
      self.assertEqual( expected, actual, msg = msg )


      expected = {
                   'prop': 3.1,
                   'value': {
                              'prop': 3.2,
                              'value': 'abc',
                            },
                 }
      actual = S.types.lib.resolveDefaults( kw3, ['value'] )
      msg = "Invalid nested resolveDefaults with subNames and no kwargs."
      self.assertEqual( expected, actual, msg = msg )


      expected = {
                   'prop': 3.0,
                   'value': {
                              'prop': 5.0,
                              'value': {
                                         'prop': 10.0,
                                         'value': -10.0,
                                       },
                            },
                 }
      actual = S.types.lib.resolveDefaults( kw3,
                                    value=MySubStyle( prop = 5.0,
                                      value = MySubStyle( prop = 10.0,
                                         value = -10.0 ) ) )
      msg = "Invalid nested resolveDefaults with nested dict kwarg."
      self.assertEqual( expected, actual, msg = msg )

   #-----------------------------------------------------------------------
   def testStylePath( self ):
      """A basic test of 'stylePath' utility function."""
      os.environ[ "STYLEPATH" ] = "/path/to/style1:/path/to/style2"

      desired = [ '/path/to/style1', '/path/to/style2' ]
      actual = S.types.lib.stylePath( '$STYLEPATH' )

      msg = "Incorrect STYLEPATH"
      self.assertEqual( desired, actual, msg = msg )

