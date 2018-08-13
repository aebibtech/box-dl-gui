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
import argparse
import os

from downloader import download_file
from scraper import Scraper, url_checker

# globals
parser = argparse.ArgumentParser(usage='%(prog)s [options]')
parser.add_argument('url', metavar='URL', type=str, help="Input box.com shared url")
parser.add_argument('--driver-path', default=None, dest='driver_location',
                    type=str, help="Specify your chrome driver path")
parser.add_argument('--wait-time', default=15, dest='wait_time',
                    type=int, help="Wait time for selenium to load in seconds (default: 15)")
parser.add_argument('--use-x11', default=False, action='store_false', dest='use_x11',
                    help='Use X11 Virtual Display (For OSX/Linux Only)')
parser.add_argument('--version', action='version', version='Box.com PDF Downloader Version 1.0')
parser.add_argument('--out', default=os.path.dirname(os.path.abspath(__file__)) + "/dl_files/",
                    dest="output_location", type=str, help="Output file folder location")
args = parser.parse_args()


def main():
    style = "=+" * 20
    if url_checker(args.url) is False:  # url format check
        raise argparse.ArgumentTypeError('Value has to be in full url format http:// or http://')
    print(style)
    print("Box.com PDF Downloader by @lfasmpao")

    box_object = Scraper(args.url, args.driver_location, args.use_x11, args.wait_time)
    print("Please wait for about {} seconds...".format(args.wait_time))
    box_object.load_url()
    dl_name = box_object.get_download_title()
    print(style)
    print("DATA TO BE DOWNLOADED\nTitle: {}\nBox.com URL: {}".format(dl_name, args.url))

    print(style)
    dl_url = box_object.get_download_url()
    print("Download URL:", dl_url)
    print(style)
    box_object.clean()  # clean

    # make directory
    directory = os.path.dirname(args.output_location)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print("Downloading..\nFile will be save as:",
          str(args.output_location + dl_name + ".pdf"))
    download_file(url=dl_url, path=str(args.output_location + dl_name + ".pdf"))


if __name__ == "__main__":
    main()
