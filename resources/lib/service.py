# -*- coding: utf-8 -*-

from resources.lib import loghelper
from resources.lib import socketreceiver

import xbmc
import xbmcaddon

def run():
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        # Get the Kodi configurations.
        addon = xbmcaddon.Addon()
        ip = addon.getSetting('ip_address')
        port = addon.getSettingInt('port')
        socket_wait_time = addon.getSettingInt('socket_wait_time')
        ifttt_token = addon.getSetting('ifttt_token')
        ifttt_start = addon.getSetting('ifttt_start')
        ifttt_stop = addon.getSetting('ifttt_stop')
        if ifttt_token != '':
            if ifttt_start != '':
                start_url = "https://maker.ifttt.com/trigger/" + ifttt_start + "/with/key/" + ifttt_token
            else:
                start_url = ''
            if ifttt_stop!= '':
                stop_url = "https://maker.ifttt.com/trigger/" + ifttt_stop + "/with/key/" + ifttt_token
            else:
                stop_url = ''
        else:
            start_url = ''
            stop_url = ''
        # Create and try to connect ot the receiver.
        receiver = socketreceiver.sReceiver(ip=ip, port=port, start_url=start_url, stop_url=stop_url)
        connected = receiver.connect()
        while connected:
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
        del receiver
        # Sleep/wait for abort
        if monitor.waitForAbort(socket_wait_time):
            # Abort was requested while waiting. We should exit
            break
