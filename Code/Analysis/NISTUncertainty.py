#-----------------------------------------------------------------------------
# Name:        NISTUncertainty
# Purpose:     To hold the uncertainty functions associated with sparameters and impedance
# Author:      Aric Sanders
# Created:     11/3/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" This module contains definitions for uncertainty analysis for NIST sparameter impedance.
It follows uncertainty equations originally found in the calrep hp basic program, and
is primarily used in the function calrep see also <a href="./SParameter.m.html">SParameter</a>.



Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html)
+ [re](https://docs.python.org/2/library/re.html)
+ [numpy](https://docs.scipy.org/doc/)
+ [math](https://docs.python.org/2/library/math.html)


Help
---------------
<a href="./index.html">`pyMez.Code.Analysis`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>

"""

#-----------------------------------------------------------------------------
# Standard Imports
import sys
import os
import re
import math
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    import numpy as np
except:
    print("The module numpy was not found,"
          "please put it on the python path")
    raise ImportError
#-----------------------------------------------------------------------------
# Module Constants
CONNECTOR_TYPES=['14 mm','7 mm', 'Type-N','3.5 mm', '2.92 mm', '2.4mm', '1.85 mm','1.0 mm',
                 'WR90','WR62','WR42','WR28','WR22','WR15','WR10']
"""Constant containing acceptable connector and waveguide types"""
# the smallest value allowed in dB (0 in linear magnitude)
MINIMUM_DB=100
"""The smallest value in dB for a linear magnitude of zero. Note this one is positive,
which is different than touchstone models definition."""

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
        uncertainty_magnitude=1/(400.-.75*frequency*math.exp(.04*frequency))
        uncertainty_phase=math.atan(uncertainty_magnitude)
    else:
        uncertainty_magnitude=1/(400.-.75*frequency*math.exp(.04*frequency))
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
    else:
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
    else:
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
    else:
        uncertainty_magnitude=.005*(1.0+magnitude_S11**2)/math.sqrt(3.)
        uncertainty_phase=math.sqrt(math.atan(uncertainty_magnitude/(magnitude_S11+.001))**2+3.36**2/3.)
    return [uncertainty_magnitude,uncertainty_phase]


def coax_s12_S_NIST(connector_type='N',frequency=1,magnitude_S21=10,format='DB'):
    """Calculates SNIST for connector type, power and frequency"""
    frequency=float(frequency)
    if re.search('mag',format,re.IGNORECASE):
        # if the format is mag then change the number to db
        magnitude=magnitude_S21
        try:
            magnitude_S21=-20.*math.log10(magnitude_S21)
        except:
            magnitude_S21=MINIMUM_DB
    if re.search('14',connector_type,re.IGNORECASE):
        if magnitude_S21>=0 and magnitude_S21<25:
            uncertainty_magnitude=.0005+.00035*frequency
            uncertainty_phase=.02+.0153*frequency
        elif magnitude_S21>=25 and magnitude_S21<40:
            uncertainty_magnitude=.02
            uncertainty_phase=.1+.017*frequency
        elif magnitude_S21>=40 and magnitude_S21<65:
            uncertainty_magnitude=.02+.00015*(magnitude_S21-40.)**2
            uncertainty_phase=.1+.017*frequency
        else:
            uncertainty_magnitude=.004
        #enforce min uncertainties
        if uncertainty_magnitude<.004:
            uncertainty_magnitude=.004

    elif re.search('7',connector_type,re.IGNORECASE):
        if magnitude_S21>=0 and magnitude_S21<25:
            if frequency>=.01 and frequency<1.:
                uncertainty_magnitude=10.**(-3.06+.051*frequency)
                uncertainty_phase=10.**(-1.95+.792*frequency)
            elif frequency>=1. and frequency<=18.:
                uncertainty_magnitude=10.**(-2.816+.038*frequency)
                uncertainty_phase=10.**(-.927+.023*frequency)
        elif magnitude_S21>=25 and magnitude_S21<40:
            if frequency>=.01 and frequency<1.:
                uncertainty_magnitude=.02
                uncertainty_phase=10.**(-.96+.259*frequency)
            elif frequency>=1. and frequency<=18.:
                uncertainty_magnitude=.02
                uncertainty_phase=.1+.017*frequency
        elif magnitude_S21>=40 and magnitude_S21<65:
            if frequency>=.01 and frequency<1.:
                uncertainty_magnitude=.02+.00015*(magnitude_S21-40)**2
                uncertainty_phase=10.**(-.96+.259*frequency)
            elif frequency>=1. and frequency<=18.:
                uncertainty_magnitude=.02+.00015*(magnitude_S21-40)**2
                uncertainty_phase=.1+.017*frequency
        else:
            uncertainty_phase=.1+.017*frequency
            uncertainty_magnitude=.004
        #enforce min uncertainties
        if uncertainty_magnitude<.004:
            uncertainty_magnitude=.004

    elif re.search('N',connector_type,re.IGNORECASE):
        if magnitude_S21>=0 and magnitude_S21<25:
            uncertainty_magnitude=10.**(-2.17+.024*frequency)
            uncertainty_phase=10.**(-1.138+.032*frequency)
        elif magnitude_S21>=25 and magnitude_S21<40:
            uncertainty_magnitude=.02
            uncertainty_phase=.1+.017*frequency
        elif magnitude_S21>=40 and magnitude_S21<65:
            uncertainty_magnitude=.02+.00015*(magnitude_S21-40.)**2
            uncertainty_phase=.1+.017*frequency
        else:
            uncertainty_magnitude=.02+.00015*(magnitude_S21-40.)**2
            uncertainty_phase=.1+.017*frequency
        #enforce min uncertainties
        if uncertainty_magnitude<.004:
            uncertainty_magnitude=.004
    elif re.search('3.5|2.92|2.4',connector_type,re.IGNORECASE):
        # All of the following cases have the same phase uncertainty
        uncertainty_phase=.1+.0098*frequency
        if re.search('3.5|2.92',connector_type,re.IGNORECASE):
            # 3.5mm and 2.92mm have the same mag relations
            if magnitude_S21>=0 and magnitude_S21<25:
                uncertainty_magnitude=.0005+.00027*frequency
            elif magnitude_S21>=25 and magnitude_S21<40:
                uncertainty_magnitude=.02
            elif magnitude_S21>=40 and magnitude_S21<65:
                uncertainty_magnitude=.02+.00015*(magnitude_S21-40.)**2
            else:
                uncertainty_magnitude = .0005 + .00027 * frequency
        elif re.search('2.4',connector_type,re.IGNORECASE):
            # 3.5mm and 2.92mm have the same mag relations
            if magnitude_S21>=0 and magnitude_S21<25:
                uncertainty_magnitude=.01+.0004*frequency
            elif magnitude_S21>=25 and magnitude_S21<40:
                uncertainty_magnitude=.03
            elif magnitude_S21>=40 and magnitude_S21<65:
                uncertainty_magnitude=.03+.00015*(magnitude_S21-40.)**2
            else:
                uncertainty_magnitude = .01 + .0004 * frequency
    else:
        uncertainty_magnitude=.002
        uncertainty_phase=.01
        #enforce min uncertainties
    if uncertainty_magnitude<.002:
        uncertainty_magnitude=.002
    #enforce min uncertainties
    if uncertainty_phase<.01:
        uncertainty_phase=.01
    if re.search('mag',format,re.IGNORECASE):
        # if the format is mag then change the uncertainty back to mag
        uncertainty_magnitude=abs((1./math.log10(math.e))*magnitude*uncertainty_magnitude/20.)
    return [uncertainty_magnitude,uncertainty_phase]

def coax_s12_type_b(connector_type='N',frequency=1,magnitude_S21=10,format='DB'):
    """Calculates the type-b uncertainty for coax connecters"""
    if re.search('mag',format,re.IGNORECASE):
        # if the format is mag then change the number to db
        magnitude=magnitude_S21
        try:
            magnitude_S21=-20.*math.log10(magnitude_S21)
        except:
            magnitude_S21=MINIMUM_DB
    uncertainty_m4=.0006*math.sqrt(frequency)+.0011
    uncertainty_m5=(1.434*math.sqrt(frequency)*5.*6.*10**6)/(.35*math.sqrt((1.4*10**7)**3))
    delta=math.sqrt((uncertainty_m4**2+uncertainty_m5**2)/3)
    uncertainty_arg4=math.atan(.01*math.sqrt((.017+.018*math.sqrt(frequency)+.05*frequency+.018*frequency**2)))
    uncertainty_arg5=12.0115*frequency*.0025
    delta_arg=math.sqrt((uncertainty_arg4**2+uncertainty_arg5**2)/3)
    if frequency<=1.:
        delta_arg=.03
    if re.search('14|7|N',connector_type,re.IGNORECASE):
        uncertainty_magnitude=delta
        uncertainty_phase=delta_arg
    elif re.search('3.5|2.92|2.4',connector_type,re.IGNORECASE):
        uncertainty_phase=delta_arg
        if re.search('3.5',connector_type,re.IGNORECASE):
            uncertainty_magnitude=2.*delta
        elif re.search('2.92',connector_type,re.IGNORECASE):
            uncertainty_magnitude=2.4*delta
        elif re.search('2.4',connector_type,re.IGNORECASE):
            uncertainty_magnitude=2.92*delta
    else :
        uncertainty_magnitude=delta
        uncertainty_phase=delta_arg
    if re.search('mag',format,re.IGNORECASE):
        #print("Converting Back to Mag")
        # if the format is mag then change the uncertainty back to mag
        uncertainty_magnitude=abs((1/math.log10(math.e))*magnitude*uncertainty_magnitude/20.)
        #print("Type B Uncertainty magnitude is {0} ".format(uncertainty_magnitude))
    return [uncertainty_magnitude,uncertainty_phase]

def waveguide_s21_S_NIST(magnitude_S21=1,format='DB'):
    """Calculates SNIST for S21 in Waveguides"""
    if re.search('mag',format,re.IGNORECASE):
        # if the format is mag then change the number to db
        magnitude=magnitude_S21
        try:
            magnitude_S21=-20.*math.log10(magnitude_S21)
        except:
            magnitude_S21=MINIMUM_DB
    uncertainty_phase=.15
    if magnitude_S21>=0 and magnitude_S21<25:
        uncertainty_magnitude=.01
    elif magnitude_S21>=25 and magnitude_S21<=40:
        uncertainty_magnitude=.02
    elif magnitude_S21>40:
        uncertainty_magnitude=.02+.00015*(magnitude_S21-40)**2
    else:
        uncertainty_magnitude=.02+.00015*(magnitude_S21-40)**2
    if re.search('mag',format,re.IGNORECASE):
        # if the format is mag then change the uncertainty back to mag
        uncertainty_magnitude=abs((1/math.log10(math.e))*magnitude*uncertainty_magnitude/20.)
    return [uncertainty_magnitude,uncertainty_phase]

def waveguide_s21_type_b(waveguide_type='WR90',magnitude_S21=1,format='DB'):
    """Calculates type B uncertainty for S21 in Waveguides"""
    if re.search('mag',format,re.IGNORECASE):
        # if the format is mag then change the number to db
        magnitude=magnitude_S21
        try:
            magnitude_S21=-20.*math.log10(magnitude_S21)
        except:
            magnitude_S21=MINIMUM_DB
    if re.search('90',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.02/math.sqrt(3)
        uncertainty_phase=.2/math.sqrt(3)
    elif re.search('62',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.02/math.sqrt(3)
        uncertainty_phase=.5/math.sqrt(3)
    elif re.search('42',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.01/math.sqrt(3)
        uncertainty_phase=.85/math.sqrt(3)
    elif re.search('28',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.01/math.sqrt(3)
        uncertainty_phase=1.0/math.sqrt(3)
    elif re.search('22',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.01/math.sqrt(3)
        uncertainty_phase=1.53/math.sqrt(3)
    elif re.search('15',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.012/math.sqrt(3)
        uncertainty_phase=2.29/math.sqrt(3)
    elif re.search('10',waveguide_type,re.IGNORECASE):
        uncertainty_magnitude=.022/math.sqrt(3)
        uncertainty_phase=3.36/math.sqrt(3)
    else:
        uncertainty_magnitude=.022/math.sqrt(3)
        uncertainty_phase=3.36/math.sqrt(3)

    if re.search('mag',format,re.IGNORECASE):
        # if the format is mag then change the uncertainty back to mag
        uncertainty_magnitude=abs((1/math.log10(math.e))*magnitude_S21*uncertainty_magnitude/20.)
    return [uncertainty_magnitude,uncertainty_phase]

def coax_power_S_NIST(connector_type='N',frequency=1.):
    """Calculates SNIST for coax power measurements"""
    if re.search('7',connector_type,re.IGNORECASE):
        uncertainty_eff=.09+.01*frequency
    elif re.search('N',connector_type,re.IGNORECASE):
        uncertainty_eff=10**(-1.4+.04*frequency)
    elif re.search('3.5',connector_type,re.IGNORECASE):
        if frequency<.05:
            uncertainty_eff=10**(-1.4+.04*frequency)
        elif frequency>=.05 and frequency<=18.:
            uncertainty_eff=.25
    else:
        uncertainty_eff=.25
    return [uncertainty_eff]

def coax_power_type_b(connector_type='N',frequency=1.):
    """Calculates type b for coax power measurements"""
    if re.search('7',connector_type,re.IGNORECASE):
        uncertainty_eff=math.sqrt((.365+.105*math.sqrt(frequency)/math.sqrt(3))**2+.2**2/3)
    elif re.search('N',connector_type,re.IGNORECASE):
        if frequency<.05:
            uncertainty_eff=math.sqrt((.365+.105*math.sqrt(frequency)/math.sqrt(3))**2+.2**2/3)
        elif frequency>=.05 and frequency<=18.:
            uncertainty_eff=math.sqrt((.09+.00267*frequency+.000223*frequency**2)**2+.2**2/3)
    elif re.search('3.5',connector_type,re.IGNORECASE):
        if frequency<.05:
            uncertainty_eff=.0103*frequency+.582
        elif frequency>=.05 and frequency<=18.:
            uncertainty_eff=.7
    else:
        uncertainty_eff=.7

    return [uncertainty_eff]

def waveguide_power_S_NIST(waveguide_type='WR90'):
    """Calculates SNIST for waveguide systems"""
    if re.search('90|62|42|28',waveguide_type,re.IGNORECASE):
        uncertainty_eff = .2
    elif re.search('22|10',waveguide_type,re.IGNORECASE):
        uncertainty_eff = .5
    elif re.search('15',waveguide_type,re.IGNORECASE):
        uncertainty_eff = .75
    else:
        uncertainty_eff = .75
    return [uncertainty_eff]

def waveguide_power_type_b(waveguide_type='WR90'):
    """Calculates type b for waveguide systems"""
    if re.search('90|62|42|28',waveguide_type,re.IGNORECASE):
        uncertainty_eff = .2
    elif re.search('22|15',waveguide_type,re.IGNORECASE):
        uncertainty_eff = .4
    elif re.search('10',waveguide_type,re.IGNORECASE):
        uncertainty_eff = .9
    else:
        uncertainty_eff = .9
    return [uncertainty_eff]

def S_NIST(wr_connector_type='Type-N', frequency=1, parameter='S11', magnitude=1.0, phase=0, format='mag'):
    """S_NIST calculates the Standard NIST uncertainty given the connector_type, parameter (S11,S12 or Power)
     frequency, magnitude and phase"""
    out=[0]
    if re.search('14|7|N|3|2', wr_connector_type, re.IGNORECASE):
        if re.search('11|22',parameter,re.IGNORECASE):
            out=coax_s11_S_NIST(connector_type=wr_connector_type, frequency=frequency)
        elif re.search('12|21',parameter,re.IGNORECASE):
            out=coax_s12_S_NIST(connector_type=wr_connector_type, magnitude_S21=magnitude,
                                frequency=frequency, format=format)
        elif re.search('p|eff',parameter,re.IGNORECASE):
            out=coax_power_S_NIST(connector_type=wr_connector_type, frequency=frequency)
    elif re.search('w', wr_connector_type, re.IGNORECASE):
        if re.search('11|22',parameter,re.IGNORECASE):
            out=waveguide_s11_S_NIST(wr_connector_type)
        elif re.search('21|12',parameter,re.IGNORECASE):
            out=waveguide_s21_S_NIST(magnitude_S21=magnitude,format=format)
        elif re.search('p|eff',parameter,re.IGNORECASE):
            out=waveguide_power_S_NIST(waveguide_type=wr_connector_type)
    return out

def type_b(wr_connector_type='Type-N', frequency=1, parameter='S11', magnitude=1.0, phase=0, format='mag'):
    """type_b calculates the Standard type_b uncertainty given the connector_type, parameter (S11,S12 or Power)
     frequency, magnitude and phase"""
    out=[0]
    if re.search('14|7|N|3|2', wr_connector_type, re.IGNORECASE):
        if re.search('11|22',parameter,re.IGNORECASE):
            out=coax_s11_type_b(connector_type=wr_connector_type, frequency=frequency,
                                magnitude_S11=magnitude)
        elif re.search('12|21',parameter,re.IGNORECASE):
            out=coax_s12_type_b(connector_type=wr_connector_type,
                                magnitude_S21=magnitude, frequency=frequency, format=format)
        elif re.search('p|eff',parameter,re.IGNORECASE):
            out=coax_power_type_b(connector_type=wr_connector_type, frequency=frequency)
    elif re.search('w', wr_connector_type, re.IGNORECASE):
        if re.search('11|22',parameter,re.IGNORECASE):
            out=waveguide_s11_type_b(wr_connector_type)
        elif re.search('21|12',parameter,re.IGNORECASE):
            out=waveguide_s21_type_b(magnitude_S21=magnitude,format=format)
        elif re.search('p|eff',parameter,re.IGNORECASE):
            out=waveguide_power_type_b(waveguide_type=wr_connector_type)
    return out


#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts
def test_uncertainty():
    frequency=np.linspace(.1,18,1000)
    s11_mag_thru=[0 for i in range(1000)]
    s12_mag_thru=[1 for i in range(1000)]

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass