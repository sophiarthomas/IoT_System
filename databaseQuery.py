from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
import mongoDBkey as key
from datetime import datetime, timedelta
from binaryTree import load_data_to_tree


# Query all devices' names from metadata
def get_device_names(metadata):
    query = {"customAttributes.type": "DEVICE"}
    devices = metadata.find(query)

    # Storing device names in a list
    device_names = []
    for device in devices:
        device_names.append(device["customAttributes"]["name"])

    return device_names


# Query 1: What is the average moisture inside my kitchen fridge in the past three hours?
def fridge_moisture(tree):
    # Get the timestamp for 3 hours ago
    time = datetime.now()
    most_recent_timestamp = int(time.timestamp())
    #most_recent_timestamp = 1733203151
    three_hours_ago_timestamp = int(most_recent_timestamp - (3 * 3600))

    virtual_devices = tree.in_order_traversal()
    total_moisture = 0
    count = 0

    for virtual_device in virtual_devices:
        for device in virtual_device.get('virtual_devices', []):
            if 'payload' in device:
                payload = device['payload']
                timestamp = int(payload['timestamp'])

                if three_hours_ago_timestamp <= timestamp <= most_recent_timestamp:
                    if 'Moisture Meter - Water' in payload:
                        moisture_value = float(payload['Moisture Meter - Water'])
                        total_moisture += moisture_value
                        count += 1
            #         else:
            #             print(f"No Moisture Meter data found in payload: {payload}")
            #     else:
            #         print(f"Dataset timestamp {timestamp} is outside the range.")
            # else:
            #     print('No payload found in this device')

    # Calculate the average moisture.
    if count > 0:
        average_moisture = total_moisture / count
        print(f"Average Moisture Meter value in last 3 hours: {average_moisture}%")
    else:
        print("No valid Moisture Meter data within the specified time range.")


# Query 2: What is the average water consumption per cycle in my smart dishwasher?
def avg_water_consumption(virtual):
    pass


# Query 3: Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?
def electricity_consumption(tree):
    pass


def main(msg):
    # Load environment variables from .env file
    load_dotenv()

    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise EnvironmentError("MONGODB_URI is not set in the environment or .env file.")

    # Create a new client and connect to the server
    client = MongoClient(uri, tlsAllowInvalidCertificates=True) # REMOVE WHEN DONE

    # Database
    db = client[key.database]

    # Collections
    devices = db[key.devices]
    metadata = db[key.metadata]
    virtual = db[key.virtual]

    # Load data into tree
    tree = load_data_to_tree()

    if msg == "What is the average moisture inside my kitchen fridge in the past three hours?":
        fridge_moisture(tree)
    elif msg == "What is the average water consumption per cycle in my smart dishwasher?":
        avg_water_consumption(tree)
    elif msg == "What device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?":
        electricity_consumption(tree)


if __name__ == "__main__":
    main("What is the average moisture inside my kitchen fridge in the past three hours?")
