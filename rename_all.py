#-----------------------------------------------------------------------------
# Name:        rename_all
# Purpose:    
# Author:      Aric Sanders
# Created:     1/1/2018
# License:     MIT License
#-----------------------------------------------------------------------------
""" Module Docstring """
#-----------------------------------------------------------------------------
# Standard Imports
import os
import re
#-----------------------------------------------------------------------------
# Third Party Imports

#-----------------------------------------------------------------------------
# Module Constants
ORIGINAL_TEXT="pyMeasure"
REPLACE_VALUE="pyMez"
#-----------------------------------------------------------------------------
# Module Functions
def replace_all(top_directory):
    """Tries to replace all occurances of ORIGINAL_TEXT with REPLACE_VALUE"""
    for directory, dirnames, filenames in os.walk(top_directory):
        for filename in filenames:
            infile=open(os.path.join(directory,filename),"r")
            infile_contents=infile.read()
            infile_contents=infile_contents.replace(ORIGINAL_TEXT,REPLACE_VALUE)
            infile.close()
            out_file=open(os.path.join(directory,filename),"w")
            out_file.write(infile_contents)
            out_file.close()
#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    replace_all("C:\ProgramData\Anaconda2\Lib\site-packages\pymez\Documentation")

    