import sys
import pyfmi
import redis
from obnl.client import ClientNode
import numpy as np


class HeatConsumer(ClientNode):
    def __init__(self, host, name, input_attributes=None, output_attributes=None, is_first=False):
        super(HeatConsumer, self).__init__(host, name, input_attributes, output_attributes, is_first)

        self.redis = redis.StrictRedis(host=host, port=6379, db=0)

    def step(self, current_time, time_step):
        print('----- ' + self.name + ' -----')
        print(self.name, 'time_step', time_step)
        print(self.name, 'current_time', current_time)

        # Send update for all output attributes
        p_heating = np.random.uniform(80, 120)
        t_heating = np.random.uniform(55, 65) + 273.15
        print(self.name, 'p_heating', ':', p_heating)
        print(self.name, 't_heating', ':', t_heating)

        self.update_attribute('p_heating', p_heating)
        self.update_attribute('t_heating', t_heating)

        self.redis.rpush('OUT_' + self.name + '_' + 'p_heating', p_heating)
        self.redis.rpush('OUT_' + self.name + '_' + 'p_heating' + '_time', current_time)

        self.redis.rpush('OUT_' + self.name + '_' + 't_heating', t_heating)
        self.redis.rpush('OUT_' + self.name + '_' + 't_heating' + '_time', current_time)
        print('=============')


if __name__ == "__main__":

    heat_cons = HeatConsumer(host=sys.argv[1],
                             name='ConsumerHeating',
                             output_attributes=["p_heating"])

    print('Start heating consumer node')
    heat_cons.start()
