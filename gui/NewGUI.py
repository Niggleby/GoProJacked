### kleines mitmach-tutorial von realpython.com | Tkinter

import tkinter as tk 
import time   #Hauptdependency für GUI hier
##vsctipp?| from tkinter import messagebox  # Für Pop-up Nachrichten
#################### Bauen von 'window' als Hauptfenster
window = tk.Tk()  # Create the main window
window.title("GoProJacked GUI")  # wird zb in taskleiste gezeigt
window.geometry("400x300")  # Set the default size of the window
#################### > noch kein output, nur ein Fenster
####################
#################### ein Text-Widget mit Inhalt:

wText = tk.Text(window, height=10, width=40, bg="lightblue", fg="black", font="Arial")  # Create a text widget
eText = tk.Text()
eText.delete("1.0", "end")  # Clear any existing text
eText.insert("1.0", "schreib!\n >") # Insert initial text
ttt = eText.get("2.2",tk.END)  # get text from line 2, character 2 to the end
time.sleep(1)  # Wait for 1 second (just to see the effect)
print(f"Verxuch MID  --  {ttt}\n")  # Get text from the first line, first 3 characters



##eText.insert("1.0", "Willkommen zu GoProJacked!\n")
eText.pack()  # Add the text widget to the window

## vllt muss '.get()' ja auch nach '.pack' kommen?!
print(f"Verxuch ENDE  --  {ttt}\n")  # Get text from the first line, first 3 characters
#################### >


'''# temp skip
bspLabel = tk.Label(window, text="Willkommen zu GoProJacked!",anchor="center",bg="black",fg="white",pady=5,height=2,width=80,font="Bauhaus")  # Create
bspLabel.pack()  # Add the label to the window
#################### > 
#################### ein Button-Widget mit Funktion
xbtn = tk.Button(window, text="Fenster Zuuu!", command=lambda: print("Button wurde geklickt!"), bg="blue", fg="white", pady=5, padx=10, font="Arial")  # Create a button
xbtn.pack()  # Add the button to the window
#################### > idk man :(
## bs|Widget.canvas = tk.Canvas(window, width=200, height=100, bg="lightgrey")  # Create a canvas widget
'''
window.mainloop()  # Start the GUI event loop

print(ttt)