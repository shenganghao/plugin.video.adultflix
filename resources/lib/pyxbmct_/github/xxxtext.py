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
import os

from packlib import kodi
import pyxbmct.addonwindow as pyxbmct
#############################################################
#################### START ADDON IMPORTS ####################
from kodi_six import xbmc, xbmcaddon

#############################################################
#################### SET ADDON ID ###########################
_self_ = xbmcaddon.Addon(id=kodi.get_id())

#############################################################
#################### SET ADDON THEME IMAGES #################
ART = xbmc.translatePath(os.path.join('special://home/addons/script.adultflix.artwork', 'resources/pyxbmct/issues'))

Background_Image = os.path.join(ART, 'tbg.png')
Button = os.path.join(ART, 'close.png')
ButtonF = os.path.join(ART, 'closef.png')


#############################################################
########## Function To Call That Starts The Window ##########
def TextWindow(Text):
    kodi.idle()

    global msg_text

    msg_text = Text

    window = Main('')
    window.doModal()
    del window


#############################################################
######### Class Containing the GUi Code / Controls ##########
class Main(pyxbmct.AddonFullWindow):

    def __init__(self, title='AdultFlix'):
        super(Main, self).__init__(title)

        # set the location and size of your window in kodi
        self.setGeometry(800, 450, 100, 50)

        ## Set The backGround Image using PYX Image
        Background = pyxbmct.Image(Background_Image)

        ## Place The BackGround Image (X, Y, W, H)
        self.placeControl(Background, -50, -1, 220, 55)

        ## function to set active controls that users interact with
        self.set_active_controls()

        self.set_info_controls()

        self.setFocus(self.button)

        ## connect the back button to pyx to close window
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        self.connect(self.button, self.close)
        self.textbox.setText(msg_text)
        self.textbox.autoScroll(1000, 2000, 1000)

    def set_info_controls(self):
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 22, 1, 140, 48)

    def set_active_controls(self):
        self.button = pyxbmct.Button('', focusTexture=ButtonF, noFocusTexture=Button)
        self.placeControl(self.button, 147, 47, 15, 6)

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=200',),
                               ('WindowClose', 'effect=fade start=100 end=0 time=300',)])
