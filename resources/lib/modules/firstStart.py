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
import os, sys
from packlib import kodi, client
from resources.lib.modules import local_utils

class run:

    def __init__(self):
    
        self.firstRunFile = os.path.join(kodi.datafolder, 'firstrun.txt')
        self.informationFile = os.path.join(kodi.addonfolder, 'resources/files/information.txt')

        if ( not os.path.isfile(self.firstRunFile) ): 
            self.checkAge()
            kodi.busy()
            try:
                countme = client.request('http://bit.ly/2vchTCP')
            except:
                pass
            kodi.idle()
            try:
                local_utils.viewDialog(self.informationFile)
            except:
                pass
        return

    def checkAge(self):

        choice = kodi.dialog.yesno(kodi.get_name(), 'To use this addon you you must be legally allowed to under the laws of your State/Country. By pressing I Agree you accept that you are legally allowed to view adult content.',yeslabel='I Agree',nolabel='Exit')
        if choice: 
            try:
                with open(self.firstRunFile,mode='w'):
                    pass
            except:
                pass
        else:
            sys.exit(1)