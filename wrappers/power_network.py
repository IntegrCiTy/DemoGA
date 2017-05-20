import sys
import pyfmi
import redis
from obnl.client import ClientNode
import numpy as np


class PowerNetwork(ClientNode):
    def __init__(self, host, name, input_attributes=None, output_attributes=None, is_first=False):
        super(PowerNetwork, self).__init__(host, name, input_attributes, output_attributes, is_first)

        self.redis = redis.StrictRedis(host=host, port=6379, db=0)

    def step(self, current_time, time_step):
        print('----- ' + self.name + ' -----')
        print(self.name, 'time_step', time_step)
        print(self.name, 'current_time', current_time)
        print(self.name, 'inputs', self.input_values)

        p = sum(self.input_values.values())

        print(self.name, 'p elec tot', p)
        self.redis.rpush('OUT_' + self.name + '_' + 'p_elec_tot', p)
        self.redis.rpush('OUT_' + self.name + '_' + 'p_elec_tot' + '_time', current_time)

        # TODO: store simulation results

        # Send update for all output attributes
        for o in self.output_attributes:
            v = np.random.normal(100, 10)
            print(self.name, o, ':', v)
            self.update_attribute(o, v)
            self.redis.rpush('OUT_' + self.name + '_' + o, v)
            self.redis.rpush('OUT_' + self.name + '_' + o + '_time', current_time)
        print('=============')


if __name__ == "__main__":
    net = PowerNetwork(host=sys.argv[1],
                       name='PowerNetwork',
                       input_attributes=["p_elec_hp_central", "p_elec_hp_cooling", "p_elec_hp_heating"],
                       is_first=True)

    print('Start power network node')
    net.start()
