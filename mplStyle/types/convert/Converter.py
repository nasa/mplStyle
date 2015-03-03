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

""": data conversion utilities.
"""

__version__ = "$Revision: #1 $"

#===========================================================================
#===========================================================================

#===========================================================================
class Converter:
   """: This class makes a callable converter an instance.

   In some cases, one might need to keep track of not just a converter
   function, but also the optional arguments that might be passed into
   it.  This class will keep track of both and call the appropriate
   converter function along with its optional arguments.

   # import style.types.convert as cvt
   # cvtList = [ cvt.Converter( cvt.toListOf, cvt.toEpoch, allowOne=True ),
   #             cvt.Converter( cvt.toListOf, cvt.toDuration, allowOne=True ) ]
   # result = cvt.toOneOf( Epoch.now(), cvtList )
   """
   #------------------------------------------------------------------------
   def __init__( self, converter, *args, **kwargs ):
      """: Create the conversion.

      = INPUT VARIABLES
      - converter   The converter function to run when converting values.
      - args        A list of positional arguments passed into the converter
                    function after the values is passed in.
      - kwargs      A dictionary of keyword-arguments passed into the converter
                    function after the positional arguments.
      """
      self.converter = converter
      self.args = args
      self.kwargs = kwargs
      
   #------------------------------------------------------------------------
   def __call__( self, value, **kwargs ):
      """: Do the conversion.

      = INPUT VARIABLES
      - value    The user input.
      - kwargs   Any additional keyword arguments to pass into the converter.

      = RETURN VALUE
      - Returns the converted object
      """
      kw = {}
      kw.update( self.kwargs )
      kw.update( kwargs )

      return self.converter( value, *self.args, **kw )

   #------------------------------------------------------------------------
   def __repr__( self ):
      """: Get a string representation of this class.

      = RETURN VALUE
      - a String representation of this class.
      """
      return str( self )

   #------------------------------------------------------------------------
   def __str__( self ):
      """: Get a string representation of this class.

      = RETURN VALUE
      - a String representation of this class.
      """
      s = "%s( " % (self.converter.__name__,)

      for value in self.args:
         s += "%s, " % (value,)

      for key in self.kwargs:
         s += "%s = %s, " % (key, self.kwargs[key])

      s += ")"

      return s

#===========================================================================
