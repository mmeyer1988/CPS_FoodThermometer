import time
from os import path
import csv
import json
from datetime import datetime
from counterfit_shims_grove.counterfit_connection import CounterFitConnection
from counterfit_shims_seeed_python_dht import DHT
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_led import GroveLed

from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

connection_string = "HostName=food-sensor-hub-masonmeyer.azure-devices.net;DeviceId=food-sensor;SharedAccessKey=Co+dqsb4jl4clIGyeitP1VBI+ym0ugHmOd7gbQPl/dw="

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('Connecting')
device_client.connect()
print('Connected')

CounterFitConnection.init('127.0.0.1', 5000)

sensor = DHT("11", 0)
led = GroveLed(5)

relay = GroveRelay(6)


temperature_file_name = 'temperature.csv'
fieldnames = ['date', 'temperature']


print('Mason Meyer - A Simple Internet Food Thermometer')

target_temperature = int(input('* Set Target Temperature (less than 550 F): '))
time_sleep = int(input('* Notify me every ___ seconds: '))

print('Target temperature : '+ str(target_temperature))
temp = 0.0
payload = 0

def handle_method_request(request):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)

device_client.on_method_request_received = handle_method_request

while temp < target_temperature:



    humi, temp = sensor.read()
    temp = int(temp)

    message = Message(json.dumps({'food-temperature': temp}))
    device_client.send_message(message)

    print('    * Current Temp: ' + str(temp) + ' * Target Temp: ' + str(target_temperature))
    print('    * Moisture Level: ', humi)
    if temp < target_temperature:
        led.off()
        print('...Still heating to ' + str(target_temperature))

    else:
        if temp != target_temperature:
            pass
        else:
            print( '        * Target Temperature ' + str(target_temperature) + ' reached!')

        if temp > target_temperature:
           led.on()
           print('*** Warning: ' + str(target_temperature) + ' exceeded!')

    

    time.sleep(time_sleep)






