import math

import pyomo.environ as pyo
from pre_processing import *
from network import *


''' 3) Optimization formulation'''

model = pyo.AbstractModel()

##### Model Sets #####
model.t = pyo.Set(initialize=get_l('time'))
model.i_pv = pyo.Set(initialize=get_l('PV'))
model.i_wind = pyo.Set(initialize=get_l('Wind'))
#
model.n = pyo.Set(initialize=get_l_n())
model.n_aux = pyo.Set(initialize=get_l_naux())
model.line = pyo.Set(initialize=get_l_branches())


##### Model Parameters #####

# System
model.demand = pyo.Param(model.t, initialize=dict_demand(get_import('Demand')))  # hourly demand [kW]
model.min_ren = pyo.Param(initialize=get_min_renewables())  # minimum percentage of renewables [pu]
model.L_prj = pyo.Param(initialize=get_L_prj())  # project lifetime [years]

# Nuclear
model.CAPEX_nuclear = pyo.Param(initialize=get_CAPEX('Nuclear'))  # €/kW installed
model.OPEX_nuclear = pyo.Param(initialize=get_OPEX('Nuclear'))  # €/kWh produced
model.cost_fuel_nuclear = pyo.Param(initialize=get_cost_fuel('Nuclear'))  # €/kWh produced
model.max_P_nuclear = pyo.Param(initialize=get_max_P('Nuclear'))  # maximum installed power [kW]
model.P_nuclear_existent = pyo.Param(initialize=get_P_existent('Nuclear'))  # installed power already in the system [kW]
model.L_nuclear = pyo.Param(initialize=get_L('Nuclear'))  # nuclear power plant lifetime [years]

# Gas
model.CAPEX_gas = pyo.Param(initialize=get_CAPEX('Gas'))  # €/kW installed
model.OPEX_gas = pyo.Param(initialize=get_OPEX('Gas'))  # €/kWh produced
model.cost_fuel_gas = pyo.Param(initialize=get_cost_fuel('Gas'))  # €/kWh produced
model.max_P_gas = pyo.Param(initialize=get_max_P('Gas'))  # maximum installed power [kW]
model.P_gas_existent = pyo.Param(initialize=get_P_existent('Gas'))  # installed power already in the system [kW]
model.L_gas = pyo.Param(initialize=get_L('Gas'))  # gas power plant lifetime [years]

# PV
model.forecast_pv = pyo.Param(model.t, model.i_pv, initialize=Forecast_i(get_import('PV')))  # hourly PV generation [MW]
model.CAPEX_pv = pyo.Param(initialize=get_CAPEX('PV'))  # €/kW installed
model.OPEX_pv = pyo.Param(initialize=get_OPEX('PV'))  # €/kWh produced
model.max_P_pv = pyo.Param(initialize=get_max_P('PV'))  # maximum installed power [kW]
model.L_pv = pyo.Param(initialize=get_L('PV'))  # PV power plant lifetime [years]

# Wind
model.forecast_wind = pyo.Param(model.t, model.i_wind, initialize=Forecast_i(get_import('Wind')))  # hourly PV generation [MW]
model.CAPEX_wind = pyo.Param(initialize=get_CAPEX('Wind'))  # €/kW installed
model.OPEX_wind = pyo.Param(initialize=get_OPEX('Wind'))  # €/kWh produced
model.max_P_wind = pyo.Param(initialize=get_max_P('Wind'))  # maximum installed power [kW]
model.L_wind = pyo.Param(initialize=get_L('Wind'))  # wind power plant lifetime [years]

# Power Flow
model.A_matrix_ini = pyo.Param(model.line, model.n_aux, initialize=get_A_matrix_ini())
model.A_matrix_fin = pyo.Param(model.line, model.n_aux, initialize=get_A_matrix_fin())
model.B_matrix = pyo.Param(model.n_aux, model.n_aux, initialize=get_B_matrix())
model.D_matrix = pyo.Param(model.line, model.line, initialize=get_D_matrix())
model.demand_nodes = pyo.Param(model.n, initialize=get_Demand_nodes())  # dict (node index: % demand [pu])
model.Pmax_line = pyo.Param(model.line, initialize=get_Pmax_lines())
model.Nuclear_nodes = pyo.Param(model.n, initialize=get_Generation_nodes('Nuclear'))  # dict (node: % nuclear power in that node [pu])
model.Gas_nodes = pyo.Param(model.n, initialize=get_Generation_nodes('Gas'))  # dict (node: % gas power in that node [pu])
model.PV_nodes = pyo.Param(model.i_pv, model.n, initialize=get_Generation_nodes('PV'))  # dict ((PV loc,node): % PV power in that node [pu])
model.Wind_nodes = pyo.Param(model.i_wind, model.n, initialize=get_Generation_nodes('Wind'))  # dict ((Wind loc,node): % Wind power in that node [pu])


##### Model Variables #####

# System

# Nuclear
model.P_nuclear = pyo.Var(within=pyo.NonNegativeReals)  # nuclear power installed [kW]
model.x_nuclear = pyo.Var(model.t, within=pyo.NonNegativeReals)  # instantaneous nuclear power generation [kW]

# Gas
model.P_gas = pyo.Var(within=pyo.NonNegativeReals)  # gas power installed [kW]
model.x_gas = pyo.Var(model.t, within=pyo.NonNegativeReals)  # instantaneous gas power generation [kW]

# PV
model.P_pv = pyo.Var(model.i_pv, within=pyo.NonNegativeReals)  # PV power installed [kWp]
model.x_pv = pyo.Var(model.t, model.i_pv, within=pyo.NonNegativeReals)  # instantaneous PV power generation [kW]

# Wind
model.P_wind = pyo.Var(model.i_wind, within=pyo.NonNegativeReals)  # wind power installed [kW]
model.x_wind = pyo.Var(model.t, model.i_wind, within=pyo.NonNegativeReals)  # instantaneous wind power generation [kW]

# Power Flow
model.P_line_t = pyo.Var(model.line, model.t, within=pyo.Reals)  # instantaneous power flowing through each line [??]
model.theta_n_t = pyo.Var(model.n, model.t, within=pyo.NonNegativeReals)  # voltage angle of each node at each instant [??]


##### Model Constraints #####

# Nuclear
def Constraint_max_P_nuclear(m):
    return m.P_nuclear <= m.max_P_nuclear
model.Constr_nuclear1 = pyo.Constraint(rule=Constraint_max_P_nuclear)
def Constraint_x_nuclear(m, t):
    return m.x_nuclear[t] == m.P_nuclear + m.P_nuclear_existent  # nuclear generation remains constant through the year
model.Constr_nuclear2 = pyo.Constraint(model.t, rule=Constraint_x_nuclear)

# Gas
def Constraint_max_P_gas(m):
    return m.P_gas <= m.max_P_gas
model.Constr_gas1 = pyo.Constraint(rule=Constraint_max_P_gas)
def Constraint_max_x_gas(m, t):
    return m.x_gas[t] <= m.P_gas + m.P_gas_existent
model.Constr_gas2 = pyo.Constraint(model.t, rule=Constraint_max_x_gas)

# PV
def Constraint_max_P_pv(m, i_pv):
    return m.P_pv[i_pv] <= m.max_P_pv
model.Constr_pv1 = pyo.Constraint(model.i_pv, rule=Constraint_max_P_pv)
def Constraint_max_x_pv(m, t, i_pv):
    return m.x_pv[t, i_pv] <= m.P_pv[i_pv] * m.forecast_pv[t, i_pv]
model.Constr_pv2 = pyo.Constraint(model.t, model.i_pv, rule=Constraint_max_x_pv)

# Wind
def Constraint_max_P_wind(m, i_wind):
    return m.P_wind[i_wind] <= m.max_P_wind
model.Constr_wind1 = pyo.Constraint(model.i_wind, rule=Constraint_max_P_wind)
def Constraint_max_x_wind(m, t, i_wind):
    return m.x_wind[t, i_wind] <= m.P_wind[i_wind] * m.forecast_wind[t, i_wind]
model.Constr_wind2 = pyo.Constraint(model.t, model.i_wind, rule=Constraint_max_x_wind)

# Balance generation=demand
def Constraint_balance_system(m, t):
    return m.demand[t] == m.x_nuclear[t] + m.x_gas[t] + sum(m.x_pv[t, i_pv] for i_pv in l_i_pv) + sum(m.x_wind[t, i_wind] for i_wind in l_i_wind)
model.Constr_balance = pyo.Constraint(model.t, rule=Constraint_balance_system)
def Constraint_min_renewables(m):
    return sum(sum(m.x_pv[t, i_pv] for i_pv in l_i_pv) + sum(m.x_wind[t, i_wind] for i_wind in l_i_wind) for t in l_t) >= m.min_ren * sum(m.demand[t] for t in l_t)
model.Constr_min_renewables = pyo.Constraint(rule=Constraint_min_renewables)

# Power Flow
def Constraint_theta_slack(m, n, t):
    if n==1:
        return m.theta_n_t[n,t]==0
    return pyo.Constraint.Skip
model.Constr_PF1 = pyo.Constraint(model.n, model.t, rule=Constraint_theta_slack)
def Constraint_DC_PF_equation(m, n_aux, t):
    Generation_node = m.x_nuclear[t] * m.Nuclear_nodes[n_aux] + m.x_gas[t] * m.Gas_nodes[n_aux] \
        + sum(m.x_pv[t,i_pv]*m.PV_nodes[i_pv,n_aux] for i_pv in l_i_pv) +\
        + sum(m.x_wind[t,i_wind]*m.Wind_nodes[i_wind,n_aux] for i_wind in l_i_wind)
    Demand_node = m.demand[t] * m.demand_nodes[n_aux]
    return Generation_node - Demand_node == sum(m.B_matrix[n_aux,naux]*(m.theta_n_t[n_aux,t]-m.theta_n_t[naux,t]) for naux in m.n_aux)#sum(m.B_matrix[n_aux,naux]*m.theta_n_t[naux,t] for naux in m.n_aux)
model.Constr_PF2 = pyo.Constraint(model.n_aux, model.t, rule=Constraint_DC_PF_equation)



##### Objective function ####

def func_obj(m):
    nuclear_cost = m.P_nuclear * (m.CAPEX_nuclear + 8760 * m.OPEX_nuclear * m.L_prj) + sum(m.x_nuclear[t] for t in l_t) * m.cost_fuel_nuclear * m.L_prj  # + (m.P_nuclear + m.P_nuclear_existent) * int(m.L_prj / m.L_nuclear) * m.CAPEX_nuclear
    gas_cost = m.P_gas * (m.CAPEX_gas + 8760 * m.OPEX_gas * m.L_prj) + sum(m.x_gas[t] for t in l_t) * m.cost_fuel_gas * m.L_prj  # + (m.P_gas + m.P_gas_existent) * int(m.L_prj / m.L_gas) * m.CAPEX_gas
    pv_cost = sum(m.P_pv[i_pv] for i_pv in l_i_pv) * (m.CAPEX_pv + 8760 * m.OPEX_pv * m.L_prj)  # + sum(m.P_pv[i_pv] for i_pv in l_i_pv) * int(m.L_prj / m.L_pv) * m.CAPEX_pv
    wind_cost = sum(m.P_wind[i_wind] for i_wind in l_i_wind) * (m.CAPEX_wind + 8760 * m.OPEX_wind * m.L_prj)  # + sum(m.P_wind[i_wind] for i_wind in l_i_wind) * int(m.L_prj / m.L_wind) * m.CAPEX_wind
    return nuclear_cost + gas_cost + pv_cost + wind_cost
model.goal = pyo.Objective(rule=func_obj, sense=pyo.minimize)


##### Optimization solving #####

instance = model.create_instance()
opt = pyo.SolverFactory('glpk')
results = opt.solve(instance)
results.write()

