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
import os.path as path
#===========================================================================

#===========================================================================
def toFile( value, allowNone=False, name="" ):
   """: Convert a value to a File object.

   The input should be a strings.  This converter will expand any
   environment variables into the actual file names.

   = INPUT VARIABLES
   - value       The input value to convert.
   - allowNone   If true, then the Python variable None is allowed as
                 an input.  The user is responsible for handling the
                 usage and conversion of this parameter then.
   - name        A name to give to this converter instance. Used in making
                 error messages easier to understand.

   = RETURN VALUE
   - Returns a path to a file.
   """
   if name:
      name = " '%s'" % name

   if value is None:
      if allowNone:
         return None
      else:
         msg = "Error calling toFile().  The input argument%s of None " \
               "is not allowed.  You must enter a valid file name." % name
         raise Exception( msg )

   # Expand any variables and normalize the path.
   return path.normpath( path.expanduser( path.expandvars( value ) ) )

#===========================================================================
