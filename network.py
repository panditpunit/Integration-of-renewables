# 1) Create network using pandapower

import pandapower as pp

# Create network object
network = pp.create_empty_network(name='Network Catalunya')

# Add buses to network
V_max = 1.1 # maximum bus voltage [pu]
V_min = 0.9 # minimum bus voltage [pu]
V_grid = 1 # the grid voltage level
# geodata = (x,y) --> coordenates used for plotting
# coords = [(x1,y1),(x2,y2)] --> where 1 is start and 2 is endpoint of the busbar
pp.create_bus(network, name="bus 1", index=1, vn_kv=V_grid, geodata=None, type="b", in_service=True, max_vm_pu=V_max, min_vm_pu=V_min, coords=None)
pp.create_bus(network, name="bus 2", index=2, vn_kv=V_grid, geodata=None, type="b", in_service=True, max_vm_pu=V_max, min_vm_pu=V_min, coords=None)
pp.create_bus(network, name="bus 3", index=3, vn_kv=V_grid, geodata=None, type="b", in_service=True, max_vm_pu=V_max, min_vm_pu=V_min, coords=None)
pp.create_bus(network, name="bus 4", index=4, vn_kv=V_grid, geodata=None, type="b", in_service=True, max_vm_pu=V_max, min_vm_pu=V_min, coords=None)
pp.create_bus(network, name="bus 5", index=5, vn_kv=V_grid, geodata=None, type="b", in_service=True, max_vm_pu=V_max, min_vm_pu=V_min, coords=None)
pp.create_bus(network, name="bus 6", index=6, vn_kv=V_grid, geodata=None, type="b", in_service=True, max_vm_pu=V_max, min_vm_pu=V_min, coords=None)
pp.create_bus(network, name="bus 7", index=7, vn_kv=V_grid, geodata=None, type="b", in_service=True, max_vm_pu=V_max, min_vm_pu=V_min, coords=None)
pp.create_bus(network, name="bus 8", index=8, vn_kv=V_grid, geodata=None, type="b", in_service=True, max_vm_pu=V_max, min_vm_pu=V_min, coords=None)
pp.create_bus(network, name="bus 9", index=9, vn_kv=V_grid, geodata=None, type="b", in_service=True, max_vm_pu=V_max, min_vm_pu=V_min, coords=None)
pp.create_bus(network, name="bus 10", index=10, vn_kv=V_grid, geodata=None, type="b", in_service=True, max_vm_pu=V_max, min_vm_pu=V_min, coords=None)
# repeat for all buses

# Add lines to network
R_lines = 0.06534 # Ohm/km --> line resistance
X_lines = 0.3978 # Ohm/km --> line reactance
C_lines = 9.1591 # nF/km ???????????????? --> line capacitance (line-to-earth)
I_max = 0.79443 # maximum thermal current [kA]
# geodata=None --> The first row should be the coordinates of bus a and the last should be the coordinates of bus b. The points in the middle represent the bending points of the line
# parallel=1 --> number of parallel line systems
# max_loading_percent=nan --> maximum current loading (only needed for OPF)
# pp.create_line_from_parameters(network, name="line 1-2", index=1, from_bus=1, to_bus=2, length_km=10, r_ohm_per_km=R_lines, x_ohm_per_km=X_lines, c_nf_per_km=C_lines, max_i_ka=I_max, geodata=None, in_service=True, parallel=1, max_loading_percent='NaN')
pp.create_line_from_parameters(network, name="line 1-2", index=1, from_bus=1, to_bus=2, length_km=40, r_ohm_per_km=R_lines, x_ohm_per_km=X_lines, c_nf_per_km=C_lines, max_i_ka=I_max, in_service=True, parallel=1, max_loading_percent='NaN')
pp.create_line_from_parameters(network, name="line 2-3", index=2, from_bus=2, to_bus=3, length_km=85, r_ohm_per_km=R_lines, x_ohm_per_km=X_lines, c_nf_per_km=C_lines, max_i_ka=I_max, in_service=True, parallel=1, max_loading_percent='NaN')
pp.create_line_from_parameters(network, name="line 3-4", index=3, from_bus=3, to_bus=4, length_km=38, r_ohm_per_km=R_lines, x_ohm_per_km=X_lines, c_nf_per_km=C_lines, max_i_ka=I_max, in_service=True, parallel=1, max_loading_percent='NaN')
pp.create_line_from_parameters(network, name="line 4-5", index=4, from_bus=4, to_bus=5, length_km=48, r_ohm_per_km=R_lines, x_ohm_per_km=X_lines, c_nf_per_km=C_lines, max_i_ka=I_max, in_service=True, parallel=1, max_loading_percent='NaN')
pp.create_line_from_parameters(network, name="line 5-6", index=5, from_bus=5, to_bus=6, length_km=41, r_ohm_per_km=R_lines, x_ohm_per_km=X_lines, c_nf_per_km=C_lines, max_i_ka=I_max, in_service=True, parallel=1, max_loading_percent='NaN')
pp.create_line_from_parameters(network, name="line 6-7", index=6, from_bus=6, to_bus=7, length_km=100, r_ohm_per_km=R_lines, x_ohm_per_km=X_lines, c_nf_per_km=C_lines, max_i_ka=I_max, in_service=True, parallel=1, max_loading_percent='NaN')
pp.create_line_from_parameters(network, name="line 7-8", index=7, from_bus=7, to_bus=8, length_km=100, r_ohm_per_km=R_lines, x_ohm_per_km=X_lines, c_nf_per_km=C_lines, max_i_ka=I_max, in_service=True, parallel=1, max_loading_percent='NaN')
pp.create_line_from_parameters(network, name="line 8-9", index=8, from_bus=8, to_bus=9, length_km=100, r_ohm_per_km=R_lines, x_ohm_per_km=X_lines, c_nf_per_km=C_lines, max_i_ka=I_max, in_service=True, parallel=1, max_loading_percent='NaN')
pp.create_line_from_parameters(network, name="line 9-10", index=9, from_bus=9, to_bus=10, length_km=100, r_ohm_per_km=R_lines, x_ohm_per_km=X_lines, c_nf_per_km=C_lines, max_i_ka=I_max, in_service=True, parallel=1, max_loading_percent='NaN')
# repeat for all lines

# Add generators to network
# pp.create_gen(network, name="slack", bus=1, p_mw=10, vm_pu=1, slack=True)
# pp.create_gen(network, name="PV1", bus=2, )

'''
# # Add generators to network object
# pp.create_gen(network, name="gen 5", bus=5, p_mw=0.75, vm_pu=1.10, \
# max_q_mvar=0.01, min_q_mvar=-0.01)
#
# # Add loads to network object
# pp.create_load(network, name="load 2", bus=2, p_mw=0.65, q_mvar=0.41)
# pp.create_load(network, name="load 3", bus=3, p_mw=0.88, q_mvar=0.56)
# pp.create_load(network, name="load 4", bus=4, p_mw=0.64, q_mvar=0.48)

# pp.runpp(network, enforce_q_lims=True)
###
'''


# 2) Create dictionaties to initialize linear Power Flow matrices (A, B and D)

import pandas as pd

def A_matrix_ini(network):  # A [branch,i] =1 if the line "branch" goes from bus "i"
                             # A [branch,i] =0 otherwise and if bus "i" is slack (bus 1)
    bus_index = list(network.bus.index)
    line_index = list(network.line.index)
    dict = {}
    for branch in line_index:
        for bus in bus_index:
            dict[branch, bus] = 0
        bus_ini = network.line["from_bus"][branch]
        if bus_ini != 1:
            dict[branch, bus_ini] = 1
    return dict

def A_matrix_fin(network):  # A [branch,i] =1 if the line "branch" comes to bus "i"
                            # A [branch,i] =0 otherwise and if bus "i" is slack (bus 1)
    bus_index = list(network.bus.index)
    line_index = list(network.line.index)
    dict = {}
    for branch in line_index:
        for bus in bus_index:
            dict[branch, bus] = 0
        bus_fin = network.line["to_bus"][branch]
        if bus_fin != 1:
            dict[branch, bus_fin] = 1
    return dict

def B_matrix(network):  # Y_bus = j * B
    bus_index = list(network.bus.index)
    dict = {}
    for i in bus_index[1:]:
        for j in bus_index[1:]:
            net=network
            #
            dict[(i, j)] = 0
            #
            if i == j:
                # B [i,i] = sum ( 1/(X*L) for all lines connected to bus i)
                df = net.line[(net.line["from_bus"] == i) | (net.line["to_bus"] == i)][["length_km", "x_ohm_per_km"]]
                for idx in df.index:
                    dict[(i, j)] += 1 / (df["length_km"][idx] * df["x_ohm_per_km"][idx])
            else:
                # B [i,j] = -1/(X*L) for the line between buses i,j
                if not (net.line[(net.line["from_bus"] == i) & (net.line["to_bus"] == j)].empty):
                    df = net.line[(net.line["from_bus"] == i) & (net.line["to_bus"] == j)]
                    dict[(i, j)] = -1 / (df["length_km"].values[0] * df["x_ohm_per_km"].values[0])
                elif not (net.line[(net.line["from_bus"] == j) & (net.line["to_bus"] == i)].empty):
                    df = net.line[(net.line["from_bus"] == j) & (net.line["to_bus"] == i)]
                    dict[(i, j)] = -1 / (df["length_km"].values[0] * df["x_ohm_per_km"].values[0])
    return dict

def D_matrix(network):  # D is a diagonal matrix with the imag(Y) values of the lines
    bus_index = list(network.bus.index)
    line_index = list(network.line.index)
    dict = {}
    for branch in line_index:
        for line in line_index:
            dict[branch, line] = 0
        line_length = network.line['length_km'][branch]
        line_x = network.line['x_ohm_per_km'][branch]
        dict[branch, branch] = 1 / (line_x * line_length)
    return dict

'''
def save_matrixes(network):
    A = A_matrix(network)
    B = B_matrix(network)
    D = D_matrix(network)
    bus_index = list(network.bus.index)[1:]
    line_index = list(network.line.index)
    df_A = pd.DataFrame([], index=line_index, columns=bus_index)
    df_B = pd.DataFrame([], index=bus_index, columns=bus_index)
    df_D = pd.DataFrame([], index=line_index, columns=line_index)
    print(A)
    print(line_index)
    print(bus_index)
    #for line in line_index:
        #for bus in bus_index:
            #df_A.iloc[line][bus] = A[line,bus]
            #print(line,bus)
save_matrixes(network)
'''

# 3) Set other network parameters

l_n = list(network.bus.index) # list with the bus indexes
l_naux = l_n[1:]  # list with the bus indexes without slack bus
l_branches = list(network.line.index)  # list with the lines indexes

Demand_nodes = {1:0,
                2:0.1,
                3:0.5,
                4:0,
                5:0.1,
                6:0,
                7:0.1,
                8:0,
                9:0.1,
                10:0.1}  # dict (node index: % demand [pu])

Pmax_line = 10**10
Pmax_lines = {line_index:Pmax_line for line_index in l_branches}  # dict (line index: maximum power flowing through the line [??])

Nuclear_nodes = {1:0, 2:0, 3:0, 4:0, 5:1, 6:0, 7:0, 8:0, 9:0, 10:0}  # dict (node: % nuclear power in that node [pu])
Gas_nodes = {1:0, 2:0, 3:1, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}  # dict (node: % gas power in that node [pu])
PV_nodes = {(1,1):0, (1,2):0, (1,3):0, (1,4):1, (1,5):0, (1,6):0, (1,7):0, (1,8):0, (1,9):0, (1,10):0,
            (2,1):0, (2,2):0, (2,3):0, (2,4):0, (2,5):0, (2,6):1, (2,7):0, (2,8):0, (2,9):0, (2,10):0}  # dict ((PV loc,node): % PV power in that node [pu])
Wind_nodes = {(1,1):1, (1,2):0, (1,3):0, (1,4):0, (1,5):0, (1,6):0, (1,7):0, (1,8):0, (1,9):0, (1,10):0,
            (2,1):0, (2,2):0, (2,3):0, (2,4):0, (2,5):0, (2,6):0, (2,7):0, (2,8):1, (2,9):0, (2,10):0}  # dict ((Wind loc,node): % Wind power in that node [pu])


def get_l_n():
    return l_n

def get_l_naux():
    return l_naux

def get_l_branches():
    return l_branches

def get_A_matrix_ini():
    A = A_matrix_ini(network)
    bus_index = list(network.bus.index)
    line_index = list(network.line.index)
    new_A = {}
    for branch in line_index:
        for bus in bus_index:
            if bus != 1:
                new_A[branch,bus] = A[branch,bus]
    return new_A

def get_A_matrix_fin():
    A = A_matrix_fin(network)
    bus_index = list(network.bus.index)
    line_index = list(network.line.index)
    new_A = {}
    for branch in line_index:
        for bus in bus_index:
            if bus != 1:
                new_A[branch,bus] = A[branch,bus]
    return new_A

def get_B_matrix():
    B = B_matrix(network)
    bus_index = list(network.bus.index)
    new_B = {}
    for i in bus_index:
        for j in bus_index:
            if (i != 1) & (j != 1):
                new_B[i,j] = B[i,j]
    return new_B

def get_D_matrix():
    return D_matrix(network)

def get_Demand_nodes():
    return Demand_nodes

def get_Pmax_lines():
    return Pmax_lines

def get_Generation_nodes(tech):
    if tech == 'Nuclear':
        return Nuclear_nodes
    elif tech == 'Gas':
        return Gas_nodes
    elif tech == 'PV':
        return PV_nodes
    elif tech == 'Wind':
        return Wind_nodes
    else:
        return
