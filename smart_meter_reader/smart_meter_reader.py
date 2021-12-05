import sys
from smeterd.meter import SmartMeter


class SmartMeterReader:
    def __init__(self, config_data):
        self.address = config_data['address']
        self.baud_rate = config_data['baud_rate']

    async def read_meter(self):
        try:
            meter = SmartMeter(self.address)
            meter.serial.baudrate = self.baud_rate
            packet = meter.read_one_packet()
            meter.disconnect()
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            result_dict = {'gas': 0.0,
                           'low_consumed': 0.0,
                           'high_consumed': 0.0,
                           'current_consumed': 0.0,
                           'produced_low': 0.0,
                           'produced_high': 0.0,
                           'current_produced': 0.0}
            return result_dict
        result_dict = {'gas': packet['gas']['total'],
                       'low_consumed': packet['kwh']['low']['consumed'],
                       'high_consumed': packet['kwh']['high']['consumed'],
                       'current_consumed': packet['kwh']['current_consumed'],
                       'produced_low': packet['kwh']['low']['produced'],
                       'produced_high': packet['kwh']['high']['produced'],
                       'current_produced': packet['kwh']['current_produced']}
        return result_dict
