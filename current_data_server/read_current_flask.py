from flask import Flask
from flask import jsonify
import yaml
from goodwe_conv_reader import GoodWeConverterReader
from smart_meter_reader import SmartMeterReader
import asyncio

app = Flask(__name__)
# reading the config file
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
readers = [ #SmartMeterReader(config['readers']['smart_meter']),
           GoodWeConverterReader(config['readers']['good_we_pvv'])]


@app.route('/', methods=['GET'])
def hello_world4():
    return jsonify({'message': 'hello world'})


@app.route('/readall', methods=['GET'])
def read_all():
    results = read_all_data()
    print(results)
    return jsonify(results)


@app.route('/readsmartreader', methods=['GET'])
def hello_world2():
    return jsonify({'message': 'hello world'})


@app.route('/readpvv', methods=['GET'])
def hello_world3():
    return jsonify({'message': 'hello world'})


def read_all_data():
    result = []
    for reader in readers:
        result.append(asyncio.run(reader.read_meter()))
    return result


if __name__ == '__main__':
    # reading the config file
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)
    app.run(debug=True, port=config['settings']['port'], host=config['settings']['host'])
