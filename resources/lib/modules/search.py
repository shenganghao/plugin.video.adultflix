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

from packlib import kodi
from resources.lib.modules import local_utils
from kodi_six import xbmcgui, xbmcplugin, xbmc
from scrapers import *
from scrapers import __all__
import sqlite3
import six
import os

buildDirectory = local_utils.buildDir
quote_plus = six.moves.urllib.parse.quote_plus

databases = xbmc.translatePath(os.path.join(kodi.datafolder, 'databases'))
searchdb = xbmc.translatePath(os.path.join(databases, 'search.db'))
specific_icon = xbmc.translatePath(os.path.join('special://home/addons/script.adultflix.artwork/resources/art/', '%s/icon.png'))
specific_fanart = xbmc.translatePath(os.path.join('special://home/addons/script.adultflix.artwork/resources/art/', '%s/fanart.jpg'))
search_icon = xbmc.translatePath(os.path.join('special://home/addons/script.adultflix.artwork/resources/art/', 'main/search.png'))

if not os.path.exists(databases):
    os.makedirs(databases)

conn = sqlite3.connect(searchdb)
c = conn.cursor()
try:
    c.executescript("CREATE TABLE IF NOT EXISTS terms (ID Integer PRIMARY KEY AUTOINCREMENT, term);")
except:
    pass
conn.close()


@local_utils.url_dispatcher.register('29')
def searchMain():

    dirlst = [
        {
            'name': kodi.giveColor('Search All Providers', 'white'), 'url': 'all', 'mode': '1', 'icon': search_icon,
            'fanart': kodi.addonfanart, 'folder': True
        }
    ]

    sources = __all__
    search_sources = []
    for i in sources:
        try:
            if eval(i + ".search_tag") == 1: search_sources.append(i)
        except:
            pass

    if search_sources:
        for i in sorted(search_sources):
            dirlst.append(
                {
                    'name': kodi.giveColor('Search ' + i.title(), 'white'), 'url': i, 'mode': '1',
                    'icon': specific_icon % i, 'fanart': specific_fanart % i, 'folder': True
                }
            )

    buildDirectory(dirlst)


@local_utils.url_dispatcher.register('1', ['url'])
def searchDecide(url):
    search_on_off = kodi.get_setting("search_setting")

    if search_on_off == "true":
        name = "null"
        url = "2|SPLIT|" + url
        searchHistory(name, url)
    else:
        url = "null|SPLIT|" + url
        mainSearch(url)


@local_utils.url_dispatcher.register('2', ['url'])
def mainSearch(url):
    if '|SPLIT|' in url: url, site = url.split('|SPLIT|')
    term = url
    if term == "null":  term = kodi.get_keyboard('Search %s' % kodi.get_name())

    if term:
        search_on_off = kodi.get_setting("search_setting")
        if search_on_off == "true":
            delTerm(term)
            addTerm(term)

        display_term = term
        term = quote_plus(term)
        term = term.lower()

        if site == 'all':
            sources = __all__
            search_sources = []
            for i in sources:
                try:
                    if eval(i + ".search_tag") == 1: search_sources.append(i)
                except:
                    pass

            if search_sources:
                i = 0
                source_num = 0
                failed_list = ''
                line1 = kodi.giveColor('Searching: ', 'white') + kodi.giveColor('%s', 'dodgerblue')
                line2 = kodi.giveColor('Found: %s videos', 'white')
                line3 = kodi.giveColor('Source: %s of ' + str(len(search_sources)), 'white')

                kodi.dp.create(kodi.get_name(), '', line2, '')
                xbmc.executebuiltin('Dialog.Close(busydialog)')
                for u in sorted(search_sources):
                    if kodi.dp.iscanceled(): break
                    try:
                        i += 1
                        progress = 100 * int(i) / len(search_sources)
                        kodi.dp.update(progress, line1 % u.title(), line2 % str(source_num), line3 % str(i))
                        search_url = eval(u + ".search_base") % term
                        try:
                            source_n = eval(u + ".content('%s',True)" % search_url)
                        except:
                            source_n = 0
                        try:
                            source_n = int(source_n)
                        except:
                            source_n = 0
                        if not source_n:
                            if failed_list == '':
                                failed_list += str(u).title()
                            else:
                                failed_list += ', %s' % str(u).title()
                        else:
                            source_num += int(source_n)
                    except:
                        pass
                kodi.dp.close()
                if failed_list != '':
                    kodi.notify(msg='%s failed to return results.' % failed_list, duration=4000, sound=True)
                    log_utils.log('Scrapers failing to return search results are :: : %s' % failed_list,
                                  xbmc.LOGERROR)
                else:
                    kodi.notify(msg='%s results found.' % str(source_num), duration=4000, sound=True)
                xbmcplugin.setContent(kodi.syshandle, 'movies')
                xbmcplugin.endOfDirectory(kodi.syshandle, cacheToDisc=True)
                local_utils.setView('search')
        else:
            search_url = eval(site + ".search_base") % term
            eval(site + ".content('%s')" % search_url)
    else:
        kodi.notify(msg='Blank searches are not allowed.')
        quit()


def searchHistory(name, url):
    searches = []
    mode, site = url.split('|SPLIT|')
    mode = int(mode)

    lst = [('New Search...', mode, 'null', 'Search AdultFlix', True), ('Clear History', 15, 'url', None, False),
           ('Disable Search History', 16, None, None, False),
           ('################## Recent Searches #########################', 999, 'url', None, False)]

    conn = sqlite3.connect(searchdb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM terms ORDER BY ID DESC")

    for (id, got_term) in c.fetchall():
        lst += [(got_term, mode, 'search_term=' + got_term, got_term, True)]

    dirlst = []

    for i in lst:
        icon = search_icon
        fanart = kodi.addonfanart
        dirlst.append(
            {'name': kodi.giveColor(i[0], 'white'), 'url': '%s|SPLIT|%s' % (i[2], site), 'mode': i[1], 'icon': icon,
             'fanart': fanart, 'description': i[3], 'folder': i[4]})

    if dirlst: buildDirectory(dirlst)

    local_utils.setView('list')


def addTerm(term):
    conn = sqlite3.connect(searchdb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("INSERT INTO terms VALUES (?,?)", (None, term))
    conn.commit()
    conn.close()


@local_utils.url_dispatcher.register('25', ['url'])
def delTerm(url):
    refresh = False
    try:
        if 'search_term=' in url:
            url = url.split('search_term=')[1]
            refresh = True
        if '|' in url:
            url = url.split('|')[0]
            refresh = True
        conn = sqlite3.connect(searchdb)
        c = conn.cursor()
        c.execute("DELETE FROM terms WHERE term = '%s'" % url)
        conn.commit()
        conn.close()
    except:
        pass

    if refresh:
        xbmc.executebuiltin("Container.Refresh")
        kodi.notify('%s removed from list.' % url.title(), duration=5000, sound=True)


@local_utils.url_dispatcher.register('15')
def clearSearch():
    if os.path.isfile(searchdb):
        choice = xbmcgui.Dialog().yesno(kodi.get_name(), kodi.giveColor('Would you like to clear all stored search history?', 'white'))
        if choice:
            try:
                os.remove(searchdb)
            except:
                kodi.notify(msg='Error removing search history.')
    xbmc.executebuiltin("Container.Refresh")


@local_utils.url_dispatcher.register('16')
def disableSearch():

    if kodi.get_setting('search_setting') == 'true':
        try:
            os.remove(searchfile)
        except:
            pass
        kodi.set_setting('search_setting', 'false')
    else:
        kodi.set_setting('search_setting', 'true')
    kodi.notify(msg='Search history disabled.')
    quit()
