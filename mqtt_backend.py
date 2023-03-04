import paho.mqtt.client as mqtt

# Define the MQTT broker and port
broker_address = "test.mosquitto.org"
broker_port = 1883

# Define the MQTT topic to subscribe to
topic = "esp/led/status"

# Define the message to publish
message = "1"

# Define the MQTT client
client = mqtt.Client()


# Define callback functions for when the client connects and receives a message
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to the topic
    client.subscribe(topic)


def on_message(client, userdata, message):
    print("Received message: " + str(message.payload.decode()))


# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Start the MQTT client loop
client.loop_start()

# Publish the message to the MQTT topic
client.publish(topic, message)

# Wait for messages to be received
input("Press Enter to quit.")

# Stop the MQTT client loop
client.loop_stop()
