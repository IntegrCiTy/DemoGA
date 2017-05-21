import sys
import json
from common.node_fmu import NodeFMU

fmu_models_folder = 'DemoGA/models_FMU/'
fmu_file = 'threeDoublePipesNode.fmu'
param_file = 'DemoGA/data/par.json'

with open(param_file) as json_data:
    parameters = json.load(json_data)

val_init = {
    't_ret_cool': parameters['t_set'] - 5,
    't_ret_heat': parameters['t_set'] + 5,
    't_ret': parameters['t_set'],
    't_sup': parameters['t_set'] - 5,
    't_sup_cool': parameters['t_set'],
    't_sup_heat': parameters['t_set'],
    'mflow_central': parameters['mflow_lake'],
    'mflow_heating': parameters['mflow_heat'],
    'mflow_cooling': parameters['mflow_cool'],
}

map_attr = {
    't_sup': 'T0_in',
    't_ret_heat': 'Th_in',
    't_ret_cool': 'Tc_in',
    't_ret': 'T0_out',
    't_sup_heat': 'Th_out',
    't_sup_cool': 'Tc_out',
    'mflow_central': 'mflow0_in'
    'mflow_heating': 'mflowh_in'
    'mflow_cooling': 'mflowc_in'
}

input_attr = ['t_sup', 't_ret_cool', 't_ret_heat']
output_attr = ['t_ret', 't_sup_cool', 't_sup_heat']

if __name__ == "__main__":

    net = NodeFMU(host=sys.argv[1],
                  name='ThermalNetwork',
                  fmu=fmu_models_folder + fmu_file,
                  map_attr=map_attr,
                  init_values=val_init,
                  output_attributes=output_attr,
                  input_attributes=input_attr,
                  is_first=True)

    print('Start thermal network node')
    net.start()
