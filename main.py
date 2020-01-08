# -*- coding: utf-8 -*-

from resources.lib import loghelper
from resources.lib import service

import xbmcaddon

# Keep this file to a minimum, as Kodi
# doesn't keep a compiled copy of this

service.run()

def main():
    # Check we have an ip and port configured.
    addon = xbmcaddon.Addon()
    if addon.getSetting('ip_address') == '':
        loghelper.log('Missing IP address', 'NOTIFICATION_ERROR')
        addon.openSettings()
    ip_address = addon.getSetting('ip_address')
    port = addon.getSetting('port')

if (__name__ == "__main__"):
    main()
