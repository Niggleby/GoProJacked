### TK & CTK Versuch Nr_1 ###
import tkinter as tk
import customtkinter as ctk
from PIL import Image

## Commands
def buton_callback():   #  wird beim klick ausgeführtt
    print("Bist'n Kek, Hah!")
imgpth = "C:\\Users\Robin\\Desktop\\Pictures\\KPXC_Logos\\Kubuntu.png"

## Anfang Fenster_1
app = ctk.CTk()
app.geometry("1200x800")

## Tabs

tbv = ctk.CTkTabview(master=app)
tbv.pack(padx=20, pady=20)

tbv.add("Tab1")
tbv.add("Tab2")
tbv.set("Tab2")

tbtn = ctk.CTkButton(master=tbv.tab("Tab1"))
tbtn.pack(padx=20, pady=20)


## Buttoms
btn = ctk.CTkButton(app, text="Kick mich du Sau!", command=buton_callback)
btn.pack(padx=20, pady=50)

myImg = ctk.CTkImage(light_image=Image.open(imgpth), size='400')
Img_lbl = ctk.CTkLabel(app, image=myImg, text="GangGangBadMan")



app.mainloop()