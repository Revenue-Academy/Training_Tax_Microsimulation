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
from matplotlib.pyplot import figure
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import numpy as np
#from taxcalc import *

from PIL import Image,ImageTk

def update_chart_list(self):
    self.chart_combo['values'] = self.chart_list

def tab6(self):
    # self.button_1_TAB6_pos_x = self.block_1_title_pos_x
    # self.button_1_TAB6_pos_y = self.block_1_title_pos_y
    """
    self.button_1_TAB6_pos_x = 0.5
    self.button_1_TAB6_pos_y = 0.1
    self.button_display_charts = ttk.Button(self.TAB6, text = "Display Charts", style='my.TButton', command=self.display_chart)
    self.button_display_charts.place(relx = self.button_1_TAB6_pos_x, rely = self.button_1_TAB6_pos_y, anchor = "w")       
    """
    
    self.combo_1_TAB6_x = 0.10
    self.combo_1_TAB6_y = 0.10
    
    self.TAB6_combo_entry_gap_x = 0.10
    self.label_1_TAB6_x = self.combo_1_TAB6_x 
    self.label_1_TAB6_y = self.combo_1_TAB6_y
    l1_TAB6=tk.Label(self.TAB6, text="Select Chart: ", font = self.fontStyle)
    l1_TAB6.place(relx = self.label_1_TAB6_x, 
                  rely = self.label_1_TAB6_y, anchor = "e")
    self.combo_2_TAB6_x = self.combo_1_TAB6_x
    self.combo_2_TAB6_y = self.label_1_TAB6_y + 0.1  
    
    """
    self.active_tax = self.find_active_taxes()
    chart_list = []
    for tax_type in self.active_tax:
        chart_list = chart_list + [tax_type+'_revenue_projection']       
        chart_list = chart_list + [tax_type+'_distribution_table']
    """
    self.chart_selection = tk.StringVar()    
    self.chart_combo = ttk.Combobox(self.TAB6, textvariable=self.chart_selection, 
                                    value=self.chart_list, font=self.text_font, postcommand = self.update_chart_list)
    #chart_combo.current(0)
    self.chart_combo.place(relx = self.combo_1_TAB6_x, 
                    rely = self.combo_1_TAB6_y, anchor = "w", width=150)
    self.chart_combo.bind("<<ComboboxSelected>>", lambda event: self.get_attribute_selection(event))
     
    # #self.image = ImageTk.PhotoImage(Image.open("world_bank.png"))
    # self.image = ImageTk.PhotoImage(Image.open("egypt_flag.jpg"))
    # #image = tk.PhotoImage(file="blank.png")
    # self.pic = tk.Label(self.TAB2,image=self.image)
    # self.pic.place(relx = 0.45, rely = 0.2, anchor = "nw")
    # self.pic.image = self.image                                                          

def display_chart(self, event, selected_chart, global_vars):
    self.selected_attribute_chart = self.attribute_selection.get()
    tax_type = selected_chart[:3]
    if (selected_chart==tax_type+'_revenue_projection'):
        df = pd.read_csv(selected_chart+'.csv', index_col=0)           
        df = df.T
        #print(df) 
        df1 = df[df.columns[df.columns.str.contains(self.selected_attribute_chart)]]
        if global_vars[tax_type+'_adjust_behavior']:
            df1.columns=['Current', 'Reform', 'Behavior']
        else:
            df1.columns=['Current', 'Reform']
        df1['Year'] = df1.index
        df1 = df1[1:]
        fig, ax = plt.subplots(figsize=(8, 6))
        #fig = plt.Figure()
        #ax = fig.add_subplot(figsize=(5, 5))
        
        plt.plot(df1.Year, df1.Current, color='r', marker='x')
        plt.plot(df1.Year, df1.Reform, color='b', marker='x')
        plt.title('Corporate tax forecast (in billion) for '+self.selected_attribute_chart)
        # for index in range(len(year_list)):
        #     ax.text(year_list[index], wt_cit[index], wt_cit[index], size=12)
        pic_filename1 = "egypt_rev_forecast.png"
        plt.savefig(pic_filename1)
        self.image = ImageTk.PhotoImage(Image.open("egypt_rev_forecast.png"))
        self.pic = tk.Label(self.TAB6,image=self.image)
        self.pic.place(relx = 0.20, rely = 0.1, anchor = "nw")
        self.pic.image = self.image             
    elif (selected_chart==tax_type+'_distribution_table'):
        if global_vars[tax_type+'_distribution_table']:
           df = pd.read_csv(selected_chart+'.csv', thousands=',') 
           df.drop('Unnamed: 0', axis=1, inplace=True)
           df = df.set_index('index')
           #figure(figsize=(8, 8), dpi=200)
           fig, ax = plt.subplots(figsize=(8, 8))              
           df.plot(kind='bar',y=[df.columns[0], df.columns[1]],figsize=(8,6))
           pic_filename1 = "egypt_dist.png"
           plt.savefig(pic_filename1)
           self.image = ImageTk.PhotoImage(Image.open("egypt_dist.png"))
           self.pic = tk.Label(self.TAB6,image=self.image)
           self.pic.place(relx = 0.20, rely = 0.1, anchor = "nw")
           self.pic.image = self.image
    elif (selected_chart==tax_type+'_etr'):
        df = pd.read_csv(selected_chart+'.csv', index_col=0)
        df = df[['ETR', 'ETR_ref']]
        df = df[:-1]
        df['ETR'] = np.where(df['ETR']>1, np.nan, df['ETR'])
        df['ETR_ref'] = np.where(df['ETR_ref']>1, np.nan, df['ETR_ref'])            
        df = df.reset_index()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax = df.plot(kind="line", x = 'index'  , y='ETR', color="b", label="ETR")
        df.plot(kind="line", x = 'index' , y="ETR_ref", color="r", label="ETR under Reform", ax=ax)            
        #fig = plt.Figure()
        #ax = fig.add_subplot(figsize=(5, 5))
        plt.xlabel('Percentile')
        plt.xticks(df.index[::5])
        plt.title('Effective Tax Rates by Percentile')
        # for index in range(len(year_list)):
        #     ax.text(year_list[index], wt_cit[index], wt_cit[index], size=12)
        pic_filename1 = "egypt_etr.png"
        plt.savefig(pic_filename1)
        self.image = ImageTk.PhotoImage(Image.open("egypt_etr.png"))
        self.pic = tk.Label(self.TAB6,image=self.image)
        self.pic.place(relx = 0.20, rely = 0.1, anchor = "nw")
        self.pic.image = self.image       
    
def get_attribute_selection(self, event):
    # self.Label1=Label(self.TAB6, text="Charts", font = self.fontStyle_sub_title)
    # self.Label1.place(relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y, anchor = "w")
    selected_chart = self.chart_selection.get()
    #print('selected_chart ', selected_chart)
    tax_type = selected_chart[:3]
    f = open('global_vars.json')
    global_vars = json.load(f)
    #print("vars['charts_ready'] ", vars['charts_ready'])
    self.image = ImageTk.PhotoImage(Image.open("blank.png"))
    self.pic = tk.Label(self.TAB6,image=self.image)
    self.pic.place(relx = 0.20, rely = 0.1, anchor = "nw")
    self.pic.image = self.image
    #print("vars['charts_ready'] ", vars['charts_ready'])
    if global_vars['charts_ready']:
        df = pd.read_csv(selected_chart+'.csv', index_col=0)
        df = df.T
        cols = df.columns[df.columns.str.startswith('current_law')]
        attribute_name=self.attribute_columns[0]
        attribute_types = [i[12:].title() for i in cols]
        l2_TAB6=tk.Label(self.TAB6, text="Select "+attribute_name+" : ", font = self.fontStyle)
        l2_TAB6.place(relx = self.combo_2_TAB6_x, 
                      rely = self.combo_2_TAB6_y, anchor = "e")        
        self.attribute_selection = tk.StringVar()    
        self.attributes_combo = ttk.Combobox(self.TAB6, textvariable=self.attribute_selection, 
                                    value=attribute_types, font=self.text_font)
        self.attributes_combo.place(relx = self.combo_2_TAB6_x, 
                    rely = self.combo_2_TAB6_y, anchor = "w", width=150)
        self.attributes_combo.bind("<<ComboboxSelected>>", lambda event: self.display_chart(event, selected_chart, global_vars))        
        
            
        # self.img1 = Image.open(pic_filename1)
        # self.img2 = self.img1.resize((500, 500), Image.ANTIALIAS)
        # self.img3 = ImageTk.PhotoImage(self.img2)
        # self.pic.configure(image=self.img3)
        # self.pic.image = self.img3
        
 
    
    