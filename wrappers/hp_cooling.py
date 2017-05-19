import sys
from common.node_fmu import NodeFMU

fmu_models_folder = '../models_FMU/'
fmu_file = 'DHS_csBlocks_hpConsumerCold.fmu'

map_attr = {
    't_in_cold': 'Tin_cold',
    't_out_cold': 'Tout_cold',
    't_in_hot': 'Tin_hot',
    't_out_hot': 'Tout_hot',
    't_set': 'Tout_cold_target',
    'p_cool': 'Pthermal_in',
    'p_elec': 'Pelectric'
}

input_attr = ['t_in_cold', 't_in_hot', 't_set', 'p_cool']
output_attr = ['t_out_cold', 't_out_hot', 'p_elec']

if __name__ == "__main__":

    hp_cool = NodeFMU(host=sys.argv[1],
                      name='HeatPumpCooling',
                      fmu=fmu_models_folder + fmu_file,
                      map_attr=map_attr,
                      output_attributes=output_attr,
                      input_attributes=input_attr,
                      is_first=True)

    print('Start cooling heat pump node')
    hp_cool.start()
