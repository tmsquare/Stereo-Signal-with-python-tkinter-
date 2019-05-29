"""    
Mode d'emploi: -- Selectionner dans la playlist ( a partir de l'ordinateur)
			    deux fichiers .wav de frequence d'echantillonnage Fe=48000
			   -- Cliquer sur le ficher .wav en position superieure
			   -- Enfin commencer a ecouter les sons et afficher les graphes avec les bouttons play et plot
"""

import os
import threading
import time

# graphical interface modules
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk

# sound playing modules
from mutagen.mp3 import MP3
from pygame import mixer

# plotting modules
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# audio data manipulation modules
import urllib
import scipy.io.wavfile
import pydub
import numpy as np
import wave
import struct


root = tk.ThemedTk()

bg_image = PhotoImage(file ="0.png")
x = Label (image = bg_image)
x.place(x=0, y=0, relwidth=1, relheight=1)

root.title("Stereo Signal")
root.geometry("1000x750")
root.get_themes()                 # Returns a list of all themes that can be set
root.set_theme("radiance")         # Sets an available theme

statusbar = ttk.Label(root, text="Welcome to Melody", relief=SUNKEN, anchor=W, font='Times 10 italic')

playlist = []

# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function


mixer.init()  # initializing the mixer


# Root Window -  LeftFrame, RightFrame
# LeftFrame - The listbox (playlist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame


frameplaylist = Frame(root)
frameplaylist.grid(row= 1, column=0, padx=10,pady=80)

playlistbox = Listbox(frameplaylist)
playlistbox.grid(row= 0, column=1)

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

addBtn = ttk.Button(frameplaylist, text="+ Add", command=browse_file)
addBtn.grid(row= 1, column=1)

delBtn = ttk.Button(frameplaylist, text="- Del", command=del_song)
delBtn.grid(row= 1, column=2)

# defining Top , Midle and Bottom frames for Signals Infos
framehaut = Frame(root)
framehaut.grid(row=0, column=0, padx=5,pady=5)

framemilieu = Frame(root)
framemilieu.grid(row=1, column=2, padx=5,pady=5)

framebas = Frame(root)
framebas.grid(row=2, column=0, padx=5,pady=60)

# defining top subFrames of each frame
topframehaut = Frame(framehaut)
topframehaut.grid(row= 0, column=0)

topframemilieu = Frame(framemilieu)
topframemilieu.grid(row= 0, column=0)

topframebas = Frame(framebas)
topframebas.grid(row= 0, column=0)

# designing top labels of each frame (Title, Longueur totale, En cours) 
infoshaut = ttk.Label(topframehaut, text='Options du Premier Signal', relief=GROOVE)
infoshaut.grid(row= 0, column=0, pady=5)

infosmilieu = ttk.Label(topframemilieu, text='Options du Signal Resultant', relief=GROOVE)
infosmilieu.grid(row= 0, column=0, pady=5)

infosbas = ttk.Label(topframebas, text='Options du Deuxieme Signal', relief=GROOVE)
infosbas.grid(row= 0, column=0, pady=5)

lengthlabelhaut = ttk.Label(topframehaut, text='Longueur Totale : --:--')
lengthlabelhaut.grid(row= 1, column=0, pady=5)

lengthlabelmilieu = ttk.Label(topframemilieu, text='Longueur Totale : --:--')
lengthlabelmilieu.grid(row= 1, column=0, pady=5)

lengthlabelbas = ttk.Label(topframebas, text='Longueur Totale : --:--')
lengthlabelbas.grid(row= 1, column=0, pady=5)

currenttimelabelhaut = ttk.Label(topframehaut, text='En Cours : --:--', relief=GROOVE)
currenttimelabelhaut.grid(row= 2, column=0, pady=5)

currenttimelabelmilieu = ttk.Label(topframemilieu, text='En Cours : --:--', relief=GROOVE)
currenttimelabelmilieu.grid(row= 2, column=0, pady=5)

currenttimelabelbas = ttk.Label(topframebas, text='En Cours : --:--', relief=GROOVE)
currenttimelabelbas.grid(row= 2, column=0, pady=5)

# top labels functions for each Frame
def show_details_haut(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabelhaut['text'] = "Longueur Totale" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count_haut, args=(total_length,))
    t1.start()

def start_count_haut(t):
    global paused_haut
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused_haut:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabelhaut['text'] = "En Cours" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def show_details_bas(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabelbas['text'] = "Longueur Totale" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count_bas, args=(total_length,))
    t1.start()


def start_count_bas(t):
    global paused_bas
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused_bas:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabelbas['text'] = "En Cours" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1

# play function of TopFrame
def play_music_haut():
    global paused_haut
    global audData_haut 
    
 
    if paused_haut:
        mixer.music.unpause()
        paused_haut = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_haut = playlist[selected_song]
            
            rate,audData_haut=scipy.io.wavfile.read(play_haut)
            scipy.io.wavfile.write(play_haut, rate, audData_haut)
            
            mixer.music.load(play_haut)
            mixer.music.play()
            show_details_haut(play_haut)
        except:
            tkinter.messagebox.showerror('Erreur Ouverture', 'Fichier inexistant ou type de fichier non supposte.')


# play function of BottomFrame
def play_music_bas():
    global paused_bas
    global audData_bas
    global rate
    
    
    if paused_bas:
        mixer.music.unpause()
        paused_bas = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_bas = playlist[selected_song+1]
            
            rate,audData_bas=scipy.io.wavfile.read(play_bas)
            scipy.io.wavfile.write(play_bas, rate, audData_bas)

            mixer.music.load(play_bas)
            mixer.music.play()
            show_details_bas(play_bas)
        except:
            tkinter.messagebox.showerror('Erreur Ouverture', 'Fichier inexistant ou type de fichier non supposte.')

# play functions of MiddleFrame
def play_music_col1():
    global paused_bas
    global a
    global stereo1
    
    
    
    a = np.array([audData_haut,audData_haut])
    stereo1=a.T
    stereo1[:,0]=0
   
    scipy.io.wavfile.write("file1.wav", rate, stereo1)
    if paused_bas:
        mixer.music.unpause()
    else:
        try:
            stop_music()
            time.sleep(1)
            mixer.music.load("file1.wav")
            mixer.music.play()
            show_details_bas(play_it)
        except:
            pass

def play_music_col2():
    global paused_bas
    global b
    global stereo2
    
    b = np.array([audData_bas,audData_bas])
    stereo2=b.T
    stereo2[:,1]=0
    
    scipy.io.wavfile.write("file2.wav", rate, stereo2)
    if paused_bas:
        mixer.music.unpause()
        paused_bas = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            mixer.music.load("file2.wav")
            mixer.music.play()
            show_details_bas(play_it)
        except:
            pass


def play_music_both():
    global paused_bas
    global c
    global stereo3
    
    c = np.array([audData_haut,audData_bas])
    stereo3=c.T
    
    scipy.io.wavfile.write("file.wav", rate, stereo3)
    if paused_bas:
        mixer.music.unpause()
        paused_bas = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            mixer.music.load("file.wav")
            mixer.music.play()
            how_details_bas(play_it)
        except:
            pass


# stop function
def stop_music():
    mixer.music.stop()
    

paused_haut = FALSE
paused_bas = FALSE


# pause functions
def pause_music_haut():
    global paused_haut
    paused_haut = TRUE
    mixer.music.pause()
def pause_music_bas():
    global paused_bas
    paused_bas = TRUE
    mixer.music.pause()
    
# plot function of TopFrame
def plot_haut():
    
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    play_haut = playlist[selected_song]
    rate,audData=scipy.io.wavfile.read(play_haut)
    #Convert the data to a numpy array.
    data = np.array(audData)
    #fft of the data
    data_fft = np.fft.fft(data)
    
    '''
    The fft returns an array of complex numbers that doesn’t tell us anything.
    data_fft[:8]: first 8 fft value.
    '''
    #Convert the complex numbers to real values
    frequencies = np.abs(data_fft)
    '''
    The numpy abs() function will take our complex signal
     and generate the real part of it.
    '''
    fig = Figure(figsize=(6,6))
    a = fig.add_subplot(211)
    a.plot(data[:1000000])
    a.set_title ("Analyse Temporelle", fontsize=16)
    b = fig.add_subplot(212)
    b.plot(frequencies[:1000000])
    b.set_title ("Analyse Frequencielle", fontsize=16)
    
    t1 = Toplevel(root) # child window for plotting
    t1.title("Graphe Signal 1")
    
    canvas = FigureCanvasTkAgg(fig, master=t1)
    canvas.get_tk_widget().grid(row = 0, column = 0)
    canvas.show()

# plot function of BottomFrame
def plot_bas():
    
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    play_bas = playlist[selected_song+1]
    rate,audData=scipy.io.wavfile.read(play_bas)
    #Convert the data to a numpy array.
    data = np.array(audData)
    #fft of the data
    data_fft = np.fft.fft(data)
    
    '''
    The fft returns an array of complex numbers that doesn’t tell us anything.
    data_fft[:8]: first 8 fft value.
    '''
    #Convert the complex numbers to real values
    frequencies = np.abs(data_fft)
    '''
    The numpy abs() function will take our complex signal
     and generate the real part of it.
    '''
    fig = Figure(figsize=(6,6))
    a = fig.add_subplot(211)
    a.plot(data[:1000000])
    a.set_title ("Analyse Temporelle", fontsize=16)
    b = fig.add_subplot(212)
    b.plot(frequencies[:1000000])
    b.set_title ("Analyse Frequencielle", fontsize=16)
    
    t1 = Toplevel(root) # child window for plotting
    t1.title("Graphe Signal 2")

    canvas = FigureCanvasTkAgg(fig, master=t1)
    canvas.get_tk_widget().grid(row = 0, column = 0)
    canvas.show()


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE

# defining middle subFrames of each frame
middleframehaut = Frame(framehaut)
middleframehaut.grid(row= 1, column=0)

middleframemilieu = Frame(framemilieu)
middleframemilieu.grid(row= 1, column=0)

middleframebas = Frame(framebas)
middleframebas.grid(row= 1, column=0)

# designing middle labels of each frame (Play, Pause, Stop , Play/Deux Colonnes, Play/Col1, Play/Col2) 
playBtnhaut = ttk.Button(middleframehaut,text="PLay", command=play_music_haut)
playBtnhaut.grid(row=0, column=0, padx=10)

playBtnbas = ttk.Button(middleframebas,text="PLay", command=play_music_bas)
playBtnbas.grid(row=0, column=0, padx=10)

playBtn1milieu = ttk.Button(middleframemilieu,text="PLay/Col1", command=play_music_col1)
playBtn1milieu.grid(row=0, column=0, padx=10)
playBtn2milieu = ttk.Button(middleframemilieu,text="PLay/Col2", command=play_music_col2)
playBtn2milieu.grid(row=0, column=1, padx=10)
playBtn3milieu = ttk.Button(middleframemilieu,text="PLay/Deux Colonnes", command=play_music_both)
playBtn3milieu.grid(row=0, column=2, padx=10)


stopBtnhaut = ttk.Button(middleframehaut,text="Stop" , command=stop_music)
stopBtnhaut.grid(row=0, column=1, padx=10)

stopBtnbas = ttk.Button(middleframebas,text="Stop" , command=stop_music)
stopBtnbas.grid(row=0, column=1, padx=10)


pauseBtnhaut = ttk.Button(middleframehaut, text="Pause", command=pause_music_haut)
pauseBtnhaut.grid(row=0, column=2, padx=10)

pauseBtnbas = ttk.Button(middleframebas, text="Pause", command=pause_music_bas)
pauseBtnbas.grid(row=0, column=2, padx=10)


# defining bottom subFrames of each frame
bottomframehaut = Frame(framehaut)
bottomframehaut.grid(row= 2, column=0)

bottomframemilieu = Frame(framemilieu)
bottomframemilieu.grid(row= 2, column=0)

bottomframebas = Frame(framebas)
bottomframebas.grid(row= 2, column=0)

# designing middle labels of each frame (Plot, Mute, Stop, Volume scale)
plotBtnhaut = ttk.Button(bottomframehaut,text="Plot",command=plot_haut)
plotBtnhaut.grid(row=0, column=0)

plotBtnbas = ttk.Button(bottomframebas,text="Plot",command=plot_bas)
plotBtnbas.grid(row=0, column=0)

stopBtnhaut = ttk.Button(bottomframemilieu,text="Stop" , command=stop_music)
stopBtnhaut.grid(row=0, column=0, padx=10)

volumeBtnhaut = ttk.Button(bottomframehaut, text="Mute", command=mute_music)
volumeBtnhaut.grid(row=0, column=1)

volumeBtnmilieu = ttk.Button(bottomframemilieu, text="Mute", command=mute_music)
volumeBtnmilieu.grid(row=0, column=1)

volumeBtnbas = ttk.Button(bottomframebas, text="Mute", command=mute_music)
volumeBtnbas.grid(row=0, column=1)

scalehaut = ttk.Scale(bottomframehaut, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scalehaut.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scalehaut.grid(row=0, column=2, pady=15, padx=30)

scalebas = ttk.Scale(bottomframebas, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scalebas.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scalebas.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
