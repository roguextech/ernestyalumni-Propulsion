## tut1.py
## tut1.m implemented in Python for cantera 
## cf. http://www.cantera.org/docs/sphinx/html/matlab/tutorials/tut1.html
############################################################################ 
## Copyleft 2016, Ernest Yeung <ernestyalumni@gmail.com>                            
## 20160124
##                                                                               
## This program, along with all its code, is free software; you can redistribute 
## it and/or modify it under the terms of the GNU General Public License as 
## published by the Free Software Foundation; either version 2 of the License, or   
## (at your option) any later version.                                        
##     
## This program is distributed in the hope that it will be useful,               
## but WITHOUT ANY WARRANTY; without even the implied warranty of              
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                 
## GNU General Public License for more details.                             
##                                                                          
## Governing the ethics of using this program, I default to the Caltech Honor Code: 
## ``No member of the Caltech community shall take unfair advantage of        
## any other member of the Caltech community.''                               
##                                                         
## linkedin     : ernestyalumni                                                    
## wordpress    : ernestyalumni                                                    
############################################################################ 
# Tutorial 1:  Getting started
#   
#  Topics:
#    - creating a gas mixture
#    - setting the state
#    - cleaning up
#
import cantera as ct
import numpy as np

gas1 = ct.Solution("gri30.xml")

print gas1()

# If you have successfully installed Cantera, you should
# see something like this when you type gas1() where you "instantiate" gas1:
#         temperature             300  K
#            pressure          101325  Pa
#             density        0.081889  kg/m^3
#    mean mol. weight         2.01588  amu
#   
#                            1 kg            1 kmol
#                         -----------      ------------
#            enthalpy         26470.1        5.336e+04     J
#     internal energy    -1.21088e+06       -2.441e+06     J
#             entropy           64914        1.309e+05     J/K
#      Gibbs function    -1.94477e+07        -3.92e+07     J
#   heat capacity c_p         14311.8        2.885e+04     J/K
#   heat capacity c_v         10187.3        2.054e+04     J/K
#   
#                             X                 Y          Chem. Pot. / RT    
#                       -------------     ------------     ------------
#                  H2              1                1         -15.7173
#       [  +52 minor]              0                0
#
# What you have just done is to create an object ("gas1") that
# implements GRI-Mech 3.0, the 53-species, 325-reaction natural gas
# combustion mechanism developed by Gregory P. Smith, David M. Golden,
# Michael Frenklach, Nigel W. Moriarty, Boris Eiteneer, Mikhail
# Goldenberg, C. Thomas Bowman, Ronald K. Hanson, Soonho Song, William
# C. Gardiner, Jr., Vitali V. Lissianski, and Zhiwei Qin. (See
# http://www.me.berkeley.edu/gri_mech/ for more information about
# GRI-Mech 3.0.)
#
# The object created by GI30 has properties you would expect for a gas
# mixture - it has a temperature, a pressure, species mole and mass
# fractions, etc. As we'll soon see, it has many other properties too.
#
# The summary of the state of 'gas1' printed above shows that new
# objects created by function GRI30 start out with a temperature of
# 300 K, a pressure of 1 atm, and have a composition that consists of
# only one species, in this case hydrogen. There is nothing special
# about H2 - it just happens to be the first species listed in the
# input file defining GRI-Mech 3.0 that the 'GRI30' function reads. In
# general, the species listed first will initially have a mole
# fraction of 1.0, and all of the others will be zero.

#  Setting the state
#  -----------------

# The state of the object can be easily changed. For example,

gas1.T = 1200

# sets the temperature to 1200 K. (Cantera always uses SI units.)

# Notice in the summary of properties that MATLAB prints after this
# command is executed that the temperature has been changed as
# requested, but the pressure has changed too. The density and
# composition have not. 
#
# When setting properties individually, some convention needs to be
# adopted to specify which other properties are held constant. This is
# because thermodynamics requires that *two* properties (not one) in
# addition to composition information be specified to fix the
# intensive state of a substance (or mixture).
#
# Cantera adopts the following convention: only one of the set
# (temperature, density, mass fractions) is altered by setting any
# single property. In particular:
#
# a) Setting the temperature is done holding density and
#    composition  fixed. (The pressure changes.)

# b) Setting the pressure is done holding temperature and
#    composition fixed. (The density changes.)
# 
# c) Setting the composition is done holding temperature
#    and density fixed. (The pressure changes).
#


# Setting multiple properties: 
# ---------------------------------------------

# If you want to set multiple properties at once, use 

gas1.TP = 900.0, 1.e5

# This statement sets both temperature and pressure at the same
# time. Any number of property/value pairs can be specified in the 
# "new" Python method 
# cf. http://www.cantera.org/docs/sphinx/html/cython/migrating.html#setting-thermodynamic-state

# The following sets the mole fractions
gas1.TP = 900.0, 1.e5
gas1.X = 'CH4:1,O2:2,N2:7.52'

# This all results in
#
#         temperature             900  K
#            pressure          100000  Pa
#             density        0.369279  kg/m^3
#    mean mol. weight         27.6332  amu
#   
#                            1 kg            1 kmol
#                         -----------      ------------
#            enthalpy          455660        1.259e+07     J
#     internal energy          184862        5.108e+06     J
#             entropy         8529.31        2.357e+05     J/K
#      Gibbs function    -7.22072e+06       -1.995e+08     J
#   heat capacity c_p          1304.4        3.604e+04     J/K
#   heat capacity c_v         1003.52        2.773e+04     J/K
#   
#                             X                 Y          Chem. Pot. / RT    
#                       -------------     ------------     ------------
#                  O2       0.190114         0.220149         -27.9596
#                 CH4       0.095057        0.0551863         -37.0813
#                  N2       0.714829         0.724665          -24.935
#       [  +50 minor]              0                0

# Other properties may also be set, including some that
# can't be set individually. The following property pairs may be
# set: (Enthalpy, Pressure), (IntEnergy, Volume), (Entropy,
# Volume), (Entropy, Pressure). In each case, the values of the
# extensive properties must be entered *per unit mass*. 

# Setting the enthalpy and pressure:
gas1.HP = 2*gas1.enthalpy_mass, 2*ct.one_atm

# The composition above was specified using a string. The format is a
# comma-separated list of <species name>:<relative mole numbers>
# pairs. The mole numbers will be normalized to produce the mole
# fractions, and therefore they are 'relative' mole numbers.  Mass
# fractions can be set in this way too by changing 'X' to 'Y' in the
# above statement.

# The composition can also be set using an array, which can be
# either a column vector or a row vector but must have the same
# size as the number of species. For example, to set all 53 mole
# fractions to the same value, do this:

x = np.ones(53) # a column vector of 53 ones
gas1.X = x

# To set the mass fractions to equal values:
gas1.Y = x

# one doesn't really need to clear up objects created in Python;
# please let me know if this is NOT the case @ernestyalumni, otherwise, 
# I reference the following:
# cf. http://eli.thegreenplace.net/2009/06/12/safely-using-destructors-in-python

######################################################################
#   end of tutorial 1
######################################################################
