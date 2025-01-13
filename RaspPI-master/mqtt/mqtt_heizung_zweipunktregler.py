#! /usr/bin/env python3

"""
Einfaches Python-Skript um Topics auf einem MQTT-Broker zu abbonieren.

Notwendige Bibliothek installieren:
 - pip3 install paho-mqtt

"""
import json
import pifacedigitalio as p
import paho.mqtt.client as mqtt
import sqlite3
import time
p.init()

DB_FILENAME = 'messungen.db'

TOPIC = "homeautomation/aussen/temperatur"

conn = sqlite3.connect(DB_FILENAME, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS temp_aussen (id INTEGER PRIMARY KEY AUTOINCREMENT,
               date DATE, value float)""")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f'Connected to broker ({reason_code}).')
    if reason_code > 0:
        print('Error connecting to broker!')

jsonmessage = 0
def on_message(client, userdata, message):
    print(f'Incoming message on topic "{message.topic}": {message.payload} (QoS: {message.qos})')
    try:
        jsonmessage=json.loads(message.payload)
        sensor_value = jsonmessage["sensor_data"][0]["sensor_value"]
        cursor.execute("""INSERT INTO temp_aussen VALUES (NULL, ?, ?)""", (time.time(), sensor_value))
        zweipunktregler(9,sensor_value,2)
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error processing message payload: {e}")

def on_publish(client, userdata, mid, reason_codes, properties):
    print(f'Publishing message on topic ({mid})')


def on_subscribe(client, userdata, mid, reason_codes, properties):
    for sub_result in reason_codes:
        if sub_result == 1:
            print(f'Subscribing to topic ({reason_codes}, {mid}).')
        if sub_result >= 128:
            print('Error subscribing to topic!')

def zweipunktregler(setpoint, temp, hysteresis):
    if temp <= setpoint - hysteresis:
        p.digital_write(0, 1)
    elif temp >= setpoint + hysteresis:
        p.digital_write(0, 0)




#erzeuge Objekt für die Verbindung zum MQTT-Broker
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# setze Funktionen für verschiedene Ereignisse
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.on_subscribe = on_subscribe
# baue Verbindung zum Broker auf
mqtt_client.connect('192.168.24.251', port=1883, keepalive=120)


# abboniere ein Thema beim Broker
mqtt_client.subscribe(TOPIC, 0)

# starte eine Endlosschleife, die auf neue Nachrichten des Brokers wartet
mqtt_client.loop_forever()