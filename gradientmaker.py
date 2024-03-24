import math
import tkinter
import numpy as np
import customtkinter as ctk





class gradientUI(ctk.CTkFrame):

    def __init__(self, master=None, masterpage = None, **kwargs):
        self.masterpage = masterpage
        self.title = kwargs.pop('gradienttitle', None)
        
    

        super().__init__(master, **kwargs)
        self.gradientres = 500
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.gradienttitle = ctk.CTkLabel(self, text = self.title, font = ('Lato', 20))
        self.gradienttitle.grid(row = 0, column = 0, pady= 10, padx = 10, sticky="w")
        self.entercolour = ctk.CTkEntry(self, width=70)
        self.entercolour.grid(row = 0, column=2, padx = 10, sticky = "e")
        self.entercolour.bind("<Return>", self.colourentered)
        self.canvaswidth = 450
        self.canvasheight = 50
        self.gradientshow = ctk.CTkCanvas(self, width = self.canvaswidth-5, height = self.canvasheight-5, bg='#181818', bd=0)
        self.gradientshow.grid(row = 1, column = 0, padx=10, columnspan=3, sticky="w")
        self.nothexcode = ctk.CTkLabel(self, text = " ", font = ('lato', 14))
        self.nothexcode.grid(row = 0, column = 1, sticky="e")


        self.colours = []
        self.gradient = ["#181818"]

        if self.title == "Gradient 1":
            self.colours = ["#B4C5E4","#3066BE","#090C9B"]
            self.gradient = self.makegradient()
            self.showgradient(self.gradient)

    def addgradient(self):
        self.masterpage.create_new_gradientUI()
    
    def colourentered(self,event):
        colour = self.entercolour.get()
        self.entercolour.delete(0,ctk.END)
        if len(colour) not in [6,7]:
            self.nothexcode.configure(text = " Not a HexCode ", bg_color = "#780116")
            return
        try:
            int(colour,16)
        except ValueError:
            try:
                int(colour[1:],16)
            except ValueError:
                self.nothexcode.configure(text = "Not a HexCode", bg_color = "#780116")
                return
        self.nothexcode.configure(text = " ", bg_color = "transparent")
        if colour[0] != "#":
            colour = "#"+ colour
        self.colours.append(colour)
        
        self.gradient = self.makegradient()
        self.showgradient(self.gradient)

    def showgradient(self, gradient):
        
        for i, colour in enumerate(gradient):
            self.gradientshow.create_rectangle(i*self.canvaswidth/len(gradient),0,(i+1)*self.canvaswidth/len(gradient),self.canvasheight, fill = colour, width = 0)
        
    def hextorgb(self, colourhex):
        
        r = int(colourhex[1]+colourhex[2],16)
        g = int(colourhex[3]+colourhex[4],16)
        b = int(colourhex[5]+colourhex[6],16)
        return np.array([r,g,b])
    
    def rgbtohex(self, colourrgb):
        
        r = round(colourrgb[0])
        g = round(colourrgb[1])
        b = round(colourrgb[2])
        colourhex = "#{:02X}{:02X}{:02X}".format(r,g,b)
        
        return colourhex

    def makegradient(self):
        if len(self.colours) <= 1:
            return self.colours*self.gradientres
        
        count = 0
        coloursrgb = []
        gradienthex = []
        
        
        for colourhex in self.colours:
            coloursrgb.append(self.hextorgb(colourhex))
        n = math.floor(self.gradientres/((len(self.colours)-1)*2))
        
        for i in range(len(coloursrgb)-1):
            
            delta = (coloursrgb[i+1] - coloursrgb[i])/n
            for j in range(n):
                nexthex = self.rgbtohex(coloursrgb[i]+delta*j)
            
                gradienthex.append(nexthex)
        
        gradienthex = gradienthex + gradienthex[::-1]

        return gradienthex

class GradientMaker(ctk.CTkToplevel):

    def create_new_gradientUI(self):
        
        self.gradientcount += 1
        newgradient=gradientUI(self.scrollframe, self, gradienttitle="Gradient " + str(self.gradientcount))
        newgradient.grid(column = 1, row = self.gradientcount, sticky="news", padx=10, pady=15)
        self.gradients.append(newgradient)
        radiobutton = ctk.CTkRadioButton(self.scrollframe, text = " ", width=0,
                                             variable= self.activegradnum, command = self.updategradient, value=len(self.radiobuttons)+1)
        radiobutton.grid(column = 0, row = self.gradientcount, padx=10, sticky="news")
        radiobutton.select()
        self.radiobuttons.append(radiobutton)
        self.updategradient()

    def updategradient(self):
        self.gradient = self.gradients[self.activegradnum.get()-1].gradient

    def close(self):
        self.updategradient()
        self.withdraw()

    def open(self):
        self.deiconify()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gradientcount = 0
        self.gradients = []
        self.radiobuttons = []
        self.geometry("500x400")
        self.title("Make Gradient")
        self.addbutton = ctk.CTkButton(self, text = "Add Gradient", command = self.create_new_gradientUI, fg_color = '#264027', hover_color = '#1F331F', font = ('lato', 14))
        self.addbutton.grid(column = 0, row = 0, padx=10, pady=20)
        self.closebutton = ctk.CTkButton(self, text="Save and Close", fg_color='#780116', font = ('lato', 14), hover_color = '#640214', command = self.close)
        self.closebutton.grid(column = 1, row = 0, padx=10, pady=20)

        self.activegradnum = tkinter.IntVar()
        self.scrollframe = ctk.CTkScrollableFrame(self, width = 440, height = 300)
        self.scrollframe.columnconfigure(0, weight = 1)
        self.scrollframe.columnconfigure(1, weight = 5)
        self.scrollframe.grid(column = 0, row = 1, columnspan = 2, padx=20, pady=0)
        
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        self.create_new_gradientUI()
        self.updategradient()

       
