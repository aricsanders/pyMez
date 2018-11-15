#-----------------------------------------------------------------------------
# Name:        Names.py
# Purpose:   A helper module that determines automatic
#               file names for data saving
# Author:      Aric Sanders
# Created:     2016/01/20
# License:     MIT License
#-----------------------------------------------------------------------------
""" The module names contains the functions for automatically 
generating file names

  Help
---------------
<a href="./index.html">`pyMez.Code.Utils`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""
#-------------------------------------------------------------------------------
# Standard Package Imports

import os
import re
import datetime
import glob
#-------------------------------------------------------------------------------
# Module Constants
GENERAL_DESCRIPTORS=['Log','Measurement','State','Settings']

#-------------------------------------------------------------------------------
# Module Functions
def get_date():
    """Returns todays date in 'yyyymmdd' format"""
    today=datetime.date.today()
    return today.strftime('%Y%m%d')
    
def get_filename_iterator(base_name=None,directory=None,extension=None,padding=3):
    """ Returns the number of files in directory with base_name +1, padded by padding"""
    iterator=0
    replacement_string="{:0"+str(padding)+"d}"
    if extension is None:
        extension="*"
    if base_name is None:
        return replacement_string.format(1)
    elif directory is None:
        file_names=glob.glob('*.'+extension)
        for name in file_names:
            if re.match(base_name,name):
                iterator+=1
        return replacement_string.format(iterator+1)

    else:
        file_names=glob.glob(directory+'/*.'+extension)
        for name in file_names:
            name=os.path.split(name)[1]
            if re.match(base_name,name):
                iterator+=1
        return replacement_string.format(iterator+1)

def auto_name(specific_descriptor=None,general_descriptor=None,directory=None,extension='xml',padding=3):
    """ Returns an automatically generated name for a file in a directory"""
    if not specific_descriptor is None:
        name=specific_descriptor
        if not general_descriptor is None:
            name=name+'_'+general_descriptor
        name=name+'_'+get_date()+'_'
        name=name+get_filename_iterator(name,directory,extension,padding)+'.'+extension
        return name
    else:
        return None

def split_filename(filename):
    """Returns a list of file name pieces. The list will contain any CamelCase, snake_case or
    common delimiter seperated words (last element is nominally the file extension)"""
    out_string=re.sub("([\a-z])([\A-Z])",r'\1 \2',filename)
    out_list=re.split("[\W|\.|_]+",out_string)
    return out_list

def change_extension(file_path,new_extension=None):
    "Changes the extension of file path to the new one"
    if new_extension is None:
        return file_path
    else:
    # just to make it uniform, remove any . and add it back in
        new_extension="."+new_extension.replace(".","")
        return re.sub("\.\w+",new_extension,file_path)
def filename_decrement(filename,padding=3):
    """Takes an autogenrated file name in the form specific_descriptor_general_descriptor_date_iterator and
    decreases the iterator by 1"""
    replacement_string="{:0"+str(padding)+"d}"
    filename_pattern="(?P<base_name>[\w|_]+)_(?P<iterator>\d+).[\w]+"
    match=re.search(filename_pattern,filename,re.IGNORECASE)
    if match:
        i=match.groupdict()["iterator"]
        iterator=int(i)
        iterator-=1
        new_filename=re.sub(i,replacement_string.format(iterator),filename)
        return new_filename
    else:
        print("Filename did not conform to the base_name_iterator.extension pattern")

def filename_increment(filename,padding=3):
    """Takes an autogenrated file name in the form specific_descriptor_general_descriptor_date_iterator and
    decreases the iterator by 1"""
    replacement_string="{:0"+str(padding)+"d}"
    filename_pattern="(?P<base_name>[\w|_]+)_(?P<iterator>\d+).[\w]+"
    match=re.search(filename_pattern,filename,re.IGNORECASE)
    if match:
        i=match.groupdict()["iterator"]
        iterator=int(i)
        iterator+=1
        new_filename=re.sub(i,replacement_string.format(iterator),filename)
        return new_filename
    else:
        print("Filename did not conform to the base_name_iterator.extension pattern")
    
            
#-------------------------------------------------------------------------------
# Module Scripts

def test_module():
    """ Tests the module by writing files in the current working directory """
    base_name='Test_File'
    number_files=20
    print('The result of get_filename_iterator() is %s'%get_filename_iterator(base_name,extension='txt'))
    print('-'*80)
    print('\n')
    print('The current working diretory is %s \n'%os.getcwd())
    for i in range(number_files):
        try:
            new_name=base_name+"_"+get_filename_iterator(base_name,extension='txt')+'.txt'
            f=open(new_name,'w')
            f.write(str(i))
            f.close()
            print("Wrote New File %s"%new_name)
        except:
            raise
            print('failed')
    print("End of test")
    print('\n')
    print('-'*80)
            
def clean_up_test_module():
    """ Deletes the files writen by test_module() """
    base_name='Test_File'
    number_files=int(get_filename_iterator(base_name,extension='txt'))-1
    print("The number of files is {:0d}".format(number_files))
    print('\n\nThe result of get_filename_iterator(base_name,os.getcwd(),"txt") is %s'%get_filename_iterator(base_name,extension='txt'))
    print('-'*80)
    print('The current working diretory is %s \n'%os.getcwd())
    for i in range(number_files):
        try:
            new_name=base_name+'_'+"{:03d}".format(i+1)+'.txt'
            os.remove(new_name)
            print("Removed File %s"%new_name)
            
        except:
            raise
            print('failed')
    print("End of cleanup")
    print('\n')
    print('-'*80)
def test_auto_name():
    """Tests the auto name function"""
    print(("The result of auto_name('Test','AutoName',None,'txt) is {0}".format(auto_name('Test',
                                                                                         'AutoName',
                                                                                         None,'txt'))))

def test_filename_change_iterator():
    """Tests the filename decrement and increment functions"""
    name=auto_name('Test','AutoName',None,'txt')
    print(("The original name is {0}".format(name)))
    print(("-"*80))
    print(("The result of filename_increment is {0}".format(filename_increment(name))))
    print(("-"*80))
    print(("The result of filename_decrement is {0}".format(filename_decrement(name))))

#-------------------------------------------------------------------------------
# Module Runner

if __name__ == '__main__':
    test_module()
    clean_up_test_module()
    test_auto_name()
    test_filename_change_iterator()
        