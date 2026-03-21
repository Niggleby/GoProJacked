import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Ab hier streaming imports:
import stream_setup as stup
import time
### VARS ###

GOPRO_STREAM_URL = "udp://10.5.5.9:8554"

### OBJEKTE ###

test = stup.GoProClient()

### DEFs ###

def open_proxy_stream():
    window = tk.Toplevel()
    window.title("GoPro Live Stream")

    label = tk.Label(window)
    label.pack()

    cap = cv2.VideoCapture("udp://127.0.0.1:5000")

    def update_frame():
        ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            label.config(image=img)
            label.image = img

        window.after(30, update_frame)

    update_frame()

    def on_close():
        cap.release()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

def open_stream():
    """VERALTET > Sauberer mit 'open_proxy_stream'
    Open the GoPro live stream in a new window"""
    window = tk.Toplevel()
    window.title("GoPro Live Stream")

    label = tk.Label(window)
    label.pack()

    cap = cv2.VideoCapture(GOPRO_STREAM_URL)

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.config(image=imgtk)
        window.after(10, update_frame)

    update_frame()
    window.mainloop()

### MAIN ###

if test.start_stream():
    pass
    test.start_keep_alive()
    time.sleep(3)
    open_proxy_stream()
else: print("ERROR")