#!/usr/bin/env python
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

"""
Test the InstallAs() Environment method.
"""

import os.path
import sys
import TestSCons

test = TestSCons.TestSCons()

test.subdir('install', 'subdir')

install = test.workpath('install')
install_file1_out = test.workpath('install', 'file1.out')
install_file2_out = test.workpath('install', 'file2.out')
install_file3_out = test.workpath('install', 'file3.out')

#
test.write('SConstruct', r"""
env = Environment(INSTALLDIR=r'%s', SUBDIR='subdir')
InstallAs(r'%s', 'file1.in')
env.InstallAs([r'%s', r'%s'], ['file2.in', r'%s'])
""" % (install,
       install_file1_out,
       os.path.join('$INSTALLDIR', 'file2.out'),
       install_file3_out,
       os.path.join('$SUBDIR', 'file3.in')))

test.write('file1.in', "file1.in\n")
test.write('file2.in', "file2.in\n")
test.write(['subdir', 'file3.in'], "subdir/file3.in\n")

test.run(arguments = '.')

test.fail_test(test.read(install_file1_out) != "file1.in\n")
test.fail_test(test.read(install_file2_out) != "file2.in\n")
test.fail_test(test.read(install_file3_out) != "subdir/file3.in\n")

test.up_to_date(arguments = '.')

#
test.pass_test()