# Box.com PDF Downloader GUI
# Copyright (C) 2022 aebibtech
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

import tkinter as tk
import tkinter.ttk as ttk
import platform
import os
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
import sv_ttk
import time
import threading

window = tk.Tk()
window.title("Box.com Downloader GUI")
window.wm_resizable(width=False, height=False)

if platform.system() == "Windows":
    from winreg import *

# For Windows only
def theme():
    try:
        registry = ConnectRegistry(None, HKEY_CURRENT_USER)
        key = OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
        mode = QueryValueEx(key, "AppsUseLightTheme")
        sv_ttk.set_theme("light" if mode[0] else "dark")
        # window.after(100, theme)
    except:
        pass


bold = font.Font(weight="bold")

# Frame - Save Path
frm_save = tk.Frame(borderwidth=2,border=1)
frm_save.pack(padx=5, pady=5)

lbl_save = ttk.Label(master=frm_save, text="Save Path")
lbl_save.grid(row=0, column=0, padx=5, pady=5)

en_save = ttk.Entry(master=frm_save, width=58)

path = ""
try:
    fh = open(os.path.expanduser("~/.lastsavepath"), "r")
    path = fh.read()
    en_save.insert(0, path)
    fh.close()
except:
    pass

if en_save.get() == "":
    en_save.insert(0, os.path.expanduser("~/Downloads").replace("\\", "/"))

en_save.bind('<Key>', lambda _: 'break') # Disable any keypress on entry field
en_save.grid(row=0, column=1, padx=5, pady=5)

def evt_set_path():
    path = filedialog.askdirectory(title="Choose PDF Save Path")

    if not path == "":
        en_save.delete(0, tk.END)
        en_save.insert(0, path)
        try:
            conf = os.path.expanduser("~/.lastsavepath")
            fh = open(conf, "w")
            fh.write(path)
            fh.close()
        except:
            pass


btn_save = ttk.Button(master=frm_save, text="Browse", command=evt_set_path)
btn_save.grid(row=0, column=2, padx=5, pady=5)
# End

# Frame Download Links
frm_dl = tk.Frame(borderwidth=2, border=1)
frm_dl.pack()

lbl_links = ttk.Label(master=frm_dl, text="Paste box.com links here:")
lbl_links.grid(row=0, padx=5, pady=5, sticky="w")

txt_links = tk.Text(master=frm_dl, width=63, height=20)
txt_links.grid(row=1, padx=5, pady=5)

lbl_status = ttk.Label(master=frm_dl,text="Status: Ready")

def clear():
    global lbl_status
    txt_links.delete("1.0", "end")
    lbl_status.config(text="Status: Ready")


def evt_download(btn: tk.Button):
    global lbl_status
    from scraper import Scraper, url_checker
    from downloader import download_file

    btn["state"] = "disabled"

    urls = txt_links.get("1.0", "end").split()
    if urls == []:
        messagebox.showinfo(message="Nothing to download.")
        btn["state"] = "enabled"
        return
    driver_path = None
    if platform.system() == "Windows":
        driver_path = os.path.expanduser("~\scoop\shims\chromedriver.exe")
    if platform.system() == "Linux":
        driver_path = "/usr/bin/chromedriver"

    lbl_status.config(text="Status: Checking Links")
    for url in urls:
        if not url.startswith("https://"):
            clear()
            lbl_status.config(text="Status: Invalid URL")
            time.sleep(1)
            lbl_status.config(text="Status: Ready")
            btn["state"] = "enabled"
            return

    lbl_status.config(text="Status: Downloading")
    for url in urls:
        box_object = Scraper(url, driver_path, False, 10)
        box_object.load_url()
        dl_name = box_object.get_download_title()
        dl_url = box_object.get_download_url()
        output_location = en_save.get()

        if not output_location.endswith("/"):
            output_location += "/"

        box_object.clean()  # clean
        directory = os.path.dirname(output_location)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        download_file(url=dl_url, path=str(output_location + dl_name + ".pdf"))
        if os.path.exists(str(output_location + dl_name + ".pdf")):
            lbl_status.config(text="Status: Download Successful!")
            time.sleep(2.5)
            lbl_status.config(text="Status: Ready")
        else:
            lbl_status.config("Status: Download Failed.")
            time.sleep(2.5)
            lbl_status.config(text="Status: Ready")

        clear()
        btn["state"] = "enabled"
    


btn_dl = ttk.Button(master=frm_dl, text="Download", command=lambda: threading.Thread(target=evt_download, args=[btn_dl]).start())
btn_dl.grid(row=2, padx=5, pady=5, sticky="w")


lbl_status.grid(row=2, padx=100, pady=5, sticky="w")
# End

# If Windows, apply themes
pl = platform.system()
print("Platform:", pl)
if pl == "Windows":
    theme()

window.mainloop()