"""engine.SCons.Tool.f90

Tool-specific initialization for the generic Posix f90 Fortran compiler.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import SCons.Defaults
import SCons.Scanner.Fortran
import SCons.Tool
import SCons.Util
import fortran

compilers = ['f90']

#
F90Action = SCons.Action.Action("$F90COM")
ShF90Action = SCons.Action.Action("$SHF90COM")
F90PPAction = SCons.Action.Action("$F90PPCOM")
ShF90PPAction = SCons.Action.Action("$SHF90PPCOM")

#
F90Suffixes = ['.f90']
F90PPSuffixes = []
if SCons.Util.case_sensitive_suffixes('.f90', '.F90'):
    F90PPSuffixes.append('.F90')
else:
    F90Suffixes.append('.F90')

#
F90Scan = SCons.Scanner.Fortran.FortranScan("F90PATH")

for suffix in F90Suffixes + F90PPSuffixes:
    SCons.Defaults.ObjSourceScan.add_scanner(suffix, F90Scan)

#
F90Generator = fortran.VariableListGenerator('F90', 'FORTRAN', '_FORTRAND')
F90FlagsGenerator = fortran.VariableListGenerator('F90FLAGS', 'FORTRANFLAGS')
ShF90Generator = fortran.VariableListGenerator('SHF90', 'SHFORTRAN', 'F90', 'FORTRAN', '_FORTRAND')
ShF90FlagsGenerator = fortran.VariableListGenerator('SHF90FLAGS', 'SHFORTRANFLAGS')

def add_to_env(env):
    """Add Builders and construction variables for f90 to an Environment."""
    env.AppendUnique(FORTRANSUFFIXES = F90Suffixes + F90PPSuffixes)

    static_obj, shared_obj = SCons.Tool.createObjBuilders(env)

    for suffix in F90Suffixes:
        static_obj.add_action(suffix, F90Action)
        shared_obj.add_action(suffix, ShF90Action)
        static_obj.add_emitter(suffix, SCons.Defaults.StaticObjectEmitter)
        shared_obj.add_emitter(suffix, SCons.Defaults.SharedObjectEmitter)

    for suffix in F90PPSuffixes:
        static_obj.add_action(suffix, F90PPAction)
        shared_obj.add_action(suffix, ShF90PPAction)
        static_obj.add_emitter(suffix, SCons.Defaults.StaticObjectEmitter)
        shared_obj.add_emitter(suffix, SCons.Defaults.SharedObjectEmitter)
  
    env['_F90G']      = F90Generator
    env['_F90FLAGSG'] = F90FlagsGenerator
    env['F90COM']     = '$_F90G $_F90FLAGSG $_F90INCFLAGS $_FORTRANMODFLAG -c -o $TARGET $SOURCES'
    env['F90PPCOM']   = '$_F90G $_F90FLAGSG $CPPFLAGS $_CPPDEFFLAGS $_F90INCFLAGS $_FORTRANMODFLAG -c -o $TARGET $SOURCES'

    env['_SHF90G']      = ShF90Generator
    env['_SHF90FLAGSG'] = ShF90FlagsGenerator
    env['SHF90COM']   = '$_SHF90G $_SHF90FLAGSG $_F90INCFLAGS $_FORTRANMODFLAG -c -o $TARGET $SOURCES'
    env['SHF90PPCOM'] = '$_SHF90G $_SHF90FLAGSG $CPPFLAGS $_CPPDEFFLAGS $_F90INCFLAGS $_FORTRANMODFLAG -c -o $TARGET $SOURCES'

    env['_F90INCFLAGS'] = '$( ${_concat(INCPREFIX, F90PATH, INCSUFFIX, __env__, RDirs)} $)'

def generate(env):
    fortran.add_to_env(env)
    add_to_env(env)

    env['_FORTRAND'] = env.Detect(compilers) or 'f90'

def exists(env):
    return env.Detect(compilers)