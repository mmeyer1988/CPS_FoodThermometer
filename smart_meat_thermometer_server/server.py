import random
import sys
from azure.iot.hub import IoTHubRegistryManager
import os
import time
from azure.iot.hub.models import CloudToDeviceMethod

iothub_connection_str = "HostName=food-sensor-hub-masonmeyer.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=S4BfiAWLsCw917bRQJb8veS74WGC483T3bB7c2W8wVM="
device_id = "food-sensor"

method_name1 = "relay_on"
method_payload1 = ""

try:
    # Create IoTHubRegistryManager
    registry_manager = IoTHubRegistryManager(iothub_connection_str)

    deviceMethod = CloudToDeviceMethod(method_name=method_name1, payload=method_payload1)
    registry_manager.invoke_device_method(device_id, deviceMethod)
    print("executed method: " + method_name1 + " " + method_payload1)
    time.sleep(3)

except Exception as ex:
    print("Unexpected error {0}".format(ex))
except KeyboardInterrupt:
    print("iothub_registry_manager_sample stopped")