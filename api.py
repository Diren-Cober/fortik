# Author: Kirill Leontyev (DC)


import sys
import os.path

#################################################################################
from os.path import (abspath, split, exists)
from inspect import getsourcefile

# The usual way to use: import this module or some things from it.
# Sounds simple...
# However, the system must be initialized, and this means making some imports,
# .. that is why we need to know where the current copy of fortik is located.
# So, let's do some esoterics! =)

location = split(abspath(getsourcefile(lambda: None)))[0]
sys.path.append(location)
# 1. We pass in-place defined lambda to os.path.getsourcefile => we get *THIS* file's name.
# 2. os.abspath provides us with the full name of *THIS* file.
# 3. os.split(...)[0] extracts catalogue's name.
# 4. sys.path is used while making imports - we've just patched it!
del (abspath, split, getsourcefile)  # Unloading...
#################################################################################
