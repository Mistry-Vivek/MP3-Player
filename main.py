import PySimpleGUI as ps
from pygame import mixer
import eyed3

import os

music = []

"""mixer.init()

for x in range(len(music)-1):
    mixer.music.queue(music[x+1])

mixer.music.load(music[0])
mixer.music.play(1)"""

layout = [[ps.Text("Add songs to library:"),ps.Button("Browse")],
          [ps.Button("Play"),ps.Button("Pause"),ps.Button("Quit")],
          [ps.Text("Currently Playing:",key="title",size=(24,1))],
          [ps.Text("Album:",key="album",size=(24,1))],
          [ps.Text("Artist:",key="artist",size=(24,1))],
          [ps.Button("Next Track"),ps.Button("Prev Track")]]
   

window = ps.Window("MP3 PLAYER").Layout(layout)

playing = False
thissong = 0      

#def queue(x):
   # for i in range(len(music)):
    #    if x < i:
     #       mixer.music.queue(music[i])
    
def vol(x):
    mixer.Sound.set_volume(x)
    
def nextt():
    global thissong
    if (len(music) > thissong + 1):
        thissong += 1
    else:
        thissong = 0
    play()

def prevt():
    global thissong
    if (len(music) > thissong + 1):
        thissong -= 1
    else:
        thissong = 0
    play()
        
def updateinfo():
    global audiofile
    audiofile = eyed3.load(music[thissong])
    window.FindElement("title").update("Currently Playing: " + audiofile.tag.title)
    window['title'].set_size((len("Currently Playing: " + audiofile.tag.title),1))
    window.FindElement("album").update("Album: " + audiofile.tag.album)
    window['album'].set_size((len("Album: " + audiofile.tag.album),1))
    window.FindElement("artist").update("Artist: " + audiofile.tag.artist)
    window['artist'].set_size((len("Artist: " + audiofile.tag.artist),1))
    print(audiofile)
    
    
def validate():
    if len(music) == 0: 
        return ("LIBRARY IS EMPTY")

def play():
    global thissong
    playing = True
    #print(music[thissong].replace("`",""))
    mixer.music.load(music[thissong])
    mixer.music.play()
    updateinfo()
    #queue(thissong)

def pause(x):
    if x:
       mixer.music.unpause()
       #print(1)
       return False
    else:
        mixer.music.pause()
        #print(2)
        return True
       
def quit():
    mixer.music.stop()
    window.close()

def browse():
    newfolder = ps.PopupGetFolder("Please select an file to add",no_window="True")
    allfiles = (os.listdir(newfolder))
    for file in os.listdir(newfolder):
        if file.endswith(".mp3"):
            music.append(newfolder + "/" + file)       
    """if not newfile == None:
        music.append(newfile)"""


while True:
    mixer.init()
    event, values = window.read()
    #print(event,values)
    if event is None:
        break
    if event == "Play":
        if not validate() == "LIBRARY IS EMPTY":
            play()
            for x in range(len(music)-1):
               mixer.music.queue(music[x+1])
        else:
            ps.Popup("LIBRARY IS EMPTY")
    if event == "Pause":
        window.FindElement("title").update(validate())
        if not validate() == "LIBRARY IS EMPTY":
            playing = pause(playing)    
    if event == "Quit":
        quit()
        break
    if event == "Browse":
        try:
            browse()
        except:
            ps.Popup("Nothing was added!")
        #print(music)
    if event == "Next Track":
        if not validate() == "LIBRARY IS EMPTY":
            nextt()
        else:
            ps.Popup("LIBRARY IS EMPTY")
    if event == "Prev Track":
        if not validate() == "LIBRARY IS EMPTY":
            prevt()
        else:
            ps.Popup("LIBRARY IS EMPTY")
        
    
"""mixer.init()
mixer.music.load(newfile)
mixer.music.play(1)
print(music)


"""
