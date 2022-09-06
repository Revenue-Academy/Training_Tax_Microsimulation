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
from matplotlib.ticker import NullFormatter
rcParams.update({'figure.autolayout': True})
import numpy as np
#from taxcalc import *

from PIL import Image,ImageTk

def update_chart_list(self):
    self.chart_combo['values'] = self.chart_list

def tab6(self):
    global_vars = self.get_inputs()
    #print('global_vars[chart_list] ', global_vars['chart_list'])
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
    chart_list = global_vars['chart_list']
    self.chart_selection = tk.StringVar() 
    self.chart_combo = ttk.Combobox(self.TAB6, textvariable=self.chart_selection, 
                                    value=chart_list, font=self.text_font)
    #chart_combo.current(0)
    self.chart_combo.place(relx = self.combo_1_TAB6_x, 
                    rely = self.combo_1_TAB6_y, anchor = "w", width=150)
    
    f = open('global_vars.json')
    global_vars = json.load(f)
    
    #self.chart_combo.bind("<<ComboboxSelected>>", lambda event: self.get_attribute_selection(event))
    self.chart_combo.bind("<<ComboboxSelected>>", lambda event: self.display_chart(event, global_vars))
    # #self.image = ImageTk.PhotoImage(Image.open("world_bank.png"))
    # self.image = ImageTk.PhotoImage(Image.open("egypt_flag.jpg"))
    # #image = tk.PhotoImage(file="blank.png")
    # self.pic = tk.Label(self.TAB2,image=self.image)
    # self.pic.place(relx = 0.45, rely = 0.2, anchor = "nw")
    # self.pic.image = self.image                                                          

def display_chart(self, event, global_vars):    
    def formatter(x, pos):
        return str(round(x / 1e6, 1))
        
    self.image = ImageTk.PhotoImage(Image.open("blank.png"))
    self.pic = tk.Label(self.TAB6,image=self.image)
    self.pic.place(relx = 0.20, rely = 0.1, anchor = "nw")
    
    #self.selected_attribute_chart = self.attribute_selection.get()
    selected_chart = self.chart_selection.get()
    
    #print('selected_chart ', selected_chart)
    #tax_type = selected_chart[:3]
    #f = open('global_vars.json')
    #global_vars = json.load(f)
    #print('global vars', global_vars)
    #tax_type = selected_chart[:3]
    if global_vars['pit']:
        tax_type = 'pit'
        tax_collection_var = 'pitax'        
    elif global_vars['cit']:
        tax_type = 'cit'
        tax_collection_var = 'citax'        
    else:
        tax_type = 'vat'
    start_year= global_vars['start_year']
    data_start_year= global_vars['data_start_year']
    kakwani_list = global_vars['kakwani_list']      
    
    if (selected_chart==tax_type+'_revenue_projection'):
        df = pd.read_csv(selected_chart+'.csv', index_col=0)           
        df = df.T
        
        if tax_type == 'pit':
            df = df
            if self.vars[tax_type+'_adjust_behavior']:
                df.columns=['Current Law', 'Reform', 'Behavior']
            else:
                df.columns=['Current Law', 'Reform']
        elif tax_type == 'cit':
            if self.vars[tax_type+'_adjust_behavior']:
                df = df[df.columns[:3]]
                df.columns=['Current Law', 'Reform', 'Behavior']
            else:
                df = df[df.columns[:2]]
                df.columns=['Current Law', 'Reform']
        df1 = df.rename_axis('Year').reset_index()
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.plot(df1['Year'], df1['Current Law'], color='r', marker='x',
                 label='Current Law')
        plt.plot(df1['Year'], df1['Reform'], color='b', marker='o', 
                 markerfacecolor='None', markeredgecolor='b',
                 label='Reform')
        plt.legend()
        plt.title('Personal Income Tax forecast (in billions)')
        pic_filename1 = "rev_forecast.png"
        plt.savefig(pic_filename1)
        self.image = ImageTk.PhotoImage(Image.open("rev_forecast.png"))
        self.pic = tk.Label(self.TAB6,image=self.image)
        self.pic.place(relx = 0.20, rely = 0.1, anchor = "nw")
        self.pic.image = self.image             
    elif (selected_chart==tax_type+'_distribution_table'):
        df = pd.read_csv(selected_chart+'.csv', thousands=',') 
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df = df.set_index('index')
        df.index.names = ['Decile']
        fig, ax = plt.subplots(figsize=(8, 8))  
        #drop the rows that includes the average and top 1%
        df=df[:-4]
        ax = df.plot(kind='bar',y=[tax_collection_var+'_'+str(data_start_year), tax_collection_var+'_'+str(start_year), tax_collection_var+'_ref_'+str(start_year)],figsize=(7, 7))
        ax.set_xlabel("Assessable Income Deciles")
        ax.yaxis.set_major_formatter(formatter)
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.set_ylabel("Tax Liability in millions")      
        pic_filename1 = "distribution_chart.png"
        plt.savefig(pic_filename1)
        self.image = ImageTk.PhotoImage(Image.open("distribution_chart.png"))
        self.pic = tk.Label(self.TAB6,image=self.image)
        self.pic.place(relx = 0.20, rely = 0.1, anchor = "nw")
        self.pic.image = self.image
    
    elif (selected_chart==tax_type+'_distribution_table_top1'):
        df = pd.read_csv(selected_chart+'.csv', thousands=',') 
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df = df.set_index('index')
        df.index.names = ['Decile']
        fig, ax = plt.subplots(figsize=(8, 8))              
        ax=df.plot(kind='bar',y=[tax_collection_var+'_'+str(data_start_year), tax_collection_var+'_'+str(start_year), tax_collection_var+'_ref_'+str(start_year)],figsize=(7, 7))       
        ax.set_xlabel("Assessable Income Deciles")
        ax.yaxis.set_major_formatter(formatter)
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.set_ylabel("Tax Liability in millions")        
        pic_filename1 = "distribution_chart_top.png"
        plt.savefig(pic_filename1)
        self.image = ImageTk.PhotoImage(Image.open("distribution_chart_top.png"))
        self.pic = tk.Label(self.TAB6,image=self.image)
        self.pic.place(relx = 0.20, rely = 0.1, anchor = "nw")
        self.pic.image = self.image
    
    elif (selected_chart==tax_type+'_distribution_table_income_bins'):
        df = pd.read_csv(selected_chart+'.csv', thousands=',') 
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df = df.set_index('index')
        df.index.names = ['Income Group']
        #df1=df[df.columns[0]][2:][:-1]
        df1 = df[[tax_collection_var+'_'+str(start_year), tax_collection_var+'_ref_'+str(start_year)]][2:][:-1]
        #print('df1 is ', df1)
        df1['pct1'] = df1[tax_collection_var+'_'+str(start_year)]/df1[tax_collection_var+'_'+str(start_year)].sum()
        df1['pct2'] = df1[tax_collection_var+'_ref_'+str(start_year)]/df1[tax_collection_var+'_ref_'+str(start_year)].sum()
        print("df1['pct2'] is", df1['pct2'])
        labels1 = []
        for i in range(len(df1['pct1'])):
            if df1['pct1'][i]<0.05:
                labels1=labels1+['']
            else:
                labels1=labels1+[df1.index[i]]
            
        fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10,7)) #ax1,ax2 refer to your two pies
        w1,l1,p1 = ax1.pie(df1.pct1,labels=labels1,autopct = '%1.1f%%', startangle=90, pctdistance=1) #plot first pie
        pctdists = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.3, 0.3]
        for t,d in zip(p1, pctdists):
            xi,yi = t.get_position()
            ri = np.sqrt(xi**2+yi**2)
            phi = np.arctan2(yi,xi)
            x = d*ri*np.cos(phi)
            y = d*ri*np.sin(phi)
            t.set_position((x,y))
        ax1.set_title('Under Current Law')
        ax1.legend(df1.index, fontsize='small',bbox_to_anchor=(1.1, 1.0))  
        labels2 = []
        for i in range(len(df1['pct2'])):
            if df1['pct2'][i]<0.05:
                labels2=labels2+['']
            else:
                labels2=labels2+[df1.index[i]]
                
        w2,l2,p2 = ax2.pie(df1.pct2,labels=labels2,autopct = '%1.1f%%', startangle=90, pctdistance=1) #plot first pie
        for t,d in zip(p2, pctdists):
            xi,yi = t.get_position()
            ri = np.sqrt(xi**2+yi**2)
            phi = np.arctan2(yi,xi)
            x = d*ri*np.cos(phi)
            y = d*ri*np.sin(phi)
            t.set_position((x,y))        
        ax2.set_title('Under Reform')
      
        fig.suptitle('Contribution to Tax Revenue by Income Groups in '+str(start_year))
        pic_filename1 = "tax_contribution.png"
        plt.savefig(pic_filename1)
        self.image = ImageTk.PhotoImage(Image.open("tax_contribution.png"))
        self.pic = tk.Label(self.TAB6,image=self.image)
        self.pic.place(relx = 0.20, rely = 0.1, anchor = "nw")
        self.pic.image = self.image
        
    elif (selected_chart==tax_type+'_etr'):        
        df = pd.read_csv(selected_chart+'.csv', index_col=0)
        #gini_list =  [0.512656785663004, 0.48923307967360324, 0.48409656284722513]
        #df = pd.read_csv('pit_etr'+'.csv', index_col=0)        
        df = df[:-1]
        df['ETR'] = np.where(df['ETR']>1, np.nan, df['ETR'])
        df['ETR_ref'] = np.where(df['ETR_ref']>1, np.nan, df['ETR_ref'])
        maxy = max(df['ETR'].max(), df['ETR_ref'].max())         
        df = df.reset_index()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax=df.plot(kind="line", x='index', y=['ETR', 'ETR_ref'], color=["r", "b"], label=["ETR "+str(start_year), "ETR Under Reform "+str(start_year)]) 
        #col = ['r', 'b', 'y', 'c', 'm', 'k', 'g', 'r', 'b', 'y']
        #ax.set_xlabel('Percentile')
        ax.set_xticks(np.arange(0, 101, 10))
        ax.set_xticklabels(list(df.index[::10])+[100])       
        ax.set_title('Effective Tax Rates (ETR) by Percentile')
        ax.set_xlabel("Assessable Income Percentile")
        kakwani_text0 = str(start_year)+' Pre Tax Gini                        : '+ str(round(kakwani_list[0],3))
        kakwani_text1 = str(start_year)+' Kakwani Index (Current Law): '+ str(round(kakwani_list[1],3))
        kakwani_text2 = str(start_year)+' Kakwani Index (Reform)       : '+ str(round(kakwani_list[2],3))
        ax.text(5, 5.5*(maxy/10), kakwani_text0, fontsize = 8)
        ax.text(5, 5*(maxy/10), kakwani_text1, fontsize = 8)
        ax.text(5, 4.5*(maxy/10), kakwani_text2, fontsize = 8)
        pic_filename1 = "etr.png"
        plt.savefig(pic_filename1)
        self.image = ImageTk.PhotoImage(Image.open("etr.png"))
        self.pic = tk.Label(self.TAB6,image=self.image)
        self.pic.place(relx = 0.20, rely = 0.1, anchor = "nw")
        self.pic.image = self.image       
    
def get_attribute_selection(self, event):
    selected_chart = self.chart_selection.get()
    tax_type = selected_chart[:3]
    f = open('global_vars.json')
    global_vars = json.load(f)
    self.image = ImageTk.PhotoImage(Image.open("blank.png"))
    self.pic = tk.Label(self.TAB6,image=self.image)
    self.pic.place(relx = 0.20, rely = 0.1, anchor = "nw")
    self.pic.image = self.image
    if global_vars['charts_ready']:
        df = pd.read_csv(tax_type+'_revenue_projection.csv', index_col=0)
        df = df.T
        #print('df columns ', df.columns)
        cols = df.columns[df.columns.str.startswith('current_law')]
        #print('self.attribute_cols ', self.attribute_columns)
        
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
        
 
    
    