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
import sv_ttk
import time
import threading
import subprocess

# Get the platform where this app is run
# Used for: opening save path, determining chromedriver path, themes
pl = platform.system()

class BoxGUIApp(tk.Tk):
    def __init__(self):
        """
        Initializes a new Box GUI Window.
        """
        super().__init__()
        self.title("Box.com Downloader GUI")
        self.wm_resizable(width=False, height=False)

        # Frame for Save Path
        self.frm_save = tk.Frame(borderwidth=2,border=1)
        self.frm_save.pack(padx=5, pady=5)
        frm_save = self.frm_save
        self.lbl_save = ttk.Label(master=frm_save, text="Save Path")
        self.lbl_save.grid(row=0, column=0, padx=5, pady=5)
        self.en_save = ttk.Entry(master=frm_save, width=58)
        self.get_last_path()
        self.en_save.bind('<Key>', lambda _: 'break') # Disable any keypress on entry field
        self.en_save.grid(row=0, column=1, padx=5, pady=5)
        self.btn_save = ttk.Button(master=frm_save, text="Browse", command=self.evt_set_path)
        self.btn_save.grid(row=0, column=2, padx=5, pady=5)
        # End Frame for Save Path

        # Frame for Download Links
        self.frm_dl = tk.Frame(borderwidth=2, border=1)
        self.frm_dl.pack()
        frm_dl = self.frm_dl
        self.lbl_links = ttk.Label(master=frm_dl, text="Paste box.com links here:")
        self.lbl_links.grid(row=0, padx=5, pady=5, sticky="w")
        self.txt_links = tk.Text(master=frm_dl, width=63, height=20)
        self.txt_links.grid(row=1, padx=5, pady=5)
        self.lbl_status = ttk.Label(master=frm_dl,text="Ready")
        self.lbl_status.grid(row=2, padx=5, pady=5, sticky="w")
        self.btn_dl = ttk.Button(master=frm_dl, text="Download", command=lambda: threading.Thread(target=self.evt_download).start())
        self.btn_dl.grid(row=0, padx=130, pady=5, sticky="e")
        self.btn_open_fol = ttk.Button(master=frm_dl, text="Open Save Path", command=self.evt_open_fol)
        self.btn_open_fol.grid(row=0, padx=5, pady=5, sticky="e")
        # End Frame for Download Links

    def get_last_path(self):
        """
        Retrieves the last save path set by the user from the ~/.lastsavepath file.
        """
        en_save = self.en_save
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

    def reset(self):
        """
        Removes all of the contents of the Links text box.
        """
        self.txt_links.delete("1.0", "end")
        self.lbl_status.config(text="Ready")
        self.btn_dl["state"] = "enabled"
    
    def evt_set_path(self):
        """
        Event handler for the Browse button.
        """
        en_save = self.en_save
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


    def evt_open_fol(self):
        """
        Event handler for the Open Save Path button.
        """
        global pl
        f_exp = ""
        if pl == "Windows":
            fol = os.path.normpath(self.en_save.get())
            f_exp = os.path.join(os.getenv("WINDIR"), "explorer.exe")
            subprocess.run([f_exp, fol])
        elif pl == "Linux":
            os.system("xdg-open {}".format(self.en_save.get())) # really?


    def evt_download(self):
        """
        Event Handler for the Download button.
        """
        btn = self.btn_dl
        txt_links = self.txt_links
        lbl_status = self.lbl_status
        en_save = self.en_save
        global pl
        from scraper import Scraper, url_checker
        from downloader import download_file

        btn["state"] = "disabled"

        urls = txt_links.get("1.0", "end").split()
        if urls == []:
            messagebox.showinfo(message="Nothing to download.")
            btn["state"] = "enabled"
            return
        driver_path = None
        if pl == "Windows":
            driver_path = os.path.expanduser("~\scoop\shims\chromedriver.exe")
        if pl == "Linux":
            driver_path = "/usr/bin/chromedriver"

        for url in urls:
            lbl_status.config(text="Checking Link")
            if not url_checker(url):
                lbl_status.config(text="Invalid URL")
                time.sleep(1)
                lbl_status.config(text="Ready")
                continue
            box_object = Scraper(url, driver_path, False, 10)
            box_object.load_url()
            dl_name = None
            dl_url = None
            try:
                dl_name = box_object.get_download_title()
                dl_url = box_object.get_download_url()
            except:
                lbl_status.config(text="Invalid Box link.")
                time.sleep(1)
                lbl_status.config(text="Ready")
                continue

            output_location = en_save.get()

            if not output_location.endswith("/"):
                output_location += "/"

            box_object.clean()  # clean
            directory = os.path.dirname(output_location)
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            if dl_name is not None and dl_url is not None:
                lbl_status.config(text="Downloading")
                time.sleep(1)
                lbl_status.config(text="Saving as {}".format(str(dl_name + ".pdf")))
                download_file(url=dl_url, path=str(output_location + dl_name + ".pdf"))
                if os.path.exists(str(output_location + dl_name + ".pdf")):
                    lbl_status.config(text="Download Successful!")
                    time.sleep(1.5)
                else:
                    lbl_status.config("Download Failed.")
                    time.sleep(1.5)

        self.reset()

    
    # # For Windows only
    def theme(self):
        """
        Apply sv_ttk theme on Windows 10 and above.
        """
        global pl
        if pl == "Windows":
            from winreg import ConnectRegistry, OpenKey, QueryValueEx, HKEY_CURRENT_USER

        try:
            registry = ConnectRegistry(None, HKEY_CURRENT_USER)
            key = OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
            mode = QueryValueEx(key, "AppsUseLightTheme")
            sv_ttk.set_theme("light" if mode[0] else "dark")
        except:
            pass


if __name__ == "__main__":
    App = BoxGUIApp()

    # If Windows, apply theme
    if pl == "Windows":
        App.theme()

    App.mainloop()