#-----------------------------------------------------------------------------
# Name:        Instruments.py
# Purpose:     To deal with controlling instruments
# Author:      Aric Sanders
# Created:     2016/06/23
#-----------------------------------------------------------------------------
""" The Module Instruments Contains Classes and functions to control 
instruments; GPIB,RS232 and other visa instruments. Instrument control classes are
wrappers around the pyvisa instrument class with static xml based metadata added in. In addition,
instruments have an emulation_mode that allows for the tracking of commands when not connected to a
viable communications bus.


Examples
--------
    #!python
    >> from pyMez import *
    >> vna=VNA("GPIB::16")
    >> vna.initialize()
    >> s2p=vna.measure_sparameters()
    >> s2p.show()

<a href="../../../Examples/html/VNA_Measurement_Example_WR15.html">VNA Measurement Examples</a>

Help
---------------
<a href="./index.html">`pyMez.Code.InstrumentControl`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""

# TODO:Fix Save State, and importing from DataHandlers
#-------------------------------------------------------------------------------
# Standard Imports-- All in the python standard library
import os
import re
from types import *
from ctypes import *
import datetime,time
import sys

#-------------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try: 
    from PIL import Image
    PIL_AVAILABLE=1
except:
    print('PIL is required for some camera operations')
    PIL_AVAILABLE=0
try:
    import visa,pyvisa
except:
    print("To control comm and gpib instruments this module requires the package PyVisa")
    print(" Please download it at  http://pyvisa.sourceforge.net/ ")
    print(" Or add it to the Python Path")
    pass 
try:
    #raise
    import Code.DataHandlers.XMLModels
    InstrumentSheet=Code.DataHandlers.XMLModels.InstrumentSheet
    InstrumentState=Code.DataHandlers.XMLModels.InstrumentState
    DATA_SHEETS=1
    #print dir(pyMez)
except:
    # If the import of DataHandlers Does not work 
    class  InstrumentSheet():pass
    DATA_SHEETS=0
    print("Can't Find MySelf")
    pass

try:
    from Code.Utils.Alias import *
    METHOD_ALIASES=1
except:
    METHOD_ALIASES=0
    pass 
try:
    from Code.Utils.Names import *
except:
    print("Could not load pyMez.Code.Utils.Names")
    pass
try:
    from Code.DataHandlers.TouchstoneModels import *
except:
    print("Could not load Code.DataHandlers.TouchstoneModels")
    pass
try:
    from Code.DataHandlers.NISTModels import *
except:
    print("Could not load Code.DataHandlers.NISTModels")
    pass
try:
    import numpy as np
except:
    print("Could not load numpy")
    pass
#-------------------------------------------------------------------------------
# Module Constants
ACTIVE_COMPONENTS=[PIL_AVAILABLE,DATA_SHEETS,METHOD_ALIASES]
INSTRUMENT_TYPES=['GPIB','COMM','OCEAN_OPTICS','MIGHTEX','LABJACK']
INSTRUMENTS_DEFINED=[]
#TODO Make PYMEASURE_ROOT be read from the settings folder
PYMEASURE_ROOT=os.path.join(os.path.dirname( __file__ ), '..','..')
VNA_FREQUENCY_UNIT_MULTIPLIERS={"Hz":1.,"kHz":10.**3,"MHz":10.**6,"GHz":10.**9,"THz":10.**12}

[EMULATION_S2P,EMULATION_S1P,EMULATION_W1P,EMULATION_W2P,EMULATION_SWITCH_TERMS]=[None,None,None,None,None]
try:
    EMULATION_S2P=S2PV1(os.path.join(TESTS_DIRECTORY,"704b.S2P"))
    EMULATION_S1P=S1PV1(os.path.join(TESTS_DIRECTORY,"Power_Meter.s1p"))
    EMULATION_W1P=W1P(os.path.join(TESTS_DIRECTORY,"Line_4909_WR15_Wave_Parameters_Port2_20180313_001.w1p"))
    EMULATION_W2P=W2P(os.path.join(TESTS_DIRECTORY,"Line_5079_WR15_Wave_Parameters_20180313_001.w2p"))
    EMULATION_SWITCH_TERMS=S2PV1(os.path.join(TESTS_DIRECTORY,"GTrue_Thru_WR15_Switch_Terms_20180313_001.s2p"))
    EMULATION_FILES_PRESENT=True
except:
    EMULATION_FILES_PRESENT=False
    print("Emulation files were not present, the emulation decorator will only return None or the original method")

#-------------------------------------------------------------------------------
# Module Functions

def emulation_data(data=None):
    """emulation data is a method decorator that returns a set of emulation data if the instrument mode is
    self.emulation_mode=True.
    For example just add @emulation_data(data_to_return) before an instrument method. This decorator also
    is conditional that the emulated data can be found. If there is a problem then it only returns the method
    undecorated"""
    def method_decorator(method):
        def return_data(self,*args,**kwargs):
            if self.emulation_mode and not data==None:
                return data
            elif data==None:
                print("No data was present to return in emulation_mode, returning None instead.")
                return None
            else:
                return method(self,*args,**kwargs)
        return return_data
    return method_decorator

def whos_there():
    """Whos_there is a function that prints the idn string for all
    GPIB instruments connected"""
    resource_manager = visa.ResourceManager()
    resource_list=resource_manager.list_resources()
    gpib_resources=[]
    gpib_idn_dictionary={}
    for instrument in resource_list:
        if re.search("GPIB|USB",instrument,re.IGNORECASE):
            try:
                resource=resource_manager.open_resource(instrument)
                gpib_resources.append(resource)
                idn=resource.query("*IDN?")
                gpib_idn_dictionary[instrument]=idn
            except:
                print("{0} did not respond to idn query".format(instrument))
    if gpib_resources:
        for instrument_name,idn in gpib_idn_dictionary.items():
            print(("{0} is at address {1}".format(idn,instrument_name)))
        #return gpib_idn_dictionary
    else:
        print("There are no GPIB resources available")



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
    elif isinstance(object, InstanceType) or ClassType:
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
                
def find_description(identifier,output='path',directory=None):
    """ Finds an instrument description in pyMez/Instruments given an identifier, 
    outputs a path or the file. Right now this outputs the first sheet that matches the identifier"""
    if isinstance(identifier,str):
        # Now read in all the Instrument sheets and look for a match
        if directory is None:
            instrument_folder=os.path.join(PYMEASURE_ROOT,'Instruments')
        else:
            instrument_folder=directory
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

def fix_segment_table(segment_table):
    """Given a list of dictionaries in the form [{"start":start_frequency,
    "stop":stop_frequency,"number_points":number_points,"step":frequency_step}...] returns a table that is ordered by start
    frequency and has no overlapping points"""
    segment_table = sorted(segment_table, key=lambda x: x["start"])
    i = 0
    while (i + 1 < len(segment_table)):
        if segment_table[i]["stop"] == segment_table[i + 1]["start"]:
            segment_table[i + 1]["start"] = segment_table[i + 1]["start"] + segment_table[i + 1]["step"]
            segment_table[i + 1]["number_points"] -= 1
        i += 1
    return segment_table
#-------------------------------------------------------------------------------
# Class Definitions

class VisaInstrumentError(Exception):
    def __init__(self,*args):
        Exception.__init__(self,*args)


class EmulationInstrument(InstrumentSheet):
    """ General Class to communicate with COMM and GPIB instruments
    This is a blend of the pyvisa resource and an xml description. """

    def __init__(self, resource_name=None, **options):
        """ Intializes the VisaInstrument Class"""
        defaults = {"state_directory": os.getcwd(),
                    "instrument_description_directory": os.path.join(PYMEASURE_ROOT, 'Instruments')}
        self.options = {}
        for key, value in defaults.items():
            self.options[key] = value
        for key, value in options.items():
            self.options[key] = value
        # First we try to look up the description and get info from it
        if DATA_SHEETS:
            try:
                self.info_path = find_description(resource_name,
                                                  directory=self.options["instrument_description_directory"])
                InstrumentSheet.__init__(self, self.info_path, **self.options)
                self.info_found = True
                self.DEFAULT_STATE_QUERY_DICTIONARY = self.get_query_dictionary()
            except:
                print('The information sheet was not found defaulting to address')
                self.DEFAULT_STATE_QUERY_DICTIONARY = {}
                self.info_found = False
                self.instrument_address = resource_name
                self.name = resource_name.replace(":", "_")
                pass
        else:
            self.info_found = False
            self.DEFAULT_STATE_QUERY_DICTIONARY = {}
            self.instrument_address = resource_name

        # Create a description for state saving
        if self.info_found:
            self.description = {'Instrument_Description': self.path}
        else:
            self.description = {'Instrument_Description': self.instrument_address}

        self.state_buffer = []
        self.STATE_BUFFER_MAX_LENGTH = 10
        self.write_buffer=[]
        self.read_buffer=[]
        self.history=[]
        #self.resource_manager = visa.ResourceManager()
        # Call the visa instrument class-- this gives ask,write,read
        #self.resource = self.resource_manager.open_resource(self.instrument_address)
        self.current_state = self.get_state()

    def write(self, command):
        "Writes command to instrument"
        now=datetime.datetime.utcnow().isoformat()
        self.write_buffer.append(command)
        self.history.append({"Timestamp":now,"Action":"self.write",
                             "Argument":command,"Response":None})


    def read(self):
        "Reads from the instrument"
        now=datetime.datetime.utcnow().isoformat()
        out="Buffer Read at {0}".format(now)
        self.read_buffer.append(out)
        time.sleep(.001)
        self.history.append({"Timestamp":now,"Action":"self.read",
                             "Argument":None,"Response":out})
        return out

    def query(self, command):
        "Writes command and then reads a response"
        self.write(command)
        return self.read()


    def ask(self, command):
        "Writes command and then reads a response"
        return self.query(command)

    def set_state(self, state_dictionary=None, state_table=None):
        """ Sets the instrument to the state specified by Command:Value pairs"""
        if state_dictionary:
            if len(self.state_buffer) + 1 < self.STATE_BUFFER_MAX_LENGTH:
                self.state_buffer.append(self.get_state())
            else:
                self.state_buffer.pop(1)
                self.state_buffer.insert(-1, self.get_state())
            for state_command, value in state_dictionary.items():
                self.write(state_command + ' ' + str(value))
            self.current_state = self.get_state()
        if state_table:
            if "Index" in list(state_table[0].keys()):
                state_table = sorted(state_table, key=lambda x: x["Index"])
            if len(self.state_buffer) + 1 < self.STATE_BUFFER_MAX_LENGTH:
                self.state_buffer.append(self.get_state())
            else:
                self.state_buffer.pop(1)
                self.state_buffer.insert(-1, self.get_state())
            # now we need to write the command
            for state_row in state_table:
                # a state row has a set and value
                state_command = state_row["Set"]
                value = state_row["Value"]
                self.write(state_command + ' ' + str(value))

    def get_state(self, state_query_dictionary=None, state_query_table=None):
        """ Gets the current state of the instrument. get_state accepts any query dictionary in
        the form state_query_dictionary={"GPIB_SET_COMMAND":"GPIB_QUERY_COMMAND",...} or any state_query_table
        in the form [{"Set":"GPIB_SET_COMMAND","Query":"GPIB_QUERY_COMMAND","Index":Optional_int_ordering commands,
        if no state is provided it returns the DEFAULT_STATE_QUERY_DICTIONARY as read in from the InstrumentSheet"""
        if not state_query_table:
            if state_query_dictionary is None or len(state_query_dictionary) == 0:
                state_query_dictionary = self.DEFAULT_STATE_QUERY_DICTIONARY
            state = dict([(state_command, self.query(str(query)).replace("\n", "")) for state_command, query
                          in state_query_dictionary.items()])
            return state
        else:
            # a state_query_table is a list of dictionaries, each row has at least a Set and Query key but could
            # have an Index key that denotes order
            if "Index" in list(state_query_table[0].keys()):
                state_query_table = sorted(state_query_table, key=lambda x: int(x["Index"]))
                state = []
                for state_row in state_query_table:
                    set = state_row["Set"]
                    query = state_row["Query"]
                    index = state_row["Index"]
                    state.append({"Set": set, "Value": self.query(query).replace("\n", ""), "Index": index})
                return state
            else:
                state = []
                for state_row in state_query_table:
                    set = state_row["Set"]
                    query = state_row["Query"]
                    state.append({"Set": set, "Value": self.query(query).replace("\n", "")})
                return state

    def update_current_state(self):
        self.current_state = self.get_state()

    def save_current_state(self):
        """ Saves the state in self.current_state attribute """
        self.current_state = self.get_state()
        self.save_state(None, state_dictionary=self.current_state)

    def save_state(self, state_path=None, state_dictionary=None, state_table=None):
        """ Saves any state dictionary to an xml file, with state_path, if not specified defaults to autonamed state
         """
        if state_path is None:
            state_path = auto_name(specific_descriptor=self.name, general_descriptor="State",
                                   directory=self.options["state_directory"])
        if state_dictionary:
            new_state = InstrumentState(None, **{"state_dictionary": state_dictionary,
                                                 "style_sheet": "./DEFAULT_STATE_STYLE.xsl"})
        elif state_table:
            new_state = InstrumentState(None, **{"state_table": state_table,
                                                 "style_sheet": "./DEFAULT_STATE_STYLE.xsl"})
        else:
            new_state = InstrumentState(None, **{"state_dictionary": self.get_state(),
                                                 "style_sheet": "./DEFAULT_STATE_STYLE.xsl"})

        try:
            new_state.add_state_description()
            new_state.append_description(description_dictionary=self.description)
        except:
            raise  # pass
        new_state.save(state_path)
        return state_path

    def load_state(self, file_path):
        """Loads a state from a file."""
        # TODO put a UDT to state_table
        state_model = InstrumentState(file_path)
        self.set_state(state_table=state_model.get_state_list_dictionary())

    def close(self):
        """Closes the VISA session"""
        print("Emulation Instrument has been closed")
        
class VisaInstrument(InstrumentSheet):
    """ General Class to communicate with COMM and GPIB instruments
    This is a blend of the pyvisa resource and an xml description. If there is no device connected
     enters into a emulation mode. Where all the commands are logged as .history and the attribute emulation_mode=True"""
    def __init__(self,resource_name=None,**options):
        """ Initializes the VisaInstrument Class"""
        defaults={"state_directory":os.getcwd(),
                  "instrument_description_directory":os.path.join(PYMEASURE_ROOT,'Instruments')}
        self.options={}
        for key,value in defaults.items():
            self.options[key]=value
        for key,value in options.items():
            self.options[key]=value
        # First we try to look up the description and get info from it
        if DATA_SHEETS:
            try: 
                self.info_path=find_description(resource_name,
                                                directory=self.options["instrument_description_directory"])
                InstrumentSheet.__init__(self,self.info_path,**self.options)
                self.info_found=True
                self.DEFAULT_STATE_QUERY_DICTIONARY=self.get_query_dictionary()
            except:
                print('The information sheet was not found defaulting to address')
                self.DEFAULT_STATE_QUERY_DICTIONARY={}
                self.info_found=False
                self.instrument_address=resource_name
                self.name=resource_name.replace(":","_")
                pass
        else:
            self.info_found=False
            self.DEFAULT_STATE_QUERY_DICTIONARY={}
            self.instrument_address=resource_name
        
        # Create a description for state saving
        if self.info_found:
            self.description={'Instrument_Description':self.path}
        else:
            self.description={'Instrument_Description':self.instrument_address}
        
        self.state_buffer=[]
        self.STATE_BUFFER_MAX_LENGTH=10
        try:
            self.resource_manager=visa.ResourceManager()
            # Call the visa instrument class-- this gives ask,write,read
            self.resource=self.resource_manager.open_resource(self.instrument_address)
            self.emulation_mode = False
        except:
            print("Unable to load resource entering emulation mode ...")
            self.resource=EmulationInstrument(self.instrument_address)
            self.history=self.resource.history
            self.emulation_mode=True
        self.current_state=self.get_state()
        

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

    def set_state(self,state_dictionary=None,state_table=None):
        """ Sets the instrument to the state specified by state_dictionary={Command:Value,..} pairs, or a list of dictionaries
        of the form state_table=[{"Set":Command,"Value":Value},..]"""
        if state_dictionary:
            if len(self.state_buffer)+1<self.STATE_BUFFER_MAX_LENGTH:
                self.state_buffer.append(self.get_state())
            else:
                self.state_buffer.pop(1)
                self.state_buffer.insert(-1,self.get_state())
            for state_command,value in state_dictionary.items():
                self.write(state_command+' '+str(value))
            self.current_state=self.get_state()
        if state_table:
            if "Index" in list(state_table[0].keys()):
                state_table=sorted(state_table,key=lambda x:x["Index"])
            if len(self.state_buffer)+1<self.STATE_BUFFER_MAX_LENGTH:
                self.state_buffer.append(self.get_state())
            else:
                self.state_buffer.pop(1)
                self.state_buffer.insert(-1,self.get_state())
            # now we need to write the command
            for state_row in state_table:
                # a state row has a set and value
                state_command=state_row["Set"]
                value=state_row["Value"]
                self.write(state_command+' '+str(value))
            
    def get_state(self,state_query_dictionary=None,state_query_table=None):
        """ Gets the current state of the instrument. get_state accepts any query dictionary in
        the form state_query_dictionary={"GPIB_SET_COMMAND":"GPIB_QUERY_COMMAND",...} or any state_query_table
        in the form [{"Set":"GPIB_SET_COMMAND","Query":"GPIB_QUERY_COMMAND","Index":Optional_int_ordering commands,
        if no state is provided it returns the DEFAULT_STATE_QUERY_DICTIONARY as read in from the InstrumentSheet"""
        if not state_query_table:
            if state_query_dictionary is None or len(state_query_dictionary)==0 :
                state_query_dictionary=self.DEFAULT_STATE_QUERY_DICTIONARY
            state=dict([(state_command,self.query(str(query)).replace("\n","")) for state_command,query
            in state_query_dictionary.items()])
            return state
        else:
            # a state_query_table is a list of dictionaries, each row has at least a Set and Query key but could
            # have an Index key that denotes order
            if "Index" in list(state_query_table[0].keys()):
                state_query_table=sorted(state_query_table,key=lambda x:int(x["Index"]))
                state=[]
                for state_row in state_query_table:
                    set=state_row["Set"]
                    query=state_row["Query"]
                    index=state_row["Index"]
                    state.append({"Set":set,"Value":self.query(query).replace("\n",""),"Index":index})
                return state
            else:
                state=[]
                for state_row in state_query_table:
                    set=state_row["Set"]
                    query=state_row["Query"]
                    state.append({"Set":set,"Value":self.query(query).replace("\n","")})
                return state
    
    def update_current_state(self):
        self.current_state=self.get_state()
   
    def save_current_state(self):
        """ Saves the state in self.current_state attribute """
        self.current_state=self.get_state()
        self.save_state(None,state_dictionary=self.current_state)
        
    def save_state(self,state_path=None,state_dictionary=None,state_table=None,refresh_state=False):
        """ Saves any state dictionary to an xml file, with state_path,
         if not specified defaults to autonamed state and the default state dictionary refreshed at the time
         of the method call. If refresh_state=True it gets the state at the time of call otherwise
         the state is assumed to be all ready complete. state=instrument.get_state(state_dictionary) and then
         instrument.save_state(state). Or instrument.save_state(state_dictionary=state_dictionary,refresh=True)
         """
        if state_path is None:
            state_path=auto_name(specific_descriptor=self.name,general_descriptor="State",
                                 directory=self.options["state_directory"])
            state_path=os.path.join(self.options["state_directory"],state_path)
        if state_dictionary:
            if refresh_state:
                state_dictionary=self.get_state(state_dictionary)
            new_state=InstrumentState(None,**{"state_dictionary":state_dictionary,
                                              "style_sheet":"./DEFAULT_STATE_STYLE.xsl"})
        elif state_table:
            if refresh_state:
                state_table=self.get_state(state_table)
            new_state=InstrumentState(None,**{"state_table":state_table,
                                              "style_sheet":"./DEFAULT_STATE_STYLE.xsl"})
        else:
            new_state=InstrumentState(None,**{"state_dictionary":self.get_state(),
                                              "style_sheet":"./DEFAULT_STATE_STYLE.xsl"})

        try:
            new_state.append_description(description_dictionary=self.description)
        except: raise #pass

        new_state.save(state_path)
        return state_path

    def load_state(self,file_path):
        """Loads a state from a file."""
        #TODO put a UDT to state_table
        state_model=InstrumentState(file_path)
        self.set_state(state_table=state_model.get_state_list_dictionary())

    def close(self):
        """Closes the VISA session"""
        self.resource_manager.close()


class VNA(VisaInstrument):
    """Control class for a linear VNA.
    The .measure_sparameters ans .measure_switch_terms return a S2PV1
    class that can be saved, printed or have a simple plot using show(). The attribute frequency_list
    stores the frequency points as Hz."""

    def __init__(self, resource_name=None, **options):
        """Initializes the E8631A control class"""
        defaults = {"state_directory": os.getcwd(), "frequency_units": "Hz"}
        self.options = {}
        for key, value in defaults.items():
            self.options[key] = value
        for key, value in options.items():
            self.options[key] = value
        VisaInstrument.__init__(self, resource_name, **self.options)
        if self.emulation_mode:
            self.power = -20
            self.IFBW = 10
            self.frequency_units = self.options["frequency_units"]
            self.frequency_table = []
            # this should be if SENS:SWE:TYPE? is LIN or LOG
            self.sweep_type ="LIN"
        else:
            self.power = self.get_power()
            self.IFBW = self.get_IFBW()
            self.frequency_units = self.options["frequency_units"]
            self.frequency_table = []
            # this should be if SENS:SWE:TYPE? is LIN or LOG
            self.sweep_type = self.get_sweep_type()
            if re.search("LIN", self.sweep_type, re.IGNORECASE):
                start = float(self.query("SENS:FREQ:START?").replace("\n", ""))
                stop = float(self.query("SENS:FREQ:STOP?").replace("\n", ""))
                number_points = int(self.query("SENS:SWE:POIN?").replace("\n", ""))
                self.frequency_list = np.linspace(start, stop, number_points).tolist()
            elif re.search("LOG", self.sweep_type, re.IGNORECASE):
                start = float(self.query("SENS:FREQ:START?").replace("\n", ""))
                stop = float(self.query("SENS:FREQ:STOP?").replace("\n", ""))
                number_points = int(self.query("SENS:SWE:POIN?").replace("\n", ""))
                logspace_start = np.log10(start)
                logspace_stop = np.log10(stop)
                self.frequency_list = [round(x, ndigits=3) for x in np.logspace(logspace_start, logspace_stop,
                                                                                     num=number_points, base=10).tolist()]
            elif re.search("SEG", self.sweep_type, re.IGNORECASE):
                number_segments = int(self.query("SENS:SEGM:COUN?").replace("\n", ""))
                for i in range(number_segments):
                    start = float(self.query("SENS:SEGM{0}:FREQ:START?".format(i + 1)).replace("\n", ""))
                    stop = float(self.query("SENS:SEGM{0}:FREQ:STOP?".format(i + 1)).replace("\n", ""))
                    number_points = int(self.query("SENS:SEGM{0}:SWE:POIN?".format(i + 1)).replace("\n", ""))
                    step = (stop - start) / float(number_points - 1)
                    self.frequency_table.append({"start": start, "stop": stop,
                                                 "number_points": number_points, "step": step})
                    self.frequency_table = fix_segment_table(self.frequency_table)
                    frequency_list = []
                    for row in self.frequency_table[:]:
                        new_list = np.linspace(row["start"], row["stop"], row["number_points"]).tolist()
                        frequency_list = frequency_list + new_list
                    self.frequency_list = frequency_list
            else:
                self.frequency_list = []

    def add_trace(self,trace_name,trace_parameter,drive_port=1,display_trace=True):
        """Adds a single trace to the VNA. Trace parameters vary by instrument and can be ratios of
        recievers or raw receiver values. For instance, R1 is the a1 wave. Traditional Sparameters
        do not require the identification of a drive_port. Does not display trace on the front panel"""
        if re.search("S",trace_parameter,re.IGNORECASE):
            self.write("CALCulate:PARameter:DEFine '{0}',{1}".format(trace_name,trace_parameter))
        else:
            self.write("CALCulate:PARameter:DEFine '{0}',{1},{2}".format(trace_name, trace_parameter,drive_port))
        if display_trace:
            self.write("DISPlay:WINDow1:TRACe1:FEED '{0}'".format(trace_name))

    def read_trace(self,trace_name):
        """Returns a 2-d list of [[reParameter1,imParameter1],..[reParameterN,imParameterN]] where
         n is the number of points in the sweep. User is responsible for triggering the sweep and retrieving
          the frequency array vna.get_frequency_list()"""
        self.write('FORM:ASC,0')
        # First get the A and Blists
        self.write('CALC:PAR:SEL "{0}"'.format(trace_name))
        self.write('CALC:FORM MLIN')
        while self.is_busy():
            time.sleep(.01)
        out_string = self.query('CALC:DATA? SDATA')
        out_string=out_string.replace("\n", "").split(",")
        re_list=out_string[0::2]
        im_list=out_string[1::2]
        out_list=[[float(real_parameter),float(im_list[index])] for index,real_parameter in enumerate(re_list)]
        return out_list

    def trigger_sweep(self):
        """Triggers a single sweep of the VNA, note you need to wait for the sweep to finish before reading the
        values. It takes ~ #ports sourced*#points/IFBW """
        self.write("INITiate:CONTinuous OFF")
        self.write("ABORT;INITiate:IMMediate;*wai")

    def get_trace_catalog(self):
        """Returns the trace catalog as a string"""
        trace_string = self.query("CALC:PAR:CAT?")
        return trace_string

    def get_trace_list(self):
        """Returns the active trace names as a list"""
        trace_string = self.query("CALC:PAR:CAT?")
        trace_list = trace_string.replace("\n", "").split(",")[0::3]
        return trace_list

    def delete_all_traces(self):
        """Deletes all active traces"""
        trace_string = self.query("CALC:PAR:CAT?")
        # remove endline, split on , and then take every third one
        trace_list = trace_string.replace("\n", "").split(",")[0::3]
        for trace in trace_list:
            self.write("CALC:PAR:DEL '{0}'".format(trace))


    def set_source_output(self,state=0):
        """Sets all of the outputs of the VNA to OFF(0) or ON (1). This disables/enables all the source outputs."""
        self.write("OUTP {0}".format(state))

    def get_source_output(self):
        """Returns the state of the outputs. This is equivelent to vna.query('OUTP?')"""
        state=self.query("OUTP?")
        return int(state.replace("\n",""))

    def add_all_traces(self,**options):
        """Adds all Sparameter and wave parameter traces.
        Does not initialize the instrument. The trace names match those in the
        measure methods (S11,S12,..S22) and (A1_D1,B1_D1..B2_D2) by default it
        assumes port 1 and port 2 are being used. In addition, it assumes the B receiver names are [A,B,C,D].
         This method will cause an error if the traces are already defined"""
        defaults = {"port1": 1,"port2":2, "b_name_list": ["A", "B", "C", "D"]}
        initialize_options = {}
        for key, value in defaults.items():
            initialize_options[key] = value
        for key, value in options.items():
            initialize_options[key] = value
        self.write("DISPlay:WINDow1:STATE ON")
        scattering_parameter_names=["S11","S12","S21","S22"]
        trace_definitions=["S{0}{1}".format(initialize_options["port1"],initialize_options["port1"]),
                           "S{0}{1}".format(initialize_options["port1"], initialize_options["port2"]),
                           "S{0}{1}".format(initialize_options["port2"], initialize_options["port1"]),
                           "S{0}{1}".format(initialize_options["port2"], initialize_options["port2"])]
        for index,name in enumerate(scattering_parameter_names):
            self.write("CALCulate:PARameter:DEFine '{0}',{1}".format(name,trace_definitions[index]))
            self.write("DISPlay:WINDow1:TRACe{1}:FEED '{0}'".format(name,index+1))
        b1_name = initialize_options["b_name_list"][initialize_options["port1"] - 1]
        b2_name= initialize_options["b_name_list"][initialize_options["port2"] - 1]
        # Initialize Port 1 traces A1_D1,B1_D1,B2_D1
        self.write("CALCulate:PARameter:DEFine 'A{0}_D{0}',R{0},{0}".format(initialize_options["port1"]))
        self.write("DISPlay:WINDow1:TRACe5:FEED 'A{0}_D{0}'".format(initialize_options["port1"]))
        self.write("CALCulate:PARameter:DEFine 'B{0}_D{0}',{1},{0}".format(initialize_options["port1"],b1_name))
        self.write("DISPlay:WINDow1:TRACe6:FEED 'B{0}_D{0}'".format(initialize_options["port1"]))
        self.write("CALCulate:PARameter:DEFine 'A{1}_D{0}',R{1},{0}".format(initialize_options["port1"],
                                                                            initialize_options["port2"] ))
        self.write("DISPlay:WINDow1:TRACe7:FEED 'A{1}_D{0}'".format(initialize_options["port1"],
                                                                    initialize_options["port2"]))

        self.write("CALCulate:PARameter:DEFine 'B{1}_D{0}',{2},{0}".format(initialize_options["port1"],
                                                                           initialize_options["port2"],
                                                                           b2_name))
        self.write("DISPlay:WINDow1:TRACe8:FEED 'B{1}_D{0}'".format(initialize_options["port1"],
                                                                           initialize_options["port2"]))
        # Initialize Port 2 Traces A1_D2,B1_D2,

        self.write("CALCulate:PARameter:DEFine 'A{0}_D{1}',R{0},{1}".format(initialize_options["port1"],
                                                                            initialize_options["port2"] ))
        self.write("DISPlay:WINDow1:TRACe9:FEED 'A{0}_D{1}'".format(initialize_options["port1"],
                                                                    initialize_options["port2"]))
        self.write("CALCulate:PARameter:DEFine 'B{0}_D{1}',{2},{1}".format(initialize_options["port1"],
                                                                           initialize_options["port2"],
                                                                           b1_name))
        self.write("DISPlay:WINDow1:TRACe10:FEED 'B{0}_D{1}'".format(initialize_options["port1"],
                                                                    initialize_options["port2"]))


        self.write("CALCulate:PARameter:DEFine 'A{1}_D{1}',R{1},{1}".format(initialize_options["port1"],
                                                                            initialize_options["port2"] ))
        self.write("DISPlay:WINDow1:TRACe11:FEED 'A{1}_D{1}'".format(initialize_options["port1"],
                                                                    initialize_options["port2"]))
        self.write("CALCulate:PARameter:DEFine 'B{1}_D{1}',{2},{1}".format(initialize_options["port1"],
                                                                           initialize_options["port2"],
                                                                           b2_name))
        self.write("DISPlay:WINDow1:TRACe12:FEED 'B{1}_D{1}'".format(initialize_options["port1"],
                                                                    initialize_options["port2"]))


    def initialize_s2p(self, **options):
        """Intializes the system to take two sparameters"""
        defaults = {"reset": False}
        initialize_options = {}
        for key, value in defaults.items():
            initialize_options[key] = value
        for key, value in options.items():
            initialize_options[key] = value
        if initialize_options["reset"]:
            self.write("SYST:FPRESET")
        self.write("DISPlay:WINDow1:STATE ON")
        self.write("CALCulate:PARameter:DEFine 'S11',S11")
        self.write("DISPlay:WINDow1:TRACe1:FEED 'S11'")
        self.write("CALCulate:PARameter:DEFine 'S12',S12")
        self.write("DISPlay:WINDow1:TRACe2:FEED 'S12'")
        self.write("CALCulate:PARameter:DEFine 'S21',S21")
        self.write("DISPlay:WINDow1:TRACe3:FEED 'S21'")
        self.write("CALCulate:PARameter:DEFine 'S22',S22")
        self.write("DISPlay:WINDow1:TRACe4:FEED 'S22'")
        self.sweep_type = self.get_sweep_type()
        if re.search("LIN", self.sweep_type, re.IGNORECASE):
            start = float(self.query("SENS:FREQ:START?").replace("\n", ""))
            stop = float(self.query("SENS:FREQ:STOP?").replace("\n", ""))
            number_points = int(self.query("SENS:SWE:POIN?").replace("\n", ""))
            self.frequency_list = np.linspace(start, stop, number_points).tolist()
        elif re.search("LOG", self.sweep_type, re.IGNORECASE):
            start = float(self.query("SENS:FREQ:START?").replace("\n", ""))
            stop = float(self.query("SENS:FREQ:STOP?").replace("\n", ""))
            number_points = int(self.query("SENS:SWE:POIN?").replace("\n", ""))
            logspace_start = np.log10(start)
            logspace_stop = np.log10(stop)
            self.frequency_list = [round(x, ndigits=3) for x in np.logspace(logspace_start, logspace_stop,
                                                                                 num=number_points, base=10).tolist()]
        elif re.search("SEG", self.sweep_type, re.IGNORECASE):
            number_segments = int(self.query("SENS:SEGM:COUN?").replace("\n", ""))
            for i in range(number_segments):
                start = float(self.query("SENS:SEGM{0}:FREQ:START?".format(i + 1)).replace("\n", ""))
                stop = float(self.query("SENS:SEGM{0}:FREQ:STOP?".format(i + 1)).replace("\n", ""))
                number_points = int(self.query("SENS:SEGM{0}:SWE:POIN?".format(i + 1)).replace("\n", ""))
                step = (stop - start) / float(number_points - 1)
                self.frequency_table.append({"start": start, "stop": stop,
                                             "number_points": number_points, "step": step})
                self.frequency_table = fix_segment_table(self.frequency_table)
                frequency_list = []
                for row in self.frequency_table[:]:
                    new_list = np.linspace(row["start"], row["stop"], row["number_points"]).tolist()
                    frequency_list = frequency_list + new_list
                self.frequency_list = frequency_list
        else:
            self.frequency_list = []

    def initialize(self,**options):
        """A handler to initialize the system to acquire the parameters of choice.
        The default behavior is to initialize_s2p"""
        defaults={"parameters":"s2p"}
        self.initialize_options={}
        for key,value in defaults.items():
            self.initialize_options[key]=value
        for key,value in options.items():
            self.initialize_options[key]=value
        if re.search("s2p",self.initialize_options["parameters"],re.IGNORECASE):
            self.initialize_s2p(**self.initialize_options)
        elif re.search("w1p",self.initialize_options["parameters"],re.IGNORECASE):
            self.initialize_w1p(**self.initialize_options)
        elif re.search("w2p",self.initialize_options["parameters"],re.IGNORECASE):
            self.initialize_w2p(**self.initialize_options)
        else:
            print("Initialization failed because it did not understand {0}".format(self.initialize_options))


    def set_power(self, power):
        """Sets the power of the Instrument in dbm"""
        self.write('SOUR:POW {0}'.format(power))

    def get_power(self):
        "Returns the power of the instrument in dbm"
        return self.query('SOUR:POW?')

    def get_sweep_type(self):
        "Returns the current sweep type. It can be LIN, LOG, or SEG"
        return self.query("SENS:SWE:TYPE?")

    def set_IFBW(self, ifbw):
        """Sets the IF Bandwidth of the instrument in Hz"""
        self.write('SENS:BAND {0}'.format(ifbw))
        self.write('SENS:BAND:TRAC OFF')
        self.IFBW = ifbw

    def get_IFBW(self):
        """Returns the IFBW of the instrument in Hz"""
        ifbw = float(self.query('SENS:BAND?'))
        self.IFBW = ifbw
        return ifbw

    def set_frequency_units(self, frequency_units="Hz"):
        """Sets the frequency units of the class, all values are still written to the VNA
        as Hz and the attrbiute frequncy_list is in Hz,
        however all commands that deal with sweeps and measurements will be in units"""
        for unit in list(VNA_FREQUENCY_UNIT_MULTIPLIERS.keys()):
            if re.match(unit, frequency_units, re.IGNORECASE):
                self.frequency_units = unit

    def add_segment(self, start, stop=None, number_points=None, step=None, frequency_units="Hz"):
        """Sets the VNA to a segment mode and appends a single entry in the frequency table. If start is the only specified
        parameter sets the entry to start=stop and number_points = 1. If step is specified calculates the number of points
        and sets start, stop, number_points on the VNA. It also stores the value into the attribute frequency_list.
        Note this function was primarily tested on an agilent which stores frequency to the nearest mHz.
        """
        # first handle the start only case
        if stop is None and number_points is None:
            stop = start
            number_points = 1
        # fix the frequency units
        for unit in list(VNA_FREQUENCY_UNIT_MULTIPLIERS.keys()):
            if re.match(unit, frequency_units, re.IGNORECASE):
                start = start * VNA_FREQUENCY_UNIT_MULTIPLIERS[unit]
                stop = stop * VNA_FREQUENCY_UNIT_MULTIPLIERS[unit]
                if step:
                    step = step * VNA_FREQUENCY_UNIT_MULTIPLIERS[unit]
                self.frequency_units = unit
        # handle creating step and number of points
        if number_points is None and not step is None:
            number_points = round((stop - start) / step) + 1
        elif number_points is None:
            number_points = 201  # I don't like the default for n_points this far down in the code
            step = (stop - start) / (number_points - 1)
        else:
            step = (stop - start) / (number_points - 1)

        # append the new segment to self.frequency_table and fix any strangeness
        self.frequency_table.append({"start": start, "stop": stop, "number_points": number_points, "step": step})
        self.frequency_table = fix_segment_table(self.frequency_table[:])

        # update the frequency_list
        frequency_list = []
        for row in self.frequency_table[:]:
            new_list = np.linspace(row["start"], row["stop"], row["number_points"]).tolist()
            frequency_list = frequency_list + new_list
        self.frequency_list = frequency_list

        # now we write the segment to the instrument
        if not re.search("SEG", self.get_sweep_type(), re.IGNORECASE):
            self.write('SENS:SWE:TYPE SEGM')

        # now get the number of segments and add or delete the right amount to make it line up with self.frequency_table
        # This routine is broken

        number_segments = int(self.query("SENS:SEGM:COUN?").replace("\n", ""))
        #print(("{0} is {1}".format("number_segments", number_segments)))
        if len(self.frequency_table) < number_segments:
            difference = number_segments - len(self.frequency_table)
            max_segment = number_segments
            while (difference != 0):
                self.write("SENS:SEGM{0}:DEL".format(max_segment))
                max_segment -= 1
                difference -= 1
        elif len(self.frequency_table) > number_segments:
            difference = len(self.frequency_table) - number_segments
            max_segment = number_segments + 1
            #print(("{0} is {1}".format("difference", difference)))
            while (difference != 0):
                self.write("SENS:SEGM{0}:ADD".format(max_segment))
                max_segment += 1
                difference -= 1
                #print(("{0} is {1}".format("difference", difference)))
        else:
            pass

        for row_index, row in enumerate(self.frequency_table[:]):
            [start, stop, number_points] = [row["start"], row["stop"], row["number_points"]]
            # SENSe<cnum>:SEGMent<snum>:SWEep:POINts <num>
            self.write("SENS:SEGM{0}:FREQ:START {1}".format(row_index + 1, start))
            self.write("SENS:SEGM{0}:FREQ:STOP {1}".format(row_index + 1, stop))
            self.write("SENS:SEGM{0}:SWE:POIN {1}".format(row_index + 1, number_points))
            self.write("SENS:SEGM{0}:STAT ON".format(row_index + 1))

    def remove_segment(self,segment=1):
        """Removes a the segment, default is segment 1 """
        self.write("SENS:SEGM{0}:DEL".format(segment))

    def remove_all_segments(self):
        """Removes all segments from VNA"""
        segment_count = int(self.query("SENS:SEGM:COUN?").replace("\n", ""))
        for i in range(segment_count):
            segment = segment_count - i
            self.write("SENS:SEGM{0}:DEL".format(segment))

    def write_frequency_table(self, frequency_table=None):
        """Writes frequency_table to the instrument, the frequency table should be in the form
        [{start:,stop:,number_points:}..] or None"""
        if frequency_table is None:
            frequency_table = self.frequency_table[:]
        for row_index, row in enumerate(frequency_table[:]):
            [start, stop, number_points] = [row["start"], row["stop"], row["number_points"]]
            # SENSe<cnum>:SEGMent<snum>:SWEep:POINts <num>
            self.write("SENS:SEGM{0}:FREQ:START {1}".format(row_index + 1, start))
            self.write("SENS:SEGM{0}:FREQ:STOP {1}".format(row_index + 1, stop))
            self.write("SENS:SEGM{0}:SWE:POIN {1}".format(row_index + 1, number_points))
            self.write("SENS:SEGM{0}:STAT ON".format(row_index + 1))

    def set_frequency(self, start, stop=None, number_points=None, step=None, type='LIN', frequency_units="Hz"):
        """Sets the VNA to a linear mode and creates a single entry in the frequency table. If start is the only specified
        parameter sets the entry to start=stop and number_points = 1. If step is specified calculates the number of points
        and sets start, stop, number_points on the VNA. It also stores the value into the attribute frequency_list.
        Note this function was primarily tested on an agilent which stores frequency to the nearest mHz.
        """

        if stop is None and number_points is None:
            stop = start
            number_points = 1

        for unit in list(VNA_FREQUENCY_UNIT_MULTIPLIERS.keys()):
            if re.match(unit, frequency_units, re.IGNORECASE):
                start = start * VNA_FREQUENCY_UNIT_MULTIPLIERS[unit]
                stop = stop * VNA_FREQUENCY_UNIT_MULTIPLIERS[unit]
                if step:
                    step = step * VNA_FREQUENCY_UNIT_MULTIPLIERS[unit]
                self.frequency_units = unit
        if number_points is None and not step is None:
            number_points = round((stop - start) / step) + 1

        if re.search("LIN", type, re.IGNORECASE):
            self.write('SENS:SWE:TYPE LIN')
            self.frequency_list = np.linspace(start, stop, number_points).tolist()
        elif re.search("LOG", type, re.IGNORECASE):
            self.write('SENS:SWE:TYPE LOG')
            logspace_start = np.log10(start)
            logspace_stop = np.log10(stop)
            self.frequency_list = [round(x, ndigits=3) for x in np.logspace(logspace_start, logspace_stop,
                                                                                 num=number_points, base=10).tolist()]
        else:
            self.write('SENS:SWE:TYPE LIN')
            self.frequency_list = [round(x, ndigits=3) for x in np.linspace(start, stop, number_points).tolist()]
        self.write("SENS:FREQ:START {0}".format(start))
        self.write("SENS:FREQ:STOP {0}".format(stop))
        self.write("SENS:SWE:POIN {0}".format(number_points))

    def get_frequency(self):
        "Returns the frequency in python list format"
        return self.get_frequency_list()

    def is_busy(self):
        """Checks if the instrument is currently doing something and returns a boolean value"""
        opc = bool(self.resource.query("*OPC?"))
        return not opc

    def clear_window(self, window=1):
        """Clears the  window of traces. Does not delete the variables"""
        string_response = self.query("DISPlay:WINDow{0}:CATalog?".format(window))
        traces = string_response.split(",")
        for trace in traces:
            self.write("DISP:WIND{0}:TRAC{1}:DEL".format(window, trace))

    @emulation_data(EMULATION_SWITCH_TERMS)
    def measure_switch_terms(self, **options):
        """Measures switch terms and returns a s2p table in forward and reverse format. To return in port format
        set the option order= "PORT"""
        defaults = {"view_trace": True,"initialize":True,"order":"FR"}
        self.measure_switch_term_options = {}
        for key, value in defaults.items():
            self.measure_switch_term_options[key] = value
        for key, value in options.items():
            self.measure_switch_term_options[key] = value
        # this resets the traces to be based on swith terms
        # Set VS to be remotely triggered by GPIB
        self.write("SENS:HOLD:FUNC HOLD")
        self.write("TRIG:REM:TYP CHAN")
        if self.measure_switch_term_options["initialize"]:

            # Set the Channel to have 2 Traces
            self.write("CALC1:PAR:COUN 2")
            # Trace 1 This is port 2 or Forward Switch Terms
            self.write("CALC1:PAR:DEF 'FWD',R2B,1")  # note this command is different for vector star A2,B2
            if self.measure_switch_term_options["view_trace"]:
                self.write("DISPlay:WINDow1:TRACe5:FEED 'FWD'")
            # Trace 2 This is port 1 or Reverse Switch Terms
            self.write("CALC1:PAR:DEF 'REV',R1A,2")
            if self.measure_switch_term_options["view_trace"]:
                self.write("DISPlay:WINDow1:TRACe6:FEED 'REV'")

        # Select Channel
        self.write("CALC1:SEL;")
        self.write("ABORT;TRIG:SING;")
        # Sleep for the duration of the scan
        time.sleep(len(self.frequency_list) * 2.5 / float(self.IFBW))
        # wait for other functions to be completed
        # while self.is_busy():
        #     time.sleep(.01)
        # Set the read format
        self.write("FORM:ASC,0")
        # Read in the data
        self.write("CALC:PAR:SEL 'FWD';")
        foward_switch_string = self.query("CALC:DATA? SDATA")
        while self.is_busy():
            time.sleep(.01)
        self.write("CALC:PAR:SEL 'REV';")
        reverse_switch_string = self.query("CALC:DATA? SDATA")

        # Anritsu Specific String Parsing
        foward_switch_string=re.sub("#\d+\n","",foward_switch_string)
        reverse_switch_string=re.sub("#\d+\n","",reverse_switch_string)

        # Now parse the string
        foward_switch_list = foward_switch_string.replace("\n", "").split(",")
        reverse_switch_list = reverse_switch_string.replace("\n", "").split(",")
        real_foward = foward_switch_list[0::2]
        imaginary_forward = foward_switch_list[1::2]
        real_reverse = reverse_switch_list[0::2]
        imaginary_reverse = reverse_switch_list[1::2]
        switch_data = []
        if re.search("f",self.measure_switch_term_options["order"],re.IGNORECASE):
            for index, frequency in enumerate(self.frequency_list[:]):
                new_row = [frequency,
                           real_foward[index], imaginary_forward[index],
                           real_reverse[index], imaginary_reverse[index],
                           0, 0,
                           0, 0]
                new_row = [float(x) for x in new_row]
                switch_data.append(new_row)
        elif re.search("p",self.measure_switch_term_options["order"],re.IGNORECASE):
            for index, frequency in enumerate(self.frequency_list[:]):
                new_row = [frequency,
                           real_reverse[index], imaginary_reverse[index],
                           real_foward[index], imaginary_forward[index],
                           0, 0,
                           0, 0]
                new_row = [float(x) for x in new_row]
                switch_data.append(new_row)
        option_line = "# Hz S RI R 50"
        # add some options here about auto saving
        # do we want comment options?
        s2p = S2PV1(None, option_line=option_line, data=switch_data)
        s2p.change_frequency_units(self.frequency_units)
        return s2p

    @emulation_data(EMULATION_S2P)
    def measure_sparameters(self, **options):
        """Triggers a single sparameter measurement for all 4 parameters and returns a SP2V1 object"""
        defaults = {"trigger": "single"}
        self.measure_sparameter_options = {}
        for key, value in defaults.items():
            self.measure_sparameter_options[key] = value
        for key, value in options.items():
            self.measure_sparameter_options[key] = value
        if self.measure_sparameter_options["trigger"] in ["single"]:
            self.write("INITiate:CONTinuous OFF")
            self.write("ABORT;INITiate:IMMediate;*wai")
            # now go to sleep for the time to take the scan
            time.sleep(len(self.frequency_list) * 2 / float(self.IFBW))

        # wait for other functions to be completed
        while self.is_busy():
            time.sleep(.01)
        # Set the format to ascii and set up sweep definitions
        self.write('FORM:ASC,0')
        # First get the Sparameter lists
        self.write('CALC:PAR:SEL S11')
        self.write('CALC:FORM MLIN')
        while self.is_busy():
            time.sleep(.01)
        s11_string = self.query('CALC:DATA? SDATA')

        self.write('CALC:PAR:SEL S12')
        self.write('CALC:FORM MLIN')
        while self.is_busy():
            time.sleep(.01)
        s12_string = self.query('CALC:DATA? SDATA')
        self.write('CALC:PAR:SEL S21')
        self.write('CALC:FORM MLIN')
        while self.is_busy():
            time.sleep(.01)
        s21_string = self.query('CALC:DATA? SDATA')
        self.write('CALC:PAR:SEL S22')
        self.write('CALC:FORM MLIN')
        while self.is_busy():
            time.sleep(.01)
        s22_string = self.query('CALC:DATA? SDATA')

        # String Parsing, Vector star specific, but no harm to Keysight, Rohde
        s11_string=re.sub("#\d+\n","",s11_string)
        s12_string=re.sub("#\d+\n","",s12_string)
        s21_string=re.sub("#\d+\n","",s21_string)
        s22_string=re.sub("#\d+\n","",s22_string)


        s11_list = s11_string.replace("\n", "").split(",")
        s12_list = s12_string.replace("\n", "").split(",")
        s21_list = s21_string.replace("\n", "").split(",")
        s22_list = s22_string.replace("\n", "").split(",")
        # Construct a list of lists that is data in RI format
        reS11 = s11_list[0::2]
        imS11 = s11_list[1::2]
        reS12 = s12_list[0::2]
        imS12 = s12_list[1::2]
        reS21 = s21_list[0::2]
        imS21 = s21_list[1::2]
        reS22 = s22_list[0::2]
        imS22 = s22_list[1::2]
        sparameter_data = []
        for index, frequency in enumerate(self.frequency_list[:]):
            new_row = [frequency,
                       reS11[index], imS11[index],
                       reS21[index], imS21[index],
                       reS12[index], imS12[index],
                       reS22[index], imS22[index]]
            new_row = [float(x) for x in new_row]
            sparameter_data.append(new_row)
        option_line = "# Hz S RI R 50"
        # add some options here about auto saving
        # do we want comment options?
        s2p = S2PV1(None, option_line=option_line, data=sparameter_data)
        s2p.change_frequency_units(self.frequency_units)
        return s2p


    def initialize_w2p(self,**options):
        """Initializes the system for w2p acquisition"""
        defaults = {"reset": False, "port1": 1,"port2":2, "b_name_list": ["A", "B", "C", "D"]}
        initialize_options = {}
        for key, value in defaults.items():
            initialize_options[key] = value
        for key, value in options.items():
            initialize_options[key] = value
        if initialize_options["reset"]:
            self.write("SYST:FPRESET")
        b1_name = initialize_options["b_name_list"][initialize_options["port1"] - 1]
        b2_name= initialize_options["b_name_list"][initialize_options["port2"] - 1]
        # Initialize Port 1 traces A1_D1,B1_D1,B2_D1
        self.write("DISPlay:WINDow1:STATE ON")
        self.write("CALCulate:PARameter:DEFine 'A{0}_D{0}',R{0},{0}".format(initialize_options["port1"]))
        self.write("DISPlay:WINDow1:TRACe1:FEED 'A{0}_D{0}'".format(initialize_options["port1"]))
        self.write("CALCulate:PARameter:DEFine 'B{0}_D{0}',{1},{0}".format(initialize_options["port1"],b1_name))
        self.write("DISPlay:WINDow1:TRACe2:FEED 'B{0}_D{0}'".format(initialize_options["port1"]))
        self.write("CALCulate:PARameter:DEFine 'A{1}_D{0}',R{1},{0}".format(initialize_options["port1"],
                                                                            initialize_options["port2"] ))
        self.write("DISPlay:WINDow1:TRACe3:FEED 'A{1}_D{0}'".format(initialize_options["port1"],
                                                                    initialize_options["port2"]))

        self.write("CALCulate:PARameter:DEFine 'B{1}_D{0}',{2},{0}".format(initialize_options["port1"],
                                                                           initialize_options["port2"],
                                                                           b2_name))
        self.write("DISPlay:WINDow1:TRACe4:FEED 'B{1}_D{0}'".format(initialize_options["port1"],
                                                                           initialize_options["port2"]))
        # Initialize Port 2 Traces A1_D2,B1_D2,

        self.write("CALCulate:PARameter:DEFine 'A{0}_D{1}',R{0},{1}".format(initialize_options["port1"],
                                                                            initialize_options["port2"] ))
        self.write("DISPlay:WINDow1:TRACe5:FEED 'A{0}_D{1}'".format(initialize_options["port1"],
                                                                    initialize_options["port2"]))
        self.write("CALCulate:PARameter:DEFine 'B{0}_D{1}',{2},{1}".format(initialize_options["port1"],
                                                                           initialize_options["port2"],
                                                                           b1_name))
        self.write("DISPlay:WINDow1:TRACe6:FEED 'B{0}_D{1}'".format(initialize_options["port1"],
                                                                    initialize_options["port2"]))


        self.write("CALCulate:PARameter:DEFine 'A{1}_D{1}',R{1},{1}".format(initialize_options["port1"],
                                                                            initialize_options["port2"] ))
        self.write("DISPlay:WINDow1:TRACe7:FEED 'A{1}_D{1}'".format(initialize_options["port1"],
                                                                    initialize_options["port2"]))
        self.write("CALCulate:PARameter:DEFine 'B{1}_D{1}',{2},{1}".format(initialize_options["port1"],
                                                                           initialize_options["port2"],
                                                                           b2_name))
        self.write("DISPlay:WINDow1:TRACe8:FEED 'B{1}_D{1}'".format(initialize_options["port1"],
                                                                    initialize_options["port2"]))
        self.sweep_type = self.get_sweep_type()
        self.frequency_list=self.get_frequency_list()


    def initialize_w1p(self, **options):
        """Initializes the system for w1p acquisition, default works for ZVA"""
        defaults = {"reset": False, "port": 1, "b_name_list": ["A", "B", "C", "D"],"source_port":1}
        initialize_options = {}
        for key, value in defaults.items():
            initialize_options[key] = value
        for key, value in options.items():
            initialize_options[key] = value
        if initialize_options["reset"]:
            self.write("SYST:FPRESET")
        b_name = initialize_options["b_name_list"][initialize_options["port"] - 1]
        self.write("DISPlay:WINDow1:STATE ON")
        self.write("CALCulate:PARameter:DEFine 'A{0}_D{0}',R{0}".format(initialize_options["port"]))
        self.write("DISPlay:WINDow1:TRACe1:FEED 'A{0}_D{0}'".format(initialize_options["port"]))
        self.write("CALCulate:PARameter:DEFine 'B{0}_D{0}',{1}".format(initialize_options["port"],
                                                                       b_name))
        self.write("DISPlay:WINDow1:TRACe2:FEED 'B{0}_D{0}'".format(initialize_options["port"]))
        self.sweep_type = self.get_sweep_type()
        if re.search("LIN", self.sweep_type, re.IGNORECASE):
            start = float(self.query("SENS:FREQ:START?").replace("\n", ""))
            stop = float(self.query("SENS:FREQ:STOP?").replace("\n", ""))
            number_points = int(self.query("SENS:SWE:POIN?").replace("\n", ""))
            self.frequency_list = np.linspace(start, stop, number_points).tolist()
        elif re.search("LOG", self.sweep_type, re.IGNORECASE):
            start = float(self.query("SENS:FREQ:START?").replace("\n", ""))
            stop = float(self.query("SENS:FREQ:STOP?").replace("\n", ""))
            number_points = int(self.query("SENS:SWE:POIN?").replace("\n", ""))
            logspace_start = np.log10(start)
            logspace_stop = np.log10(stop)
            self.frequency_list = [round(x, ndigits=3) for x in np.logspace(logspace_start, logspace_stop,
                                                                                 num=number_points, base=10).tolist()]
        elif re.search("SEG", self.sweep_type, re.IGNORECASE):
            self.frequency_table=[]
            number_segments = int(self.query("SENS:SEGM:COUN?").replace("\n", ""))
            for i in range(number_segments):
                start = float(self.query("SENS:SEGM{0}:FREQ:START?".format(i + 1)).replace("\n", ""))
                stop = float(self.query("SENS:SEGM{0}:FREQ:STOP?".format(i + 1)).replace("\n", ""))
                number_points = int(self.query("SENS:SEGM{0}:SWE:POIN?".format(i + 1)).replace("\n", ""))
                step = (stop - start) / float(number_points - 1)
                self.frequency_table.append({"start": start, "stop": stop,
                                             "number_points": number_points, "step": step})
                self.frequency_table = fix_segment_table(self.frequency_table)
                frequency_list = []
                for row in self.frequency_table[:]:
                    new_list = np.linspace(row["start"], row["stop"], row["number_points"]).tolist()
                    frequency_list = frequency_list + new_list
                self.frequency_list = frequency_list
        else:
            self.frequency_list = []

    def get_frequency_list(self):
        "Returns the frequency list as read from the VNA"
        self.sweep_type = self.get_sweep_type()
        if re.search("LIN", self.sweep_type, re.IGNORECASE):
            start = float(self.query("SENS:FREQ:START?").replace("\n", ""))
            stop = float(self.query("SENS:FREQ:STOP?").replace("\n", ""))
            number_points = int(self.query("SENS:SWE:POIN?").replace("\n", ""))
            self.frequency_list = np.linspace(start, stop, number_points).tolist()
        elif re.search("LOG", self.sweep_type, re.IGNORECASE):
            start = float(self.query("SENS:FREQ:START?").replace("\n", ""))
            stop = float(self.query("SENS:FREQ:STOP?").replace("\n", ""))
            number_points = int(self.query("SENS:SWE:POIN?").replace("\n", ""))
            logspace_start = np.log10(start)
            logspace_stop = np.log10(stop)
            self.frequency_list = np.logspace(logspace_start, logspace_stop,num=number_points, base=10).tolist()

        elif re.search("SEG", self.sweep_type, re.IGNORECASE):
            self.frequency_table=[]
            number_segments = int(self.query("SENS:SEGM:COUN?").replace("\n", ""))
            for i in range(number_segments):
                start = float(self.query("SENS:SEGM{0}:FREQ:START?".format(i + 1)).replace("\n", ""))
                stop = float(self.query("SENS:SEGM{0}:FREQ:STOP?".format(i + 1)).replace("\n", ""))
                number_points = int(self.query("SENS:SEGM{0}:SWE:POIN?".format(i + 1)).replace("\n", ""))
                step = (stop - start) / float(number_points - 1)
                self.frequency_table.append({"start": start, "stop": stop,
                                             "number_points": number_points, "step": step})
                self.frequency_table = fix_segment_table(self.frequency_table)
            frequency_list = []
            for row in self.frequency_table[:]:
                new_list = np.linspace(row["start"], row["stop"], row["number_points"]).tolist()
                frequency_list = frequency_list + new_list
            self.frequency_list = frequency_list
        else:
            self.frequency_list = []
        return self.frequency_list[:]

    @emulation_data(EMULATION_W1P)
    def measure_w1p(self, **options):
        """Triggers a single w1p measurement for a specified
        port and returns a w1p object."""
        defaults = {"trigger": "single", "port": 1,
                    "b_name_list": ["A", "B", "C", "D"],
                    "w1p_options": None}
        self.measure_w1p_options = {}
        for key, value in defaults.items():
            self.measure_w1p_options[key] = value
        for key, value in options.items():
            self.measure_w1p_options[key] = value
        if self.measure_w1p_options["trigger"] in ["single"]:
            self.write("INITiate:CONTinuous OFF")
            self.write("ABORT;INITiate:IMMediate;*wai")
            # now go to sleep for the time to take the scan
            time.sleep(len(self.frequency_list) * 2 / float(self.IFBW))

        # wait for other functions to be completed
        while self.is_busy():
            time.sleep(.01)
        # Set the format to ascii and set up sweep definitions
        self.write('FORM:ASC,0')
        # First get the A and Blists
        self.write('CALC:PAR:SEL "A{0}_D{0}"'.format(self.measure_w1p_options["port"]))
        self.write('CALC:FORM MLIN')
        while self.is_busy():
            time.sleep(.01)
        a_string = self.query('CALC:DATA? SDATA')

        self.write('CALC:PAR:SEL  B{0}_D{0}'.format(self.measure_w1p_options["port"]))
        self.write('CALC:FORM MLIN')
        while self.is_busy():
            time.sleep(.01)
        b_string = self.query('CALC:DATA? SDATA')

        # Anritsu Specific String Parsing
        a_string=re.sub("#\d+\n","",a_string)
        b_string=re.sub("#\d+\n","",b_string)

        # String Parsing
        a_list = a_string.replace("\n", "").split(",")
        b_list = b_string.replace("\n", "").split(",")



        # Construct a list of lists that is data in RI format
        re_a = a_list[0::2]
        im_a = a_list[1::2]
        re_b = b_list[0::2]
        im_b = b_list[1::2]
        wparameter_data = []
        for index, frequency in enumerate(self.frequency_list[:]):
            new_row = [frequency / 10. ** 9,
                       re_a[index], im_a[index],
                       re_b[index], im_b[index]]
            new_row = [float(x) for x in new_row]
            wparameter_data.append(new_row)
        column_names = ["Frequency", "reA1_D1", "imA1_D1", "reB1_D1", "imB1_D1"]
        # add some options here about auto saving
        # do we want comment options?
        options = {"column_names_begin_token": "!", "data_delimiter": "  ", "column_names": column_names,
                   "data": wparameter_data, "specific_descriptor": "Wave_Parameters",
                   "general_descriptor": "One_Port", "extension": "w1p",
                   "column_types":["float" for column in column_names]}
        if self.measure_w1p_options["w1p_options"]:
            for key,value in self.measure_w1p_options["w1p_options"].items():
                options[key]=value
        w1p = AsciiDataTable(None, **options)
        return w1p

    @emulation_data(EMULATION_W2P)
    def measure_w2p(self, **options):
        """Triggers a single w2p measurement for a specified
        port and returns a w2p object."""
        defaults = {"trigger": "single", "port1": 1,"port2":2,
                    "b_name_list": ["A", "B", "C", "D"],
                    "w2p_options": None}
        self.measure_w2p_options = {}
        for key, value in defaults.items():
            self.measure_w2p_options[key] = value
        for key, value in options.items():
            self.measure_w2p_options[key] = value
        if self.measure_w2p_options["trigger"] in ["single"]:
            self.write("INITiate:CONTinuous OFF")
            self.write("ABORT;INITiate:IMMediate;*wai")
            # now go to sleep for the time to take the scan
            time.sleep(len(self.frequency_list) * 2 / float(self.IFBW))

        # wait for other functions to be completed
        while self.is_busy():
            time.sleep(.01)
        # Set the format to ascii and set up sweep definitions
        self.write('FORM:ASC,0')
        # First get the A and B lists drive port 1
        # Note this could be a loop over the list = [a1_d1,b1_d1,b2_d1...,b2_d2]
        waveparameter_names=[]
        for drive_port in [self.measure_w2p_options["port1"], self.measure_w2p_options["port2"]]:
            for detect_port in [self.measure_w2p_options["port1"], self.measure_w2p_options["port2"]]:
                for receiver in ["A","B"]:
                    waveparameter_names.append("{0}{1}_D{2}".format(receiver,detect_port,drive_port))
        # now get data for all of them
        all_wave_raw_string=[]
        for waveparameter in waveparameter_names:
            self.write('CALC:PAR:SEL "{0}"'.format(waveparameter))
            self.write('CALC:FORM MLIN')
            while self.is_busy():
                time.sleep(.01)
            all_wave_raw_string .append(self.query('CALC:DATA? SDATA'))

        # Anritsu specific parsing
        for index,wave in enumerate(all_wave_raw_string):
            all_wave_raw_string[index]=re.sub("#\d+\n","",wave)

        # String Parsing
        all_wave_list=[x.replace("\n","").split(",") for x in all_wave_raw_string]
        # Construct a list of lists that is data in RI format
        re_all_wave_list = [a_list[0::2] for a_list in all_wave_list]
        im_all_wave_list = [a_list[1::2] for a_list in all_wave_list]
        wparameter_data = []
        for index, frequency in enumerate(self.frequency_list[:]):
            re_row=[re[index] for re in re_all_wave_list ]
            im_row=[im[index] for im in im_all_wave_list]
            wave_row=[]
            for index,value in enumerate(re_row):
                wave_row.append(value)
                wave_row.append(im_row[index])
            new_row = [frequency / 10. ** 9]+wave_row
            new_row = [float(x) for x in new_row]
            wparameter_data.append(new_row)
        waveparameter_column_names=[]
        for drive_port in [self.measure_w2p_options["port1"], self.measure_w2p_options["port2"]]:
            for detect_port in [self.measure_w2p_options["port1"], self.measure_w2p_options["port2"]]:
                for receiver in ["A","B"]:
                    for complex_type in ["re","im"]:
                        waveparameter_column_names.append("{3}{0}{1}_D{2}".format(receiver,
                                                                                  detect_port,
                                                                                  drive_port,
                                                                                  complex_type))
        column_names = ["Frequency"]+waveparameter_column_names
        # add some options here about auto saving
        # do we want comment options?
        options = {"column_names_begin_token": "!", "data_delimiter": "  ", "column_names": column_names,
                   "data": wparameter_data, "specific_descriptor": "Wave_Parameters",
                   "general_descriptor": "Two_Port", "extension": "w2p",
                   "column_types":["float" for column in column_names]}
        if self.measure_w2p_options["w2p_options"]:
            for key,value in self.measure_w2p_options["w2p_options"].items():
                options[key]=value
        w2p = W2P(None, **options)
        return w2p

class PowerMeter(VisaInstrument):
    """Controls power meters"""
    def initialize(self):
        """Initializes the power meter to a state with W units"""
        self.write("*RST")
        time.sleep(.1)
        self.write("UNIT:POW W")
        self.write("INIT")

    def set_frequency(self,frequency=1*10**9):
        """Sets the frequency of the power meter"""
        self.write("SENS:FREQ {0}".format(frequency))

    def get_frequency(self):
        "Returns the frequency of the power meter"
        frequency=self.query("SENS:FREQ?").replace("\n","")
        return float(frequency)

    def get_reading(self):
        """Initializes and fetches a reading"""
        self.write("INIT")
        return float(self.query("FETCh?").replace("\n",""))

    def set_units(self,unit="W"):
        """Sets the power meters units, acceptable units are W or adBM"""
        # Todo put an input checker on this to only allow desired commands
        self.write("UNIT:POW {0}".format(unit))

    def get_units(self,unit="W"):
        """Gets the power meters units"""
        # Todo put an input checker on this to only allow desired commands
        unit=self.query("UNIT:POW?").replace("\n","")
        return unit

class NRPPowerMeter(PowerMeter):
    """Controls RS power meters"""
    def initialize(self):
        """Initializes the power meter to a state with W units, 10ms aperture and Avgerage power readings"""
        self.write("*RST")
        time.sleep(.1)
        self.write("UNIT:POW W")
        self.write("SENS:FUNC POW:AVG")
        self.write("SENS:APER 10 MS")
        self.write("INIT")

class HighSpeedOscope(VisaInstrument):
    """Control Class for high speed oscilloscopes. Based on Keysight/Agilent 86100C Based on code from Diogo """

    def initialize(self, **options):
        """Initializes the oscilloscope  for data collection"""
        defaults = {"reset": True}
        initialize_options = {}
        for key, value in defaults.items():
            initialize_options[key] = value
        for key, value in options.items():
            initialize_options[key] = value
        pass

    def measure_waves(self, **options):
        """Returns data for a measurement in an AsciiDataTable"""
        defaults = {"number_frames": 1, "number_points": self.get_number_points(),
                    "timebase_scale": self.get_timebase_scale(), "channels": [1, 2, 3, 4],
                    "initial_time_offset": self.get_time_position(), "timeout_measurement": 10000,
                    "save_data": False, "data_format": "dat", "directory": os.getcwd(),
                    "specific_descriptor": "Scope", "general_descriptor": "Measurement", "add_header": False,
                    "output_table_options": {"data_delimiter": "\t", "treat_header_as_comment": True},
                    "download_format":"ASCII","verbose_timing":False,
                    }
        self.measure_options = {}
        for key, value in defaults.items():
            self.measure_options[key] = value
        for key, value in options.items():
            self.measure_options[key] = value
        if self.measure_options["verbose_timing"]:
            start_timer=datetime.datetime.now()
            print(("The .measure_waves method began at {0}".format(start_timer)))

        self.set_number_points(self.measure_options["number_points"])
        channel_string_list = ["CHAN1", "CHAN2", "CHAN3", "CHAN4"]

        # begin by setting timeout to timeout_measurement
        timeout = self.resource.timeout
        self.resource.timeout = self.measure_options["timeout_measurement"]

        # now calculate timestep
        self.measure_options["timestep"] = 10.*float(self.measure_options["timebase_scale"]) / float(self.measure_options["number_points"])
        time_step = self.measure_options["timestep"]

        # now configure the scope for data transfer
        # define the way the data is transmitted from the instrument to the PC
        # Word -> 16bit signed integer
        # now we choose if you want it to be bin or ASCII
        if re.search("asc",self.measure_options["download_format"],re.IGNORECASE):
            self.write(':WAV:FORM ASCII')
        else:
            self.write(':WAV:FORM WORD')
            # little-endian
            self.write(':WAV:BYT LSBF')
        number_rows = self.measure_options["number_points"] * self.measure_options["number_frames"]
        # this is the way diogo did it
        # number of points
        number_points = self.measure_options["number_points"]
        if self.measure_options["verbose_timing"]:
            setup_timer=datetime.datetime.now()
            time_difference=setup_timer-start_timer
            print(("The setup of the sweep finished at {0} and took {1} seconds".format(setup_timer,time_difference)))
        frames_data = []
        for frame_index in range(self.measure_options["number_frames"]):
            if self.measure_options["verbose_timing"]:
                frame_timer=datetime.datetime.now()
                time_difference=frame_timer-start_timer
                print((" Frame {0} began at {1}, {2} seconds from measure_waves begin ".format(frame_index,
                                                                                              frame_timer,
                                                                                              time_difference.seconds)))
            new_frame = []

            # calculate time position for this frame
            time_position = frame_index * self.measure_options["timebase_scale"]*10. + self.measure_options[
                "initial_time_offset"]

            # define postion to start the acquisition
            self.write(':TIM:POS {0}ns'.format(time_position))

            if self.measure_options["verbose_timing"]:
                timer=datetime.datetime.now()
                print(("Writing Channel Command at {0}".format(timer)))

            # acquire channels desired
            channel_string = ""
            for channel_index, channel in enumerate(self.measure_options["channels"]):
                if channel_index == len(self.measure_options["channels"]) - 1:
                    channel_string = channel_string + "{0}".format(channel_string_list[channel - 1])
                else:
                    channel_string = channel_string + "{0},".format(channel_string_list[channel - 1])
            channel_command = ":DIG {0}".format(channel_string)
            self.write(channel_command)

            if self.measure_options["verbose_timing"]:
                timer=datetime.datetime.now()
                print(("Finished Writing Channel Command at {0}".format(timer)))
            # trigger reading and wait
            self.write("*OPC?")

            if self.measure_options["verbose_timing"]:
                timer=datetime.datetime.now()
                print(("Finshed Trigger Command and Started to Read Channels at {0}".format(timer)))
            # get data from the necessary channels
            for channel_read_index, channel_read in enumerate(self.measure_options["channels"]):
                # get data for channel 1
                self.write(':WAV:SOUR CHAN{0}'.format(channel_read))
                # get data
                if re.search("asc", self.measure_options["download_format"], re.IGNORECASE):
                    data_column = self.resource.query(':WAV:DATA?')
                    data_column = data_column.replace("\n", "").replace("1-", "-").split(",")
                else:
                    # This downloads the data as signed 16bit ints
                    # Need a conversion to volts
                    data_column=self.resource.query_binary_values(':WAV:DATA?', datatype='h')


                new_frame.append(data_column)
                # print("{0} is {1}".format("data_column",data_column))
                if self.measure_options["verbose_timing"]:
                    timer = datetime.datetime.now()
                    print(("Finshed Data Acquistion for Channel {0} at {1}".format(channel_read,timer)))
            frames_data.append(new_frame)


        if self.measure_options["verbose_timing"]:
            timer = datetime.datetime.now()
            print(("Data Manipulation Began at {0}".format(timer)))
        # reshape measurement data
        measurement_data = [list(range(len(frames_data[0]))) for x in range(number_points * len(frames_data))]
        #         print(len(measurement_data))
        #         print(len(measurement_data[0]))
        #         print("{0} is{1}".format("len(frames_data)",len(frames_data)))
        #         print("{0} is{1}".format("len(frames_data[0])",len(frames_data[0])))
        #         print("{0} is{1}".format("len(frames_data[0][0])",len(frames_data[0][0])))
        if self.measure_options["verbose_timing"]:
            timer = datetime.datetime.now()
            print(("Data reshaping step1 ended at {0}".format(timer)))
        for frame_index, frame in enumerate(frames_data):
            for column_index, column in enumerate(frame):
                for row_index, row in enumerate(column):
                    number_rows = len(column)
                    # print("{0} is {1}".format("([row_index+frame_index*number_rows],[column_index],[frame_index])",
                    #([row_index + frame_index * number_rows], [column_index], [frame_index])))
                    measurement_data[row_index + frame_index * number_rows][column_index] =frames_data[frame_index][column_index][row_index]

        if self.measure_options["verbose_timing"]:
            timer = datetime.datetime.now()
            print(("Data reshaping step 2 ended at {0}".format(timer)))
        # reset timeout
        self.resource.timeout = timeout
        data_out = []
        time_start = self.measure_options["initial_time_offset"]

        for row_index, data_row in enumerate(measurement_data):
            new_row = [time_start + row_index * time_step] + data_row
            data_out.append(new_row)
        if self.measure_options["add_header"]:
            header = []
            for key, value in self.measure_options.items():
                header.append("{0} = {1}".format(key, value))
        else:
            header = None
        column_names = ["Time"]
        for channel in self.measure_options["channels"]:
            column_names.append(channel_string_list[channel - 1])

        table_options = {"data": data_out,
                         "header": header,
                         "specific_descriptor": self.measure_options["specific_descriptor"],
                         "general_descriptor": self.measure_options["general_descriptor"],
                         "extension": "dat",
                         "directory": self.measure_options["directory"],
                         "column_names": column_names}
        if re.search("asc",self.measure_options["download_format"],re.IGNORECASE):
            table_options["column_types"]=["float" for i in range(len(column_names))]
        else:
            table_options["column_types"]=["float"]+["int" for i in range(len(column_names)-1)]

        for key, value in self.measure_options["output_table_options"].items():
            table_options[key] = value

        output_table = AsciiDataTable(None, **table_options)

        if self.measure_options["save_data"]:
            data_save_path = auto_name(specific_descriptor=self.measure_options["specific_descriptor"],
                                       general_descriptor=self.measure_options["general_descriptor"],
                                       directory=self.measure_options["directory"],
                                       extension='dat'
                                       , padding=3)
            output_table.path = data_save_path
            output_table.save()

        if self.measure_options["verbose_timing"]:
            timer = datetime.datetime.now()
            print(("Data Manipulation Ended at {0}".format(timer)))

        return output_table


    def get_error_state(self):
        """Returns the error state of the oscope"""
        state = self.query(':SYSTEM:ERROR? STRING')
        self.error_state = state
        return state


    def set_number_points(self, number_points=16384):
        """Sets the number of points for the acquisition"""
        self.write(':ACQ:POINTS {0}'.format(number_points))


    def get_number_points(self):
        """Returns the number of points in the waveform"""
        number_points = int(self.query(':ACQ:POINTS?'))
        return number_points


    def set_time_position(self, time=50):
        """Sets the time in ns to start the acquisition"""
        self.write(':TIM:POS {0}ns'.format(time))


    def get_time_position(self):
        """Returns the time position in ns"""
        position = float(self.query(":TIM:POS?"))
        return position * 10 ** 9


    def set_timebase_scale(self, time_scale=40.96):
        """Sets the timebase scale in ns"""
        self.write(':TIM:SCAL {0}ns'.format(time_scale))


    def get_timebase_scale(self):
        """Returns the timebase scale in ns"""
        time_scale = float(self.query(':TIM:SCAL?'))
        return time_scale * 10 ** 9


    def set_trigger_source(self, source="FPAN"):
        """Sets the tigger source, 'FPAN' Frontpanel or 'FRUN' freerun"""
        self.write(':TRIG:SOUR {0}'.format(source))


    def get_trigger_source(self):
        """Returns the trigger source FPAN for FrontPanel or FRUN for free run"""
        source = self.query(':TRIG:SOUR?')


    def set_trigger_level(self, level=10):
        """Sets the trigger level in mv"""
        self.write(':TRIG:LEV {0}m'.format(level))


    def get_trigger_level(self):
        """Returns the trigger level"""
        level = self.query(':TRIG:LEV?')


    def set_channel_scale(self, scale=10, channel=1):
        """Sets the scale in mv of channel. Default is 10mv/division on channel 1"""
        self.write(':CHAN{0}:SCAL {1}m'.format(channel, scale))


    def get_channel_scale(self, channel=1):
        "Returns the scale for a specified channel, the default is channel 1"
        scale = self.query(':CHAN{0}:SCAL?'.format(channel))
        return scale

    def set_channel_offset(self, offset=0, channel=1):
        """Sets the scale in mv of channel. Default is 10mv/division on channel 1"""
        self.write(':CHAN{0}:OFFSet {1}'.format(channel, offset))


    def get_channel_offset(self, channel=1):
        "Returns the scale for a specified channel, the default is channel 1"
        offset = self.query(':CHAN{0}:OFFSet?'.format(channel))
        return offset

    def set_channel_bandwidth(self, bandwidth="LOW", channel=1):
        """Sets the specified channel's bandwith to LOW, MED or HIGH, default is to set channel 1 to LOW"""
        self.write(':CHAN{0}:BAND {1}'.format(channel, bandwidth))


    def get_channel_bandwidth(self, channel=1):
        """Returns the selected channels bandwidth"""
        bandwidth = self.query(':CHAN{0}:BAND?'.format(channel))
        return bandwidth


    def set_trigger_slope(self, slope="POS"):
        """Sets the trigger slope on the oscope choose from POS or NEG"""
        self.write(':TRIG:SLOP {0}'.format(slope))


    def get_trigger_slope(self):
        """Returns the trigger slope either POS or NEG"""
        slope = self.query(":TRIG:SLOP?")
        return slope


#-------------------------------------------------------------------------------
# Module Scripts

def test_determine_instrument_type():
    print('Type is %s'%determine_instrument_type('GPIB::22'))
    print('Type is %s'%determine_instrument_type('COMM::1'))
    print('Type is %s'%determine_instrument_type('CoMm::1')) 
    print('Type is %s'%determine_instrument_type('SRS830')) 
    print('Type is %s'%determine_instrument_type('36111')) 
    class blank():pass
    new=blank()
    print(type(new))
    print('Type is %s'%determine_instrument_type(new))
    new.instrument_type='Ocean_Optics'
    print(new.instrument_type)
    print('Type is %s'%determine_instrument_type(new))
    TF=(isinstance(new, InstanceType) or ClassType)
    print(TF)
    print(dir(new))
    print('instrument_type' in dir(new))
        


def test_find_description():
    """Tests the function find description"""
    print("The path of the description of %s is %s"%('Lockin2',find_description('Lockin2')))
    print("The File Contents are:")
    print(find_description('Lockin2','file'))
     
def test_VisaInstrument(address="GPIB::21"):
    """ Simple test of the VisaInstrument class"""
    instrument=VisaInstrument(address)
    #print instrument.ask('*IDN?')
    print(dir(instrument))
    print(instrument.idn)
    print(instrument.DEFAULT_STATE_QUERY_DICTIONARY)
    print(instrument.current_state)
    print('Writing 0 volts to AUX4')
    instrument.set_state(state_dictionary={'AUXV 4,':0})
    print(instrument.current_state)
    print(instrument.state_buffer)
    print(instrument.commands)

#-------------------------------------------------------------------------------
# Module Runner       

if __name__ == '__main__':
    #test_IV()
    #test_find_description()
    test_VisaInstrument()
    #user_terminate=raw_input("Please Press Any key To Finish:")
    
