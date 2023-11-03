#-----------------------------------------------------------------------------
#  Copyright (C) 2023 Alberto Sottile, Michael Harvey
#
#  Distributed under the terms of the 3-clause BSD License.
#
#  Usage: python -m darkdetect [watch]
#-----------------------------------------------------------------------------

import darkdetect
import sys

def print_theme(theme):
    print('Current theme: {}'.format(theme))

print_theme(darkdetect.theme())

# demonstrate use of listener
if len(sys.argv) == 2 and sys.argv[1] == 'watch':
        darkdetect.listener(print_theme)

