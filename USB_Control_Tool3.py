
import subprocess
import tkinter as tk
from tkinter import messagebox

def enable_usb_ports():
    subprocess.run(["sudo", "modprobe", "usb-storage"])

def disable_usb_ports():
    subprocess.run(["sudo", "rmmod", "usb-storage"])

def mount_usb_device(device_path, mount_path):
    subprocess.run(["sudo", "mount", device_path, mount_path])

def unmount_usb_device(mount_path):
    subprocess.run(["sudo", "umount", mount_path])

def start_another_application():
    subprocess.Popen(["/path/to/your/application"])

def show_message(title, message):
    messagebox.showinfo(title, message)

def toggle_mount_unmount():
    status = check_mount_status()
    if status == "mounted":
        unmount_usb_device("/mnt/usb")
        show_message("Success", "USB device unmounted successfully.")
        mount_button["text"] = "Mount"
    elif status == "unmounted":
        mount_usb_device("/dev/sdb1", "/mnt/usb")  
        show_message("Success", "USB device mounted successfully.")
        mount_button["text"] = "Unmount"
    else:
        show_message("Error", "Error checking mount status.")

def check_mount_status():
    return "unmounted"  

def exit_application():
    app.destroy() 

app = tk.Tk()
app.title("USB Control Tool")
app.attributes('-fullscreen', True)  


button_frame = tk.Frame(app)
button_frame.pack(pady=30)  


enable_button = tk.Button(button_frame, text="Enable USB Ports", command=enable_usb_ports)
disable_button = tk.Button(button_frame, text="Disable USB Ports", command=disable_usb_ports)

enable_button.pack(side="left", padx=10)  
disable_button.pack(side="left", padx=10)  


button_gap1 = tk.Label(app)
button_gap1.pack()


mount_label = tk.Label(app, text="Mount USB Device:")
mount_label.pack()

device_path_entry = tk.Entry(app)
device_path_entry.pack()

mount_button = tk.Button(app, text="Mount", command=toggle_mount_unmount)
mount_button.pack()


button_gap2 = tk.Label(app)
button_gap2.pack()


start_app_button = tk.Button(app, text="Start Application", command=start_another_application)
start_app_button.pack()


button_gap3 = tk.Label(app)
button_gap3.pack()


exit_button = tk.Button(app, text="Exit", command=exit_application)
exit_button.pack()

app.mainloop()

