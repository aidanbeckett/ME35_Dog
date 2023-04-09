import time
import os
import paho.mqtt.client as mqtt #import the client1
import time
import asyncio_mqtt as asyncmqtt
from me35secrets import *

topic = 'walk'

# PC MQTT Overall Setup
toggleAdafruitDashboardSetup = False

compClient = mqtt.Client('dog')

compClient.connect(ip)

def on_message(user, userName, msg):
    print("Message Received: {0}".format(msg.payload.decode()))

compClient.on_message = on_message
compClient.loop_start()
compClient.subscribe(topic)

# Adafruit IO Dashboard Interaction
# Note: Rate limit = 30 points per minute
import Adafruit_IO
import sys

aio = Adafruit_IO.MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

initiateProtocolFeed = "status"

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format("all"))
    # Subscribe to changes on a feed.
    client.subscribe(initiateProtocolFeed)

def subscribe(client, userdata, mid, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format(initiateProtocolFeed, granted_qos[0]))

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed "{0}" received new value: {1}'.format(feed_id, payload))
    send_message(payload)
    # if(feed_id == initiateProtocolFeed):
        
    # else:
    #     if(payload == "0"):
    #         print("Button has been released.")
    #     else:
    #         print("Unconfigured Feed")

def send_message(msg):
    compClient.publish(topic, msg)
    
# Setup the callback functions defined above.
aio.on_subscribe  = subscribe
aio.on_message = message
aio.on_connect    = connected
aio.on_disconnect = disconnected

# aio.loop_background()

# Connect to the Adafruit IO server.
aio.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
aio.loop_blocking()