#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

def theme():
    return 'Light'
        
def isDark():
    return theme() == 'Dark'
    
def isLight():
    return theme() == 'Light'
