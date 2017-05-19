import sys
from common.node_fmu import NodeFMU

fmu_models_folder = '../../models_FMU/'
fmu_file = 'DHS_csBlocks_hpCentral.fmu'

map_attr = {
    't_in_cold': 'Tin_cold',
    't_out_cold': 'Tout_cold',
    't_in_hot': 'Tin_hot',
    't_out_hot': 'Tout_hot',
    't_set': 'Tout_hot_target',
    'p_heat_in': 'Pthermal_in',
    'p_heat_out': 'Pthermal_out',
    'p_elec': 'Pelectric'
}

input_attr = ['t_in_cold', 't_in_hot', 't_set']
output_attr = ['t_out_cold', 't_out_hot', 'p_elec', 'p_heat_in', 'p_heat_out']

if __name__ == "__main__":

    hp_lake = NodeFMU(host=sys.argv[1],
                      name='HeatPumpCentral',
                      fmu=fmu_models_folder + fmu_file,
                      map_attr=map_attr,
                      output_attributes=output_attr,
                      input_attributes=input_attr,
                      is_first=True)

    print('Start central heat pump node')
    hp_lake.start()
