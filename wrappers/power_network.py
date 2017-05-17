import pyfmi
import redis
from obnl.client import ClientNode
import numpy as np


class PowerNetwork(ClientNode):
    def __init__(self, host, name, input_attributes=None, output_attributes=None, is_first=False):
        super(PowerNetwork, self).__init__(host, name, input_attributes, output_attributes, is_first)

        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def step(self, current_time, time_step):
        print('----- ' + self.name + ' -----')
        print(self.name, 'time_step', time_step)
        print(self.name, 'current_time', current_time)
        print(self.name, 'inputs', self.input_values)

        print(self.name, 'p elec tot', sum(self.input_values.values()))

        # TODO: store simulation results

        # Send update for all output attributes
        for o in self.output_attributes:
            v = np.random.normal(100, 10)
            print(self.name, o, ':', v)
            self.update_attribute(o, v)
        print('=============')


if __name__ == "__main__":
    net = PowerNetwork(host='localhost',
                       name='PowerNetwork',
                       input_attributes=["p_elec_hp_central", "p_elec_hp_cooling", "p_elec_hp_heating"])

    print('Start power network node')
    net.start()
