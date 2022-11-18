# Integration of renewable energy sustems to the grid
# Asignment 1

# Nuclear: constant generation, 1 source
# Gas: generation as desired, 1 source
# PV: generation as forecast, multiple sources
# Wind: generation as forecast, multiple sources

# Comments: to have multiple sources, modify section 5
#           it can be added replacement costs to the objective function
#           max_P in pv and wind is the same for all locations (if not, change program)

import pandas
from main import min_renewables

''' 1) Import/introduce data '''

import_demand = pandas.read_excel('Data.xlsx', sheet_name='Demand', header=0, index_col=None)  # demand = import_demand.iloc[:,1]
import_pv = pandas.read_excel('Data.xlsx', sheet_name='PV', header=0, index_col=None)  # pv_i = import_pv.iloc[:,i] // i=1...
import_wind = pandas.read_excel('Data.xlsx', sheet_name='Wind', header=0, index_col=None)  # wind_i = import_wind.iloc[:,i] // i=1...

# min_renewables = 0  # minimum percentage of renewables [pu]
L_prj = 50  # project lifetime [years]

# Nuclear
CAPEX_nuclear = 3600  # €/kW installed
OPEX_nuclear = 0.02  # €/kWh produced
cost_fuel_nuclear = 0.0001  # €/kWh produced
max_P_nuclear = 1000**10  # maximum installed power [kW] --> inf = 1000**10 // no nuclear = 0
P_nuclear_existent = 0  # installed power already in the system [kW]
L_nuclear = 60  # nuclear power plant lifetime [years]

# Gas
CAPEX_gas = 823  # €/kW installed
OPEX_gas = 0.15  # €/kWh produced
cost_fuel_gas = 0.0001  # €/kWh produced
max_P_gas = 1000**10  # maximum installed power [kW] --> inf = 1000**10 // no gas = 0
P_gas_existent = 0  # installed power already in the system [kW]
L_gas = 30  # gas power plant lifetime [years]

# PV
CAPEX_pv = 1337.5/10  # €/kW installed
OPEX_pv = 0.0021  # €/kWh produced
max_P_pv = 10000**10  # maximum installed power [kW] --> inf = 1000**10 // no PV = 0
L_pv = 25  # PV power plant lifetime [years]

# Wind
CAPEX_wind = 1429/10  # €/kW installed
OPEX_wind = 0.0039  # €/kWh produced
max_P_wind = 1000**10  # maximum installed power [kW] --> inf = 1000**10 // no wind = 0
L_wind = 25  # wind power plant lifetime [years]



''' 2) Pre-processing'''

l_t = list(range(365*24))  # number of periods (365 days)
l_i_pv = list(range(1, import_pv.shape[1]))
l_i_wind = list(range(1, import_wind.shape[1]))

def dict_demand(importa):
    dict_Forecast = {t: importa.iloc[t, 1] for t in l_t}
    return dict_Forecast
def Forecast_i(importa):
    n_locations = importa.shape[1]
    dict_Forecast = {(t, i): importa.iloc[t, i] for t in l_t for i in list(range(1, n_locations))}
    return dict_Forecast


def get_import(x):
    if x == 'Demand':
        return import_demand
    elif x == 'PV':
        return import_pv
    elif x == 'Wind':
        return import_wind
    else:
        return
def get_l(x):
    if x == 'time':
        return l_t
    elif x == 'PV':
        return l_i_pv
    elif x == 'Wind':
        return l_i_wind
    else:
        return
def get_min_renewables():
    return min_renewables
def get_L_prj():
    return L_prj
def get_CAPEX(tech):
    if tech == 'Nuclear':
        return CAPEX_nuclear
    elif tech == 'Gas':
        return CAPEX_gas
    elif tech == 'PV':
        return CAPEX_pv
    elif tech == 'Wind':
        return CAPEX_wind
    else:
        return
def get_OPEX(tech):
    if tech == 'Nuclear':
        return OPEX_nuclear
    elif tech == 'Gas':
        return OPEX_gas
    elif tech == 'PV':
        return OPEX_pv
    elif tech == 'Wind':
        return OPEX_wind
    else:
        return
def get_cost_fuel(tech):
    if tech == 'Nuclear':
        return cost_fuel_nuclear
    elif tech == 'Gas':
        return cost_fuel_gas
    else:
        return
def get_max_P(tech):
    if tech == 'Nuclear':
        return max_P_nuclear
    elif tech == 'Gas':
        return max_P_gas
    elif tech == 'PV':
        return max_P_pv
    elif tech == 'Wind':
        return max_P_wind
    else:
        return
def get_P_existent(tech):
    if tech == 'Nuclear':
        return P_nuclear_existent
    elif tech == 'Gas':
        return P_gas_existent
    else:
        return
def get_L(tech):
    if tech == 'Nuclear':
        return L_nuclear
    elif tech == 'Gas':
        return L_gas
    elif tech == 'PV':
        return L_pv
    elif tech == 'Wind':
        return L_wind
    else:
        return
