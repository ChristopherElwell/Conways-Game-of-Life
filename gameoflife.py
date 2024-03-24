import copy
import os
from random import randrange
from time import sleep
import time
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import re
import math
import csv
from tkinter import filedialog
from gradientmaker import *

class gameoflife(ctk.CTk):

    def cellpressed(self,event,state):
        #if self.toggle == 1:
            #pass
        
        btnnum = [math.floor(event.x/self.n),math.floor(event.y/self.n)]

        try:
            if self.statesnow[btnnum[1]][btnnum[0]] == 0:
                self.canvas.itemconfigure(self.cells[btnnum[1]][btnnum[0]], fill = self.onoff[1])
                self.statesnow[btnnum[1]][btnnum[0]] = 1
                
            elif state:
                self.canvas.itemconfigure(self.cells[btnnum[1]][btnnum[0]], fill = self.onoff[0])
                self.statesnow[btnnum[1]][btnnum[0]] = 0
        except IndexError:
            pass
        
    def nextcolour(self):
        self.colour += 1 
        try:
            self.onoff[1] = self.colours[self.colour]
        except IndexError:
            self.colour = 0
            self.onoff[1] = self.colours[self.colour]

    def rungame(self):
        self.nextcolour()
        points = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
        for j in [row for row in range(len(self.statesnow)) if 1 in self.statesnow[row]]:
            for i in [column for column in range(len(self.statesnow[j])) if self.statesnow[j][column] == 1]:
                surroundings = 0
                for point in points:
                    try:
                        surroundings += self.statesnow[j+point[0]][i+point[1]]
                    except IndexError:
                        pass
                
                #Death Rule
                if surroundings <= 1 or surroundings >= 4:
                    self.statestobe[j][i] = 0
                    self.canvas.itemconfigure(self.cells[j][i], fill = self.onoff[0])

                #Survival Rule
                elif surroundings in [2,3]:
                    self.statestobe[j][i] = 1
                
                for secondpoint in points:
                    try:
                        nearby = self.statesnow[j+secondpoint[0]][i+secondpoint[1]]
                    except IndexError:
                        pass
                    else: 
                        if nearby == 0:
                            deadsurroundings = 0
                            for deadpoint in points:
                                try:
                                    deadsurroundings += self.statesnow[j+secondpoint[0]+deadpoint[0]][i+secondpoint[1]+deadpoint[1]]
                                except IndexError:
                                    pass
                            
                            #Birth Rule
                            if deadsurroundings == 3:
                                self.statestobe[j+secondpoint[0]][i+secondpoint[1]] = 1
                                self.canvas.itemconfigure(self.cells[j+secondpoint[0]][i+secondpoint[1]], fill = self.onoff[1])

    
        if self.statesnow == self.statestobe:
            self.togglegame()

        for j in range(self.size[0]):
            for i in range(self.size[1]):
                self.statesnow[j][i] = self.statestobe[j][i]
                #self.btns[i][j].config(bg=self.onoff[self.statesnow[i][j]])


        if self.toggle == 1:
            self.after(self.speed, self.rungame) 

    def togglegame(self):
        if self.toggle == 1:
            self.toggle = 0
            self.gamerunbtn.configure(text="Run Game")
            if self.cleargamebtn.cget("state") == "disabled":
                self.cleargamebtn.configure(state="normal")
            self.menubar.entryconfigure("Load Pattern", state = "normal")
            self.savestate = self.statesnow
        else:
            self.toggle = 1
            self.gamerunbtn.configure(text="Stop Game")
            if self.cleargamebtn.cget("state") == "normal":
                self.cleargamebtn.configure(state="disabled")
            self.menubar.entryconfigure("Load Pattern", state = "disable")
            if self.gradientmaker is not None:
                self.colours = self.gradientmaker.gradient
                self.nextcolour
            
            self.rungame()

    def cleargame(self):
        for j in range(self.size[0]):
            for i in range(self.size[1]):
                self.statesnow[j][i] = 0
                self.statestobe[j][i] = 0
                self.canvas.itemconfigure(self.cells[j][i], fill = self.onoff[0])
                self.colour = randrange(len(self.colours))
                self.nextcolour()

    def sizegame(self):
        match self.size:
            case [5,5]:
                self.n = 90
                self.geometry("500x550")
            case [10,10]:
                self.n = 45
                self.geometry("500x550")
            case [20,20]:
                self.n = 25
                self.geometry("500x550")
            case [50,50]:
                self.n = 10
                self.geometry("500x550")
            case [50,100]:
                self.n = 10
                self.geometry("1100x600")
            case [100,100]:
                self.n = 7
                self.geometry("800x800")
            case [100,200]:
                self.n = 5
                self.geometry("1100x600")
            case [200,200]:
                self.n = 3
                self.geometry("800x600")

        self.canvassize = [self.size[1]*self.n, self.size[0]*self.n]

    def begingame(self, selected_size, firsttime):
        self.nextcolour()
        
        if firsttime == False:
            self.savestate = self.statesnow
        self.size = [int((re.findall(r"\d+", selected_size))[1]), int((re.findall(r"\d+", selected_size))[0])]
        self.statesnow = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.statestobe = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]
       
        self.sizegame()

        if firsttime == False:
            self.canvas.destroy()
            for j in [row for row in range(len(self.savestate)) if 1 in self.savestate[row]]:
                for i in [column for column in range(len(self.savestate[j])) if self.savestate[j][column] == 1]:
                    try:
                        self.statesnow[round((self.size[0]-len(self.savestate))/2)+j][round((self.size[1]-len(self.savestate[j]))/2)+i] = 1
                    except IndexError:
                        pass
        
        self.canvas = ctk.CTkCanvas(self, width=self.canvassize[0], height=self.canvassize[1], bg="#282729", border=0)
        self.canvas.grid(column = 0, row = 2, pady=20)
        self.canvas.bind("<Button-1>", lambda event: self.cellpressed(event, True))
        self.canvas.bind("<B1-Motion>", lambda event: self.cellpressed(event, False))
        
        self.cells = []
        for j in range(self.size[0]):
            self.cells.append([])
            for i in range(self.size[1]):
                cell = self.canvas.create_rectangle(self.n*i, self.n*j, self.n*(i+1), self.n*(j+1), width = 0, fill=self.onoff[self.statesnow[j][i]])
                #self.canvas.tag_bind(cell, '<Button-1>', lambda event, cellnum = (i,j): self.cellpressed(cellnum))
                self.cells[j].append(cell)

    def reload(self, selected_size):
        self.begingame(selected_size, False)

    def initializevars(self):
        self.gamesizes = ["5x5","10x10","20x20", "50x50", "100x50", "100x100", "200x100", "200x200"]
        self.size_var = ctk.StringVar(self)
        self.size_var.set(self.gamesizes[3])
        self.size = [50,50]
        self.toggle = 0
        self.onoff = ["#282729","colour","#F4E3B2", "red"]
        self.waszero = False
        self.savestate = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.timer = 0
        self.colour = 0
        
    def initializebuttons(self):
        self.columnconfigure(0, weight=1)
        self.btnframe = ctk.CTkFrame(self, width = 600, height = 20)
        self.btnframe.columnconfigure(0, weight=1)
        self.btnframe.columnconfigure(1, weight=1)
        self.btnframe.columnconfigure(2, weight=1)
        self.gamerunbtn = ctk.CTkButton(self.btnframe, text="Run Game", command=self.togglegame, width = 100)
        self.gamerunbtn.grid(column = 0, row = 0)
        self.cleargamebtn = ctk.CTkButton(self.btnframe, text="Clear Game", command=self.cleargame, width = 100)
        self.cleargamebtn.grid(column = 1, row = 0)
        self.gamesizemenu = ctk.CTkOptionMenu(self.btnframe, variable = self.size_var, values = self.gamesizes, command=self.reload, width = 100)
        self.gamesizemenu.grid(column = 2, row = 0)
        self.btnframe.grid(column = 0, row = 0, pady=20, padx=20, sticky="news")

        self.menubar = tk.Menu(self)
        self.opengradient = tk.Menu(self.menubar, tearoff=0)
        self.opengradient.add_command(label="Open Gradient Editor", command = self.opengradienteditor)
        self.menubar.add_cascade(label="Gradients", menu=self.opengradient)
        self.config(menu=self.menubar)

        self.speedscale=ctk.CTkSlider(self, from_=0, to = 100, orientation="horizontal", command=self.speedchange)
        self.speedscale.set(50)
        self.speedscale.grid(column = 0, row = 1, pady=0, sticky="n")
        self.speedchange("event")
        self.load = tk.Menu(self.menubar, tearoff=0)
        self.load.add_command(label="Select Pattern Folder", command = lambda: self.choosepatternfolder("empty"))
        self.menubar.add_cascade(label="Load Pattern", menu=self.load)
        self.config(menu=self.menubar)  
        self.gradientisopen = False

    def opengradienteditor(self):
            self.gradientmaker.deiconify()

    def speedchange(self,event):
        
        slidersetting = self.speedscale.get()
        self.speed = round(-7/5*float(slidersetting)) + 150
    
        if int(slidersetting) == 0:
            self.toggle = 1
            self.togglegame()
        if int(slidersetting) == 0:
            self.waszero = True
        if self.waszero and int(slidersetting) != 0:
            self.toggle = 0
            self.togglegame()
            self.waszero = False
    
    def choosepatternfolder(self, directory):
        if directory == "empty": 
            directory = filedialog.askdirectory()
        all_files_and_dirs = os.listdir(directory)
        filepaths = [os.path.join(directory, filename) for filename in all_files_and_dirs]
        loads = [f.replace(".txt", "") for f in all_files_and_dirs if ".txt" in f]
        
        loadoptions = []
        self.load.delete(0, 'end')
        self.load.add_command(label="Select Pattern Folder", command = lambda: self.choosepatternfolder("empty"))
        for i, file in enumerate(loads):
            loadoption = self.load.add_command(label=file, 
            command = lambda directory = directory, filepath = filepaths[i]: self.importpattern(directory, filepath))
            loadoptions.append(loadoption) 

    def readRLE(self,File_object):

        line = File_object.readline()
        while line[0] == "#":
            line = File_object.readline()

        xy = [int((re.findall(r"\d+", line))[0]), int((re.findall(r"\d+", line))[1])]

        pattern = []
        pattern.append(xy)

        ptext = File_object.read()

        codes = re.findall(r"(\d*[ob]|\$)", ptext)
        j = 1
        pattern.append([])
        for code in codes:
            if code == "$":
                pattern.append([])
                j += 1
                i = 0
            else:
                num = re.findall(r"(\d+)", code)
                if len(num) == 0:
                    num = 1
                else:
                    num = int(num[0])

                if "o" in code:
                    state = 1
                else:
                    state = 0
                
                for _ in range(num):
                    pattern[j].append(state)
        return pattern

    def importpattern(self,directory,filepath):
        File_object = open(filepath,"r")
        self.pointslasthover = []
        pattern = self.readRLE(File_object)
        patternpoints = []
        for j, value in enumerate(pattern): 
            if 1 in value and j > 0:
                for i, value in enumerate(pattern[j]): 
                    if value == 1:
                        patternpoints.append([j,i])
        self.canvas.bind("<Motion>", lambda event, pattern = pattern, patternpoints = patternpoints: 
                         self.hoverpattern(event, pattern, patternpoints))
        self.cleargamebtn.configure(text = "End Load", command = self.endload)
        self.bind("<Escape>", self.endload)
        self.canvas.unbind("<B1-Motion>")
        self.gamerunbtn.configure(state="disabled")
        self.canvas.bind("<Button-1>", 
        lambda event, patternpoints = patternpoints, pattern=pattern, i = 0: 
                        self.printingpress(event, patternpoints, pattern, i))

    def endload(self, event=None):
        self.gamerunbtn.configure(state="normal")
        self.canvas.unbind("<Motion>")
        self.unbind("<Escape>")
        self.canvas.bind("<B1-Motion>", lambda event: self.cellpressed(event, False))
        self.canvas.bind("<Button-1>", lambda event: self.cellpressed(event, True))
        self.cleargamebtn.configure(text="Clear Game", command=self.cleargame)
        
        for j, row in enumerate(self.hoverstate):
            if 2 in row:
                for i, value in enumerate(row):
                    if value == 2 and self.statesnow[j][i] == 1:
                        self.canvas.itemconfigure(self.cells[j][i], fill = self.onoff[1])
                    elif value == 2 and self.statesnow[j][i] != 1:
                        self.canvas.itemconfigure(self.cells[j][i], fill = self.onoff[0])
                           
    def printingpress(self, event, patternpoints, pattern, i):
        btnnum = [math.floor(event.x/self.n),math.floor(event.y/self.n)]
        try:
            point = patternpoints[i]
        except IndexError:
            pass
        else:
            i += 1
            try:
                self.statesnow[point[0]+btnnum[1]-round(pattern[0][1]/2)][point[1]+btnnum[0]-round(pattern[0][0]/2)] = 1
            except IndexError:
                pass
            else:
                self.canvas.itemconfig(self.cells[point[0]+btnnum[1]-round(pattern[0][1]/2)][point[1]+btnnum[0]-round(pattern[0][0]/2)], fill = self.onoff[self.statesnow[point[0]+btnnum[1]-round(pattern[0][1]/2)][point[1]+btnnum[0]-round(pattern[0][0]/2)]])
            self.nextcolour()
            self.after(round(500/len(patternpoints)), self.printingpress, event, patternpoints, pattern, i)    
                
    def hoverpattern(self, event, pattern, patternpoints):
        
        self.hoverstate = copy.deepcopy(self.statesnow)
        
        btnnum = [math.floor(event.x/self.n),math.floor(event.y/self.n)]
        
        for point in self.pointslasthover:
            try: 
                colornum = self.statesnow[point[0]][point[1]]
            except IndexError:
                pass
            else:
                self.canvas.itemconfigure(self.cells[point[0]][point[1]], fill = self.onoff[colornum])
        
        self.pointslasthover = []
        
        for point in patternpoints:
            y = btnnum[1]+point[0]-round(pattern[0][1]/2)
            x = btnnum[0]+point[1]-round(pattern[0][0]/2)
            try:
                self.hoverstate[y][x] = 2
                self.canvas.itemconfigure(self.cells[y][x], fill = self.onoff[2])
            except IndexError:
                pass
            
            self.pointslasthover.append([y,x])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
        self.geometry("800x400")
        
        self.initializevars()
        self.gradientmaker = GradientMaker(self)
        self.gradientmaker.close()
        self.colours = self.gradientmaker.gradient
        self.sizegame()
        self.initializebuttons()
       
        
        self.begingame(self.gamesizes[3], True)

        self.mainloop()     

mainwindow = gameoflife()
mainwindow.mainloop()