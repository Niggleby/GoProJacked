import cv2
import tkinter as tk
from PIL import Image, ImageTk

GOPRO_STREAM_URL = "udp://10.5.5.9:8554"

def open_stream():
    """Open the GoPro live stream in a new window"""
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
