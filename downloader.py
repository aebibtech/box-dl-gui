# Box.com PDF Downloader
# Copyright (C) 2018 lfasmpao
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib3
from urllib3.exceptions import InsecureRequestWarning


def download_file(url, path):
    r = None
    http = urllib3.PoolManager()
    try:
        r = http.request('GET', url, preload_content=False)
    except InsecureRequestWarning:
        pass
    with open(path, 'wb') as out:
        while True:
            data = r.read(1024)
            if not data:
                break
            out.write(data)
    r.release_conn()
