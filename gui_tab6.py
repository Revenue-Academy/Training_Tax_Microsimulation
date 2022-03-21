# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 20:56:40 2022

@author: wb305167
"""
import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter.messagebox import showinfo
from tkinter import filedialog

from threading import Thread

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#from taxcalc import *

from PIL import Image,ImageTk
  

def tab6(self):
    # self.button_1_TAB6_pos_x = self.block_1_title_pos_x
    # self.button_1_TAB6_pos_y = self.block_1_title_pos_y
    self.button_1_TAB6_pos_x = 0.5
    self.button_1_TAB6_pos_y = 0.1
    self.button_display_charts = ttk.Button(self.TAB6, text = "Display Charts", style='my.TButton', command=self.display_chart)
    self.button_display_charts.place(relx = self.button_1_TAB6_pos_x, rely = self.button_1_TAB6_pos_y, anchor = "w")       
    
    # #self.image = ImageTk.PhotoImage(Image.open("world_bank.png"))
    # self.image = ImageTk.PhotoImage(Image.open("egypt_flag.jpg"))
    # #image = tk.PhotoImage(file="blank.png")
    # self.pic = tk.Label(self.TAB2,image=self.image)
    # self.pic.place(relx = 0.45, rely = 0.2, anchor = "nw")
    # self.pic.image = self.image                                                          
  
def display_chart(self):
    # self.Label1=Label(self.TAB6, text="Charts", font = self.fontStyle_sub_title)
    # self.Label1.place(relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y, anchor = "w")
    f = open('global_vars.json')
    vars = json.load(f)
    adjust_behavior = 0
    if self.vars['cit'] == 1:
        tax_type = 'cit'
        adjust_behavior = vars[tax_type+'_adjust_behavior']
    
    df = pd.read_csv('revenue_projections.csv')
    df = df.T
    if adjust_behavior:
        df.columns=['Current', 'Reform', 'Behavior']
    else:
        df.columns=['Current', 'Reform']
    df['Year'] = df.index
    df = df[1:]
    fig, ax = plt.subplots(figsize=(5, 5))
    #fig = plt.Figure()
    #ax = fig.add_subplot(figsize=(5, 5))
    
    plt.plot(df.Year, df.Current, color='r', marker='x')
    plt.plot(df.Year, df.Reform, color='b', marker='x')
    plt.title('Corporate tax forecast (in billion EGP)')
    # for index in range(len(year_list)):
    #     ax.text(year_list[index], wt_cit[index], wt_cit[index], size=12)
    pic_filename1 = "egypt_rev_forecast.png"
    plt.savefig(pic_filename1)
    
    # self.img1 = Image.open(pic_filename1)
    # self.img2 = self.img1.resize((500, 500), Image.ANTIALIAS)
    # self.img3 = ImageTk.PhotoImage(self.img2)
    # self.pic.configure(image=self.img3)
    # self.pic.image = self.img3
    
    self.image = ImageTk.PhotoImage(Image.open("egypt_rev_forecast.png"))
    self.pic = tk.Label(self.TAB6,image=self.image)
    self.pic.place(relx = 0.45, rely = 0.2, anchor = "nw")
    self.pic.image = self.image   
    
    