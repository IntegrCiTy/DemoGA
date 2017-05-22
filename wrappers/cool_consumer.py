import sys
import pyfmi
import redis
from obnl.client import ClientNode
import numpy as np


class CoolConsumer(ClientNode):
    def __init__(self, host, name, input_attributes=None, output_attributes=None, is_first=False):
        super(CoolConsumer, self).__init__(host, name, input_attributes, output_attributes, is_first)

        self.redis = redis.StrictRedis(host=host, port=6379, db=0)

    def step(self, current_time, time_step):
        print('----- ' + self.name + ' -----')
        print(self.name, 'time_step', time_step)
        print(self.name, 'current_time', current_time)

        # Send update for all output attributes
        p_cooling = np.random.uniform(10, 50)
        t_cooling = np.random.uniform(1, 5) + 273.15
        print(self.name, 'p_cooling', ':', p_cooling)
        print(self.name, 't_cooling', ':', t_cooling)

        self.update_attribute('p_cooling', p_cooling)
        self.update_attribute('t_cooling', t_cooling)

        self.redis.rpush('OUT_' + self.name + '_' + 'p_cooling', p_cooling)
        self.redis.rpush('OUT_' + self.name + '_' + 'p_cooling' + '_time', current_time)

        self.redis.rpush('OUT_' + self.name + '_' + 't_cooling', t_cooling)
        self.redis.rpush('OUT_' + self.name + '_' + 't_cooling' + '_time', current_time)
        print('=============')


if __name__ == "__main__":

    cool_cons = CoolConsumer(host=sys.argv[1],
                             name='ConsumerCooling',
                             output_attributes=["p_cooling"])

    print('Start cooling consumer node')
    cool_cons.start()
