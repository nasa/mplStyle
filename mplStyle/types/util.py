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

""": Utility module."""

__version__ = "$Revision: #1 $"

#===========================================================================
import sys
#===========================================================================

def mergeExceptions( exception, msg ):
   """: Merge a thrown exception with a new contextual message.

   = EXAMPLE

   # try:
   #    value = myDict['DSS 45']
   # except Exception, e:
   #    msg = 'Error trying to extract the data for the tracking station ' \
   #          'DSS 45.  That station has no data configured for it.'
   #    raise util.mergeException( e, msg )

   = INPUT VARIABLES
   - exception  The Python Exception object to convert.
   - msg        A single string of new message to add to the exception.

   = RETURN VALUE
   - Returns a tuple of three elements.  These are the same as those returned
     by sys.exc_info().  The return three elements should be raised (see the
     example above) to preserve the traceback data in the exception.
   """
   # Get the Python exception data and add the new error message into it.
   ( errorType, errorValue, errorTraceback ) = sys.exc_info()
   newError = Exception( str( exception ) + "\n" + str( msg ) )

   return newError, None, errorTraceback
 
#===========================================================================
