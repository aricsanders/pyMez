#-----------------------------------------------------------------------------
# Name:        NISTUncertainty
# Purpose:     To hold the uncertainty functions associated with sparameters and impedance
# Author:      Aric Sanders
# Created:     11/3/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" This module contains definitions for uncertainty analysis for NIST sparameter impedance"""

#-----------------------------------------------------------------------------
# Standard Imports
import sys
import os
import re
import math
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
#-----------------------------------------------------------------------------
# Module Constants
CONNECTOR_TYPES=['14 mm','7 mm', 'Type-N','3.5 mm', '2.92 mm', '2.4mm', '1.85 mm','1.0 mm',
                 'WR90','WR62','WR42','WR28','WR22','WR15','WR10']
#-----------------------------------------------------------------------------
# Module Functions
def coax_s11_S_NIST(connector_type='Type-N',frequency=1.0):
    """Calculates S_NIST, for S11 in coax systems"""
    if re.search('14',connector_type,re.IGNORECASE):
        uncertainty_magnitude=.0005
        uncertainty_phase=math.atan(uncertainty_magnitude)
    elif re.search('7',connector_type,re.IGNORECASE):
        uncertainty_magnitude=10.0**(-3.303+.025*frequency)
        uncertainty_phase=math.atan(uncertainty_magnitude)
    elif re.search('N',connector_type,re.IGNORECASE):
        uncertainty_magnitude=10.0**(-3.327+.046*frequency)
        uncertainty_phase=math.atan(uncertainty_magnitude)
    elif re.search('3.5',connector_type,re.IGNORECASE):
        uncertainty_magnitude=10.0**(-3.281+.03*frequency)
        uncertainty_phase=math.atan(uncertainty_magnitude)
    elif re.search('2.9',connector_type,re.IGNORECASE):
        uncertainty_magnitude=10.0**(-3.281+.03*frequency)
        uncertainty_phase=math.atan(uncertainty_magnitude)
    elif re.search('2.4',connector_type,re.IGNORECASE):
        # TODO: Fix this, the printed version is blurry
        uncertainty_magnitude=10.0**(-3.281+.03*frequency)
        uncertainty_phase=math.atan(uncertainty_magnitude)
    return [uncertainty_magnitude,uncertainty_phase]

def coax_s11_type_b(connector_type='Type-N',frequency=1.0,magnitude_S11=1.0):
    """Calculates Type-B uncertainties for S11 in a coax system"""
    Dx=.001*(1.61+.07*math.sqrt(frequency)+.04/frequency)+.0012
    Dy=.001*(.01*frequency+.04/frequency)
    uncertainty_m1=math.sqrt(Dx**2+Dy**2)
    uncertainty_m2=.00008/frequency
    uncertainty_m3=.1651*math.sqrt(frequency)*5.*6*10**6/(.35*math.sqrt((1.4*10**7)**3))
    delta=math.sqrt((uncertainty_m1**2+uncertainty_m2**2+uncertainty_m3**2)/3)
    uncertainty_arg1=math.atan(uncertainty_m1/magnitude_S11)
    uncertainty_arg2=math.atan(uncertainty_m2/magnitude_S11)
    uncertainty_arg3=12.0115*frequency*.0025
    delta_arg=math.sqrt((uncertainty_arg1**2+uncertainty_arg2**2+uncertainty_arg3**2)/3)
    if re.search('14',connector_type,re.IGNORECASE):
        uncertainty_magnitude=delta
        uncertainty_phase=.5*delta_arg
    elif re.search('7',connector_type,re.IGNORECASE):
        uncertainty_magnitude=delta
        uncertainty_phase=delta_arg
    elif re.search('N',connector_type,re.IGNORECASE):
        uncertainty_magnitude=delta
        uncertainty_phase=delta_arg
    elif re.search('3.5',connector_type,re.IGNORECASE):
        uncertainty_magnitude=2*delta
        uncertainty_phase=2*delta_arg
    elif re.search('2.9',connector_type,re.IGNORECASE):
        uncertainty_magnitude=2.4*delta
        uncertainty_phase=2.4*delta_arg
    elif re.search('2.4',connector_type,re.IGNORECASE):
        uncertainty_magnitude=2.92*delta
        uncertainty_phase=2.92*delta_arg
    return [uncertainty_magnitude,uncertainty_phase]

def waveguide_s11_S_NIST(waveguide_type='WR90'):
    """Caluclates the S NIST Uncertainity for S11 on waveguide systems"""
    if re.search('90|62|42|28',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.0015
        uncertainty_phase=.09
    elif re.search('22|15',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.003
        uncertainty_phase=.17
    elif re.search('10',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.004
        uncertainty_phase=.23
    return [uncertainty_magnitude,uncertainty_phase]

def waveguide_s11_type_b(waveguide_type='WR90',magnitude_S11=1.0):
    """Calculates type B uncertainties for waveguides"""
    if re.search('90',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.003*(1.0+magnitude_S11**2)/math.sqrt(3.)
        uncertainty_phase=math.sqrt(math.atan(uncertainty_magnitude/(magnitude_S11+.001))**2+0.2**2/3.)
    elif re.search('62',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.003*(1.0+magnitude_S11**2)/math.sqrt(3.)
        uncertainty_phase=math.sqrt(math.atan(uncertainty_magnitude/(magnitude_S11+.001))**2+0.5**2/3.)
    elif re.search('42',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.002*(1.0+magnitude_S11**2)/math.sqrt(3.)
        uncertainty_phase=math.sqrt(math.atan(uncertainty_magnitude/(magnitude_S11+.001))**2+0.85**2/3.)
    elif re.search('28',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.002*(1.0+magnitude_S11**2)/math.sqrt(3.)
        uncertainty_phase=math.sqrt(math.atan(uncertainty_magnitude/(magnitude_S11+.001))**2+1.0**2/3.)
    elif re.search('22',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.004*(1.0+magnitude_S11**2)/math.sqrt(3.)
        uncertainty_phase=math.sqrt(math.atan(uncertainty_magnitude/(magnitude_S11+.001))**2+1.53**2/3.)
    elif re.search('15',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.004*(1.0+magnitude_S11**2)/math.sqrt(3.)
        uncertainty_phase=math.sqrt(math.atan(uncertainty_magnitude/(magnitude_S11+.001))**2+2.29**2/3.)
    elif re.search('10',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.005*(1.0+magnitude_S11**2)/math.sqrt(3.)
        uncertainty_phase=math.sqrt(math.atan(uncertainty_magnitude/(magnitude_S11+.001))**2+3.36**2/3.)
    return [uncertainty_magnitude,uncertainty_phase]




def S_NIST(connector_type='Type-N', frequency=1, s_parameter='S11',magnitude=1.0, phase=0):
    """S_NIST calculates the Standard NIST uncertainty given the connector_type, parameter (S11,S12 or Power)
     frequency, magnitude and phase"""
    pass


#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass