import pyfmi
import redis
from obnl.client import ClientNode


class NodeFMU(ClientNode):
    def __init__(self, host, name, fmu, map_attr, init_values=None, input_attributes=None, output_attributes=None, is_first=False):
        super(NodeFMU, self).__init__(host, name, input_attributes, output_attributes, is_first)

        self.model = pyfmi.load_fmu(fmu, log_level=2)
        self.redis = redis.StrictRedis(host=host, port=6379, db=0)

        self.map_attr = map_attr

        try:
            self.model.setup_experiment()
        except AttributeError:
            pass

        self.model.initialize()

        if init_values:
            for key, value in init_values.items():
                self.model.set(self.map_attr[key], value)

    def step(self, current_time, time_step):
        print('----- ' + self.name + ' -----')
        print(self.name, 'time_step', time_step)
        print(self.name, 'current_time', current_time)
        print(self.name, 'inputs', self.input_values)

        # Set input values to FMU + send IN values to redis (/!\ at time values)
        for o, value in self.input_values.items():
            self.model.set(self.map_attr[o], value)
            self.redis.rpush('IN_' + self.name + '_' + o, value)
            self.redis.rpush('IN_' + self.name + '_' + o + '_time', current_time)

        opts = self.model.simulate_options()
        opts['initialize'] = False
        opts['result_handling'] = "memory"

        # Run simulation step
        res = self.model.simulate(start_time=current_time - time_step, final_time=current_time, options=opts)

        # TODO: store intern state simulation results

        # Send update for all output attributes + send OUT values to redis
        for o in self.output_attributes:
            print(self.name, o, ':', res[self.map_attr[o]][-1])
            self.update_attribute(o, res[self.map_attr[o]][-1])
            self.redis.rpush('OUT_' + self.name + '_' + o, *res[self.map_attr[o]])
            self.redis.rpush('OUT_' + self.name + '_' + o + '_time', *res['time'])
        print('=============')
