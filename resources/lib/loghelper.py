from resources.lib import kodilogging
import xbmcaddon
import xbmc
import xbmcgui

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
        #xbmcgui.Dialog().notification(addon_path, 'addon_path: ' + str(addon_path), xbmcgui.NOTIFICATION_ERROR, 5000)
        image_num = addon.getSetting('icon_style')
        #xbmcgui.Dialog().notification(addon_name, 'icon_style: ' + str(image_num), xbmcgui.NOTIFICATION_ERROR, 5000)
        #xbmcgui.Dialog().notification(addon_name, 'icon_color: ' + str(addon.getSettingBool('icon_color')), xbmcgui.NOTIFICATION_ERROR, 5000)
        if addon.getSettingBool('icon_color'):
            icon = addon_path + "/media/icons/infodialogs/" + "VolBlack" + image_num  + ".png"
        else:
            icon = addon_path + "/media/icons/infodialogs/" + "VolWhite" + image_num + ".png"
        xbmc.log('{0} - {1}'.format(addon_name, "icon: " + icon), level=xbmc.LOGDEBUG)
        #xbmcgui.Dialog().notification(addon_name, 'icon: ' + str(icon), xbmcgui.NOTIFICATION_ERROR, 5000)
        #xbmcgui.Dialog().notification(addon_name, 'icon path: ' + addon_path + "/media/icons/infodialogs/" + icon, xbmcgui.NOTIFICATION_ERROR, 5000)
        xbmcgui.Dialog().notification(addon_name, '{0}'.format(msg_text), icon, addon.getSettingInt('display_time'))
