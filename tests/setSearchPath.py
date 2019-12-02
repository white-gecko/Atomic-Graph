import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
             inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
print(parentdir)
sys.path.insert(0, "{}/".format(parentdir))
