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
from packlib import kodi, client, dom_parser2, log_utils
from resources.lib.modules import player, local_utils
from resolveurl import hmf


@local_utils.url_dispatcher.register('810', ['url'], ['name', 'iconimage', 'pattern'])
def find(url, name=None, iconimage=None, pattern=None):

    kodi.busy()
    
    try: url,site = url.split('|SPLIT|')
    except: 
        site = 'Unknown'
        log_utils.log('Error getting site information from :: %s' % (url), xbmc.LOGERROR)
    
    try:
        if 'streamingporn.xyz' in url:
            c = client.request(url)
            r = dom_parser2.parse_dom(c, 'a', req=['href','class','rel','target'])
            r = [i for i in r if i.attrs['class'] == 'external']
            r = [client.request(i.attrs['href'], output='geturl') for i in r]
            r = [i for i in r if hmf.HostedMediaFile(i).valid_url()]
            url = multi(r)
        elif 'spreadporn.org' in url:
            c = client.request(url)
            r = dom_parser2.parse_dom(c, 'li', req=['data-show','data-link'])
            r = [(i.attrs['data-link']) for i in r]
            url = multi(r)
        elif 'pandamovie.eu' in url:
            c = client.request(url)
            r = dom_parser2.parse_dom(c, 'a', req='id')
            r = [(i.attrs['href']) for i in r]
            url = multi(r)
        elif 'xtheatre.net' in url:
            c = client.request(url)
            pattern = '''<iframe\s*src=['"](?:[^'"]+)['"]\s*data-lazy-src=['"]([^'"]+)'''
            r = re.findall(pattern,c)
            url = multi(r)
        elif 'sexkino.to' in url:   
            c = client.request(url)
            u = dom_parser2.parse_dom(c, 'iframe', {'class': ['metaframe','rptss']})
            r = dom_parser2.parse_dom(c, 'tr')
            r = [dom_parser2.parse_dom(i, 'a', req='href') for i in r]
            r = [client.request(i[0].attrs['href']) for i in r if i]
            r = [i.attrs['src'] for i in u] + [re.findall("window.location.href='([^']+)", i)[0] for i in r]
            url = multi(r)               
    except:
        kodi.idle()
        kodi.notify(msg='Error getting link for (Link Finer) %s' % name)
        kodi.idle()
        quit()
    
    url += '|SPLIT|%s' % site
    kodi.idle()
    player.resolve_url(url, name, iconimage)


def multi(r):
     
    r = [(re.findall('(?://)(?:www.)?([^.]+).', i)[0].title(), i) for i in r if hmf.HostedMediaFile(i).valid_url()]
     
    names = []
    srcs  = []

    if len(r) > 1:
        for i in sorted(r, reverse=True):
            names.append(kodi.giveColor(i[0],'white',True))
            srcs.append(i[1])
        selected = kodi.dialog.select('Select a link.',names)
        if selected < 0:
            kodi.notify(msg='No option selected.')
            kodi.idle()
            quit()
        else:
            url = srcs[selected]
            return url
    else:
        return r[0][1]
