import sys
from common.node_fmu import NodeFMU

fmu_models_folder = 'DemoGA/models_FMU/'
fmu_file = 'threeDoublePipesNode.fmu'

map_attr = {
    't_sup': 'T0_in',
    't_ret_heat': 'Th_in',
    't_ret_cool': 'Tc_in',
    't_ret': 'T0_out',
    't_sup_heat': 'Th_out',
    't_sup_cool': 'Tc_out'
}

input_attr = ['t_sup', 't_ret_cool', 't_ret_heat']
output_attr = ['t_ret', 't_sup_cool', 't_sup_heat']

if __name__ == "__main__":

    net = NodeFMU(host=sys.argv[1],
                  name='ThermalNetwork',
                  fmu=fmu_models_folder + fmu_file,
                  map_attr=map_attr,
                  output_attributes=output_attr,
                  input_attributes=input_attr)

    print('Start thermal network node')
    net.start()
