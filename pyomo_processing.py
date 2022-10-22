import pandas as pd
import numpy as np


folder = 'CSV/'

file_data = pd.read_csv(folder+'data.csv', sep=';', header=0, index_col=0, usecols=['t', 'Demand', 'PV1', 'PV2', 'W1', 'W2'])
file_techparam = pd.read_csv(folder+'techparam.csv',sep=',', header=0, index_col=0, usecols=['CAPEX', 'OPEX'])


## Sets ##

# Time set
l_t = list(file_data.index.values)

def set_t():
    return l_t

# Tech sets

l_tech = list(file_techparam.index.values)

def set_tech():
    return l_tech


# Economic parameters
def param_CAPEX():
    dict_CAPEX = {tech: file_techparam['CAPEX'][tech] for tech in l_tech}
    return dict_CAPEX

def param_OPEX():
    dict_OPEX = {tech: file_techparam['OPEX'][tech] for tech in l_tech}
    return dict_OPEX

# Demand

def param_D():
    dict_demand = {t: file_data['Demand'][t] for t in l_t}
    return dict_demand
    
# Renewable parameters

def param_PV1():
    dict_PV1 = {t: file_data['PV1'][t] for t in l_t}
    return dict_PV1

def param_PV2():
    dict_PV2 = {t: file_data['PV2'][t] for t in l_t}
    return dict_PV2
    
def param_wind1():
    dict_wind1 = {t: file_data['W1'][t] for t in l_t}
    return dict_wind1
    
def param_wind2():
    dict_wind2={t: file_data['W2'][t] for t in l_t}
    return dict_wind2