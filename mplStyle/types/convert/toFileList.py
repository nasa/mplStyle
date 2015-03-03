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

""": type conversion utilities.

This module contains utilities used to convert data into a specific type.
"""

__version__ = "$Revision: #1 $"

#===========================================================================
import glob
import os.path
#===========================================================================

EXIST = 1
NEW = 2
MAY_EXIST = 3

#===========================================================================
def toFileList( value, mode, allowNone=False, allowOne=True, name="" ):
   """: Convert a value to a list of filenames.

   The input should be a list of strings.  This converter will iterate
   over the strings and expand any environment variables and any
   wildcards out to return a list of path object.

   = INPUT VARIABLES
   - value       The input value to convert.
   - mode        If 'Exist', then the file must exist or an error is thrown.
                 If 'New', then no checks are made on the files existence.
                 If 'May Exist', then no checks are made on the files
                 existence.  If 'Exist' or 'May Exist', then any wildcards
                 or env variables are expanded.
   - allowNone   If true, then the Python variable None is allowed as
                 an input.  The user is responsible for handling the
                 usage and conversion of this parameter then.
   - allowOne    If allowOne is true, then the input can be a single string.
   - name        A name to give to this converter instance. Used in making
                 error messages easier to understand.

   = RETURN VALUE
   - Returns a list of file names.
   """
   mode = mode.lower()

   if name:
      name = " '%s'" % name

   if mode == "exist":
      mode = EXIST
   elif mode == "new":
      mode = NEW
   elif mode == "may exist":
      mode = MAY_EXIST
   else:
      msg = "Invalid toFileList mode flag '%s'.  Valid inputs are " \
            "'Exist', 'May Exist', or 'New'." % ( mode )
      raise Exception( msg )

   if value is None and allowNone:
      return None

   if allowOne and isinstance( value, str ):
      value = [ value ]

   if not isinstance( value, list ):
      msg = "Error trying to input a list of file names.  The input " \
            "value is not a list.\nInput%s: %s" % ( name, value )
      raise Exception( msg )
      
   result = []
   for v in value:
      # Expand any variables and normalize the path.
      p = os.path.normpath( os.path.expanduser( os.path.expandvars( v ) ) )

      # Allow any files.
      if mode == NEW:
         result.append( p )
         
      # Find only existing files.
      else:
         # See if we need to glob.  We can't just pass the input to
         # glob because it will return nothing for regular files
         # (like 'gin.boa') if they don't exist.
         if '*' in v:
            elems = glob.glob( v )
            elems.sort()
            result += elems

         elif mode == EXIST and not os.path.exists( p ):
            msg = "Error trying to find a file for reading.  The " \
                  "requested file doesn't exist.\nFile%s: %s" % ( name, p )
            raise Exception( msg )

         else:
            result.append( p )

   return result

#===========================================================================
