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
    """öffnet internen restream von Port 5000 mit OpenCV"""
    window = tk.Toplevel()
    window.title("GoPro Live Stream")
    label = tk.Label(window)
    label.pack(fill="both", expand=True)

    cap = cv2.VideoCapture("udp://127.0.0.1:5000")

    def update_proxy_frame():
        ret, frame = cap.read()          
        print("Frame:", ret)        # debug
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Aktuelle Fenstergröße holen:
            w = window.winfo_width()
            h = window.winfo_height()
            # Dynamisch skalieren:
            #if w > 1 and h > 1:
            #    frame = cv2.resize(frame, (w, h))
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            label.config(image=img)
            label.image = img
        window.after(30, update_proxy_frame)
    update_proxy_frame() # <- anscheinend wichtig?!
    #window.mainloop # <- vllt überflüssig

    def on_close():
        cap.release()
        test.stop_keep_alive()
        test.stop_proxy_stream()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)


### MAIN ###

# tk-root fenster erzeugen und dann verstecken
root = tk.Tk()
root.withdraw()

if test.start_stream():
    test.start_keep_alive()
    test.start_proxy_stream()
    time.sleep(2) # Bonuszeit für OpenCv
    open_proxy_stream()

root.mainloop()