# -*- coding: utf-8 -*-

from resources.lib import loghelper
from resources.lib import socketreceiver

import xbmc
import xbmcaddon

def run():
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        # Get the configured ip, port, and time out to reconnect.
        addon = xbmcaddon.Addon()
        ip = addon.getSetting('ip_address')
        port = addon.getSettingInt('port')
        socket_wait_time = addon.getSettingInt('socket_wait_time')
        try:
            receiver = socketreceiver.sReceiver(ip=ip, port=port)
            receiver.connect()
            while True:
                events = receiver.sel.select(timeout=1)
                if events:
                    print("events" , repr(events))
                    for key, mask in events:
                        # Get the wait time after sending volume notification.
                        addon = xbmcaddon.Addon()
                        volume_wait_time = addon.getSettingInt('volume_wait_time') / 1000.00
                        receiver.listener_service(key, mask, volume_wait_time)
                # Check for a socket being monitored to continue.
                if not receiver.sel.get_map():
                    break
        except Exception as ex:
            loghelper.log("Socket error on " + ip + ":" + str(port) + ": " + str(ex) , 'NOTIFICATION_ERROR')
        else:
            del receiver
        # Sleep/wait for abort
        if monitor.waitForAbort(socket_wait_time):
            # Abort was requested while waiting. We should exit
            break
