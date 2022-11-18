
l_min_renewables = [0.3,0.1,0.2,]  # minimum percentage of renewables [pu]
l_save_results = ['Results30.xlsx','Results10.xlsx','Results20.xlsx']

ii=0
for ii in range(3):
    min_renewables = l_min_renewables[ii]
    save_results = l_save_results[ii]

    from post_processing import *
