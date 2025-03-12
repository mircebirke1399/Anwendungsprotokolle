
"""
Einfacher OPC UA-Client

Notwendige Bibliothek installieren:

    apt-get install python3-lxml
    pip3 install opcua 

Für den Zugriff auf Variablen wird die OPC UA Notation genutzt:

    ns=<namespaceIndex>;<identifiertype>=<identifier>
    
    <namespace index> -> namespace index
    <identifier type> -> flag that specifies the identifier type:
                         Flag	Identifier Type
                         i	    NUMERIC (UInteger)
                         s	    STRING (String)
                         g	    GUID (Guid)
                         b	    OPAQUE (ByteString)

Quelle: http://documentation.unified-automation.com/uasdkhp/1.0.0/html/_l2_ua_node_ids.html

"""

import time
from opcua import Client
from influxdb_client_3 import InfluxDBClient3, Point

#certificate_path = "C:\\Users\\mirco\\OneDrive\\VIT\\Anwendungsprotokolle\\RaspPI-master\\opc\\opc ua\\client_certificate.pem"
#private_key_path = "C:\\Users\\mirco\\OneDrive\\VIT\\Anwendungsprotokolle\\RaspPI-master\\opc\\opc ua\\client_key.pem"
#set_uri = "urn:opc-client.local"
client = Client("opc.tcp://192.168.24.100:4840")
#client.set_security_string(f"Basic256Sha256,SignAndEncrypt,{certificate_path},{private_key_path}")
#s setze Benutzername und Passwort
client.set_user('opc')
client.set_password('opc')


# Set up InfluxDB connection details
bucket = "VIT"
org = "BBS Brinkstr"
token = "LWncOl3iI2z3vQgH4gVrvdsRO2n4YEt4NcQkbzxrYbqvF1_-ciJtgtivnIhpl_G-CjcRPonXh1-iR5cXuiqpqA=="
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"

clientInflux = InfluxDBClient3(host=url, token=token, org=org)
database="VIT"

def connect_opc_client():
    while True:
        try:
            client.connect()
            print("Connected to OPC UA server")
            return
        except Exception as e:
            print(f"Failed to connect to OPC UA server: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)


def read_and_write_data():
    try:
        # greife auf Elemente im Baum zu
        root = client.get_root_node()
        objects = client.get_objects_node()

        while True:
            # erzeuge Objekte für Knoten aus dem Baum über OPC UA Notation
            zufall1 = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi 64 SL.Application.GVL.Zufall1')
            zufall2 = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi 64 SL.Application.GVL.Zufall2')
            zufall3 = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi 64 SL.Application.GVL.Zufall3')

            # OPC-Variablen besitzen vier Attribute: Datentyp, Wert, Status, Zeitstempel
            data = zufall1.get_data_value()
            print('************ Variable: Ausgang ************')
            print('Datentyp:    ', data.Value.VariantType)
            print('Wert:        ', data.Value.Value)
            print('Status:      ', data.StatusCode)
            print('Zeitstempel: ', data.SourceTimestamp)
            print('*******************************************')

            # Variablen Zufall auslesen
            print('Wert der Variable "zufall1": ', zufall1.get_value())
            print('Wert der Variable "zufall2": ', zufall2.get_value())
            print('Wert der Variable "zufall3": ', zufall3.get_value())

            data = {
                "point1": {
                    "variable": "Zufall 1",
                    "count": zufall1.get_value(),
                },
                "point2": {
                    "variable": "Zufall 2",
                    "count": zufall2.get_value(),
                },
                "point3": {
                    "variable": "Zufall 3",
                    "count": zufall3.get_value(),
                },
            }

            for key in data:
                point = (
                    Point("census")
                    .tag("variable", data[key]["variable"])
                    .field("value", data[key]["count"])
                )
                clientInflux.write(database=database, record=point)
                time.sleep(1)  # separate points by 1 second

            print("Complete. Return to the InfluxDB UI.")
            time.sleep(5)  # Pause between data reads

    except Exception as e:
        print(f"Error reading or writing data: {e}")
        print("Attempting to reconnect to OPC UA server...")
        client.disconnect()
        connect_opc_client()
        read_and_write_data()

try:
    connect_opc_client()
    read_and_write_data()
finally:
    client.disconnect()