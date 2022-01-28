import goodwe


class GoodWeConverterReader:
    def __init__(self, cfg):
        self.ip_address = cfg['ip_address']
        self.objects = cfg['objects_to_read']

    async def read_meter(self):
        try:
            inverter = await goodwe.connect(self.ip_address)
            runtime_data = await inverter.read_runtime_data()
            result_dict = {}
            for item in self.objects:
                index = [object.id_ for object in inverter.sensors()].index(item)
                sensor = inverter.sensors()[index]
                result_dict[item] = runtime_data[sensor.id_]
                return result_dict
        except:
            # goodwe is off line so write 0.0 and return that
            result_dict = {}
            for item in self.objects:
                result_dict[item] = 0.0
                print('exception inverter not running')
                return result_dict