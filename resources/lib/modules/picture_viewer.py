# -*- coding: utf-8 -*-

'''
    AdultFlix XXX Addon (18+) for the Kodi Media Center
    Kodi is a registered trademark of the XBMC Foundation.
    We are not connected to or in any other way affiliated with Kodi - DMCA: legal@tvaddons.co
    Support: https://github.com/tvaddonsco/plugin.video.adultflix

        License summary below, for more details please read license.txt file

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 2 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from __future__ import absolute_import

from kodi_six import xbmc
import re
from packlib import client, kodi
from resources.lib.modules import local_utils


@local_utils.url_dispatcher.register('805', ['url'], ['name', 'iconimage'])
def resolve_url(url, name=None, iconimage=None):

    kodi.busy()

    if 'motherless.com' in url:
        r = client.request(url)
        img = re.findall('''<meta\s*property=["']og:image["']\s*content=["']([^'"]+)''', r)[0]
        SHOW = "ShowPicture(" + img + ')'
        kodi.idle()
        xbmc.executebuiltin(SHOW)
    elif '8muses.com' in url:
        try:
            r = client.request(url)
            dir = re.findall('''<input\s*type=['"]hidden['"]\s*id=['"]imageDir['"]\s*value=['"]([^'"]+)''', r)[0]
            icon_id = re.findall('''<input\s*type=['"]hidden['"]\s*id=['"]imageName['"]\s*value=['"]([^'"]+)''', r)[0]
            display_url = 'https://cdn.ampproject.org/i/s/www.8muses.com/%ssmall/%s' % (dir,icon_id)
            SHOW = "ShowPicture(" + display_url + ')'
        except:
            SHOW = "ShowPicture(" + url + ')'
        kodi.idle()
        xbmc.executebuiltin(SHOW)
    else:
        SHOW = "ShowPicture(" + url + ')'
        kodi.idle()
        xbmc.executebuiltin(SHOW)
