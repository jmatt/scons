#!/usr/bin/env python
#
# Copyright (c) 2001-2010 The SCons Foundation
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

"""
Test the root.name argument for the Slides HTML builder.
"""

import os
import sys
import TestSCons

test = TestSCons.TestSCons()

if not (sys.platform.startswith('linux') and
        os.path.isdir('/usr/share/xml/docbook/stylesheet/docbook-xsl/slides') and
        os.path.isdir('/usr/share/xml/docbook/custom/slides/3.3.1')):
    test.skip_test('Wrong OS or no "slides" stylesheets installed, skipping test.\n')

try:
    import libxml2
    import libxslt
except:
    try:
        import lxml
    except:
        test.skip_test('Cannot find installed Python binding for libxml2 or lxml, skipping test.\n')

test.dir_fixture('image')

# Normal invocation
test.run(stderr=None)
test.must_exist(test.workpath('manual.html'))
test.must_exist(test.workpath('toc.html'))
test.must_exist(test.workpath('foil01.html'))
test.must_exist(test.workpath('foilgroup01.html'))

# Cleanup
test.run(arguments='-c')
test.must_not_exist(test.workpath('manual.html'))
test.must_not_exist(test.workpath('toc.html'))
test.must_not_exist(test.workpath('foil01.html'))
test.must_not_exist(test.workpath('foilgroup01.html'))

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
