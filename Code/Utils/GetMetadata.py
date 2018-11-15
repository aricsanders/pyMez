#-----------------------------------------------------------------------------
# Name:        GetMetadata
# Purpose:     To retrieve metadata on files
# Author:      Aric Sanders
# Created:     2/22/2016
# Licence:     MIT License
#-----------------------------------------------------------------------------
""" This module gets metadata on files from the filesystem (Windows only) or
the file itself.

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
# Standard Imports
import os,sys
import datetime
import re
#-------------------------------------------------------------------------------
# Third party imports

# The windows metafile imports
if os.name=='nt':
    try: 
        import pythoncom                    # Com interface for windows
        from win32com import storagecon     # storage constants
        
    except:
        print('Error in importing pythoncom, win32com. Check that pywintypes27 snf pythoncom27 dlls are in win32/lib')
        pass
# Try to import EXIF for Jpeg and Tiff stuff
try:
    import EXIF
    EXIF_AVAILABLE=1
except:
    EXIF_AVAILABLE=0
    pass 

#Try to import PIL for image info
try:
    from PIL import Image
    PIL_AVAILABLE=1
except:
    PIL_AVAILABLE=0
    pass
#-------------------------------------------------------------------------------
# Module Constants
IMAGE_FILE_EXTENSIONS=['jpg','png','tif','bmp','gif']
OS_STAT_FIELDS=['mode','ino','device','number_links','user_id','group_id',
'size','acess_time','mod_time','creation_time']
GET_STATS_FIELDS=['author','title','subject','keywords','comments','category']
TESTS_DIRECTORY=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Tests')

#-------------------------------------------------------------------------------
# Module Functions
def get_stats(path):
    """ Function returns author,title,subject,keywords,comments,category using 
    the COM interface on windows"""
    # this is code lifted from a message by Earle_Williams@ak.blm.gov
    # I changed some things
    author=title=subject=keywords=comments=category=None
    try:
        #This is all MS stuff
        pssread=pythoncom.StgOpenStorageEx(path,
        storagecon.STGM_READ|storagecon.STGM_SHARE_EXCLUSIVE,
        storagecon.STGFMT_FILE, 0 , pythoncom.IID_IPropertySetStorage)
    except:
        try:
            stg = pythoncom.StgOpenStorage(path, None,
            storagecon.STGM_READ|storagecon.STGM_SHARE_EXCLUSIVE )

            pssread = stg.QueryInterface(pythoncom.IID_IPropertySetStorage)
        except:
            print("No extended storage")
        else:
            try: 
                ps=pssread.Open(pythoncom.FMTID_SummaryInformation,
                storagecon.STGM_READ|storagecon.STGM_SHARE_EXCLUSIVE)
            except:
                pass
            else:
                author,title,subject,keywords,comments = ps.ReadMultiple(\
                (storagecon.PIDSI_AUTHOR, storagecon.PIDSI_TITLE, 
                storagecon.PIDSI_SUBJECT, storagecon.PIDSI_KEYWORDS, 
                storagecon.PIDSI_COMMENTS) )
            try: 
                ps=pssread.Open(pythoncom.FMTID_DocSummaryInformation,
                storagecon.STGM_READ|storagecon.STGM_SHARE_EXCLUSIVE)
            except:
                pass
            else:
                category = ps.ReadMultiple( (storagecon.PIDDSI_CATEGORY,) )[0]
        stat_list=[author,title,subject,keywords,comments,category]
        stat_dictionary=dict([(Field,stat_list[index]) for index,Field in 
        enumerate(GET_STATS_FIELDS)])
        return stat_dictionary
    else:
        try: 
            ps=pssread.Open(pythoncom.FMTID_SummaryInformation,
            storagecon.STGM_READ|storagecon.STGM_SHARE_EXCLUSIVE)
        except:
            pass
        else:
            author,title,subject,keywords,comments = ps.ReadMultiple(
            (storagecon.PIDSI_AUTHOR, storagecon.PIDSI_TITLE, 
            storagecon.PIDSI_SUBJECT, storagecon.PIDSI_KEYWORDS, 
            storagecon.PIDSI_COMMENTS) )
        try: 
            ps=pssread.Open(pythoncom.FMTID_DocSummaryInformation,
            storagecon.STGM_READ|storagecon.STGM_SHARE_EXCLUSIVE)
        except:
            pass
        else:
            category = ps.ReadMultiple( (storagecon.PIDDSI_CATEGORY,) ) [0]
        try: 
            ps=pssread.Open(pythoncom.FMTID_UserDefinedProperties,
            storagecon.STGM_READ|storagecon.STGM_SHARE_EXCLUSIVE)
        except:
            pass
        else:
            pass
        stat_list=[author,title,subject,keywords,comments,category]
        stat_dictionary=dict([(Field,stat_list[index]) for index,Field in 
        enumerate(GET_STATS_FIELDS)])
        return stat_dictionary
    
def get_system_metadata(path):
    """ Returns a dictionary of the data found with os.stat """
    metadata_dictionary=dict([(Field,os.stat(path)[index]) for index,Field in \
    enumerate(OS_STAT_FIELDS)])
    for key,value in metadata_dictionary.items():
        if 'time' in key:
            metadata_dictionary[key]=\
            datetime.datetime.fromtimestamp(value).isoformat()
    return metadata_dictionary
def get_file_metadata(path):
    """ Returns Windows File System information using com"""
    metadata_dictionary={}
    for key,value in get_stats(path).items():
        metadata_dictionary[key]=value
    return metadata_dictionary
def get_image_metadata(path):
    """ Returns Image Data Using PIL """
    file_extension=path.split('.')[-1].lower()
    metadata_dictionary={}
    if file_extension in IMAGE_FILE_EXTENSIONS and PIL_AVAILABLE:
        im=Image.open(path)
        for key,value in im.info.items():
            metadata_dictionary[key]=value
        del(im)
        if EXIF_AVAILABLE:
            try:
                f=open(path,'rb')
                EXIF_dictionary=EXIF.process_file(f)
                
                for key,value in EXIF_dictionary.items():
                    metadata_dictionary[key.replace(' ','_')]=value 
            except: pass              
        return metadata_dictionary
    else:
        return None
    
def get_python_metadata(path):
    """ Returns the first Docstring from python file, only .py extensions"""
    file_extension=path.split('.')[-1].lower()
    if not file_extension == 'py':
        return
    else: 
        f=open(path,'r')
        quote_number=0
        string=''
        for line in f.readlines():
            if '#' in line:
                pass
            elif '\"""' in line:
                if quote_number<2:
                    quote_number=line.count('\"\"\"')+quote_number
                    string=string+line
                elif quote_number==2:
                    return {'Python_Docstring':string}

    
def get_metadata(path):
    """ Gets system or file metadata """
    # First we get the easy stuff --- Do the formating later
    metadata_dictionary=dict([(Field,os.stat(path)[index]) for index,Field in \
    enumerate(OS_STAT_FIELDS)])
    for key,value in metadata_dictionary.items():
        if 'time' in key:
            metadata_dictionary[key]=\
            datetime.datetime.fromtimestamp(value).isoformat()
    # Now for the detailed stuff
    try: 
        for key,value in get_stats(path).items():
            metadata_dictionary[key]=value
    except: pass
    # now the image stuff
    file_extension=path.split('.')[-1].lower()
    if file_extension in IMAGE_FILE_EXTENSIONS and PIL_AVAILABLE:
        im=Image.open(path)
        for key,value in im.info.items():
            metadata_dictionary[key]=value
        del(im)
                  
    return metadata_dictionary

                
#-------------------------------------------------------------------------------
# Script Functions
def test_get_metadata(test_file_path='Data_Table_021311_1.xml'):
    """ Script to test the metadata function """
    os.chdir(TESTS_DIRECTORY)
    print('The Test Path is: %s'%os.path.join(TESTS_DIRECTORY,test_file_path))
    print('-'*80)
    for key,value in get_metadata(test_file_path).items():
        print('%s : %s'%(key,value))
        
def test_get_python_metadata():
    os.chdir(TESTS_DIRECTORY)
    MD=get_python_metadata(os.path.join(TESTS_DIRECTORY,'test_metadata.py'))
    print(MD)
    # for key,value in MD.iteritems():
    #     print '%s : %s'%(key,value)
            
    
#-------------------------------------------------------------------------------
# Module Runner    

if __name__ == '__main__':
    test_get_metadata()
    test_get_python_metadata()