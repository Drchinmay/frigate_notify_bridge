import json
import time
import paho.mqtt.client as mqtt

# Load HA addon options
with open("/data/options.json") as f:
    options = json.load(f)

MQTT_HOST = options.get("mqtt_host")
MQTT_PORT = options.get("mqtt_port", 1883)
MQTT_TOPIC = options.get("mqtt_topic", "frigate/events")

if not MQTT_HOST:
    raise ValueError("MQTT host not configured")

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with code:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print("Message received:", msg.topic, msg.payload.decode())

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_start()

while True:
    time.sleep(5)
