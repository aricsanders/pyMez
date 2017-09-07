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
import sys

#-------------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
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
    import Code.DataHandlers.XMLModels
    InstrumentSheet=Code.DataHandlers.XMLModels.InstrumentSheet
    InstrumentState=Code.DataHandlers.XMLModels.InstrumentState
    DATA_SHEETS=1
    #print dir(pyMeasure)
except:
    # If the import of DataHandlers Does not work 
    class  InstrumentSheet():pass
    DATA_SHEETS=0
    print "Can't Find MySelf"
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
    print("Could not load pyMeasure.Code.Utils.Names")
    pass
try:
    from Code.DataHandlers.TouchstoneModels import *
except:
    print("Could not load Code.DataHandlers.TouchstoneModels")
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
                
def find_description(identifier,output='path',directory=None):
    """ Finds an instrument description in pyMeasure/Instruments given an identifier, 
    outputs a path or the file. Right now this outputs the first sheet that matches the identifier"""
    if type(identifier) in StringTypes:
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


class FakeInstrument(InstrumentSheet):
    """ General Class to communicate with COMM and GPIB instruments
    This is a blend of the pyvisa resource and an xml description. """

    def __init__(self, resource_name=None, **options):
        """ Intializes the VisaInstrument Class"""
        defaults = {"state_directory": os.getcwd(),
                    "instrument_description_directory": os.path.join(PYMEASURE_ROOT, 'Instruments')}
        self.options = {}
        for key, value in defaults.iteritems():
            self.options[key] = value
        for key, value in options.iteritems():
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
            for state_command, value in state_dictionary.iteritems():
                self.write(state_command + ' ' + str(value))
            self.current_state = self.get_state()
        if state_table:
            if "Index" in state_table[0].keys():
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
                          in state_query_dictionary.iteritems()])
            return state
        else:
            # a state_query_table is a list of dictionaries, each row has at least a Set and Query key but could
            # have an Index key that denotes order
            if "Index" in state_query_table[0].keys():
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
        print("Fake Instrument has been closed")
        
class VisaInstrument(InstrumentSheet):
    """ General Class to communicate with COMM and GPIB instruments
    This is a blend of the pyvisa resource and an xml description. """
    def __init__(self,resource_name=None,**options):
        """ Intializes the VisaInstrument Class"""
        defaults={"state_directory":os.getcwd(),
                  "instrument_description_directory":os.path.join(PYMEASURE_ROOT,'Instruments')}
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
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
        
        self.resource_manager=visa.ResourceManager()
        # Call the visa instrument class-- this gives ask,write,read
        self.resource=self.resource_manager.open_resource(self.instrument_address)
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
        """ Sets the instrument to the state specified by Command:Value pairs"""
        if state_dictionary:
            if len(self.state_buffer)+1<self.STATE_BUFFER_MAX_LENGTH:
                self.state_buffer.append(self.get_state())
            else:
                self.state_buffer.pop(1)
                self.state_buffer.insert(-1,self.get_state())
            for state_command,value in state_dictionary.iteritems():
                self.write(state_command+' '+str(value))
            self.current_state=self.get_state()
        if state_table:
            if "Index" in state_table[0].keys():
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
            in state_query_dictionary.iteritems()])
            return state
        else:
            # a state_query_table is a list of dictionaries, each row has at least a Set and Query key but could
            # have an Index key that denotes order
            if "Index" in state_query_table[0].keys():
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
        
    def save_state(self,state_path=None,state_dictionary=None,state_table=None):
        """ Saves any state dictionary to an xml file, with state_path, if not specified defaults to autonamed state
         """
        if state_path is None:
            state_path=auto_name(specific_descriptor=self.name,general_descriptor="State",
                                 directory=self.options["state_directory"])
        if state_dictionary:
            new_state=InstrumentState(None,**{"state_dictionary":state_dictionary,
                                              "style_sheet":"./DEFAULT_STATE_STYLE.xsl"})
        elif state_table:
            new_state=InstrumentState(None,**{"state_table":state_table,
                                              "style_sheet":"./DEFAULT_STATE_STYLE.xsl"})
        else:
            new_state=InstrumentState(None,**{"state_dictionary":self.get_state(),
                                              "style_sheet":"./DEFAULT_STATE_STYLE.xsl"})

        try:
            new_state.add_state_description()
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
        for key, value in defaults.iteritems():
            self.options[key] = value
        for key, value in options.iteritems():
            self.options[key] = value
        VisaInstrument.__init__(self, resource_name, **self.options)
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
        elif re.search("LIN", self.sweep_type, re.IGNORECASE):
            start = float(self.query("SENS:FREQ:START?").replace("\n", ""))
            stop = float(self.query("SENS:FREQ:STOP?").replace("\n", ""))
            number_points = int(self.query("SENS:SWE:POIN?").replace("\n", ""))
            logspace_start = np.log10(start)
            logspace_stop = np.log10(stop)
            self.frequency_list = map(lambda x: round(x, ndigits=3), np.logspace(logspace_start, logspace_stop,
                                                                                 num=number_points, base=10).tolist())
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
        """Intializes the system"""
        defaults = {"reset":True}
        initialize_options = {}
        for key, value in defaults.iteritems():
            initialize_options[key] = value
        for key, value in options:
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
        elif re.search("LIN", self.sweep_type, re.IGNORECASE):
            start = float(self.query("SENS:FREQ:START?").replace("\n", ""))
            stop = float(self.query("SENS:FREQ:STOP?").replace("\n", ""))
            number_points = int(self.query("SENS:SWE:POIN?").replace("\n", ""))
            logspace_start = np.log10(start)
            logspace_stop = np.log10(stop)
            self.frequency_list = map(lambda x: round(x, ndigits=3), np.logspace(logspace_start, logspace_stop,
                                                                                 num=number_points, base=10).tolist())
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
        for unit in VNA_FREQUENCY_UNIT_MULTIPLIERS.keys():
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
        for unit in VNA_FREQUENCY_UNIT_MULTIPLIERS.keys():
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
        print("{0} is {1}".format("number_segments", number_segments))
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
            print("{0} is {1}".format("difference", difference))
            while (difference != 0):
                self.write("SENS:SEGM{0}:ADD".format(max_segment))
                max_segment += 1
                difference -= 1
                print("{0} is {1}".format("difference", difference))
        else:
            pass

        for row_index, row in enumerate(self.frequency_table[:]):
            [start, stop, number_points] = [row["start"], row["stop"], row["number_points"]]
            # SENSe<cnum>:SEGMent<snum>:SWEep:POINts <num>
            self.write("SENS:SEGM{0}:FREQ:START {1}".format(row_index + 1, start))
            self.write("SENS:SEGM{0}:FREQ:STOP {1}".format(row_index + 1, stop))
            self.write("SENS:SEGM{0}:SWE:POIN {1}".format(row_index + 1, number_points))
            self.write("SENS:SEGM{0}:STAT ON".format(row_index + 1))

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

        for unit in VNA_FREQUENCY_UNIT_MULTIPLIERS.keys():
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
            self.frequency_list = map(lambda x: round(x, ndigits=3), np.logspace(logspace_start, logspace_stop,
                                                                                 num=number_points, base=10).tolist())
        else:
            self.write('SENS:SWE:TYPE LIN')
            self.frequency_list = map(lambda x: round(x, ndigits=3),
                                      np.linspace(start, stop, number_points).tolist())
        self.write("SENS:FREQ:START {0}".format(start))
        self.write("SENS:FREQ:STOP {0}".format(stop))
        self.write("SENS:SWE:POIN {0}".format(number_points))

    def get_frequency(self):
        "Returns the frequency in python list format"
        return self.frequency_list

    def is_busy(self):
        """Checks if the instrument is currently doing something and returns a boolean value"""
        opc = bool(self.resource.query("*OPC?"))
        return not opc

    def measure_switch_terms(self, **options):
        """Measures switch terms and returns a s2p table in forward and reverse format"""
        defaults = {"view_trace":True}
        self.measure_switch_term_options = {}
        for key, value in defaults.iteritems():
            self.measure_switch_term_options[key] = value
        for key, value in options:
            self.measure_switch_term_options[key] = value
        # this resets the traces to be based on swith terms
        # Set VS to be remotely triggered by GPIB
        self.write("SENS:HOLD:FUNC HOLD")
        self.write("TRIG:REM:TYP CHAN")
        # Set the Channel to have 2 Traces
        self.write("CALC1:PAR:COUN 2")
        # Trace 1 This is port 2 or Forward Switch Terms
        self.write("CALC1:PAR:DEF 'FWD',R2,1") # note this command is different for vector star A2,B2
        if self.measure_switch_term_options["view_trace"]:
            self.write("DISPlay:WINDow1:TRACe5:FEED 'FWD'")
        # Trace 2 This is port 1 or Reverse Switch Terms
        self.write("CALC1:PAR:DEF 'REV',R1,2")
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
        self.write("FORM:DATA ASC")
        # Read in the data
        self.write("CALC:PAR:SEL FWD;")
        foward_switch_string = self.query("CALC:DATA? SDATA")
        while self.is_busy():
            time.sleep(.01)
        self.write("CALC:PAR:SEL REV;")
        reverse_switch_string = self.query("CALC:DATA? SDATA")
        # Now parse the string
        foward_switch_list = foward_switch_string.replace("\n", "").split(",")
        reverse_switch_list = reverse_switch_string.replace("\n", "").split(",")
        real_foward = foward_switch_list[0::2]
        imaginary_forward = foward_switch_list[1::2]
        real_reverse = reverse_switch_list[0::2]
        imaginary_reverse = reverse_switch_list[1::2]
        switch_data = []
        for index, frequency in enumerate(self.frequency_list[:]):
            new_row = [frequency,
                       real_foward[index], imaginary_forward[index],
                       real_reverse[index], imaginary_reverse[index],
                       0, 0,
                       0, 0]
            new_row = map(lambda x: float(x), new_row)
            switch_data.append(new_row)
        option_line = "# Hz S RI R 50"
        # add some options here about auto saving
        # do we want comment options?
        s2p = S2PV1(None, option_line=option_line, data=switch_data)
        s2p.change_frequency_units(self.frequency_units)
        return s2p

    def measure_sparameters(self, **options):
        """Triggers a single sparameter measurement for all 4 parameters and returns a SP2V1 object"""
        defaults = {"trigger": "single"}
        self.measure_sparameter_options = {}
        for key, value in defaults.iteritems():
            self.measure_sparameter_options[key] = value
        for key, value in options:
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
        self.write('FORM:ASCII')
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
        # String Parsing
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
            new_row = map(lambda x: float(x), new_row)
            sparameter_data.append(new_row)
        option_line = "# Hz S RI R 50"
        # add some options here about auto saving
        # do we want comment options?
        s2p = S2PV1(None, option_line=option_line, data=sparameter_data)
        s2p.change_frequency_units(self.frequency_units)
        return s2p

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
    
