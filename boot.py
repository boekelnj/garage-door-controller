# notbookies
# 4/21/18
# This file is executed on every boot (including wake-boot from deepsleep)

import gc       
gc.collect()    

SSID = '********'
PASSWD = '********'

# Function for wifi connection.
# Unsure if best practice is to have this here or in main.py
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()
