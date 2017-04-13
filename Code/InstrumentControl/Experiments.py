#-----------------------------------------------------------------------------
# Name:        Experiments.py
# Purpose:     To control experiments.
#
# Author:      Aric Sanders
# Created:     2016/06/23
# Licence:     MIT
#-----------------------------------------------------------------------------
""" Experiments is a base module for controlling experiments"""

#-------------------------------------------------------------------------------
# Standard Imports
import os
import time
import datetime
import sys

#-------------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
# try:
#     import pyMeasure
# except:
#     print("The topmost pyMeasure folder was not found please make sure that the directory directly above it is on sys.path")
#     raise

try:
    import Code.InstrumentControl.Instruments
    import Code.DataHandlers.XMLModels
except:
    print "This module requires pyMeasure.Code to be on sys.path"
    raise

try: 
    from scipy import linspace,stats
except:
    print """ This module uses scipy linspace, if scipy is not available you must
    define your own linspace function under this comment"""
    raise
#-------------------------------------------------------------------------------
# Module Constants

PYMEASURE_ROOT=os.path.join(os.path.dirname( __file__ ), '..','..')
"Root directory of pyMeasure"
KEITHLEY_INSTRUMENT_SHEET=os.path.join(PYMEASURE_ROOT,
'Instruments','KEITHLEY6487_NSOM.xml').replace('\\','/')
"The file path to the Keithley 6487 instrument sheet."


#-------------------------------------------------------------------------------
# Module Classes

class KeithleyIV():
    """ This class is for an experiment consisting of the Keithley piccoammeter 
    taking a two point measurement using its internal voltage source written 02/2011"""
    
    def __init__(self):
        """ initializes the KeithleyIV experiment class"""
        try:
            self.instrument=Code.InstrumentControl.Instruments.VisaInstrument('Keithley')
        except:
            print 'Entering Fake Mode'
            pass
        self.notes=''
        self.name=''
        self.data_list=[]
        self.data_dictionary={}
        pass
    def initialize_keithley(self):
        """Sends intialization string to Keithley picoammeter"""
        try:
            initialize_list=["*RST","FUNC 'CURR'","SYST:ZCH:STAT ON",
            "CURR:RANG 2E-4","INIT","SYST:ZCOR:STAT OFF","SYST:ZCOR:ACQ",
            "SYST:ZCH:STAT OFF","SYST:ZCOR ON","SOUR:VOLT:STAT ON",
            "FORM:ELEM ALL","CURR:RANG:AUTO ON"]
            
            for command in initialize_list:
                self.instrument.write(command)
            # TODO: Check for Instrument Errors
            
        except:
            print('An error intializing the keithley has occurred')
        
    def write_voltage(self,voltage):
        """Sets the Keithley to a specified voltage """
        try:
            self.instrument.write("SOUR:VOLT "+str(voltage))
            
        except:
            print('An error talking to the keithley has occurred')    
            
    def make_voltage_list(self,start,stop,number_points,bowtie=False):
         """ Makes a voltage sweep list given stop,start,number_of_points
         and a boolen that determines if all sweeps begin and end on zero"""
         if not bowtie:
            try:
                if (type(start)!=float or type(stop)!=float or type(number_points)!=float):
                    [start,stop,number_points]=map(lambda x: float(x),[start,stop,number_points])
                voltage_array=linspace(start,stop,number_points)
                voltage_list=voltage_array.tolist()
                return voltage_list
            except:
                print "make_voltage_list failed"
         elif bowtie:
            try:
                if (type(start)!=float or type(stop)!=float or type(number_points)!=float):
                    [start,stop,number_points]=map(lambda x: float(x),[start,stop,number_points])
                array_1=linspace(float(0),start,number_points)
                list_1=array_1.tolist()
                array_2=linspace(float(0),stop,number_points)
                list_2=array_2.tolist()
                voltage_list=array_1.tolist()
                list_1.reverse()
                voltage_list=voltage_list+list_1
                voltage_list=voltage_list+list_2
                list_2.reverse()
                voltage_list=voltage_list+list_2
                return voltage_list 
            except:
                raise
                print "make_voltage_list failed"    
    def take_IV(self,voltage_list,auto_range=True,settle_time=.02):
        """ Method for taking an IV"""
        self.data_list=[]
        if auto_range:
            for index,v in enumerate(voltage_list):
                self.write_voltage(v)
                
                time.sleep(settle_time)
                self.current_reading=self.instrument.ask('READ?') 
                current=self.current_reading.split(',')[0]
                current=current.replace('A','')   
                self.data_list.append({'Index':index,
                'Voltage':self.current_reading.split(',')[-1].replace("\n",""),
                'Current':current})
                self.instrument.write("CURR:RANG:AUTO ON")
    def save_data(self):
        """ Saves the data in xml format"""
##        self.current_state=pyMeasure.Code.DataHandlers.States.InstruemntState(**self.instrument.get_state())
##        self.current_state.add_state_description({'Instrument_Description':self.instrument.path})
##        self.current_state.save()
        self.calculate_resistance()
        self.data_dictionary['Data_Description']={'Current':'Current in Amps',
        'Voltage':'Voltage in Volts','Index':'Order in which the point was taken',
        'Instrument_Description':KEITHLEY_INSTRUMENT_SHEET,
        'Date':datetime.datetime.utcnow().isoformat(),
        'Notes':self.notes,'Name':self.name,'Resistance':str(self.resistance)}
        self.data_dictionary['Data']=self.data_list
        self.state=Code.DataHandlers.XMLModels.InstrumentState(None,state_dictionary=self.instrument.get_state(),
                                                               style_sheet=os.path.join(Code.DataHandlers.XMLModels.TESTS_DIRECTORY,
                                                                                             "../XSL/DEFAULT_STATE_STYLE.xsl"))
        self.state.add_state_description(description={"State_Description":{"Instrument_Description":KEITHLEY_INSTRUMENT_SHEET}})
        self.data_dictionary["Data_Description"]["State"]="./"+self.state.path
        self.state.save()
        self.measurement_data=Code.DataHandlers.XMLModels.DataTable(None,data_dictionary=self.data_dictionary,
                                                                    style_sheet=os.path.join(Code.DataHandlers.XMLModels.TESTS_DIRECTORY,
                                                                                             "../XSL/DEFAULT_MEASUREMENT_STYLE.xsl"))
        self.measurement_data.save()   
        
    def plot_data(self):
        voltage_list=[]
        current_list=[]
        for data in self.data_list:
            voltage_list.append(float(data['Voltage']))
            current_list.append(float(data['Current']))
        try:
            
            import matplotlib.pyplot as plt
            fig=plt.figure("IV")
            plt.plot(voltage_list,current_list)
            plt.xlabel("Voltage (V)")
            plt.ylabel("Current (A)")
            plt.show()
            return fig
        except:
            raise
            print('An Error in the function plot has occurred')

    def calculate_resistance(self):
        voltage_list=[]
        current_list=[]
        for data in self.data_list:
            voltage_list.append(float(data['Voltage']))
            current_list.append(float(data['Current']))
        [a,b,ar,br,err]=stats.linregress(voltage_list,current_list)
        self.resistance=1/a     
             
#-------------------------------------------------------------------------------
# Module Scripts

def test_KeithleyIV():
    """ Tests the keithleyIV class"""
    experiment=KeithleyIV()
    print experiment.make_voltage_list(-1,1,100)
    print experiment.make_voltage_list(-1,1,100,True)
    fake_list=experiment.make_voltage_list(-1,1,10,True)
    for index,voltage in enumerate(fake_list):
        
        current=voltage/12000.1
        experiment.data_list.append({'Index':index,'Voltage':voltage,'Current':current})
    experiment.notes='This is fake Data'
    #experiment.save_data()
    experiment.plot_data()
#-------------------------------------------------------------------------------
# Module Runner



if __name__ == '__main__':
    test_KeithleyIV()
