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

from packlib import kodi, log_utils
import os
from resources.lib.modules import local_utils
from kodi_six import xbmc, xbmcgui

buildDirectory = local_utils.buildDir
databases = xbmc.translatePath(os.path.join(kodi.datafolder, 'databases'))
favoritesdb = xbmc.translatePath(os.path.join(databases, 'favorites.db'))
fav_icon = xbmc.translatePath(os.path.join('special://home/addons/script.adultflix.artwork/resources/art/main', 'favourites.png'))

if not os.path.exists(databases):
    os.makedirs(databases)
conn = sqlite3.connect(favoritesdb)
c = conn.cursor()
try:
    c.executescript("CREATE TABLE IF NOT EXISTS favorites (name, url, mode, image, folder);")
except:
    pass
conn.close()


@local_utils.url_dispatcher.register('23')
def getFavorites():
    dirlist = []
    lst = [('Clear Favourites', None, 38, fav_icon, None, None, False, False),
           ('----------------------------------', None, 999, fav_icon, None, None, False, False)
           ]
    conn = sqlite3.connect(favoritesdb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM favorites ORDER BY name ASC")
    for (name, url, mode, iconimage, _folder) in c.fetchall():
        try:
            site = url.split('|SPLIT|')[1]
        except:
            site = None
        if site: name = '[%s Video] %s' % (site, name)
        if _folder:
            name = '[%s] %s' % ('Directory', name)
        else:
            _folder = False
        lst += [(name, url, mode, iconimage, None, 'del', _folder, True)]
    conn.close()

    for i in lst:
        if not i[3]:
            icon = kodi.addonicon
        else:
            icon = i[3]
        if not i[4]:
            fanart = kodi.addonfanart
        else:
            fanart = i[4]
        dirlist.append(
            {
                'name': kodi.giveColor(i[0], 'white'), 'url': i[1], 'mode': i[2], 'icon': icon, 'fanart': fanart,
                'fav': i[5], 'folder': i[6], 'isDownloadable': i[7]
            }
        )

    if len(lst) < 3:
        dirlist.append(
            {
                'name': kodi.giveColor('No Favorites Found', 'white'), 'url': 'None', 'mode': 999, 'icon': fav_icon,
                'fanart': fanart, 'folder': False
            }
        )

    buildDirectory(dirlist)


@local_utils.url_dispatcher.register('100', ['fav', 'favmode', 'name', 'url', 'iconimage', 'folder'])
def Favorites(fav, favmode, name, url, img, _folder):
    if fav == "add":
        delFav(url)
        addFav(favmode, name, url, img, _folder)
        kodi.notify('Favorite added', 'Item added to the favorites')
    elif fav == "del":
        delFav(url)
        log_utils.log('Deleting %s from favorites' % (url), xbmc.LOGNOTICE)
        kodi.notify('Favorite deleted', 'Item removed from the list')
        xbmc.executebuiltin('Container.Refresh')


@local_utils.url_dispatcher.register('38')
def clearFavorites():
    if os.path.isfile(favoritesdb):
        choice = xbmcgui.Dialog().yesno(kodi.get_name(),
                                        kodi.giveColor('Would you like to clear all of your favorites?', 'white'))
        if choice:
            try:
                os.remove(favoritesdb)
            except:
                kodi.notify(msg='Error clearing favorites.')
    xbmc.executebuiltin("Container.Refresh")


def addFav(mode, name, url, img, _folder):
    conn = sqlite3.connect(favoritesdb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("INSERT INTO favorites VALUES (?,?,?,?,?)", (name, url, mode, img, _folder))
    conn.commit()
    conn.close()


def delFav(url):
    conn = sqlite3.connect(favoritesdb)
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE url = '%s'" % url)
    conn.commit()
    conn.close()
