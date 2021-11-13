import tkinter as tk
from tkinter import ttk
import os
from config import *
import cli_main
from PIL import ImageTk, Image
from pygubu.widgets.scrolledframe import ScrolledFrame
import Metacritic_API
import wget


class Grip:
    def __init__(self, parent, disable=None, releasecmd=None):
        self.parent = parent
        self.root = parent.winfo_toplevel()

        self.disable = disable
        if type(disable) == 'str':
            self.disable = disable.lower()

        self.releaseCMD = releasecmd

        self.parent.bind('<Button-1>', self.relative_position)
        self.parent.bind('<ButtonRelease-1>', self.drag_unbind)

    def relative_position(self, event):
        cx, cy = self.parent.winfo_pointerxy()
        geo = self.root.geometry().split("+")
        self.oriX, self.oriY = int(geo[1]), int(geo[2])
        self.relX = cx - self.oriX
        self.relY = cy - self.oriY

        self.parent.bind('<Motion>', self.drag_wid)

    def drag_wid(self, event):
        cx, cy = self.parent.winfo_pointerxy()
        d = self.disable
        x = cx - self.relX
        y = cy - self.relY
        if d == 'x':
            x = self.oriX
        elif d == 'y':
            y = self.oriY
        self.root.geometry('+%i+%i' % (x, y))

    def drag_unbind(self, event):
        self.parent.unbind('<Motion>')
        if self.releaseCMD != None:
            self.releaseCMD()

root = tk.Tk()
os.chdir("Themes")
style = ttk.Style(root)
if theme == "forest":
    root.tk.call("source", "forest-" + theme_style + ".tcl")
    style.theme_use('forest-' + theme_style)
elif theme == "azure":
    root.tk.call("source", "azure-" + theme_style + ".tcl")
    if theme_style == "dark":
        style.theme_use('azure-' + theme_style)
    else:
        style.theme_use('azure')
elif theme == "sun-valley":
    root.tk.call("source", "sun-valley.tcl")
    root.tk.call("set_theme", theme_style)
style.configure('Left.TButton', anchor='w')
os.chdir("..")


def Show_Back_Button():
    Search_Results = Metacritic_API.Search_MetaCritic(Search_Text.get(), 'ps3')
    Search_Results_Keys = Search_Results[1]
    Search_Results = Search_Results[0]
    if len(Search_Results) > 0:
        for child in Search_Results_Frame.winfo_children():
            child.destroy()
        Search_Frame.pack_forget()
        Back_Button.pack(side='left', padx=5, pady=5)
        Search_Frame.pack()
        Main_Content.pack_forget()
        Search_Results_Entries = []
        Search_Results_Icons = []
        os.chdir("Game_Info")
        os.chdir("Images")
        listdir = os.listdir()
        for i in range(len(os.listdir())):
            os.remove(listdir[i])
        for i in range(len(Search_Results_Keys)):
            wget.download(Search_Results[Search_Results_Keys[i]][0], out=Search_Results[Search_Results_Keys[i]][0].split("/")[-1])
        for i in range(len(Search_Results_Keys)):
            Search_Results_Icons.append(Image.open(Search_Results[Search_Results_Keys[i]][0].split("/")[-1]))
            Search_Results_Icons[i] = Search_Results_Icons[i].convert("RGBA")
            Search_Results_Icons[i] = ImageTk.PhotoImage(Search_Results_Icons[i])
        for i in range(0, len(Search_Results), 2):
            Search_Results_Entries.append(ttk.Frame(Search_Results_Frame))
            Search_Results_Entries[i].pack(side='top', fill="x", padx=5)
            Search_Results_Entries.append(ttk.Button(Search_Results_Entries[i], text=Search_Results_Keys[i], image=Search_Results_Icons[int(i / 2)], compound="left", style="Left.TButton"))
            Search_Results_Entries[i + 1].photo = Search_Results_Icons[int(i / 2)]
            Search_Results_Entries[i + 1].pack(side='left', pady="5 0", fill="x", expand=True, anchor="w")
        Search_Results_Frame.pack(expand=True, fill='both', side='top')
        Search_Results_Nav_Frame.pack(expand=True, fill='both', side='bottom')
        Search_Results_Holder.pack(expand=True, fill='both', side='right')
        Nav_Seperator.pack_forget()
        Nav_Seperator.pack(expand='true', fill='y', side='top')
        os.chdir("..")
        os.chdir("..")

    else:
        for child in Search_Results_Frame.winfo_children():
            child.destroy()
        Search_Frame.pack_forget()
        Back_Button.pack(side='left', padx=5, pady=5)
        Search_Frame.pack()
        Main_Content.pack_forget()
        os.chdir("..")
        Search_Results_Entries = []
        Search_Results_Entries.append(ttk.Frame(Search_Results_Frame))
        Search_Results_Entries[0].pack(side='top', fill="x")
        Search_Results_Entries.append(ttk.Label(Search_Results_Entries[0], text="No Results Found :("))
        Search_Results_Entries[1].pack(side='left', pady="5 0")
        Search_Results_Frame.pack(expand=True, fill='both', side='top')
        Search_Results_Nav_Frame.pack(expand=True, fill='both', side='bottom')
        Search_Results_Holder.pack(expand=True, fill='both', side='right')
        Nav_Seperator.pack_forget()
        Nav_Seperator.pack(expand='true', fill='y', side='top')


def Hide_Back_Button():
    Back_Button.pack_forget()
    Search_Results_Holder.pack_forget()
    Nav_Seperator.pack_forget()
    Main_Content.pack(expand='true', fill='both', side='right', padx="5 0")
    Nav_Seperator.pack(expand='true', fill='y', side='top')
    Search_Box.delete(0, tk.END)


os.chdir('Images_Universal')
Search_Icon = Image.open("Search.png")
Search_Icon = Search_Icon.convert("RGBA")
Button_Sizer = root.winfo_screenwidth() // 42
Title_Bar = ttk.Frame(root)
root.wm_attributes('-fullscreen','true')
Close_Button = ttk.Button(Title_Bar, text="X", command=lambda: root.destroy(), width=2)
Close_Button.pack(side='right', padx=5, pady=5)
Back_Button = ttk.Button(Title_Bar, text='<-', width=2)
Back_Button.configure(command=Hide_Back_Button)
Back_Button.pack_forget()
Search_Frame = ttk.Frame(Title_Bar)
Search_Text = tk.StringVar()
Search_Box = ttk.Entry(Search_Frame, textvariable=Search_Text, width=40)
Search_Box.pack(pady=5, padx='0 5', side='left')
root.update()
Search_Icon = Search_Icon.resize((15,15))
Search_Icon = ImageTk.PhotoImage(Search_Icon)
Search_Button = ttk.Button(Search_Frame, image=Search_Icon, width=15, command=Show_Back_Button)
Search_Button.pack(side='right', pady=5)
Search_Frame.pack()
Titlebar_Separator = ttk.Separator(Title_Bar, orient='horizontal')
Titlebar_Separator.pack(side='bottom', fill='x')
Title_Bar.pack(side="top", fill='x')
os.chdir('..')

Search_Results_Holder = ttk.Frame(root)
Search_Results_Frame = ttk.Frame(Search_Results_Holder)
Search_Results_Nav_Frame = ttk.Frame(Search_Results_Holder)

if theme_style == "light":
    os.chdir("Images_Light")
if theme_style == "dark":
    os.chdir("Images_Dark")

Download_Icon = Image.open("download.png")
Download_Icon = Download_Icon.convert("RGBA")
Download_Icon = Download_Icon.resize((Button_Sizer, Button_Sizer))
Download_Icon = ImageTk.PhotoImage(Download_Icon)
PS1_Icon = Image.open("ps1.png")
PS1_Icon = PS1_Icon.convert("RGBA")
PS1_Icon = PS1_Icon.resize((Button_Sizer, Button_Sizer))
PS1_Icon = ImageTk.PhotoImage(PS1_Icon)
PS2_Icon = Image.open("ps2.png")
PS2_Icon = PS2_Icon.convert("RGBA")
PS2_Icon = PS2_Icon.resize((Button_Sizer, Button_Sizer))
PS2_Icon = ImageTk.PhotoImage(PS2_Icon)
PS3_Icon = Image.open("ps3.png")
PS3_Icon = PS3_Icon.convert("RGBA")
PS3_Icon = PS3_Icon.resize((Button_Sizer, Button_Sizer))
PS3_Icon = ImageTk.PhotoImage(PS3_Icon)
PSP_Icon = Image.open("psp.png")
PSP_Icon = PSP_Icon.convert("RGBA")
PSP_Icon = PSP_Icon.resize((Button_Sizer, Button_Sizer))
PSP_Icon = ImageTk.PhotoImage(PSP_Icon)
Settings_Icon = Image.open("settings.png")
Settings_Icon = Settings_Icon.convert("RGBA")
Settings_Icon = Settings_Icon.resize((Button_Sizer, Button_Sizer))
Settings_Icon = ImageTk.PhotoImage(Settings_Icon)
Wii_Icon = Image.open("wii.png")
Wii_Icon = Wii_Icon.convert("RGBA")
Wii_Icon = Wii_Icon.resize((Button_Sizer, Button_Sizer))
Wii_Icon = ImageTk.PhotoImage(Wii_Icon)
Wii_U_Icon = Image.open("wii-u.png")
Wii_U_Icon = Wii_U_Icon.convert("RGBA")
Wii_U_Icon = Wii_U_Icon.resize((Button_Sizer, Button_Sizer))
Wii_U_Icon = ImageTk.PhotoImage(Wii_U_Icon)
Xbox_Icon = Image.open("xbox.png")
Xbox_Icon = Xbox_Icon.convert("RGBA")
Xbox_Icon = Xbox_Icon.resize((Button_Sizer, Button_Sizer))
Xbox_Icon = ImageTk.PhotoImage(Xbox_Icon)
Xbox_360_Icon = Image.open("xbox-360.png")
Xbox_360_Icon = Xbox_360_Icon.convert("RGBA")
Xbox_360_Icon = Xbox_360_Icon.resize((Button_Sizer, Button_Sizer))
Xbox_360_Icon = ImageTk.PhotoImage(Xbox_360_Icon)

os.chdir("..")
os.chdir("Images_Universal")
Simulator_Games_Button_1_Icon = Image.open(recommended_games_PS3_simulation[0][1])
Simulator_Games_Button_1_Icon = Simulator_Games_Button_1_Icon.resize((100, 100))
Simulator_Games_Button_1_Icon = ImageTk.PhotoImage(Simulator_Games_Button_1_Icon)
Simulator_Games_Button_2_Icon = Image.open(recommended_games_PS3_simulation[1][1])
Simulator_Games_Button_2_Icon = Simulator_Games_Button_2_Icon.resize((100, 100))
Simulator_Games_Button_2_Icon = ImageTk.PhotoImage(Simulator_Games_Button_2_Icon)
Simulator_Games_Button_3_Icon = Image.open(recommended_games_PS3_simulation[2][1])
Simulator_Games_Button_3_Icon = Simulator_Games_Button_3_Icon.resize((100, 100))
Simulator_Games_Button_3_Icon = ImageTk.PhotoImage(Simulator_Games_Button_3_Icon)
Simulator_Games_Button_4_Icon = Image.open(recommended_games_PS3_simulation[3][1])
Simulator_Games_Button_4_Icon = Simulator_Games_Button_4_Icon.resize((100, 100))
Simulator_Games_Button_4_Icon = ImageTk.PhotoImage(Simulator_Games_Button_4_Icon)
Simulator_Games_Button_5_Icon = Image.open(recommended_games_PS3_simulation[4][1])
Simulator_Games_Button_5_Icon = Simulator_Games_Button_5_Icon.resize((100, 100))
Simulator_Games_Button_5_Icon = ImageTk.PhotoImage(Simulator_Games_Button_5_Icon)
Simulator_Games_Button_6_Icon = Image.open(recommended_games_PS3_simulation[5][1])
Simulator_Games_Button_6_Icon = Simulator_Games_Button_6_Icon.resize((100, 100))
Simulator_Games_Button_6_Icon = ImageTk.PhotoImage(Simulator_Games_Button_6_Icon)
Simulator_Games_Button_7_Icon = Image.open(recommended_games_PS3_simulation[6][1])
Simulator_Games_Button_7_Icon = Simulator_Games_Button_7_Icon.resize((100, 100))
Simulator_Games_Button_7_Icon = ImageTk.PhotoImage(Simulator_Games_Button_7_Icon)
Simulator_Games_Button_8_Icon = Image.open(recommended_games_PS3_simulation[7][1])
Simulator_Games_Button_8_Icon = Simulator_Games_Button_8_Icon.resize((100, 100))
Simulator_Games_Button_8_Icon = ImageTk.PhotoImage(Simulator_Games_Button_8_Icon)
Simulator_Games_Button_9_Icon = Image.open(recommended_games_PS3_simulation[8][1])
Simulator_Games_Button_9_Icon = Simulator_Games_Button_9_Icon.resize((100, 100))
Simulator_Games_Button_9_Icon = ImageTk.PhotoImage(Simulator_Games_Button_9_Icon)
Simulator_Games_Button_10_Icon = Image.open(recommended_games_PS3_simulation[9][1])
Simulator_Games_Button_10_Icon = Simulator_Games_Button_10_Icon.resize((100, 100))
Simulator_Games_Button_10_Icon = ImageTk.PhotoImage(Simulator_Games_Button_10_Icon)
Simulator_Games_Button_11_Icon = Image.open(recommended_games_PS3_simulation[10][1])
Simulator_Games_Button_11_Icon = Simulator_Games_Button_11_Icon.resize((100, 100))
Simulator_Games_Button_11_Icon = ImageTk.PhotoImage(Simulator_Games_Button_11_Icon)
Simulator_Games_Button_12_Icon = Image.open(recommended_games_PS3_simulation[11][1])
Simulator_Games_Button_12_Icon = Simulator_Games_Button_12_Icon.resize((100, 100))
Simulator_Games_Button_12_Icon = ImageTk.PhotoImage(Simulator_Games_Button_12_Icon)
Simulator_Games_Button_13_Icon = Image.open(recommended_games_PS3_simulation[12][1])
Simulator_Games_Button_13_Icon = Simulator_Games_Button_13_Icon.resize((100, 100))
Simulator_Games_Button_13_Icon = ImageTk.PhotoImage(Simulator_Games_Button_13_Icon)
Simulator_Games_Button_14_Icon = Image.open(recommended_games_PS3_simulation[13][1])
Simulator_Games_Button_14_Icon = Simulator_Games_Button_14_Icon.resize((100, 100))
Simulator_Games_Button_14_Icon = ImageTk.PhotoImage(Simulator_Games_Button_14_Icon)
Simulator_Games_Button_15_Icon = Image.open(recommended_games_PS3_simulation[14][1])
Simulator_Games_Button_15_Icon = Simulator_Games_Button_15_Icon.resize((100, 100))
Simulator_Games_Button_15_Icon = ImageTk.PhotoImage(Simulator_Games_Button_15_Icon)
Simulator_Games_Button_16_Icon = Image.open(recommended_games_PS3_simulation[15][1])
Simulator_Games_Button_16_Icon = Simulator_Games_Button_16_Icon.resize((100, 100))
Simulator_Games_Button_16_Icon = ImageTk.PhotoImage(Simulator_Games_Button_16_Icon)
Simulator_Games_Button_17_Icon = Image.open(recommended_games_PS3_simulation[16][1])
Simulator_Games_Button_17_Icon = Simulator_Games_Button_17_Icon.resize((100, 100))
Simulator_Games_Button_17_Icon = ImageTk.PhotoImage(Simulator_Games_Button_17_Icon)
Simulator_Games_Button_18_Icon = Image.open(recommended_games_PS3_simulation[17][1])
Simulator_Games_Button_18_Icon = Simulator_Games_Button_18_Icon.resize((100, 100))
Simulator_Games_Button_18_Icon = ImageTk.PhotoImage(Simulator_Games_Button_18_Icon)
Simulator_Games_Button_19_Icon = Image.open(recommended_games_PS3_simulation[18][1])
Simulator_Games_Button_19_Icon = Simulator_Games_Button_19_Icon.resize((100, 100))
Simulator_Games_Button_19_Icon = ImageTk.PhotoImage(Simulator_Games_Button_19_Icon)
Simulator_Games_Button_20_Icon = Image.open(recommended_games_PS3_simulation[19][1])
Simulator_Games_Button_20_Icon = Simulator_Games_Button_20_Icon.resize((100, 100))
Simulator_Games_Button_20_Icon = ImageTk.PhotoImage(Simulator_Games_Button_20_Icon)
Simulator_Games_Button_21_Icon = Image.open(recommended_games_PS3_simulation[20][1])
Simulator_Games_Button_21_Icon = Simulator_Games_Button_21_Icon.resize((100, 100))
Simulator_Games_Button_21_Icon = ImageTk.PhotoImage(Simulator_Games_Button_21_Icon)
Simulator_Games_Button_22_Icon = Image.open(recommended_games_PS3_simulation[21][1])
Simulator_Games_Button_22_Icon = Simulator_Games_Button_22_Icon.resize((100, 100))
Simulator_Games_Button_22_Icon = ImageTk.PhotoImage(Simulator_Games_Button_22_Icon)
Simulator_Games_Button_23_Icon = Image.open(recommended_games_PS3_simulation[22][1])
Simulator_Games_Button_23_Icon = Simulator_Games_Button_23_Icon.resize((100, 100))
Simulator_Games_Button_23_Icon = ImageTk.PhotoImage(Simulator_Games_Button_23_Icon)
Simulator_Games_Button_24_Icon = Image.open(recommended_games_PS3_simulation[23][1])
Simulator_Games_Button_24_Icon = Simulator_Games_Button_24_Icon.resize((100, 100))
Simulator_Games_Button_24_Icon = ImageTk.PhotoImage(Simulator_Games_Button_24_Icon)

Vertical_Tabs = tk.IntVar()
Header_Content_Tabs = tk.IntVar()
Left_Navigation = ttk.Frame(root)
if theme == 'sun-valley':
    PS1_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=0, image=PS1_Icon)
    PS1_Button.configure(style='Toggle.TButton')
    PS1_Button.pack(padx='5', pady='5', side='top')
    PS2_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=1, image=PS2_Icon)
    PS2_Button.configure(style='Toggle.TButton')
    PS2_Button.pack(side='top')
    PS3_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=2, image=PS3_Icon)
    PS3_Button.configure(style='Toggle.TButton')
    PS3_Button.pack(pady='5', side='top')
    PSP_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=3, image=PSP_Icon)
    PSP_Button.configure(style='Toggle.TButton')
    PSP_Button.pack(side='top')
    Xbox_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=4, image=Xbox_Icon)
    Xbox_Button.configure(style='Toggle.TButton')
    Xbox_Button.pack(pady='5', side='top')
    Xbox_360_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=5, image=Xbox_360_Icon)
    Xbox_360_Button.configure(style='Toggle.TButton')
    Xbox_360_Button.pack(side='top')
    Wii_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=6, image=Wii_Icon)
    Wii_Button.configure(style='Toggle.TButton')
    Wii_Button.pack(pady='5', side='top')
    Wii_U_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=7, image=Wii_U_Icon)
    Wii_U_Button.configure(style='Toggle.TButton')
    Wii_U_Button.pack(side='top')
    Settings_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=8, image=Settings_Icon)
    Settings_Button.configure(style='Toggle.TButton')
    Settings_Button.pack(pady='0 5', side='bottom')
    Downloads_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=9, image=Download_Icon)
    Downloads_Button.configure(style='Toggle.TButton')
    Downloads_Button.pack(pady='5', side='bottom')
if theme == 'azure' or theme == 'forest':
    PS1_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=0, image=PS1_Icon)
    PS1_Button.configure(style='ToggleButton')
    PS1_Button.pack(padx='5', pady='5', side='top')
    PS2_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=1, image=PS2_Icon)
    PS2_Button.configure(style='ToggleButton')
    PS2_Button.pack(side='top')
    PS3_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=2, image=PS3_Icon)
    PS3_Button.configure(style='ToggleButton')
    PS3_Button.pack(pady='5', side='top')
    PSP_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=3, image=PSP_Icon)
    PSP_Button.configure(style='ToggleButton')
    PSP_Button.pack(side='top')
    Xbox_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=4, image=Xbox_Icon)
    Xbox_Button.configure(style='ToggleButton')
    Xbox_Button.pack(pady='5', side='top')
    Xbox_360_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=5, image=Xbox_360_Icon)
    Xbox_360_Button.configure(style='ToggleButton')
    Xbox_360_Button.pack(side='top')
    Wii_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=6, image=Wii_Icon)
    Wii_Button.configure(style='ToggleButton')
    Wii_Button.pack(pady='5', side='top')
    Wii_U_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=7, image=Wii_U_Icon)
    Wii_U_Button.configure(style='ToggleButton')
    Wii_U_Button.pack(side='top')
    Settings_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=8, image=Settings_Icon)
    Settings_Button.configure(style='ToggleButton')
    Settings_Button.pack(pady='0 5', side='bottom')
    Downloads_Button = ttk.Radiobutton(Left_Navigation, variable=Vertical_Tabs, value=9, image=Download_Icon)
    Downloads_Button.configure(style='ToggleButton')
    Downloads_Button.pack(pady='5', side='bottom')
Left_Navigation.configure(cursor='arrow', height='200', takefocus=False, width='200')
Left_Navigation.pack(anchor='w', expand='false', fill='y', side='left')
Main_Content = ScrolledFrame(root, scrolltype='vertical')
Main_Content_Header_Frame = ttk.Frame(Main_Content.innerframe)
Header_Content_Selector = ttk.Frame(Main_Content_Header_Frame)
if theme == 'sun-valley':
    Header_Content_1 = ttk.Radiobutton(Header_Content_Selector, variable=Header_Content_Tabs, value=10)
    Header_Content_1.configure(style='Toggle.TButton')
    Header_Content_1.pack(padx='5', pady='5', side='top')
    Header_Content_2 = ttk.Radiobutton(Header_Content_Selector, variable=Header_Content_Tabs, value=11)
    Header_Content_2.configure(style='Toggle.TButton')
    Header_Content_2.pack(pady='5', side='top')
    Header_Content_3 = ttk.Radiobutton(Header_Content_Selector, variable=Header_Content_Tabs, value=12)
    Header_Content_3.configure(style='Toggle.TButton')
    Header_Content_3.pack(pady='5', side='top')
    Header_Content_4 = ttk.Radiobutton(Header_Content_Selector, variable=Header_Content_Tabs, value=13)
    Header_Content_4.configure(style='Toggle.TButton')
    Header_Content_4.pack(pady='5', side='top')
    Header_Content_5 = ttk.Radiobutton(Header_Content_Selector, variable=Header_Content_Tabs, value=14)
    Header_Content_5.configure(style='Toggle.TButton')
    Header_Content_5.pack(padx='5', pady='5', side='top')
if theme == 'azure' or theme == 'forest':
    Header_Content_1 = ttk.Radiobutton(Header_Content_Selector, variable=Header_Content_Tabs, value=10)
    Header_Content_1.configure(style='ToggleButton')
    Header_Content_1.pack(padx='5', pady='5', side='top')
    Header_Content_2 = ttk.Radiobutton(Header_Content_Selector, variable=Header_Content_Tabs, value=11)
    Header_Content_2.configure(style='ToggleButton')
    Header_Content_2.pack(pady='5', side='top')
    Header_Content_3 = ttk.Radiobutton(Header_Content_Selector, variable=Header_Content_Tabs, value=12)
    Header_Content_3.configure(style='ToggleButton')
    Header_Content_3.pack(pady='5', side='top')
    Header_Content_4 = ttk.Radiobutton(Header_Content_Selector, variable=Header_Content_Tabs, value=13)
    Header_Content_4.configure(style='ToggleButton')
    Header_Content_4.pack(pady='5', side='top')
    Header_Content_5 = ttk.Radiobutton(Header_Content_Selector, variable=Header_Content_Tabs, value=14)
    Header_Content_5.configure(style='ToggleButton')
    Header_Content_5.pack(padx='5', pady='5', side='top')
Header_Content_Selector.configure(height='200', width='200')
Header_Content_Selector.pack(fill='y', side='right')
Header_Content_Display = ttk.Frame(Main_Content_Header_Frame)
Header_Content_Image = ttk.Label(Header_Content_Display)
Header_Content_Image.pack(anchor='center', side='top')
progressbar1 = ttk.Progressbar(Header_Content_Display)
progressbar1.configure(orient='horizontal')
progressbar1.pack(expand='false', fill='x', side='top')
button11 = ttk.Button(Header_Content_Display)
button11.pack(anchor='n', pady='5', side='right')
Header_Content_Title = ttk.Label(Header_Content_Display)
Header_Content_Title.pack(anchor='n', padx='5', pady='5', side='left')
Header_Content_Description = ttk.Label(Header_Content_Display)
Header_Content_Description.pack(anchor='n', pady='5', side='left')
Header_Content_Display.configure(height='200', width='200')
Header_Content_Display.pack(expand='true', fill='both', side='left')
Main_Content_Header_Frame.configure(height='200', width='200')
Main_Content_Header_Frame.pack(fill='x', side='top')
separator2 = ttk.Separator(Main_Content.innerframe)
separator2.configure(orient='horizontal')
separator2.pack(expand='false', fill='both', pady='5', side='top')
Simulator_Games = ttk.Frame(Main_Content.innerframe)
Simulator_Games_Title = ttk.Label(Simulator_Games)
Simulator_Games_Title.configure(text='Recommended Racing Games', font=('-size', 16, '-weight', 'bold'))
Simulator_Games_Title.pack(anchor='w', side='top')
Simulator_Games_Content = ScrolledFrame(Simulator_Games, scrolltype='horizontal')
Simulator_Games_Button_1 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[0][0],
                                      image=Simulator_Games_Button_1_Icon, compound='top')
Simulator_Games_Button_1.pack(side='left', padx=5, pady=10, fill='y')
Simulator_Games_Button_2 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[1][0],
                                      image=Simulator_Games_Button_2_Icon, compound='top')
Simulator_Games_Button_2.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_3 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[2][0],
                                      image=Simulator_Games_Button_3_Icon, compound='top')
Simulator_Games_Button_3.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_4 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[3][0],
                                      image=Simulator_Games_Button_4_Icon, compound='top')
Simulator_Games_Button_4.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_5 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[4][0],
                                      image=Simulator_Games_Button_5_Icon, compound='top')
Simulator_Games_Button_5.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_6 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[5][0],
                                      image=Simulator_Games_Button_6_Icon, compound='top')
Simulator_Games_Button_6.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_7 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[6][0],
                                      image=Simulator_Games_Button_7_Icon, compound='top')
Simulator_Games_Button_7.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_8 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[7][0],
                                      image=Simulator_Games_Button_8_Icon, compound='top')
Simulator_Games_Button_8.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_9 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[8][0],
                                      image=Simulator_Games_Button_9_Icon, compound='top')
Simulator_Games_Button_9.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_10 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[9][0],
                                       image=Simulator_Games_Button_10_Icon, compound='top')
Simulator_Games_Button_10.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_11 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[10][0],
                                       image=Simulator_Games_Button_11_Icon, compound='top')
Simulator_Games_Button_11.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_12 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[11][0],
                                       image=Simulator_Games_Button_12_Icon, compound='top')
Simulator_Games_Button_12.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_13 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[12][0],
                                       image=Simulator_Games_Button_13_Icon, compound='top')
Simulator_Games_Button_13.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_14 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[13][0],
                                       image=Simulator_Games_Button_14_Icon, compound='top')
Simulator_Games_Button_14.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_15 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[14][0],
                                       image=Simulator_Games_Button_15_Icon, compound='top')
Simulator_Games_Button_15.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_16 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[15][0],
                                       image=Simulator_Games_Button_16_Icon, compound='top')
Simulator_Games_Button_16.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_17 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[16][0],
                                       image=Simulator_Games_Button_17_Icon, compound='top')
Simulator_Games_Button_17.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_18 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[17][0],
                                       image=Simulator_Games_Button_18_Icon, compound='top')
Simulator_Games_Button_18.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_19 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[18][0],
                                       image=Simulator_Games_Button_19_Icon, compound='top')
Simulator_Games_Button_19.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_20 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[19][0],
                                       image=Simulator_Games_Button_20_Icon, compound='top')
Simulator_Games_Button_20.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_21 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[20][0],
                                       image=Simulator_Games_Button_21_Icon, compound='top')
Simulator_Games_Button_21.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_22 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[21][0],
                                       image=Simulator_Games_Button_22_Icon, compound='top')
Simulator_Games_Button_22.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_23 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[22][0],
                                       image=Simulator_Games_Button_23_Icon, compound='top')
Simulator_Games_Button_23.pack(side='left', padx='0 5', pady=10, fill='y')
Simulator_Games_Button_24 = ttk.Button(Simulator_Games_Content.innerframe, text=recommended_games_PS3_simulation[23][0],
                                       image=Simulator_Games_Button_24_Icon, compound='top')
Simulator_Games_Button_24.pack(side='left', padx='0 5', pady=10, fill='y')

if len(Simulator_Games_Button_1['text']) >= 15:
    Simulator_Games_Button_1['text'] = Simulator_Games_Button_1['text'][0:13] + '...'
if len(Simulator_Games_Button_2['text']) >= 15:
    Simulator_Games_Button_2['text'] = Simulator_Games_Button_2['text'][0:13] + '...'
if len(Simulator_Games_Button_3['text']) >= 15:
    Simulator_Games_Button_3['text'] = Simulator_Games_Button_3['text'][0:13] + '...'
if len(Simulator_Games_Button_4['text']) >= 15:
    Simulator_Games_Button_4['text'] = Simulator_Games_Button_4['text'][0:13] + '...'
if len(Simulator_Games_Button_5['text']) >= 15:
    Simulator_Games_Button_5['text'] = Simulator_Games_Button_5['text'][0:13] + '...'
if len(Simulator_Games_Button_6['text']) >= 15:
    Simulator_Games_Button_6['text'] = Simulator_Games_Button_6['text'][0:13] + '...'
if len(Simulator_Games_Button_7['text']) >= 15:
    Simulator_Games_Button_7['text'] = Simulator_Games_Button_7['text'][0:13] + '...'
if len(Simulator_Games_Button_8['text']) >= 15:
    Simulator_Games_Button_8['text'] = Simulator_Games_Button_8['text'][0:13] + '...'
if len(Simulator_Games_Button_9['text']) >= 15:
    Simulator_Games_Button_9['text'] = Simulator_Games_Button_9['text'][0:13] + '...'
if len(Simulator_Games_Button_10['text']) >= 15:
    Simulator_Games_Button_10['text'] = Simulator_Games_Button_10['text'][0:13] + '...'
if len(Simulator_Games_Button_11['text']) >= 15:
    Simulator_Games_Button_11['text'] = Simulator_Games_Button_11['text'][0:13] + '...'
if len(Simulator_Games_Button_12['text']) >= 15:
    Simulator_Games_Button_12['text'] = Simulator_Games_Button_12['text'][0:13] + '...'
if len(Simulator_Games_Button_13['text']) >= 15:
    Simulator_Games_Button_13['text'] = Simulator_Games_Button_13['text'][0:13] + '...'
if len(Simulator_Games_Button_14['text']) >= 15:
    Simulator_Games_Button_14['text'] = Simulator_Games_Button_14['text'][0:13] + '...'
if len(Simulator_Games_Button_15['text']) >= 15:
    Simulator_Games_Button_15['text'] = Simulator_Games_Button_15['text'][0:13] + '...'
if len(Simulator_Games_Button_16['text']) >= 15:
    Simulator_Games_Button_16['text'] = Simulator_Games_Button_16['text'][0:13] + '...'
if len(Simulator_Games_Button_17['text']) >= 15:
    Simulator_Games_Button_17['text'] = Simulator_Games_Button_17['text'][0:13] + '...'
if len(Simulator_Games_Button_18['text']) >= 15:
    Simulator_Games_Button_18['text'] = Simulator_Games_Button_18['text'][0:13] + '...'
if len(Simulator_Games_Button_19['text']) >= 15:
    Simulator_Games_Button_19['text'] = Simulator_Games_Button_19['text'][0:13] + '...'
if len(Simulator_Games_Button_20['text']) >= 15:
    Simulator_Games_Button_20['text'] = Simulator_Games_Button_20['text'][0:13] + '...'
if len(Simulator_Games_Button_21['text']) >= 15:
    Simulator_Games_Button_21['text'] = Simulator_Games_Button_21['text'][0:13] + '...'
if len(Simulator_Games_Button_22['text']) >= 15:
    Simulator_Games_Button_22['text'] = Simulator_Games_Button_22['text'][0:13] + '...'
if len(Simulator_Games_Button_23['text']) >= 15:
    Simulator_Games_Button_23['text'] = Simulator_Games_Button_23['text'][0:13] + '...'
if len(Simulator_Games_Button_24['text']) >= 15:
    Simulator_Games_Button_24['text'] = Simulator_Games_Button_24['text'][0:13] + '...'

Simulator_Games_Content.configure(usemousewheel=False)
Simulator_Games_Content.pack(fill='x', side='top')
Simulator_Games.configure(height='250')
Simulator_Games.pack(fill='x', side='top')
separator1 = ttk.Separator(Main_Content.innerframe)
separator1.configure(orient='horizontal')
separator1.pack(expand='false', fill='both', pady='5', side='top')
Shooter_Games = ttk.Frame(Main_Content.innerframe)
Shooter_Games_Title = ttk.Label(Shooter_Games)
Shooter_Games_Title.configure(text='Recommended Shooter Games', font=('-size', 16, '-weight', 'bold'))
Shooter_Games_Title.pack(anchor='w', side='top')
Shooter_Games_Content = ScrolledFrame(Shooter_Games, scrolltype='horizontal')
Shooter_Games_Button_1 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_1.pack(side='left', padx='5')
Shooter_Games_Button_2 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_2.pack(side='left', padx='0 5')
Shooter_Games_Button_3 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_3.pack(side='left', padx='0 5')
Shooter_Games_Button_4 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_4.pack(side='left', padx='0 5')
Shooter_Games_Button_5 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_5.pack(side='left', padx='0 5')
Shooter_Games_Button_6 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_6.pack(side='left', padx='0 5')
Shooter_Games_Button_7 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_7.pack(side='left', padx='0 5')
Shooter_Games_Button_8 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_8.pack(side='left', padx='0 5')
Shooter_Games_Button_9 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_9.pack(side='left', padx='0 5')
Shooter_Games_Button_10 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_10.pack(side='left', padx='0 5')
Shooter_Games_Button_11 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_11.pack(side='left', padx='0 5')
Shooter_Games_Button_12 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_12.pack(side='left', padx='0 5')
Shooter_Games_Button_13 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_13.pack(side='left', padx='0 5')
Shooter_Games_Button_14 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_14.pack(side='left', padx='0 5')
Shooter_Games_Button_15 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_15.pack(side='left', padx='0 5')
Shooter_Games_Button_16 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_16.pack(side='left', padx='0 5')
Shooter_Games_Button_17 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_17.pack(side='left', padx='0 5')
Shooter_Games_Button_18 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_18.pack(side='left', padx='0 5')
Shooter_Games_Button_19 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_19.pack(side='left', padx='0 5')
Shooter_Games_Button_20 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_20.pack(side='left', padx='0 5')
Shooter_Games_Button_21 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_21.pack(side='left', padx='0 5')
Shooter_Games_Button_22 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_22.pack(side='left', padx='0 5')
Shooter_Games_Button_23 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_23.pack(side='left', padx='0 5')
Shooter_Games_Button_24 = ttk.Button(Shooter_Games_Content.innerframe)
Shooter_Games_Button_24.pack(side='left', padx='0 5')
Shooter_Games_Content.configure(usemousewheel=False)
Shooter_Games_Content.pack(fill='x', side='top')
Shooter_Games.configure(height='200', width='200')
Shooter_Games.pack(fill='x', side='top')
Main_Content.configure(usemousewheel=True)
Main_Content.pack(expand='true', fill='both', side='right', padx="5 0")
Nav_Seperator = ttk.Separator()
Nav_Seperator.configure(orient='horizontal')
Nav_Seperator.pack(expand='true', fill='y', side='top')

root.mainloop()
