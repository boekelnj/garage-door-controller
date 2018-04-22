# notbookies
# 4/21/18
# This file is run after boot.py

from time import sleep
from umqtt.simple import MQTTClient
import machine

SERVER_NAME = '********'
SERVER_IP = '********'
USER = '********'
PASSWD = '********'

# Setup of GPIO.
switch = machine.Pin(14, machine.Pin.IN)
relay = machine.Pin(5, machine.Pin.OUT, value=0)
led = machine.Pin(2, machine.Pin.OUT)

# Setup of MQTT channels.
t_debug = '/homeIO/garage/door/debug/'
t_sub = b'/homeIO/garage/door/cmd/'   # Unsure why, but this only works as a byte object.
t_pub = '/homeIO/garage/door/state/'

# Call back fuction for subscription.
# Will be executed upon receipt of message.
def sub_cb(topic, msg):
    print((topic, msg))
    if msg == b'0' and switch.value() == 1:
        relay.value(1)
        sleep(0.5)
        relay.value(0)
    elif msg == b'1' and switch.value() == 0:
        relay.value(1)
        sleep(0.5)
        relay.value(0)

# Unsure why, but every example I found connects and disconnects every loop, 
# instead of staying connected.
# Also unsure why the IP is passed into the function instead of when client is instantiated.
def main(server=SERVER_IP):
    while True:
        client = MQTTClient(
            SERVER_NAME,
            server, port=1883,
            user=USER,
            password=PASSWD
        )
        client.set_callback(sub_cb)
        client.connect()
        client.subscribe(t_sub, qos=1)

        # Currently the two sleep calls below are necessary to get check_msg() to run.
        # Need to figure out why, because as it is right now it is possible to miss commands
        # between disconnect and reconnect.
        sleep(1)
        client.check_msg()
        sleep(1)

        if switch.value() == 0:
            pub = 'OPEN'
        elif switch.value() == 1:
            pub = 'CLOSED'
        else:
            pub = 'ERR'
        
        # Publish message based on above, and set quality of service to 1 (see mqtt docs).
        client.publish(topic=t_pub, msg=pub, qos=1)
        client.disconnect()

if __name__ == "__main__":
    # Blink LED on ESP if boot is okay.
    for x in range(0,3):
        led.value(0)
        sleep(0.25)
        led.value(1)
        sleep(0.25)
    main()
