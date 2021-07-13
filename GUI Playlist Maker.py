from tkinter import *
import random
import os, fnmatch
import pathlib
import random
import shelve
from pathlib import Path


root = Tk()
root.title('Playlist Maker')

# open cabinet
cabinet=shelve.open(os.path.join(Path(__file__).resolve().parents[0], 'newcabinet'))
dirList=cabinet['dirList']
songListList=cabinet['songListList']
lengthList=cabinet['lengthList']
cabinet.close()

extraTime=int(0)
actualSongList=[]


#functions

def saveSonglist():
    cabinet=shelve.open(os.path.join(Path(__file__).resolve().parents[0], 'newcabinet'))
    cabinet['dirList']=dirList
    cabinet['songListList']=songListList
    cabinet['lengthList']=lengthList
    cabinet.close()



def addFrame(x):

    rowOffset=3
    offsetRow=rowOffset + x

    frameTwo = Frame(root, pady=3)
    frameTwo.grid(row=offsetRow, sticky="ew")
    frameTwo.columnconfigure(1, weight=0)
    frameTwo.columnconfigure(2, weight=1)

    dirTitle=dirList[x]
    mainLabel=Label(frameTwo, text=os.path.basename(dirTitle), relief = RIDGE, font=(30), padx=50, width=3)
    mainLabel.grid(row=offsetRow, column=1, sticky='w')

    slider_value = IntVar()
    slider_value.set(50)
    slider = Scale(frameTwo, from_=0, to=100, orient='horizontal', variable=slider_value, label="Weight")
    slider.grid(row=offsetRow, column=2, sticky='ew')

    enableVar=IntVar()

    enableToggle = Checkbutton(frameTwo, text="Enable", variable=enableVar)
    enableToggle.grid(row=offsetRow, column=0)

    extractVar=IntVar()

    extractToggle=Checkbutton(frameTwo, text="Remove Played Songs", variable=extractVar)
    extractToggle.grid(row=offsetRow, column=3, padx=20)

    blockList = []
    blockList.append(enableVar)
    blockList.append(slider_value)
    blockList.append(extractVar)


    return blockList

def tryPlaylist():
    anyEnabled=False
    for x in range(len(dirList)):
        if (int(frameList[x][0].get())==1):
            anyEnabled=True

    durationVar.set(num(durationVar.get()))




    
    if anyEnabled:
        makePlaylist()


def songpull(funcsonglist, funcsonglistlen, funcduration, extract):

    if funcsonglist == []:
        return funcduration

    songzip=list(zip(funcsonglist, funcsonglistlen))

    random.shuffle(songzip)
    random.shuffle(songzip)
    a, b = zip(*songzip)
    outsonglist = list(a)
    outsonglistlen = list(b)



    if (extract==1):
        funcsonglist.clear()
        funcsonglistlen.clear()



    for x  in range(len(outsonglist)):
        if funcduration > 120:
            actualSongList.append(outsonglist[x])
            funcduration=(funcduration-outsonglistlen[x])
        elif (extract==1):
            funcsonglist.append(outsonglist[x])
            funcsonglistlen.append(outsonglistlen[x])
        




    return funcduration

        

def num(s):
    try:
        return float(s)
    except ValueError:
        return ("Enter a number.")

def makePlaylist():
    totalWeight=int(0)
    for x in range(len(dirList)):
        if (int(frameList[x][0].get())==1):
            totalWeight = (totalWeight + frameList[x][1].get())
    

    durationSecs=((float(durationVar.get())*60*60))
    if ((bedtimeBool.get())==1):
        durationSecs = (durationSecs-1082)
    timePerWU = (durationSecs/totalWeight)


    for x in range(len(dirList)):
        if (int(frameList[x][0].get())==1):
            
            extratime=songpull(songListList[x], lengthList[x], ((int(frameList[x][1].get())*timePerWU)+extraTime), (int(frameList[x][2].get())))
            

    random.shuffle(actualSongList)
    random.shuffle(actualSongList)
    random.shuffle(actualSongList)

    if ((bedtimeBool.get())==1):
        for line in open(os.path.join((Path(__file__).resolve().parents[1]), "end of night.m3u"), "r"):
            actualSongList.append(line)



    outfile=open(outfileVar.get(), "w")

    for x in range(len(actualSongList)):
        outfile.write(actualSongList[x]) 
        outfile.write("\n")   

    outfile.close

    outfileVar.set(os.path.join((Path(__file__).resolve().parents[1]), "Automatic Playlist ")+str(playlistcounter.get())+".m3u")
    playlistcounter.set((playlistcounter.get()+1))
    
    actualSongList.clear()



def saveWeights():
    weightList=[]
    for x in range(len(dirList)):
        weightList.append(frameList[x][1].get())

    weightbench=shelve.open(os.path.join((Path(__file__).resolve().parents[1]), 'weightcabinet'))
    weightbench['dirList']=dirList
    weightbench['weightList']=weightList
    weightbench.close()
    lwButt.configure(text="Load Weights")


def loadWeights():
    weightbench=shelve.open(os.path.join((Path(__file__).resolve().parents[1]), 'weightcabinet'))
    testList=weightbench['dirList']
    weightList=weightbench['weightList']
    weightbench.close()

    if(testList == dirList):
        for x in range(len(dirList)):
            frameList[x][1].set(weightList[x])
    else:
        lwButt.configure(text="No Saved Weights")
    





def select_file():
    pass




# create all of the main containers
top_frame = Frame(root, pady=3)

# layout all of the main containers
#root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")

# create the widgets for the top frame
playlistcounter=IntVar()
playlistcounter.set(1)
Button(top_frame, text="Make Playlist", command=tryPlaylist).grid(row=0, column=0, sticky='nsew')
bedtimeBool=IntVar()
bedtime=Checkbutton(top_frame, text="Bedtime", variable=bedtimeBool, relief=RIDGE, padx=5)
bedtime.grid(row=0, column=1, pady=5)
durLabel=Label(top_frame, text="Duration")
durLabel.grid(row=1, column=0, pady=5)
durationVar=StringVar()
durationVar.set(0)
durationBox=Entry(top_frame, exportselection=0, textvariable=durationVar, width=5, relief=RIDGE)
durationBox.grid(row=1, column=1, pady=5)
Button(top_frame, text="Save Weights", command=saveWeights).grid(row=0, column=2, pady=5)
lwButt=StringVar()
lwButt=Button(top_frame, text="Load Weights", command=loadWeights)
lwButt.grid(row=0, column=3, pady=5)
Button(top_frame, text="Save Song Lists", command=saveSonglist).grid(row=1, column=2, sticky='nsew')
outLabel=Label(top_frame, text="Playlist Name")
outLabel.grid(row=3, column=0, pady=5)
outfileVar=StringVar()
outfileVar.set(os.path.join((Path(__file__).resolve().parents[1]), "Automatic Playlist.m3u"))
outfileBox=Entry(top_frame, exportselection=0, textvariable=outfileVar, width=70, relief=RIDGE)
outfileBox.grid(row=3, column=1, columnspan=4, pady=5)

# attempting to create next frame
frameList=[]
for x in range(len(dirList)):
    frameList.append(addFrame(x))



root.mainloop()
