#-----------------------------------------------------------------------------
# Name:        ZipModels
# Purpose:     To hold functions and models for compressed archives
# Author:      Aric Sanders
# Created:     9/15/2016
# License:     MIT License
#-----------------------------------------------------------------------------
"""
ZipModels holds classes and functions for manipulating zip files. A zipped archive is represented
by the class ZipArchive, you can open an existing file and extract_all, show the files contained zip_file.files
or add files on disk, full directories, or strings as files.

Examples
--------
    #!python
    >> from pyMez import *
    >> zip_file=ZipArchive()
    >> zip_file.add_file(os.path.join(TESTS_DIRECTORY,"test.png"))
    >> zip_file.save(os.path.join(TESTS_DIRECTORY,"test.zip")

<a href="../../../Examples/Html/ZipModels_Example.html">ZipModels Example</a>

Help
---------------
<a href="./index.html">`pyMez.Code.DataHandlers`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Reference_Index.html">Index of all Functions and Classes in pyMez</a>
</div>
"""

#-----------------------------------------------------------------------------
# Standard Imports
import sys
import os
import zipfile
import shutil

#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.Utils.Names import auto_name
except:
    print("The function auto_name in pyMez.Code.Utils.Names was not found or had an error")
    raise
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
def add_all_files(zipfile,top_directory):
    """Adds all of the files under top directory into the zipfile and closes the file"""
    for directory, dirnames, filenames in os.walk(top_directory):
        for filename in filenames:
            zipfile.write(os.path.join(directory,filename),
                          os.path.join(os.path.relpath(directory,top_directory),filename))

def extract_all(zipfile,directory):
    """Extracts all files from the zip archive to the specified directory"""
    zipfile.extractall(directory)
#-----------------------------------------------------------------------------
# Module Classes
class ZipArchive():
    """A container for zipped files, provides the ability to open, add files to, extract files from
    and save zip archives.
        !#python
        defaults={"specific_descriptor":'Data',
                  "general_descriptor":'Archive',
                  "directory":None,
                  "extension":'zip',
                  "temp_directory":None,
                  "name":None,
                  "path":None,
                  "files":None}        """
    def __init__(self,file_path=None,**options):
        " Initializes the ZipArchive class "
        # This is a general pattern for adding a lot of options some with defaults
        defaults={"specific_descriptor":'Data',
                  "general_descriptor":'Archive',
                  "directory":None,
                  "extension":'zip',
                  "temp_directory":None,
                  "name":None,
                  "path":None,
                  "files":None}
        self.options={}
        for key,value in defaults.items():
            self.options[key]=value
        for key,value in options.items():
            self.options[key]=value
        if file_path is None:
            if self.options["path"] is None:
                self.name=auto_name(self.options["specific_descriptor"],
                                    self.options["general_descriptor"],
                                    self.options["directory"],
                                    self.options["extension"])
                if self.options['directory'] is None:
                    self.path=self.name
                else:
                    self.path=os.path.join(self.options["directory"],self.name)
            else:
                self.path=self.options["path"]
            self.zip_file=zipfile.ZipFile(self.path,'w')
            if self.options["files"] is not None:
                for file_name in self.options["files"]:
                    self.zip_file.write(file_name,os.path.split(file_name)[1])
        else:
            self.zip_file=zipfile.ZipFile(file_path,'a')
        self.files=self.zip_file.namelist()

    def save(self,path=None,**save_options):
        """Saves the file to path"""
        if path is None:
            pass
        else:
            if not self.options["temp_directory"]:
                try:
                    os.mkdir("./Temp")
                except:
                    pass
                self.options["temp_directory"]="./Temp"
            temp_path=os.path.join(self.options["temp_directory"],"temp_file")
            temp_extracted=extract_all(self.zip_file,temp_path)
            temp_zip=zipfile.ZipFile(path,'w')
            add_all_files(temp_zip,temp_path)
            # need to delete the temp folder
            shutil.rmtree(temp_path)
            temp_zip.close()


    def extract_all(self,destination_directory=None):
        """Extract all in the destination directory (default is current working directory)"""
        if destination_directory is None:
            destination_directory=os.getcwd()
        extract_all(self.zip_file,destination_directory)

    def add_all_from_directory(self,directory=None):
        """Adds all files in the directory"""
        if directory is None:
            directory=os.getcwd()
        add_all_files(self.zip_file,directory)
        self.files=self.zip_file.namelist()

    def add_file(self,file_path,archive_name=None):
        """Adds the file specified by file_path to the zip archive"""
        if archive_name is None:
            archive_name=os.path.split(file_path)[1]
        self.zip_file.write(file_path,archive_name)
        self.files=self.zip_file.namelist()

    def close(self):
        "Closes the archive"
        self.zip_file.close()

    def write_string(self,data_string,archive_file_name=None):
        """writes data string to the zipped file archive_name in the archive"""
        self.zip_file.writestr(archive_file_name,data_string)
        self.files = self.zip_file.namelist()

    def __del__(self):
        "Class Destructor"
        self.zip_file.close()
#-----------------------------------------------------------------------------
# Module Scripts
# Todo: Make this script actually test functionality of ZipArchive
def test_ZipArchive(file_path="Test_Zip_File.zip"):
    #os.chdir()
    file_names=[file_path]
    test_string="A test string"
    new_zip=ZipArchive(None,files=file_names)
    new_zip.add_file(file_path,archive_name="New_directory/file.txt")
    #new_zip.add_all_from_directory(r"C:\Users\sandersa\PyCharm Projects\Jupyter-Notebooks\Radical_Correction_Files")
    new_zip.write_string(test_string,"String_test.txt")
    print(new_zip.files)
    new_zip.close()
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass