import yaml

from meter_reader import MeterReader
from smart_meter_reader import SmartMeterReader
from goodwe_conv_reader import GoodWeConverterReader



def main(cfg_file):
    #reading the config file
    with open("config.yaml", "r") as f:
        config = yaml.load(f)
    meter_reader = MeterReader(config['overall'])
    meter_reader.add_reader(SmartMeterReader(config['smart_meter']))
    meter_reader.add_reader(GoodWeConverterReader(config['good_we_pvv']))
    meter_reader.start_reading()



if __name__ == '__main__':
    main()
