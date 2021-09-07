import tkinter.ttk as ttk
import os


def AppList(parent, name="App", no_modify=True, uninstall_command="", modify_command="", theme_name="", theme_style=""):
    List_Entry = ttk.Frame(parent)
    os.chdir("Themes")
    List_Entry.tk.call("source", theme_name)
    List_Entry.tk.call("set_theme", theme_style)
    Game_Name_Label = ttk.Label(List_Entry, text=name)
    Game_Name_Label.pack(fill='x', padx='5', pady='5', side='left')
    Uninstall_Button = ttk.Button(List_Entry, text='Uninstall', command=uninstall_command)
    Uninstall_Button.pack(padx='0 5', pady='5', side='right')
    if not no_modify:
        Modify_Button = ttk.Button(List_Entry, text='Modify', command=modify_command)
        Modify_Button.pack(padx='5', pady='5', side='right')
