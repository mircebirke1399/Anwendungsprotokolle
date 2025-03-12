
import os, time
from influxdb_client_3 import InfluxDBClient3, Point

# Set up InfluxDB connection details
bucket = "VIT"
org = "BBS Brinkstr"
token = "LWncOl3iI2z3vQgH4gVrvdsRO2n4YEt4NcQkbzxrYbqvF1_-ciJtgtivnIhpl_G-CjcRPonXh1-iR5cXuiqpqA=="
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"

# Create InfluxDB client
client = InfluxDBClient3(host=url, token=token, org=org)


database="production_data"

data = {
  "point1": {
    "location": "Klamath",
    "species": "bees",
    "count": 23,
  },
  "point2": {
    "location": "Portland",
    "species": "ants",
    "count": 30,
  },
  "point3": {
    "location": "Klamath",
    "species": "bees",
    "count": 28,
  },
  "point4": {
    "location": "Portland",
    "species": "ants",
    "count": 32,
  },
  "point5": {
    "location": "Klamath",
    "species": "bees",
    "count": 29,
  },
  "point6": {
    "location": "Portland",
    "species": "ants",
    "count": 40,
  },
}

for key in data:
  point = (
    Point("census")
    .tag("location", data[key]["location"])
    .field(data[key]["species"], data[key]["count"])
  )
  client.write(database=database, record=point)
  time.sleep(1) # separate points by 1 second

print("Complete. Return to the InfluxDB UI.")
