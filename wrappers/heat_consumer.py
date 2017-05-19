import sys
import pyfmi
import redis
from obnl.client import ClientNode
import numpy as np


class HeatConsumer(ClientNode):
    def __init__(self, host, name, input_attributes=None, output_attributes=None, is_first=False):
        super(HeatConsumer, self).__init__(host, name, input_attributes, output_attributes, is_first)

        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def step(self, current_time, time_step):
        print('----- ' + self.name + ' -----')
        print(self.name, 'time_step', time_step)
        print(self.name, 'current_time', current_time)
        print(self.name, 'inputs', self.input_values)

        # TODO: store simulation results

        # Send update for all output attributes
        for o in self.output_attributes:
            v = np.random.normal(100, 10)
            print(self.name, o, ':', v)
            self.update_attribute(o, v)
        print('=============')


if __name__ == "__main__":

    heat_cons = HeatConsumer(host=sys.argv[1],
                             name='ConsumerHeating',
                             output_attributes=["p_heating"])

    print('Start heating consumer node')
    heat_cons.start()
