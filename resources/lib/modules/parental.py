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

import hashlib
from packlib import kodi
import os
import sys
import time
from kodi_six import xbmc
from resources.lib.modules import local_utils

buildDirectory = local_utils.buildDir

databases = xbmc.translatePath(os.path.join(kodi.datafolder, 'databases'))
parentaldb = xbmc.translatePath(os.path.join(databases, 'parental.db'))
parental_icon = xbmc.translatePath(os.path.join('special://home/addons/script.adultflix.artwork/resources/art/main', 'parental_controls.png'))

if not os.path.exists(databases):
    os.makedirs(databases)
conn = sqlite3.connect(parentaldb)
c = conn.cursor()
try:
    c.executescript("CREATE TABLE IF NOT EXISTS parental (password, time);")
except:
    pass
conn.close()


def parentalCheck():
    timestamp = None
    password = None

    conn = sqlite3.connect(parentaldb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM parental")

    for (passwd, timest) in c.fetchall():
        timestamp = timest
        password = passwd
    conn.close()

    session_time = int(kodi.get_setting('session_time'))

    if password:
        try:
            now = time.time()
            check = now - 60 * session_time
            if (not timestamp): timestamp = 0
        except:
            now = time.time()
            check = now - 60 * session_time
            timestamp = 0
    else:
        return

    if (timestamp < check):

        input = kodi.get_keyboard(
            'Please Enter Your Password - %s' % kodi.giveColor('(%s Minute Session)' % str(session_time), 'red', True),
            hidden=True)
        if (not input):
            sys.exit(0)

        pass_one = hashlib.sha256(input).hexdigest()

        if password != pass_one:
            kodi.dialog.ok(kodi.get_name(), "Sorry, the password you entered was incorrect.")
            sys.exit(0)
        else:
            delEntry(password)
            addEntry(password, now)
            kodi.dialog.ok(kodi.get_name(), 'Login successful!', 'You now have a %s minute session before you will be asked for the password again.' % str(session_time))
    return


@local_utils.url_dispatcher.register('5')
def parentalControls():
    list = []
    password = None
    conn = sqlite3.connect(parentaldb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM parental")

    for (timest, passwd) in c.fetchall():
        timestamp = timest
        password = passwd
    conn.close()

    if password:
        c = [
            (kodi.giveColor('PARENTAL CONTROLS - ', 'white', True) + kodi.giveColor('ON', 'lime'), 999)
            ,
            (kodi.giveColor('Change Password', 'white'), 13)
            ,
            (kodi.giveColor('Disable Password', 'white'), 14)
        ]
    else:
        c = [
            (kodi.giveColor('PARENTAL CONTROLS - ', 'white', True) + kodi.giveColor('OFF', 'orangered'), 999)
            ,
            (kodi.giveColor('Setup Parental Password', 'white'), 13)
        ]

    for i in c:
        icon = parental_icon
        fanart = kodi.addonfanart
        list.append({'name': i[0], 'url': 'none', 'mode': i[1], 'icon': icon, 'fanart': fanart, 'folder': False})

    if list: buildDirectory(list)


@local_utils.url_dispatcher.register('13')
def parentalPin():
    input = kodi.get_keyboard('Please Set Password', hidden=True)
    if not input:
        kodi.dialog.ok(kodi.get_name(), "Sorry, no password was entered.")
        sys.exit(0)

    pass_one = input

    input = kodi.get_keyboard('Please Confirm Your Password', hidden=True)
    if not input:
        kodi.dialog.ok(kodi.get_name(), "Sorry, no password was entered.")
        sys.exit(0)

    pass_two = input

    if pass_one == pass_two:
        writeme = hashlib.sha256(pass_one).hexdigest()
        addEntry(writeme, None)
        kodi.dialog.ok(kodi.get_name(), 'Parental control has been enabled.')
        xbmc.executebuiltin("Container.Refresh")
    else:
        kodi.dialog.ok(kodi.get_name(), 'The passwords do not match, please try again.')
        sys.exit(0)


@local_utils.url_dispatcher.register('14')
def parentalOff():
    input = kodi.get_keyboard('Please Enter Your Password', hidden=True)
    if not input:
        kodi.dialog.ok(kodi.get_name(), "Sorry, no password was entered.")
        sys.exit(0)
    pass_one = hashlib.sha256(input).hexdigest()

    conn = sqlite3.connect(parentaldb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM parental")

    for (passwd, timest) in c.fetchall():
        timestamp = timest
        password = passwd
    conn.close()

    if password == pass_one:
        try:
            try:
                os.remove(parentaldb)
            except:
                pass
            kodi.dialog.ok(kodi.get_name(), 'Parental controls have been disabled.')
            xbmc.executebuiltin("Container.Refresh")
        except:
            kodi.dialog.ok(kodi.get_name(), 'There was an error disabling the parental controls.')
            xbmc.executebuiltin("Container.Refresh")
    else:
        kodi.dialog.ok(kodi.get_name(), "Sorry, the password you entered was incorrect.")
        quit()


def addEntry(passwd, timestamp):
    conn = sqlite3.connect(parentaldb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("INSERT INTO parental VALUES (?,?)", (passwd, timestamp))
    conn.commit()
    conn.close()


def delEntry(passwd):
    conn = sqlite3.connect(parentaldb)
    c = conn.cursor()
    c.execute("DELETE FROM parental WHERE password = '%s'" % passwd)
    conn.commit()
    conn.close()
