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

"""A library of top-level style functions.
"""

__version__ = "$Revision: #1 $"

#===========================================================================
import os
import os.path as path

from .SubStyle import SubStyle
#===========================================================================

__all__ = [
   'cleanupFilename',
   'mergeDicts',
   'resolveDefaults',
   'stylePath',
   ]

#===========================================================================
def cleanupFilename( fname ):
   """: Make the filename usable.

   = INPUT VARIABLES
   - fname   Given a filename, clean-it up to make sure we can use it with
             the file system.

   = RETURN VALUE
   - Returns a cleaned up form of the input file name.
   """
   fname = fname.replace( ' ', '_' )
   fname = fname.replace( '/', '_' )
   fname = fname.replace( '\\', '_' )
   fname = fname.replace( '!', '_' )
   fname = fname.replace( '*', '_' )
   fname = fname.replace( '`', '_' )
   fname = fname.replace( "'", "_" )
   fname = fname.replace( '"', "_" )
   fname = fname.replace( '{', '(' )
   fname = fname.replace( '}', ')' )
   fname = fname.replace( '&', '_and_' )

   return fname

#===========================================================================
# For internal use only.
def mergeDicts( d1, d2 ):
   """: Recursively merge two dictionary data structures.

   This essentially performs a union of nested dictionary data
   """
   r = {}
   r.update( d1 )

   for key in d2:
      value = d2[ key ]

      if key in d1:
         if isinstance( value, SubStyle ):
            value = value.kwargs()

         if isinstance( value, dict ) and ( key in d1 ):
            other = d1[ key ]

            if isinstance( other, SubStyle ):
               other = other.kwargs()

            value = mergeDicts( other, value )

      r[ key ] = value

   return r

#===========================================================================
# For internal use only.
def resolveDefaults( defaults, subNames = [], **kwargs ):
   """: Resolve a new set of defaults.

   What this funtion will do is:

      1) Make a duplicate of the default dictionary to be modified and
         returned.

      2) For each keyword-value parameter that is not set to None, that value
         will be set in the dictionary to be returned.  If the value is itself
         a dictionary, then it will be "merged" into the return dictionary.

      3) For each of the names specified by subNames that exists in the default
         dictionary, its values will be set in the dictionary to be returned.
         If the value is itself a dictionary, then it will be "merged" into the
         return dictionary.  It is important to note that the order of the
         names specified in 'subNames' is important as that is the order
         in which they are resolved.

      4) Returns the return dictionary.

   When a dictionary 'A' is "merged" into another dictionary 'B', this is much
   like the built-in dictionary 'update' method ( 'B.update( A )' ).  The
   difference is that any value in 'A' that is set to None is not 'updated'
   in 'B' and for any values that are themselves dictionaries, then they will
   be "merged".

   = INPUT VARIABLES
   - defaults  The current set of default values to resolve with.
   - subNames  A list of names of sub-properties to resolve (in the order
               to resolve them in).
   - kwargs    Optional keyword arguments to also resolve.

   = RETURN VALUE
   - Return a new dictionary of default values.
   """
   # First duplicate the given defaults
   subDefaults = {}
   subDefaults.update( defaults )

   # Next add in any keyword arguments
   for key in kwargs:
      value = kwargs[ key ]

      # If the kw value is not set, then ignore
      if value is None:
         continue

      # We have a kw value and nothing has been set yet.
      if isinstance( value, SubStyle ):
         value = value.kwargs()

      if isinstance( value, dict ) and ( key in subDefaults ):
         other = subDefaults[ key ]
         if isinstance( other, SubStyle ):
            other = other.kwargs()

         value = mergeDicts( other, value )

      # Store the value
      subDefaults[ key ] = value

   for name in subNames:
      if name in defaults:
         tmp = defaults[ name ]

         if tmp is None:
            continue

         if isinstance( tmp, SubStyle ):
            tmp = tmp.kwargs()

         if isinstance( tmp, dict ):
            subDefaults = mergeDicts( subDefaults, tmp )
         else:
            subDefaults[ name ] = tmp

   return subDefaults

#===========================================================================
def stylePath( envvar = 'STYLEPATH' ):
   """: Get the value of the STYLEPATH environment variable

   = INPUT VARIABLE
   - envvar    The name of the environment variable to use for the style path.

   = RETURN VALUE
   - Return a list of paths as defined by the STYLEPATH environment variable.
   """
   result = []

   if envvar.startswith( '$' ):
      envvar = envvar[ 1: ]

   stylepath = os.getenv( envvar, "" )
   stylepath = stylepath.split( ':' )

   for directory in stylepath:
      if len( directory.strip() ) == 0:
         continue
      p = path.normpath( path.expanduser( path.expandvars( directory ) ) )
      result.append( p )

   return result

#===========================================================================

