import sys
import json
from common.node_fmu import NodeFMU

fmu_models_folder = 'DemoGA/models_FMU/'
fmu_file = 'hpConsumerHot.fmu'
param_file = '../data/par.json'

with open(param_file) as json_data:
    parameters = json.load(json_data)

val_init = {
    't_in_cold': parameters['t_set'],
    't_in_hot': parameters['t_heat_ret'],
    't_heat': parameters['t_heat'],
    'p_heat': parameters['p_heating']
}

map_attr = {
    't_in_cold': 'Tin_cold',
    't_out_cold': 'Tout_cold',
    't_in_hot': 'Tin_hot',
    't_out_hot': 'Tout_hot',
    't_heat': 'Tout_hot_target',
    'p_heat': 'Pthermal_out',
    'p_elec': 'Pelectric'
}

input_attr = ['t_in_cold', 't_in_hot', 't_heat', 'p_heat']
output_attr = ['t_out_cold', 't_out_hot', 'p_elec']

if __name__ == "__main__":

    hp_heat = NodeFMU(host=sys.argv[1],
                      name='HeatPumpHeating',
                      fmu=fmu_models_folder + fmu_file,
                      map_attr=map_attr,
                      init_values=val_init,
                      output_attributes=output_attr,
                      input_attributes=input_attr,
                      is_first=True)

    print('Start heating heat pump node')
    hp_heat.start()
