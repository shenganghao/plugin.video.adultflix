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

#############################################################
#################### START ADDON IMPORTS ####################
import os
import re

from packlib import kodi
import pyxbmct.addonwindow as pyxbmct
from kodi_six import xbmc, xbmcaddon
from resources.lib.pyxbmct_.github import xxxtext
from resources.lib.modules import local_utils

#############################################################
#################### SET ADDON ID ###########################
_self_ = xbmcaddon.Addon(id=kodi.get_id())

#############################################################
#################### SET ADDON THEME IMAGES #################
ART = xbmc.translatePath(os.path.join('special://home/addons/script.adultflix.artwork', 'resources/pyxbmct/issues'))

Background_Image = os.path.join(ART, 'bg.png')
Button = os.path.join(ART, 'close.png')
ButtonF = os.path.join(ART, 'closef.png')
Open = os.path.join(ART, 'numbers/not-selected/open/%s.png')
Open_Selected = os.path.join(ART, 'numbers/selected/open/%s.png')
Closed = os.path.join(ART, 'numbers/not-selected/closed/%s.png')
Closed_Seleted = os.path.join(ART, 'numbers/selected/closed/%s.png')


def githubSelect(name):
    from packlib import githubissues

    githubissues.run('tvaddonsco/plugin.video.adultflix', '%s' % name)
    file = xbmc.translatePath(os.path.join(kodi.datafolder, '%s-issues-%s.csv' % (kodi.get_id(), name)))

    global msg_text

    with open(file, mode='r')as f:
        txt = f.read()
    items = re.findall('<item>(.+?)</item>', txt, re.DOTALL)
    if len(items) < 1:
        msg_text = kodi.giveColor('No %s issues with AdultFlix at this time.' % name.title(), 'deeppink', True)
    else:
        msg_text = kodi.giveColor('%s Issues with AdultFlix\n' % name.title(), 'deeppink', True) + kodi.giveColor(
            'Report Issues @ https://github.com/tvaddonsco/plugin.video.adultflix/issues', 'white',
            True) + '\n---------------------------------\n\n'
        for item in items:
            try:
                id = re.findall('<id>([^<]+)', item)[0]
            except:
                id = 'Unknown'
            try:
                user = re.findall('<username>([^<]+)', item)[0]
            except:
                user = 'Unknown'
            try:
                label = re.findall('<label>([^<]+)', item)[0]
            except:
                label = 'Unknown'
            try:
                title = re.findall('<title>([^<]+)', item)[0]
            except:
                title = 'Unknown'
            try:
                body = re.findall('<body>([^<]+)', item)[0]
            except:
                body = 'Unknown'
            try:
                created = re.findall('<created>([^<]+)', item)[0]
                date, time = created.split('T')
            except:
                date = 'Unknown'
                time = 'Unknwon'
            msg_text += '[B]ID: %s | Label: %s \nBy: %s on %s at %s[/B] \n\nTitle: %s \nMessage %s \n\n---------------------------------\n\n' \
                        % (id,
                           kodi.githubLabel(label),
                           user,
                           date,
                           time.replace('Z', ''),
                           title,
                           body)


#############################################################
########## Function To Call That Starts The Window ##########
@local_utils.url_dispatcher.register('34', ['name'])
def GitWindow(name):
    global open_issues
    global closed_issues

    try:
        open_issues = re.findall('\s+(\d+)\s+Open', name)[0]
        closed_issues = re.findall('\s+(\d+)\s+Closed', name)[0]

        if int(open_issues) in range(11, 20):
            open_issues = '10plus'
        elif int(open_issues) in range(21, 30):
            open_issues = '20plus'
        elif int(open_issues) > 30:
            open_issues = '30plus'

        if int(closed_issues) in range(11, 20):
            closed_issues = '10plus'
        elif int(closed_issues) in range(21, 30):
            closed_issues = '20plus'
        elif int(closed_issues) in range(21, 30):
            closed_issues = '30plus'
        elif int(closed_issues) in range(31, 40):
            closed_issues = '40plus'
        elif int(closed_issues) in range(41, 50):
            closed_issues = '50plus'
        elif int(closed_issues) in range(51, 100):
            closed_issues = '20plus'
        elif int(closed_issues) > 100:
            closed_issues = '100plus'
    except:
        open_issues = 'default'
        closed_issues = 'default'

    global List

    window = Main('')
    window.doModal()
    del window


# def Selection(self,xselected):

#    githubSelect(xselected)
#    xxxtext.TextWindow(msg_text)

#############################################################
######### Class Containing the GUi Code / Controls ##########
class Main(pyxbmct.AddonFullWindow):

    def __init__(self, title='KongKidz'):
        super(Main, self).__init__(title)

        # set the location and size of your window in kodi
        self.setGeometry(800, 450, 100, 50)

        ## Set The backGround Image using PYX Image
        Background = pyxbmct.Image(Background_Image)

        ## Place The BackGround Image (X, Y, W, H)
        self.placeControl(Background, -19, -1, 154, 55)

        ## function to set active controls that users interact with 
        self.set_active_controls()

        ## function to set what happens when users press left,right,up,down on your active controls
        self.set_navigation()

        ## connect the back button to pyx to close window
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        self.connect(self.Open_Issues, lambda: self.Selection('open'))
        self.connect(self.Closed_Issues, lambda: self.Selection('closed'))
        self.connect(self.button, self.close)

        self.setFocus(self.Open_Issues)

    def set_active_controls(self):
        self.Open_Issues = pyxbmct.Button('', focusTexture=Open_Selected % open_issues,
                                          noFocusTexture=Open % open_issues)
        self.Closed_Issues = pyxbmct.Button('', focusTexture=Closed_Seleted % closed_issues,
                                            noFocusTexture=Closed % closed_issues)
        self.button = pyxbmct.Button('', focusTexture=ButtonF, noFocusTexture=Button)

        self.placeControl(self.Open_Issues, 80, 2, 37, 20)
        self.placeControl(self.Closed_Issues, 80, 30, 37, 20)
        self.placeControl(self.button, 115, 22, 15, 7)

    def set_navigation(self):
        self.Open_Issues.controlRight(self.button)
        self.Closed_Issues.controlLeft(self.button)
        self.button.controlLeft(self.Open_Issues)
        self.button.controlRight(self.Closed_Issues)

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=200',),
                               ('WindowClose', 'effect=fade start=100 end=0 time=300',)])

    def Selection(self, xselected):
        githubSelect(xselected)
        xxxtext.TextWindow(msg_text)
