import tkinter as tk
from tkinter import filedialog as fd
import random
import os, fnmatch
import pathlib
import random
from pymediainfo import MediaInfo
import shelve
from pathlib import Path



""" GUI Stuff """

root = tk.Tk()


dirList = []
songListList = []
lengthList = []


def color(ndex, dir):
    button_label_list[ndex][1].config(text=dir)

def select_file(dex):
    filetypes = (
        ('Music', '*.mp4'),
        ('All files', '*.*')
    )

    filename = fd.askdirectory(
        title='Open a directory',
        initialdir=(Path(__file__).resolve().parents[1]))
    color(dex, filename)

def dump():
    global count, button_label_list
    button_label_list.append([tk.Button(frame, text="Dir", command=lambda x=count: select_file(x)), tk.Label(frame)])
    button_label_list[-1][0].grid(row=count, column=0, sticky='nsew')
    button_label_list[-1][1].grid(row=count, column=1, sticky='nsew')
    frame.columnconfigure(count, weight=1)
    count += 1

""" Non-GUI Stuff Follows """

def pullSongLists(path):
    listOfFiles = os.listdir(path)
    funclist=list()
    pattern = "*.mp4"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            funclist.append(os.path.join(path, entry))  
    random.shuffle(funclist)  
    return funclist   



def pullSongTimes(songList):
    lenlist = []
    for x in range(len(songList)):
        media_info = MediaInfo.parse(songList[x])
        lenlist.append(int(media_info.video_tracks[0].duration/1000))
    return lenlist

def dirDump():
    for entry in button_label_list:
        if (entry[1]['text']) != "":
            dirList.append(entry[1]['text'])
    
    for x in range(len(dirList)):
        songListList.append(pullSongLists(dirList[x]))

    for y in range(len(songListList)):
        lengthList.append(pullSongTimes(songListList[y]))



    cabinet=shelve.open(os.path.join(Path(__file__).resolve().parents[0], 'newcabinet'))
    cabinet['dirList']=dirList
    cabinet['songListList']=songListList
    cabinet['lengthList']=lengthList
    cabinet.close()

    evilButton.configure(text = "Done.")


nfbText=tk.StringVar()
nfbText.set("Pull and Measure")

count = 0
button_label_list = []
root.title("Music Measurer")
root.rowconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

frame = tk.Frame(root)
frame.rowconfigure(1, weight=1)
frame.grid(row=0, column=2, sticky='nsew', rowspan=2)

tk.Button(root, text="Add Directory", command=dump).grid(row=0, column=1, sticky='nsew')
tk.Button(root, text="Quit!", command=root.quit).grid(row=0, column=0, sticky='nsew')
evilButton = tk.Button(root, text="Pull and Measure", command=dirDump)
evilButton.grid(row=1, column=1, sticky='new')


root.mainloop()
