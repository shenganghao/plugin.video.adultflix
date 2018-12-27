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

import sys
from packlib import kodi
from resources.lib.modules import local_utils
# Importing this in order to register modes
# noinspection PyUnresolvedReferences
from resources.lib.modules import menus, parental, firstStart, search, picture_viewer
parentalCheck = parental.parentalCheck


def main(argv=None):

    if sys.argv:
        argv = sys.argv

    queries = local_utils.parse_query(argv[2])
    mode = queries.get('mode', None)

    local_utils.url_dispatcher.dispatch(mode, queries)
    if kodi.get_setting('dev_debug') == 'true':
        local_utils.url_dispatcher.showmodes()


if __name__ == '__main__':

    firstStart.run()
    parentalCheck()
    sys.exit(main())
