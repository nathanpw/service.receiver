# -*- coding: utf-8 -*-

from resources.lib import kodilogging
from resources.lib import service
from resources.lib import telnet
from threading import Thread

import logging
import xbmcaddon
import xbmc
import xbmcgui

# Keep this file to a minimum, as Kodi
# doesn't keep a compiled copy of this

kodilogging.config()

def log(msg_text, msg_type):
    addon = xbmcaddon.Addon()
    addon_name = addon.getAddonInfo('name')
    if addon.getSetting('debug') == 'true':
        xbmc.log('{0} - {1}'.format(addon_name, msg_text), level=xbmc.LOGDEBUG)
    if addon.getSetting('display_notification') == 'true':
        if msg_type == 'NOTIFICATION_INFO':
            xbmcgui.Dialog().notification(addon_name, '{0}'.format(msg_text), xbmcgui.NOTIFICATION_INFO, 500)
    if msg_type == 'NOTIFICATION_ERROR':
        xbmc.log('{0} - {1}'.format(addon_name, msg_text), level=xbmc.LOGDEBUG)
        xbmcgui.Dialog().notification(addon_name, '{0}'.format(msg_text), xbmcgui.NOTIFICATION_ERROR, 5000)
    if msg_type == 'VOLUME_CHANGE':
        addon_path = addon.getAddonInfo('path').decode("utf-8")
        image_num = addon.getSetting('icon_style')
        if addon.getSettingBool('icon_color'):
            icon = "VolBlack" + image_num  + ".png"
        else:
            icon = "VolWhite" + image_num + ".png"
        xbmcgui.Dialog().notification(addon_name, '{0}'.format(msg_text), addon_path + "/media/icons/infodialogs/" + icon, addon.getSettingInt('display_time'))

def listenVol(Receiver):
    monitor = xbmc.Monitor()

    while not monitor.abortRequested():
        sock =  Receiver.tn.get_socket()
        received = sock.recv(1024).decode()
        # Calculate the volume and display when changed.
        vol = findVolume(received)
        if vol != False:
            log('Volume changed: ' + str(vol), 'VOLUME_CHANGE')
        # Sleep/wait and break if abort was requested.
        if monitor.waitForAbort(1):
            break

def findVolume(string):
    pos = string.rfind("VOL")
    if  pos > -1:
        return ((int(string[pos+3:pos+6]) - 1 ) / 2.0) - 80
    else:
        return False

def main():
    # Check we have an ip and port configured.
    addon = xbmcaddon.Addon()
    if addon.getSetting('ip_address') == '':
        log('Missing IP address', 'NOTIFICATION_ERROR')
        addon.openSettings()
    ip_address = addon.getSetting('ip_address')
    port = addon.getSetting('port')

    # Connect to the receiver or exit
    try:
        Receiver = telnet.Receiver(ip_address,port)
    except:
        log('Could not connect to receiver', 'NOTIFICATION_ERROR')
        raise SystemExit

    monitor = xbmc.Monitor()

    # Start a thread to listen and update volume changes.
    Thread(target=listenVol, args=[Receiver]).start()

    while not monitor.abortRequested():
        # Sleep/wait for abort for 1 seconds
        if monitor.waitForAbort(1):
            # Abort was requested while waiting. Close the receiver connection.
            telnet.Receiver.close(Receiver)
            break

if (__name__ == "__main__"):
    main()
