"""
Adds the source files to the path for files in any subdirectory
"""
import os
import sys

file_location = os.path.dirname(os.path.abspath(__file__))
base_location= os.path.abspath(file_location)

sys.path.insert(0, base_location)
