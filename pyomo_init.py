from doctest import IGNORE_EXCEPTION_DETAIL
from operator import mod

from numpy import var
from pyomo.environ import pyo
from pyomo_preprocessing import *


model = pyo.AbstractModel()

# Sets

set_t = set_t()
model.t = pyo.Set(initialize=set_t)

set_tech = set_tech()
model.tech=pyo.Set(initialize = set_tech)


# Parameters

param_D = param_D()
param_CAPEX = param_CAPEX()
param_OPEX = param_OPEX()
param_wind1 = param_wind1()
param_wind2 = param_wind2()
param_PV1 = param_PV1()
param_PV2 = param_PV2()


model.D = pyo.Param(model.t, initialize = param_D) 
model.InNuc = pyo.Param(model.t, initialize = 5000)
model.InGas = pyo.Param(model.t, initialize = 2000)
model.CAPEX = pyo.Param(model.tech, initialize = param_CAPEX)
model.OPEX = pyo.Param(model.tech, initialize = param_OPEX)
model.wind1 = pyo.Param(model.t, initialize = param_wind1)
model.wind2 = pyo.Param(model.t, initialize = param_wind2)
model.PV1 = pyo.Param(model.t, initialize = param_PV1)
model.PV2 = pyo.Param(model.t, initialize = param_PV2)


model.lifetime = pyo.Param(initialize = 50)
model.alpha = pyo.Param(initialize=0.4)

# Variables

model.G = pyo.Var(model.t, model.tech, domain=pyo.NonNegativeReals) #Generation per tech in a given timestamp
model.P = pyo.Var(model.tech, domain=pyo.NonNegativeReals)  #Installed power per tech

# Restrictions

def Constraint_PowerBal(m,t):
    return sum(m.G[t,tech] for tech in m.tech) == m.D[t]

model.PBal = pyo.Constraint(model.t, rule = pyo.Constraint_PowerBal)

# Restrictions on generation

    
def Constraint_wind1_coeff(m, t):
    return m.G[t,'W1'] <= m.P['W1']*m.wind1[t]


def Constraint_wind2_coeff(m, t):
    return m.G[t,'W2'] <= m.P['W2']*m.wind2[t]


def Constraint_solar1_coeff(m, t):
    return m.G[t,'PV1'] <= m.P['PV1']*m.PV1[t]


def Constraint_solar2_coeff(m, t): 
    return m.G[t,'PV2'] <= m.P['PV2']*m.PV2[t]

   
def Constraint_nuclear_coeff(m, t):
    return m.G[t,'Nuclear'] == m.P['Nuclear']


def Constraint_gas_coeff(m, t):
    return m.G[t, 'Gas'] <= m.P['Gas']


model.GW1 = pyo.Constraint(model.t, rule=Constraint_wind1_coeff)
model.GW2 = pyo.Constraint(model.t, rule=Constraint_wind2_coeff)
model.GPV1 = pyo.Constraint(model.t, rule=Constraint_solar1_coeff)
model.GPV2 = pyo.Constraint(model.t, rule=Constraint_solar2_coeff)
model.GNuc = pyo.Constraint(model.t, rule=Constraint_nuclear_coeff)
model.GGas = pyo.Constraint(model.t, rule=Constraint_gas_coeff)


#Restrictions on power installed

def Constraint_NuclearInstalled(m):
    return m.P['Nuclear'] >= m.InNuc

def Constraint_GasInstalled(m):
    return m.P['Gas'] >= m.InGas

model.minPNuc = pyo.Constraint(rule=Constraint_NuclearInstalled)
model.minPGas = pyo.Constraint(rule=Constraint_GasInstalled)


#Minimum renewable penetration

def Constraint_alpha(m):
    return sum(m.G[t,'PV1']+m.G[t,'PV2']+m.G[t,'W1']+m.G[t,'W2'] for t in m.t ) >= m.alpha*sum(m.D[t] for t in m.t)

model.CAlpha = pyo.Constraint(rule=Constraint_alpha) 

#Objective function

def f_obj(m):
    return sum(m.CAPEX[tech]*m.P[tech] for tech in m.tech) - m.CAPEX['Nuclear']*m.InNuc - m.CAPEX['Gas']*m.InGas + m.lifetime*sum(m.OPEX[tech]*m.G[t,tech] for t in m.t for tech in m.tech)

model.obj = Objective(rule=f_obj, sense=minimize)


##########

instance = model.create_instance()
results = opt.solve(instance)
instance.solutions.store_to(results)
results.write(filename='results.json', format='json')