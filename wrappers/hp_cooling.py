import sys
import json
from common.node_fmu import NodeFMU

fmu_models_folder = 'DemoGA/models_FMU/'
fmu_file = 'hpConsumerCold.fmu'
param_file = 'DemoGA/data/par.json'

with open(param_file) as json_data:
    parameters = json.load(json_data)

val_init = {
    't_in_cold': parameters['t_cool_ret'],
    't_out_cold_init': parameters['t_cool_ret'],
    't_in_hot': parameters['t_set'],
    't_cool': parameters['t_cool'],
    'p_cool': parameters['p_cooling'],
    'mflow_hs': parameters['mflow_cool'],
    'mflow_cs': parameters['mflow_cool_src']
}

map_attr = {
    't_in_cold': 'Tin_cold',
    't_out_cold': 'Tout_cold',
    't_out_cold_init': 'Tout_cold_init',
    't_in_hot': 'Tin_hot',
    't_out_hot': 'Tout_hot',
    't_cool': 'Tout_cold_target',
    # 'p_cool': 'Pthermal_cons',
    'p_cool': 'Pthermal_in',
    'p_elec': 'Pelectric',
    'mflow_hs': 'mflow_in_hot',
    'mflow_cs': 'mflow_in_cold'
}

input_attr = ['t_in_cold', 't_in_hot', 't_cool', 'p_cool']
output_attr = ['t_out_cold', 't_out_hot', 'p_elec']

if __name__ == "__main__":

    hp_cool = NodeFMU(host=sys.argv[1],
                      name='HeatPumpCooling',
                      fmu=fmu_models_folder + fmu_file,
                      map_attr=map_attr,
                      init_values=val_init,
                      output_attributes=output_attr,
                      input_attributes=input_attr,
                      is_first=True)

    print('Start cooling heat pump node')
    hp_cool.start()
