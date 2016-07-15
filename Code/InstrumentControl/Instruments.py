#-----------------------------------------------------------------------------
# Name:        Instruments.py
# Purpose:     To deal with controlling instruments
# Author:      Aric Sanders
# Created:     2016/06/23
#-----------------------------------------------------------------------------
""" The Module Instruments Contains Classes and functions to control 
instruments; GPIB,RS232 and other visa instruments """

# TODO:Fix Save State, and importing from DataHandlers
#-------------------------------------------------------------------------------
# Standard Imports-- All in the python standard library
import os
import re
from types import *
from ctypes import *
import datetime,time


#-------------------------------------------------------------------------------
# Third Party Imports
try: 
    from PIL import Image
    PIL_AVAILABLE=1
except:
    print 'PIL is required for some camera operations'
    PIL_AVAILABLE=0
try:
    import visa,pyvisa
except:
    print "To control comm and gpib instruments this module requires the package PyVisa"
    print " Please download it at  http://pyvisa.sourceforge.net/ "
    print " Or add it to the Python Path"
    pass 
try:
    #raise
    import pyMeasure.Code.DataHandlers.XMLModels
    InstrumentSheet=pyMeasure.Code.DataHandlers.XMLModels.InstrumentSheet
    InstrumentState=pyMeasure.Code.DataHandlers.XMLModels.InstrumentState
    DATA_SHEETS=1
    #print dir(pyMeasure)
except:
    # If the import of DataHandlers Does not work 
    class  InstrumentSheet():pass
    DATA_SHEETS=0
    print "Can't Find MySelf"
    pass

try:
    from pyMeasure.Code.Utils.Alias import *
    METHOD_ALIASES=1
except:
    METHOD_ALIASES=0
    pass 

#-------------------------------------------------------------------------------
# Module Constants
ACTIVE_COMPONENTS=[PIL_AVAILABLE,DATA_SHEETS,METHOD_ALIASES]
INSTRUMENT_TYPES=['GPIB','COMM','OCEAN_OPTICS','MIGHTEX','LABJACK']
INSTRUMENTS_DEFINED=[]
#TODO Make PYMEASURE_ROOT be read from the settings folder
PYMEASURE_ROOT=os.path.dirname(os.path.realpath(pyMeasure.__file__))
#-------------------------------------------------------------------------------
# Module Functions

#TODO: Move these functions to DataHandlers.Instruments instead

def determine_instrument_type_from_string(string):
    """ Given a string returns the instrument type"""

    if type(string) in StringTypes:
         # Start with the easy ones
         for instrument_type in INSTRUMENT_TYPES:
            match= re.compile(instrument_type,re.IGNORECASE)
            if re.search(match,string):
                return instrument_type
         # Now read in all the Instrument sheets and look for a match
         # Returning the Name in the Instrument_Type Tag
         instrument_folder=os.path.join(PYMEASURE_ROOT,'Instruments')
         for instrument_sheet in os.listdir(instrument_folder):
             path=os.path.join(PYMEASURE_ROOT,'Instruments',instrument_sheet)
             if os.path.isfile(path):
                f=open(path,'r')
                text=f.read()
                if re.search(string,text):
                    tag_match=re.search(
                    '<Instrument_Type>(?P<instrument_type>\w+)</Instrument_Type>',
                    text)
                    try:
                        return tag_match.group('instrument_type')
                    except:pass
    else:
        return None
def determine_instrument_type(object):
    """Tries to return an instrument type given an address, name, serial #
     or class instance"""
    # attributes that normally have the type hidden in there
    # should be in the order of likelyhood 
    attritbute_names=['instrument_type','address','serial','Id'] 
    # Check to see if it is a string and then go through the possibilities
    if type(object) in StringTypes:
        return determine_instrument_type_from_string(object)
    # If it is a object or class look around in normal names looking for a string
    # to process
    elif type(object)==InstanceType or ClassType:
        for attribute in attritbute_names:
            try:
                if attribute in dir(object):
                    string=eval('object.%s'%attribute)
                    answer=determine_instrument_type_from_string(string)
                    if answer is None:pass
                    else: return answer 
            except AttributeError:        
                try:
                    string=object.__class__.__name__
                    return determine_instrument_type_from_string(string)
                except: pass 
                
def find_description(identifier,output='path'):
    """ Finds an instrument description in pyMeasure/Instruments given an identifier, 
    outputs a path or the file."""
    if type(identifier) in StringTypes:
        # Now read in all the Instrument sheets and look for a match
        instrument_folder=os.path.join(PYMEASURE_ROOT,'Instruments')
        for instrument_sheet in os.listdir(instrument_folder):
            path=os.path.join(PYMEASURE_ROOT,'Instruments',instrument_sheet)
            if os.path.isfile(path):
                f=open(path,'r')
                text=f.read()
                if re.search(identifier,text):
                    path_out=re.compile('name|path',re.IGNORECASE)
                    file_contents=re.compile('file|xml|node|contents',re.IGNORECASE)
                    if re.search(path_out,output):
                        return path
                    elif re.search(file_contents,output):
                        return text
    else:
        return None       
#-------------------------------------------------------------------------------
# Class Definitions

class VisaInstrumentError(Exception):
    def __init__(self,*args):
        Exception.__init__(self,*args)


        
class VisaInstrument(InstrumentSheet):
    """ General Class to communicate with COMM and GPIB instruments"""
    def __init__(self,resource_name=None,**key_word_arguments):
        """ Intializes the VisaInstrument Class"""
        # First we try to look up the description and get info from it
        if DATA_SHEETS:
            try: 
                self.info_path=find_description(resource_name)
                InstrumentSheet.__init__(self,self.info_path)
                self.info_found=True
                self.DEFAULT_STATE_QUERY_DICTIONARY=self.get_query_dictionary()
            except:
                print 'The information sheet was not found defaulting to address' 
                self.DEFAULT_STATE_QUERY_DICTIONARY={}
                self.info_found=False
                self.instrument_address=resource_name
                pass
        else:
            self.info_found=False
            self.DEFAULT_STATE_QUERY_DICTIONARY={}
            self.instrument_address=resource_name
        
        # Create a description for state saving
        if self.info_found:
            self.description={'State_Description':{'Instrument_Description':self.path}}
        else:
            self.description={'State_Description':{'Instrument_Description':self.instrument_address}}
        
        self.state_buffer=[]
        self.STATE_BUFFER_MAX_LENGTH=10
        
        self.resource_manager=visa.ResourceManager()
        # Call the visa instrument class-- this gives ask,write,read
        self.resource=self.resource_manager.open_resource(self.instrument_address)
        # for key,value in self.resource.__dict__.iteritems():
        #     self.__dict__[key]=value
        # pyvisa.resources.messagebased.MessageBasedResource.__init__(self,
        #                                                             **{"resource_manager":visa.ResourceManager(),
        #                                                               "resource_name":self.instrument_address})
        self.current_state=self.get_state()
        
        if METHOD_ALIASES and not self.info_found :
            for command in alias(self):
                exec(command)
    def write(self,command):
        "Writes command to instrument"
        return self.resource.write(command)
    def read(self):
        "Reads from the instrument"
        return self.resource.read()
    def query(self,command):
        "Writes command and then reads a response"
        return self.resource.query(command)
    def ask(self,command):
        "Writes command and then reads a response"
        return self.resource.query(command)
    def set_state(self,**state_dictionary):
        """ Sets the instrument to the state specified by Command:Value pairs"""
        if len(self.state_buffer)+1<self.STATE_BUFFER_MAX_LENGTH:
            self.state_buffer.append(self.get_state())
        else:
            self.state_buffer.pop(1)
            self.state_buffer.insert(-1,self.get_state())         
        for state_command,value in state_dictionary.iteritems():
            self.write(state_command+' '+str(value))
        self.current_state=self.get_state()
            
    def get_state(self,**state_query_dictionary):
        """ Gets the current state of the instrument """
        if len(state_query_dictionary)==0:
            state_query_dictionary=self.DEFAULT_STATE_QUERY_DICTIONARY
        state=dict([(state_command,self.query(str(query))) for state_command,query
        in state_query_dictionary.iteritems()])
        return state
    
    def update_current_state(self):
        self.current_state=self.get_state()
   
    def save_current_state(self):
        """ Saves the state in self.current_state attribute """
        self.current_state=self.get_state()
        self.save_state(**self.current_state)
        
    def save_state(self,state_path=None,**state_dictionary):
        """ Saves any state dictionary to an xml file, with state_name """
        new_state=InstrumentState(**state_dictionary)
        try:
            new_state.add_state_description(self.description)
        except: raise #pass
        new_state.save(state_path)


    


#-------------------------------------------------------------------------------
# Module Scripts

def test_determine_instrument_type():
    print 'Type is %s'%determine_instrument_type('GPIB::22')
    print 'Type is %s'%determine_instrument_type('COMM::1')
    print 'Type is %s'%determine_instrument_type('CoMm::1') 
    print 'Type is %s'%determine_instrument_type('SRS830') 
    print 'Type is %s'%determine_instrument_type('36111') 
    class blank():pass
    new=blank()
    print type(new)
    print 'Type is %s'%determine_instrument_type(new)
    new.instrument_type='Ocean_Optics'
    print new.instrument_type
    print 'Type is %s'%determine_instrument_type(new)
    TF=(type(new)==InstanceType or ClassType)
    print TF
    print dir(new)
    print 'instrument_type' in dir(new)
        


def test_find_description():
    """Tests the function find description"""
    print "The path of the description of %s is %s"%('Lockin2',find_description('Lockin2'))
    print "The File Contents are:"
    print find_description('Lockin2','file')
     
def test_VisaInstrument(address="GPIB::21"):
    """ Simple test of the VisaInstrument class"""
    instrument=VisaInstrument(address)
    #print instrument.ask('*IDN?')
    print dir(instrument)
    print instrument.idn
    print instrument.DEFAULT_STATE_QUERY_DICTIONARY
    print instrument.current_state
    print 'Writing 0 volts to AUX4'
    instrument.set_state(**{'AUXV 4,':0})
    print instrument.current_state
    print instrument.state_buffer
    print instrument.commands

#-------------------------------------------------------------------------------
# Module Runner       

if __name__ == '__main__':
    #test_IV()
    #test_find_description()
    test_VisaInstrument()
    #user_terminate=raw_input("Please Press Any key To Finish:")
    
