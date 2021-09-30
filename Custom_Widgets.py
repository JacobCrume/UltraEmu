import tkinter.ttk as ttk
import tkinter as tk
import os
from PIL import Image, ImageTk


def App_List(parent, name="App", no_modify=True, uninstall_command="", modify_command=""):
    List_Entry = ttk.Frame(parent)
    os.chdir("Themes")
    Game_Name_Label = ttk.Label(List_Entry, text=name)
    Game_Name_Label.pack(fill='x', padx='5', pady='5', side='left')
    Uninstall_Button = ttk.Button(List_Entry, text='Uninstall', command=uninstall_command)
    Uninstall_Button.pack(padx='0 5', pady='5', side='right')
    if not no_modify:
        Modify_Button = ttk.Button(List_Entry, text='Modify', command=modify_command)
        Modify_Button.pack(padx='5', pady='5', side='right')

def Search_App_List(parent, name="App", image="", command=""):
    List_Entry = ttk.Frame(parent)
    os.chdir("Images_Universal")
    image_tk = Image.open(image)
    image_tk = image_tk.resize((100, 100))
    image_tk = ImageTk.PhotoImage(image_tk)
    Icon_Label = ttk.Label(List_Entry, image=image_tk)
    Icon_Label.pack(fill='x', padx='5', pady='5', side='left')
    Game_Name_Label = ttk.Label(List_Entry, text=name)
    Game_Name_Label.pack(fill='x', padx='5', pady='5', side='left')
    return List_Entry

root = tk.Tk()
stuff = Search_App_List(root, name="Fuckface", image="Gran Turismo 6.png")
stuff.pack()
root.mainloop()