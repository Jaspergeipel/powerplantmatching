# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 16:06:18 2020

@author: geipel
"""
# Import required packages

import os
import pickle
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import zipfile


# Make input and ouput directories
dirs = ['input', 'output', 'output/figures', 'output/tables']
for i in dirs:
    if not os.path.isdir(i):
        os.makedirs(i)
        
# Download JRC conventional data
    url = 'https://zenodo.org/record/3349843/files/JRC-PPDB-OPEN.ver0.91.zip?download=1'
    filename = 'JRC-PPDB-OPEN.ver0.91.zip'
    filepath = os.path.join(filename)

    if not os.path.exists(filepath):
        urllib.request.urlretrieve(url, filepath)
    else:
        print('Using local file from ' + filepath + '.')
    
    zf = zipfile.ZipFile('JRC-PPDB-OPEN.ver0.91.zip', 'r')

    zf.extract('JRC_OPEN_UNITS.csv', 'input')
    if os.path.exists("input/conventionals.csv"):
        os.remove("input/conventionals.csv")
    os.rename('input/JRC_OPEN_UNITS.csv', 'input/conventionals.csv')        
    zf.extract('JRC_OPEN_PERFORMANCE.csv', 'input')
    zf.extractall('input')
    
    con_units = pd.read_csv('input/conventionals.csv',
                            encoding='utf8',
                            header=0)
    
# Fill empty cells in the chp column with 'no'
#con.chp.fillna(value='no', inplace=True)

# Read conventional power plants (OPEN PERFORMANCE)
    con_performance = pd.read_csv('input/JRC_OPEN_PERFORMANCE.csv')


    con = pd.merge(con_units, con_performance, how='outer', on=['eic_p', 'eic_g']) 

# Fill in the country you want to filter by here
    #country_chosen = 'Austria'

# Locate relevant entries in con
    #idx_con_country = con[con.country == country_chosen].index

# Create new con dataframe for the chosen country
    #con = con.loc[idx_con_country,:]
    
# Reduce con_country to entries that are not decommissioned or mothballed 
    con = con[con.status_g != 'DECOMMISSIONED']
    con = con[con.status_g != 'MOTHBALLED']
# Delete entries with capacity = 0
    con = con[con.capacity_p != 0]
    con = con[con.capacity_g != 0]
    
    
# Remove non conventional power plants
    non_conventionals_list = ['Biomass','Wind', 'solar', 'hydro', 'geothermal', 'waste', 'other']
    con_a     = con[con['type_g'].str.contains('|'.join(non_conventionals_list), case = False)]
    con         = con[~con['type_g'].str.contains('|'.join(non_conventionals_list), case = False)]
    
# Remove entries with decommissioning date before 2018
    #con = con.drop(columns = ['capacity_p','eic_p', "eic_g", "name_p","lat","lon","NUTS2", "min_load", "ramp_down","ramp_up", "minimum_up_time", "minimum_down_time"])
    con = con[(con['year_decommissioned'] > 2017) | (con['year_decommissioned'].isna())]


# Check for entries with where Efficiency is NaN and commission year is NaN
    con_eff_NaN_year_c_NaN          = con[con['eff'].isnull() & con['year_commissioned'].isnull()]
# Check for entries with where Efficiency is NaN and commission year is NOT NaN
    con_eff_NaN_year_c_NotNaN       = con[con['eff'].isnull() & con['year_commissioned'].notnull()] 
# Check for entries with where Efficiency is NOT NaN and commission year is NaN
    con_eff_notNaN_year_c_NaN          = con[con['eff'].notnull() & con['year_commissioned'].isnull()] 
# Check for entries with where Efficiency is NOT NaN and commission year is NOT NaN 
    con_eff_notNaN_year_c_notNaN    = con[con['eff'].notnull() & con['year_commissioned'].notnull()] 
    
import powerplantmatching as ppm
import pandas as pd
df = ppm.powerplants(from_url=True)

    
    #con_ommited = con[con['eff']=='nan']
    #con=con.dropna(subset=['eff'])
# Derive commission year based on efficiency?
    
