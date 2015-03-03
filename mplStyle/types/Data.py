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

""": Data module."""

__version__ = "$Revision: #1 $"

#===========================================================================
import pprint
from copy import copy, deepcopy
#===========================================================================


#===========================================================================
class Data( object ):
   """A class that lets you create abitrary data attributes.
   
   Any keyword args passed in to the constructor become data
   attributes.

   # d = Data( a=1, b='2', c=[1,2,3] )
   # print d.a
   # print d.b
   """

   #-----------------------------------------------------------------------
   def __init__( self, **kw ):
      """: Constructor.
      
      = INPUT VARIABLES
      - kw   Dictionary style keyword arguments.
      """
      self.__dict__ = kw
      
   #-----------------------------------------------------------------------
   def __str__( self ):
      ": Convert the object to a string."
      return pprint.pformat( self.__dict__ )

   #-----------------------------------------------------------------------
   def __repr__( self ):
      ": Convert the object to a string."
      return self.__str__()

   #-----------------------------------------------------------------------
   def __len__( self ):
      """: Returns the number of items contained in the specified instance.
      """
      return len( self.__dict__ )

   #-----------------------------------------------------------------------
   def __copy__( self ):
      """: Return a new duplicate instance of this object.
      """
      return Data( **copy( self.__dict__ ) )

   #-----------------------------------------------------------------------
   def __deepcopy__( self, memo ):
      """: Return a deep-copy duplicate of this object.

      = INPUT VARIABLES
      - memo   A dictionary of depp-copied objects.
      """
      return Data( **deepcopy( self.__dict__, memo ) )

   #-----------------------------------------------------------------------
   def __getitem__( self, key ):
      """: Index into the data structure.

      = INPUT VARIABLES
      - key   The dictionary key of the item to get.
      """
      return self.__dict__.__getitem__( key )

   #-----------------------------------------------------------------------
   def __setitem__( self, key, value ):
      """: Index into the data structure and set a value.

      = INPUT VARIABLES
      - key   The dictionary key of the item to set.
      - value The value to set.
      """
      return self.__dict__.__setitem__( key, value )

   #-----------------------------------------------------------------------
   def __iter__( self ):
      ": Iterate over the data structure."
      return self.__dict__.__iter__()

   #-----------------------------------------------------------------------
   def __eq__( self, rhs ):
      ": Equality comparison."
      if not isinstance( rhs, Data ):
         return False

      if len( self ) != len( rhs ):
         return False
      
      for key in self:
         if key not in rhs:
            return False

         if not ( self[key] == rhs[key] ):
            return False

      return True

   #-----------------------------------------------------------------------
   def toDict( self ):
      """: Convert Data object into standard Python dictionary.

      """
      return self.__dict__

   #-----------------------------------------------------------------------
   @staticmethod
   def fromDict( inDict ):
      """: Construct a Data object from a standard Python dictionary.

      = INPUT VARIABLES
      - inDict   The dictionary from which to construct a Data object.
      """
      newData = Data()
      newData.__dict__ = inDict 
      return newData

   #-----------------------------------------------------------------------
   def get( self, key, default=None ):
      """: Return value for the key if found; otherwise, return 'default'.

      = INPUT VARIABLES
      - key       The dictionary key of the item to get.
      - default   The value to return if the key does not exist.
      """
      return self.__dict__.get( key, default )

   #-----------------------------------------------------------------------
   def keys( self ):
      """: Return a list of  possible keys.

      = RETURN VALUE
      - Returns a list of possible key values.
      """
      return self.__dict__.keys()

   #-----------------------------------------------------------------------
   def copy( self, deep = False ):
      """: Return a new duplicate instance of this object.

      = INPUT VARIABLES
      - deep   If set to true, then this will perform a deep copy.

      = RETURN VALUE
      - A copy of this Data object.
      """
      if deep:
         return self.__deepcopy__( {} )
      else:
         return self.__copy__()

   #-----------------------------------------------------------------------

#===========================================================================
