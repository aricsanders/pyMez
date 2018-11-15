#-----------------------------------------------------------------------------
# Name:        DistributionUtils
# Purpose:    
# Author:      Aric Sanders
# Created:     1/1/2018
# License:     MIT License
#-----------------------------------------------------------------------------
""" Tools to help distribution. This began by renaming all instances of pyMeasure to
 pyMez to avoid PYPI conflicts with another package.
 Procedure:
 + update the src folder
 + update the setup.py file to contain at least a higher number of version
 + run this module to add init to all of the directories
 + from the command line in the directory with setup.py run
 >>python setup.py sdist
 >>python setup.py sdist upload

 If this fails to upload, check that the $HOME directory is properly defined and that the
 user name and password is right in .pypirc file
 After this module is ran (update the src folder

 Help
---------------
<a href="./index.html">`pyMez.Code.Utils`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""
#-----------------------------------------------------------------------------
# Standard Imports
import os
import re
#-----------------------------------------------------------------------------
# Third Party Imports

#-----------------------------------------------------------------------------
# Module Constants
ORIGINAL_TEXT="pymez"
REPLACE_VALUE="pyMez"
#-----------------------------------------------------------------------------
# Module Scripts
def replace_all(top_directory):
    """Tries to replace all occurances of ORIGINAL_TEXT with REPLACE_VALUE,
    do not run it on the git directories it corrupts the index or on images"""
    for directory, dirnames, filenames in os.walk(top_directory):
        for filename in filenames:
            try:
                if re.search("git|idea|png|jpg|gif|bmp",filename,re.IGNORECASE):
                    raise
                infile=open(os.path.join(directory,filename),"r")
                infile_contents=infile.read()
                infile_contents=infile_contents.replace(ORIGINAL_TEXT,REPLACE_VALUE)
                infile.close()
                out_file=open(os.path.join(directory,filename),"w")
                out_file.write(infile_contents)
                out_file.close()
            except:
                print(("Could not replace term in file {0}".format(os.path.join(directory,filename))))
def add_init_to_all(top_directory):
    """Script that looks for an __init__.py file in every folder and if it is not there inserts one. This is a
    very uninspired hack to the problem of including data in the distribution"""
    for directory, dirnames, filenames in os.walk(top_directory):
        if not re.search("git|idea",directory,re.IGNORECASE):

            if "__init__.py" in filenames:
                pass
            else:
                out_file=open(os.path.join(directory,"__init__.py"),"w")
                out_file.write("")
                out_file.close()




#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    #replace_all("C:\ProgramData\Anaconda2\Lib\site-packages\pymez\Code")
    #replace_all(r"C:\ProgramData\Anaconda2\Lib\site-packages\pyMez\Documentation")
    add_init_to_all(r"C:\Users\sandersa\Desktop\Distribution\src\pyMez")

    