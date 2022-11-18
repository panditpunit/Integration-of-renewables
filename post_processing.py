from pyomo_processing import *
from main import save_results

##### Extract results #####

# pyo.value(instance.___object_name___) --> pyo.value(instance.P_nuclear), pyo.value(instance.L_prj), ...

P_nuclear = instance.P_nuclear.get_values()[None]
P_gas = instance.P_gas.get_values()[None]
dict_P_pv = instance.P_pv.get_values()
dict_P_wind = instance.P_wind.get_values()

dict_x_nuclear = instance.x_nuclear.get_values()
dict_x_gas = instance.x_gas.get_values()
dict_x_pv = instance.x_pv.get_values()
dict_x_wind = instance.x_wind.get_values()

dict_P_line_t = instance.P_line_t.get_values()
dict_theta_n_t = instance.theta_n_t.get_values()

list_x_nuclear = []
list_x_gas = []
list_x_pv1 = []
list_x_pv2 = []
list_x_wind1 = []
list_x_wind2 = []
for t in l_t:
    list_x_nuclear.insert(t, dict_x_nuclear[t])
    list_x_gas.insert(t, dict_x_gas[t])
    list_x_pv1.insert(t, dict_x_pv[t, 1])
    list_x_pv2.insert(t, dict_x_pv[t, 2])
    list_x_wind1.insert(t, dict_x_wind[t, 1])
    list_x_wind2.insert(t, dict_x_wind[t, 2])
dict_col_hourly = {}
dict_col_hourly['x_nuclear'] = list_x_nuclear
dict_col_hourly['x_gas'] = list_x_gas
dict_col_hourly['x_pv1'] = list_x_pv1
dict_col_hourly['x_pv2'] = list_x_pv2
dict_col_hourly['x_wind1'] = list_x_wind1
dict_col_hourly['x_wind2'] = list_x_wind2
tabla_h = pandas.DataFrame(dict_col_hourly, index=l_t)

dict_col_sizing = {}
dict_col_sizing['Source'] = ['nuclear', 'gas', 'PV 1', 'PV 2', 'wind 1', 'wind 2']
dict_col_sizing['installed power [kW]'] = [P_nuclear, P_gas, dict_P_pv[1], dict_P_pv[2], dict_P_wind[1], dict_P_wind[2]]
tabla_sizing = pandas.DataFrame(dict_col_sizing)

def extract_PF_variables(dict,line_bus):
    list_name = []
    for t in l_t:
        list_name.insert(t, dict[line_bus,t])
    return list_name

dict_col_hourly_P_line = {}
for line in l_branches:
    dict_col_hourly_P_line[line] = extract_PF_variables(dict_P_line_t,line)
tabla_P_line = pandas.DataFrame(dict_col_hourly_P_line)

dict_col_hourly_theta = {}
for bus in l_naux:
    dict_col_hourly_theta[bus] = extract_PF_variables(dict_theta_n_t,bus)
tabla_theta = pandas.DataFrame(dict_col_hourly_theta)


##### Cost analysis #####

nuclear_CAPEX_cost = P_nuclear * CAPEX_nuclear
nuclear_OPEX_cost = P_nuclear * 8760 * OPEX_nuclear * L_prj
nuclear_fuel_cost = sum(dict_x_nuclear[t] for t in l_t) * cost_fuel_nuclear * L_prj
nuclear_replacement_cost = (P_nuclear + P_nuclear_existent) * int(L_prj / L_nuclear) * CAPEX_nuclear
nuclear_total_cost = nuclear_CAPEX_cost + nuclear_OPEX_cost + nuclear_fuel_cost + nuclear_replacement_cost

gas_CAPEX_cost = P_gas * CAPEX_gas
gas_OPEX_cost = P_gas * 8760 * OPEX_gas * L_prj
gas_fuel_cost = sum(dict_x_gas[t] for t in l_t) * cost_fuel_gas * L_prj
gas_replacement_cost = (P_gas + P_gas_existent) * int(L_prj / L_gas) * CAPEX_gas
gas_total_cost = gas_CAPEX_cost + gas_OPEX_cost + gas_fuel_cost + gas_replacement_cost

pv_CAPEX_cost = sum(dict_P_pv[i_pv] for i_pv in l_i_pv) * CAPEX_pv
pv_OPEX_cost = sum(dict_P_pv[i_pv] for i_pv in l_i_pv) * 8760 * OPEX_pv * L_prj
pv_replacement_cost = sum(dict_P_pv[i_pv] for i_pv in l_i_pv) * int(L_prj / L_pv) * CAPEX_pv
pv_total_cost = pv_CAPEX_cost + pv_OPEX_cost + pv_replacement_cost

wind_CAPEX_cost = sum(dict_P_wind[i_wind] for i_wind in l_i_wind) * CAPEX_wind
wind_OPEX_cost = sum(dict_P_wind[i_wind] for i_wind in l_i_wind) * 8760 * OPEX_wind * L_prj
wind_replacement_cost = sum(dict_P_wind[i_wind] for i_wind in l_i_wind) * int(L_prj / L_wind) * CAPEX_wind
wind_total_cost = wind_CAPEX_cost + wind_OPEX_cost + wind_replacement_cost

total_CAPEX_cost = nuclear_CAPEX_cost + gas_CAPEX_cost + pv_CAPEX_cost + wind_CAPEX_cost
total_OPEX_cost = nuclear_OPEX_cost + gas_OPEX_cost + pv_OPEX_cost + wind_OPEX_cost
total_fuel_cost = nuclear_fuel_cost + gas_fuel_cost
total_replacement_cost = nuclear_replacement_cost + gas_replacement_cost + pv_replacement_cost + wind_replacement_cost
total_cost = nuclear_total_cost + gas_total_cost + pv_total_cost + wind_total_cost

# LCOE = (CAPEX/L + OPEX) / energy production
if P_nuclear > 0.1:
    LCOE_nuclear = (nuclear_CAPEX_cost / L_nuclear + (nuclear_OPEX_cost + nuclear_fuel_cost) / L_prj) / sum(dict_x_nuclear[t] for t in l_t)
else:
    LCOE_nuclear = 'NaN'
if P_gas > 0.1:
    LCOE_gas = (gas_CAPEX_cost / L_gas + (gas_OPEX_cost + gas_fuel_cost) / L_prj) / sum(dict_x_gas[t] for t in l_t)
else:
    LCOE_gas = 'NaN'
if sum(dict_P_pv[i_pv] for i_pv in l_i_pv) > 0.1:
    LCOE_pv = (pv_CAPEX_cost / L_pv + pv_OPEX_cost / L_prj) / sum(sum(dict_x_pv[t, i_pv] for i_pv in l_i_pv) for t in l_t)
else:
    LCOE_pv = 'NaN'
if sum(dict_P_wind[i_wind] for i_wind in l_i_wind) > 0.1:
    LCOE_wind = (wind_CAPEX_cost / L_wind + wind_OPEX_cost / L_prj) / sum(sum(dict_x_wind[t, i_wind] for i_wind in l_i_wind) for t in l_t)
else:
    LCOE_wind = 'NaN'

dict_demanda = dict_demand(import_demand)
LCOE_total = total_cost / L_prj / sum(dict_demanda[t] for t in l_t)

dict_col_cost = {}
dict_col_cost['Source'] = ['nuclear', 'gas', 'PV', 'wind', 'total']
dict_col_cost['CAPEX'] = [nuclear_CAPEX_cost, gas_CAPEX_cost, pv_CAPEX_cost, wind_CAPEX_cost, total_CAPEX_cost]
dict_col_cost['OPEX'] = [nuclear_OPEX_cost, gas_OPEX_cost, pv_OPEX_cost, wind_OPEX_cost, total_OPEX_cost]
dict_col_cost['fuel'] = [nuclear_fuel_cost, gas_fuel_cost, 0, 0, total_fuel_cost]
dict_col_cost['replacement'] = [nuclear_replacement_cost, gas_replacement_cost, pv_replacement_cost, wind_replacement_cost, total_replacement_cost]
dict_col_cost['total cost [€]'] = [nuclear_total_cost, gas_total_cost, pv_total_cost, wind_total_cost, total_cost]
dict_col_cost['LCOE [€/kWh]'] = [LCOE_nuclear, LCOE_gas, LCOE_pv, LCOE_wind, LCOE_total]
tabla_cost = pandas.DataFrame(dict_col_cost)


##### Save results #####
with pandas.ExcelWriter(save_results) as writer: # 'Results.xlsx' file according to min_renewables
    tabla_h.to_excel(writer, sheet_name='hourly')
    tabla_sizing.to_excel(writer, sheet_name='sizing')
    tabla_cost.to_excel(writer, sheet_name='cost+LCOE')
    tabla_P_line.to_excel(writer, sheet_name='P_line')
    tabla_theta.to_excel(writer, sheet_name='theta_bus')

print('end')
