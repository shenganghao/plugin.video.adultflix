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

import sqlite3
import os
import re
import time
import six
from kodi_six import xbmc, xbmcaddon, xbmcgui
urlopen = six.moves.urllib.request.urlopen
unquote_plus = six.moves.urllib.parse.unquote_plus
Request = six.moves.urllib.request.Request

try:
    addon = xbmcaddon.Addon()
    get_setting = addon.getSetting
    databases = xbmc.translatePath(os.path.join('special://profile/addon_data/plugin.video.adultflix', 'databases'))
    chaturbatedb = xbmc.translatePath(os.path.join(databases, 'chaturbate.db'))

    xbmc.log('Starting AdultFlix Service', xbmc.LOGNOTICE)

    if not os.path.exists(databases):
        os.makedirs(databases)
    conn = sqlite3.connect(chaturbatedb)
    c = conn.cursor()
    try:
        c.executescript("CREATE TABLE IF NOT EXISTS chaturbate (name, url, image);")
    except:
        pass
    conn.close()

    i = 0
    j = 0

    # chat_on_off = 'false'
    chat_on_off = get_setting("chaturbate_start")

    if chat_on_off != 'true':
        xbmc.log('Exiting AdultFlix Service', xbmc.LOGNOTICE)
        quit()

    time.sleep(10)

    lst = []

    xbmc.log('Starting AdultFlix Chaturbate Monitoring', xbmc.LOGNOTICE)

    while not xbmc.Monitor().waitForAbort(1):

        if not i:
            # xbmc.log('Getting Chaturbate Monitored Performers from AdultFlix', xbmc.LOGNOTICE)
            conn = sqlite3.connect(chaturbatedb)
            conn.text_factory = str
            c = conn.cursor()
            c.execute("SELECT * FROM chaturbate")
            e = [u for u in c.fetchall()]
            conn.close()
            if len(e) < 1:
                quit()
            for (title, link, iconimage) in e:
                if (not title in str(lst)):
                    # xbmc.log('AdultFlix: Checking %s' % title, xbmc.LOGNOTICE)
                    try:
                        req = Request(link)
                        response = urlopen(req, timeout=10)
                        r = response.read()
                        response.close()
                        if '.m3u8' in r:
                            content = re.compile('default_subject:\s\"([^,]+)",').findall(r)[0]
                            content = unquote_plus(content)
                            try:
                                content = content.encode('utf-8')
                            except:
                                content = content
                            xbmcgui.Dialog().notification(title + ' online!', content, iconimage, 7500, True)
                            lst.append(title)
                            xbmc.sleep(3500)
                    except:
                        pass

        xbmc.sleep(5000)

        if i >= 2879:
            lst = []
            xbmc.log('AdultFlix: Reseting Checked List', xbmc.LOGNOTICE)
        i = (i + 1) % 60
        j = (j + 1) % 2880
except:
    pass
