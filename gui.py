import tkinter as tk
import tkinter.ttk as ttk
import platform
import os
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
import sv_ttk
from winreg import *
import time

window = tk.Tk()
window.title("Box.com Downloader GUI")
window.wm_resizable(width=False, height=False)

def monitor_changes():
    registry = ConnectRegistry(None, HKEY_CURRENT_USER)
    key = OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
    mode = QueryValueEx(key, "AppsUseLightTheme")
    sv_ttk.set_theme("light" if mode[0] else "dark")
    window.after(100, monitor_changes)


bold = font.Font(weight="bold")

# Frame - Save Path
frm_save = tk.Frame(borderwidth=2,border=1)
frm_save.pack(padx=5, pady=5)

lbl_save = ttk.Label(master=frm_save, text="Save Path")
lbl_save.grid(row=0, column=0, padx=5, pady=5)

en_save = ttk.Entry(master=frm_save, width=58)

if en_save.get() == "":
    en_save.insert(0, os.path.expanduser("~/Downloads").replace("\\", "/"))

en_save.bind('<Key>', lambda _: 'break') # Disable any keypress on entry field
en_save.grid(row=0, column=1, padx=5, pady=5)

def evt_set_path():
    path = filedialog.askdirectory(title="Choose PDF Save Path")

    if not path == "":
        en_save.delete(0, tk.END)
        en_save.insert(0, path)


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

def evt_download():
    global lbl_status
    from scraper import Scraper, url_checker
    from downloader import download_file

    urls = txt_links.get("1.0", "end").split()
    if urls == []:
        messagebox.showinfo(message="Nothing to download.")
    driver_path = os.path.expanduser("~\scoop\shims\chromedriver.exe")

    
    for url in urls:
        if url_checker(url) is False:  # url format check
            lbl_status.config(text="Status: One of the URLs is invalid.")
            #messagebox.showerror(title="One of the URLs is invalid.")
            return
        else:
            lbl_status.config(text="Status: Scraping...")
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
            
            dl_status = "Status: Downloading {} as {}".format(url, str(dl_name + ".pdf"))
            lbl_status.config(text=dl_status)
            download_file(url=dl_url, path=str(output_location + dl_name + ".pdf"))
            if os.path.exists(str(output_location + dl_name + ".pdf")):
                lbl_status.config(text="Status: Download Successful!")
                time.sleep(2.5)
                lbl_status.config(text="Status: Ready")
            else:
                lbl_status.config("Status: Download Failed.")
    


btn_dl = ttk.Button(master=frm_dl, text="Download", command=evt_download)
btn_dl.grid(row=2, padx=5, pady=5, sticky="w")


def clear():
    txt_links.delete("1.0", "end")


btn_clr = ttk.Button(master=frm_dl, text="Clear", command=clear)
btn_clr.grid(row=2, padx=95, pady=5, sticky="w")

lbl_status.grid(row=2, padx=160, pady=5, sticky="w")
# End

if platform.system() == "Windows":
    print("Platform:", platform.system())
    monitor_changes()

window.mainloop()