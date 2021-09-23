# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 21:27:09 2020

@author: wb305167
"""

import json
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter.messagebox import showinfo

from tkinter import filedialog

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

from taxcalc import *

from PIL import Image,ImageTk


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.number = 0
        self.widgets = []
        self.grid()
        self.createWidgets()

        self.reform={}
        self.selected_item = ""
        self.selected_value = ""
        self.selected_year = 2019
        self.sub_directory = "taxcalc"
        self.data_filename = "pit.csv"
        self.weights_filename = "pit_weights1.csv"
        self.policy_filename = "current_law_policy_cmie.json"
        self.growfactors_filename = self.sub_directory+"/"+"growfactors1.csv"    
        self.benchmark_filename = "tax_incentives_benchmark.json"        
        self.total_revenue_text1 = ""
        self.reform_revenue_text1 = ""
        #self.reform_filename = "app01_reform.json"

        self.fontStyle = tkfont.Font(family="Calibri", size="12")
        self.fontStyle_sub_title = tkfont.Font(family="Calibri", size="14", weight="bold")         
        self.fontStyle_title = tkfont.Font(family="Calibri", size="18", weight="bold")
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)        
        self.text_font = ('Calibri', '12')
                
        # positions
        
        self.title_pos_x = 0.5
        self.title_pos_y = 0.0
        
        self. block_1_title_pos_x = 0.1
        self.block_1_title_pos_y = 0.1
        self.block_title_entry_gap_y = 0.05
        self.block_entry_entry_gap_y = 0.05
        self.block_1_entry_x = 0.15
        self.entry_entry_gap_y = 0.03
        self.block_1_entry_1_y = (self.block_1_title_pos_y+self.block_title_entry_gap_y)
        self.block_1_entry_2_y = (self.block_1_entry_1_y+self.block_entry_entry_gap_y)
        self.block_1_entry_3_y = (self.block_1_entry_2_y+self.block_entry_entry_gap_y)
        self.block_1_entry_4_y = (self.block_1_entry_3_y+self.block_entry_entry_gap_y)        
        self.entry_button_gap = 0.02
        self.button_1_pos_x = 0.05
        self.block_block_gap = 0.1

        self.block_1A_title_pos_y = self.block_1_entry_3_y + self.entry_button_gap + self.block_block_gap        
        self.button_1_pos_y = self.block_1A_title_pos_y + self.block_title_entry_gap_y

        self.block_2_entry_1_1_x = 0.03
        self.block_2_title_pos_y = self.button_1_pos_y + self.block_block_gap
        self.text_entry_gap = 0.03
        self.block_2_entry_1_1_y = (self.block_2_title_pos_y+
                                    self.block_title_entry_gap_y+
                                    self.text_entry_gap)
        self.block_2_combo_entry_gap_x = 0.21
        self.block_2_entry_entry_gap_x = 0.04
        self.block_2_entry_1_2_x = self.block_2_entry_1_1_x + self.block_2_combo_entry_gap_x
        self.block_2_entry_1_3_x = self.block_2_entry_1_2_x + self.block_2_entry_entry_gap_x

        self.block_3_title_pos_x = 0.3
        self.block_3_title_pos_y = self.block_1A_title_pos_y
        self.block_3_entry_x = 0.35
        self.block_3_entry_y = self.block_3_title_pos_y + self.block_title_entry_gap_y      
        self.button_3_pos_x = 0.3  
        self.button_3_pos_y = self.block_3_entry_y + 2*self.entry_button_gap        
             
        self.button_add_reform_x = self.block_2_entry_1_3_x + self.block_2_entry_entry_gap_x + 0.03
        
        self.root_title=Label(text="Tax Microsimulation Model",
                 font = self.fontStyle_title)
        self.root_title.place(relx = self.title_pos_x, rely = self.title_pos_y, anchor = "n")
        
        self.l1=Label(text="Data Inputs",
                 font = self.fontStyle_sub_title)
        self.l1.place(relx = self.block_1_title_pos_x, rely = self.block_1_title_pos_y, anchor = "w")
        
        self.entry_data_filename = Entry(width=30, font = self.fontStyle)
        self.entry_data_filename.place(relx = self.block_1_entry_x, 
                                  rely = self.block_1_entry_1_y,
                                  anchor = "e")
        self.entry_data_filename.insert(END, self.data_filename)
        self.button_data_filename = ttk.Button(text = "Change Data File", style='my.TButton', command=self.input_data_filename)
        self.button_data_filename.place(relx = self.block_1_entry_x,
                                   rely = self.block_1_entry_1_y, anchor = "w")
        #button.place(x=140,y=50)
        
        self.entry_weights_filename = Entry(width=30, font = self.fontStyle)
        self.entry_weights_filename.place(relx = self.block_1_entry_x,
                                     rely = self.block_1_entry_2_y, anchor = "e")
        self.entry_weights_filename.insert(END, self.weights_filename)
        self.button_weights_filename = ttk.Button(text = "Change Weights File", style='my.TButton', command=self.input_weights_filename)
        self.button_weights_filename.place(relx = self.block_1_entry_x, 
                                      rely = self.block_1_entry_2_y, anchor = "w")
        
        self.entry_policy_filename = Entry(width=30, font = self.fontStyle)
        self.entry_policy_filename.place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_3_y, anchor = "e")
        self.entry_policy_filename.insert(END, self.policy_filename)
        self.button_policy_filename = ttk.Button(text = "Change Policy File", style='my.TButton', command=self.input_policy_filename)
        self.button_policy_filename.place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_3_y, anchor = "w")
        """
        self.entry_growfactors_filename = Entry(width=30, font = self.fontStyle)
        self.entry_growfactors_filename.place(relx = self.block_1_entry_x, 
                                    rely = self.block_1_entry_4_y, anchor = "e")
        self.entry_growfactors_filename.insert(END, self.policy_filename)
        self.button_growfactors_filename = ttk.Button(text = "Change Growfactors File", style='my.TButton', command=self.input_growfactors_filename)
        self.button_growfactors_filename.place(relx = self.block_1_entry_x, 
                                     rely = self.block_1_entry_4_y, anchor = "w")
        """        
        self.l1A=Label(text="Current Law",
                 font = self.fontStyle_sub_title)
        self.l1A.place(relx = self.block_1_title_pos_x, rely = self.block_1A_title_pos_y, anchor = "w")
        
        self.button_generate_revenue_curr_law = ttk.Button(text = "Generate Current Law Total Revenues", style='my.TButton', command=self.generate_total_revenues)
        self.button_generate_revenue_curr_law.place(relx = self.button_1_pos_x, 
                                                 rely = self.button_1_pos_y, anchor = "w")
        
        self.l2=Label(text="Reform", font = self.fontStyle_sub_title)
        self.l2.place(relx = self.block_1_title_pos_x, rely = self.block_2_title_pos_y, anchor = "w")
        
        self.l3=Label(text="Select Policy Parameter: ", font = self.fontStyle)
        self.l3.place(relx = self.block_2_entry_1_1_x, 
                 rely = self.block_2_entry_1_1_y-self.text_entry_gap, anchor = "w")
        
        self.current_law_policy, self.policy_options_list = self.policy_options()
        #self.policy_options_list.remove('gst_rate')
        self.block_widget_dict = {}
        self.block_selected_dict = {}
        self.num_reforms = 1
        
       
        self.block_widget_dict[1] = {}
        self.block_selected_dict[1] = {}
        self.block_widget_dict[1][1] = ttk.Combobox(value=self.policy_options_list, font=self.text_font, name=str(self.num_reforms))
        self.block_widget_dict[1][1].current(1)
        self.block_widget_dict[1][1].place(relx = self.block_2_entry_1_1_x, 
                        rely = self.block_2_entry_1_1_y, anchor = "w", width=300)
        
        self.block_widget_dict[1][1].bind("<<ComboboxSelected>>", self.show_policy_selection)
        
        self.l4=Label(text="Year: ", font = self.fontStyle)
        self.l4.place(relx = self.block_2_entry_1_2_x, 
                 rely = self.block_2_entry_1_1_y-self.text_entry_gap, anchor = "w")
        self.block_widget_dict[1][2] = Entry(width=6, font = self.fontStyle)
        self.block_widget_dict[1][2].place(relx = self.block_2_entry_1_2_x, rely = self.block_2_entry_1_1_y, anchor = "w")
        
        self.l5=Label(text="Value: ", font = self.fontStyle)
        self.l5.place(relx = self.block_2_entry_1_3_x, 
                 rely = self.block_2_entry_1_1_y-self.text_entry_gap, anchor = "w")
        self.block_widget_dict[1][3] = Entry(width=10, font = self.fontStyle)
        self.block_widget_dict[1][3].place(relx = self.block_2_entry_1_3_x, rely = self.block_2_entry_1_1_y, anchor = "w")
        
        self.num_reforms += 1
        self.button_add_reform = ttk.Button(text="+", style='my.TButton', command=self.create_policy_widgets, width=2)
        self.button_add_reform.place(relx = self.button_add_reform_x, rely = self.block_2_entry_1_1_y, anchor = "w")        
        
        self.button_generate_revenue_policy = ttk.Button(text = "Generate Revenue under Reform", style='my.TButton', command=self.apply_policy_change)
        self.button_2_pos_y = (self.block_2_entry_1_1_y+(self.num_reforms-1)*(self.entry_entry_gap_y)) +self.entry_button_gap
        self.button_generate_revenue_policy.place(relx = self.button_1_pos_x,
                                                    rely = self.button_2_pos_y, anchor = "w")

        self.l3A=Label(text="Tax Expenditures",
                 font = self.fontStyle_sub_title)
        self.l3A.place(relx = self.block_3_title_pos_x, rely = self.block_3_title_pos_y, anchor = "w")

        self.entry_benchmark_filename = Entry(width=30, font = self.fontStyle)
        self.entry_benchmark_filename.place(relx = self.block_3_entry_x, 
                                  rely = self.block_3_entry_y,
                                  anchor = "e")
        self.entry_benchmark_filename.insert(END, self.benchmark_filename)
        self.button_benchmark_filename = ttk.Button(text = "Change Benchmark File", style='my.TButton', command=self.input_benchmark_filename)
        self.button_benchmark_filename.place(relx = self.block_3_entry_x,
                                   rely = self.block_3_entry_y, anchor = "w")        
        self.button_generate_tax_expenditures = ttk.Button(text = "Generate Tax Expenditures", style='my.TButton', command=self.generate_tax_expenditures)
        self.button_generate_tax_expenditures.place(relx = self.button_3_pos_x, 
                                                 rely = self.button_3_pos_y, anchor = "w")        
        
        self.image = ImageTk.PhotoImage(Image.open("world_bank.png"))
        #image = tk.PhotoImage(file="blank.png")
        self.pic = tk.Label(image=self.image)
        self.pic.place(relx = 0.5, rely = 0.2, anchor = "nw")
        self.pic.image = self.image

    def Add_Reform(self, event=None):
        self.num_reforms.set(self.num_reforms.get() + 1)
            
    def createWidgets(self):
        #self.cloneButton = Button ( self, text='Clone', command=self.clone)
        #self.cloneButton.grid()
        return

    def create_policy_widgets(self):
        self.block_widget_dict[self.num_reforms] = {}
        self.block_selected_dict[self.num_reforms] = {}
        self.block_widget_dict[self.num_reforms][1] = ttk.Combobox(value=self.policy_options_list, font=self.text_font, name=str(self.num_reforms))
        self.block_widget_dict[self.num_reforms][1].current(1)
        self.block_widget_dict[self.num_reforms][1].place(relx = self.block_2_entry_1_1_x, 
                        rely = (self.block_2_entry_1_1_y+
                                (self.num_reforms-1)*(self.entry_entry_gap_y)), anchor = "w", width=300)
        self.block_widget_dict[self.num_reforms][1].bind("<<ComboboxSelected>>", self.show_policy_selection)

        self.block_widget_dict[self.num_reforms][2] = Entry(width=6, font=self.fontStyle)
        self.block_widget_dict[self.num_reforms][2].place(relx = self.block_2_entry_1_2_x,
                                                          rely = (self.block_2_entry_1_1_y+
                                (self.num_reforms-1)*(self.entry_entry_gap_y)), anchor = "w")

        self.block_widget_dict[self.num_reforms][3] = Entry(width=14, font=self.fontStyle)
        self.block_widget_dict[self.num_reforms][3].place(relx = self.block_2_entry_1_3_x,
                                                          rely = (self.block_2_entry_1_1_y+
                                (self.num_reforms-1)*(self.entry_entry_gap_y)), anchor = "w")
        self.num_reforms += 1
        self.button_2_pos_y = (self.block_2_entry_1_1_y+(self.num_reforms-1)*(self.entry_entry_gap_y))+self.entry_button_gap        
        self.button_generate_revenue_policy.place(relx = self.button_1_pos_x,
                                            rely = self.button_2_pos_y, anchor = "w")

    def popup_window(self):
        window = tk.Toplevel()

        label = tk.Label(window, text="Hello World!")
        label.pack(fill='x', padx=50, pady=5)

        button_close = tk.Button(window, text="Close", style='my.TButton', command=window.destroy)
        button_close.pack(fill='x')

    def popup_showinfo(self):
        showinfo("ShowInfo", "Hello World!")
        
    def generate_total_revenues(self):
        
        #global total_revenue_text1
        #global reform_revenue_text1
        #global selected_year
        
        self.selected_year=2019
        # create Records object containing pit.csv and pit_weights.csv input data
        recs = Records(data=self.data_filename, weights=self.weights_filename, gfactors=GrowFactors(growfactors_filename=self.growfactors_filename))
        
        grecs = GSTRecords()
        
        #print(data_filename)
        #print(weights_filename)
        # create CorpRecords object using cross-section data
        crecs1 = CorpRecords()
        # Note: weights argument is optional
        assert isinstance(crecs1, CorpRecords)
        assert crecs1.current_year == 2017
        
        # create Policy object containing current-law policy
        #policy_filename = 'current_law_policy_poland.json'
        pol = Policy(DEFAULTS_FILENAME=self.policy_filename)
        
        # specify Calculator objects for current-law policy
        calc1 = Calculator(policy=pol, records=recs, corprecords=crecs1,
                           gstrecords=grecs, verbose=False)
        
        # NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
        #       so we can continue to use pol and recs in this script without any
        #       concern about side effects from Calculator method calls on calc1.
        
        assert isinstance(calc1, Calculator)
        assert calc1.current_year == 2017
        
        np.seterr(divide='ignore', invalid='ignore')

        # popup window for the Results
        window = tk.Toplevel()
        window.geometry("600x500+140+140")
        label = tk.Label(window, text="Results")
        label.place(relx = 0.50, rely = 0.05)
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)        
        button_close = ttk.Button(window, text="Close", style='my.TButton', command=window.destroy)
        button_close.place(relx = 0.50, rely = 0.90)
        
                
        calc1.advance_to_year(self.selected_year)    
        # Produce DataFrame of results using cross-section
        calc1.calc_all()
        weighted_pitax1 = calc1.weighted_total('pitax')
        pitax_collection1 = weighted_pitax1.sum()
        
        pitax_collection_billions1 = pitax_collection1/10**9
        
        pitax_collection_str1 = '{0:.2f}'.format(pitax_collection_billions1)
        
        print('\n\n\n')
        print('TAX COLLECTION FOR THE YEAR - 2017\n')
        
        print("The PIT Collection in billions is: ", pitax_collection_billions1)
        
        total_revenue_text=""

        total_revenue_text = "TAX COLLECTION FOR THE YEAR - " + str(self.selected_year)+" : "+str(pitax_collection_str1)+" bill "
        revenue_label = Label(window, text=total_revenue_text, font=self.fontStyle)
        revenue_label.place(relx = 0.05, rely = 0.20, anchor = "w")        
        #revenue_label.config(window, text=total_revenue_text)
        
        """
        df_sector = dumpdf_1.groupby(['sector']).sum()
        df_sector['citax_millions'] = df_sector['citax']/14**6
        
        df_province = dumpdf_1.groupby(['province']).sum()
        df_province['citax_millions'] = df_province['citax']/14**6
        
        df_small_business = dumpdf_1.groupby(['small_business']).sum()
        df_small_business['citax_millions'] = df_small_business['citax']/14**6
        
        cmap = plt.cm.tab10
        colors = cmap(np.arange(len(df_sector)) % cmap.N)
        
        ax = df_sector.plot(kind='bar', use_index=True, y='citax_millions', 
                            legend=False, rot=90,
                            figsize=(8,8), color=colors)
        
        ax.set_ylabel('CIT in million ')
        ax.set_xlabel('')
        ax.set_title(' CIT collection by sector (2017)', fontweight="bold")
        pic_filename1 = 'CIT Collection 2017.png' 
        plt.savefig(pic_filename1)
        """
        
        """
        img2 = ImageTk.PhotoImage(Image.open(pic_filename1))
        pic.configure(image=img2)
        pic.image = img2
        """
        
        pic_filename1 = 'world_bank.png'
        # Show Image
        img1 = Image.open(pic_filename1)
        img2 = img1.resize((500, 500), Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(img2)
        self.pic.configure(image=img3)
        self.pic.image = img3
        
        
        """
        plt.show()
        
        cmap = plt.cm.tab14
        colors = cmap(np.arange(len(df_province)) % cmap.N)
        
        ax = df_province.plot(kind='bar', use_index=True, y='citax_millions', 
                            legend=False, rot=90,
                            figsize=(8,8), color=colors)
        ax.set_ylabel('CIT in million ')
        ax.set_xlabel('')
        ax.set_title(' CIT collection by Province (2017)', fontweight="bold")
        plt.show()
        
        cmap = plt.cm.tab14
        colors = cmap(np.arange(len(df_province)) % cmap.N)
        
        ax = df_small_business.plot(kind='bar', use_index=True, y='citax_millions', 
                            legend=False, rot=90,
                            figsize=(8,8), color=colors)
        ax.set_ylabel('CIT in million ')
        ax.set_xlabel('')
        ax.set_title(' CIT collection by Type of Business (2017)', fontweight="bold")
        plt.show()
        """
        
    def read_reform_dict(self, block_selected_dict):
        years=[]
        for k in block_selected_dict.keys():
            if (block_selected_dict[k]['selected_year'] not in years):
                years = years + [block_selected_dict[k]['selected_year']]
        ref = {}
        ref['policy']={}
        for year in years:
            policy_dict = {}
            for k in block_selected_dict.keys():
                if block_selected_dict[k]['selected_year']==year:
                    policy_dict['_'+block_selected_dict[k]['selected_item']]=[float(block_selected_dict[k]['selected_value'])]
            ref['policy'][int(year)] = policy_dict
        years.sort()
        years = [int(x) for x in years]
        return years, ref
    
    def apply_policy_change(self):
        
        for num in range(1, self.num_reforms):
            self.block_selected_dict[num]['selected_item']= self.block_widget_dict[num][1].get()
            self.block_selected_dict[num]['selected_value']= self.block_widget_dict[num][3].get()
            self.block_selected_dict[num]['selected_year']= self.block_widget_dict[num][2].get()
        
        #print(self.block_selected_dict)
        # create Records object containing pit.csv and pit_weights.csv input data
        recs = Records()
        
        grecs = GSTRecords()
        
        print("data_filename: ", self.data_filename)
        print("weights_filename: ", self.weights_filename)
        # create CorpRecords object using cross-section data
        crecs1 = CorpRecords(data=self.data_filename, weights=self.weights_filename)
        # Note: weights argument is optional
        assert isinstance(crecs1, CorpRecords)
        assert crecs1.current_year == 2017
        
        # create Policy object containing current-law policy
        pol = Policy(DEFAULTS_FILENAME=self.policy_filename)
        
        # specify Calculator objects for current-law policy
        calc1 = Calculator(policy=pol, records=recs, corprecords=crecs1,
                           gstrecords=grecs, verbose=False)
        assert isinstance(calc1, Calculator)
        assert calc1.current_year == 2017

        np.seterr(divide='ignore', invalid='ignore')
        
        pol2 = Policy(DEFAULTS_FILENAME=self.policy_filename)
        
        years, self.reform=self.read_reform_dict(self.block_selected_dict)
        print("reform dictionary: ",self.reform) 
        #reform = Calculator.read_json_param_objects('app01_reform.json', None)
        pol2.implement_reform(self.reform['policy'])
        
        calc2 = Calculator(policy=pol2, records=recs, corprecords=crecs1,
                           gstrecords=grecs, verbose=False)
        # popup window for the Results
        window = tk.Toplevel()
        window.geometry("600x500+140+140")
        label = tk.Label(window, text="Results", font=self.fontStyle)
        label.place(relx = 0.05, rely = 0.14)
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)         
        button_close = ttk.Button(window, text="Close", style='my.TButton', command=window.destroy)
        button_close.place(relx = 0.50, rely = 0.90)
        

        
        total_revenue_text={}
        reform_revenue_text={}
        revenue_dict={}
        revenue_amount_dict = {}
        num = 1
        #for year in range(years[0], years[-1]+1):            
        for year in range(2019, 2024):  
            calc1.advance_to_year(year)        
            calc2.advance_to_year(year)
            # NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
            #       so we can continue to use pol and recs in this script without any
            #       concern about side effects from Calculator method calls on calc1.
    
            # Produce DataFrame of results using cross-section
            calc1.calc_all()
            weighted_pitax1 = calc1.weighted_total('pitax')
                    
            pitax_collection_billions1 = weighted_pitax1/10**9
            
            pitax_collection_str1 = '{0:.2f}'.format(pitax_collection_billions1)
            
            print('\n\n\n')
            print('TAX COLLECTION FOR THE YEAR - 2017\n')
            
            print("The PIT Collection in billions is: ", pitax_collection_billions1)
            
            total_revenue_text[year] = "TAX COLLECTION UNDER CURRENT LAW FOR THE YEAR - " + str(year)+" : "+str(pitax_collection_str1)+" bill"
            #self.l6.config(text=total_revenue_text1)
            #self.l6.place(relx = 0.1, rely = 0.7+(num-1)*0.1, anchor = "w")
            # Produce DataFrame of results using cross-section
            calc2.calc_all()
            
            weighted_pitax2 = calc2.weighted_total('pitax')
            
            pitax_collection_billions2 = weighted_pitax2/10**9
            
            pitax_collection_str2 = '{0:.2f}'.format(pitax_collection_billions2)
            
            print('\n\n\n')
            print('TAX COLLECTION FOR THE YEAR UNDER REFORM - 2017\n')
            
            print("The PIT Collection in billions is: ", pitax_collection_billions2)
            
            reform_revenue_text[year] = "TAX COLLECTION UNDER REFORM FOR THE YEAR - " + str(year)+"           : "+str(pitax_collection_str2)+" bill "
                  

            revenue_dict[year]={}
            revenue_amount_dict[year]={}
            revenue_dict[year]['current_law']={}
            revenue_amount_dict[year]['current_law']={}
            revenue_dict[year]['current_law']['Label'] = Label(window, text=total_revenue_text[year], font=self.fontStyle)
            revenue_dict[year]['current_law']['Label'].place(relx = 0.05, rely = 0.1+(num-1)*0.15, anchor = "w")
            revenue_amount_dict[year]['current_law']['amount'] = pitax_collection_str1
            #self.l6=Label(text=self.total_revenue_text1)
            #self.l6.place(relx = 0.4, rely = 0.1, anchor = "w")
            revenue_dict[year]['reform']={}
            revenue_amount_dict[year]['reform']={}         
            revenue_dict[year]['reform']['Label'] = Label(window, text=reform_revenue_text[year], font=self.fontStyle)
            revenue_dict[year]['reform']['Label'].place(relx = 0.05, rely = 0.15+(num-1)*0.15, anchor = "w")            
            revenue_amount_dict[year]['reform']['amount'] = pitax_collection_str2
            #self.l7=Label(text=self.reform_revenue_text1)
            #self.l7.place(relx = 0.4, rely = 0.15, anchor = "w")        
            num += 1
        
        #print(revenue_amount_dict)
        df_revenue_proj = pd.DataFrame(revenue_amount_dict)
        df_revenue_proj = df_revenue_proj.T
        df_revenue_proj['Current Law'] = df_revenue_proj['current_law'].apply(pd.Series)
        df_revenue_proj['Reform'] = df_revenue_proj['reform'].apply(pd.Series)
        df_revenue_proj = df_revenue_proj.drop(['current_law', 'reform'], axis=1)
        df_revenue_proj['Current Law'] = pd.to_numeric(df_revenue_proj['Current Law'])
        df_revenue_proj['Reform'] = pd.to_numeric(df_revenue_proj['Reform'])
        print("Revenues\n", df_revenue_proj)
        ax = df_revenue_proj.plot(y=["Current Law", "Reform"], kind="bar", rot=0,
                            figsize=(8,8))
        ax.set_ylabel('(billion )')
        ax.set_xlabel('')
        ax.set_title('CIT Revenue - Current Law vs. Reforms', fontweight="bold")
        pic_filename2 = 'PIT - Current Law and Reforms.png'
        plt.savefig(pic_filename2)
        
        img1 = Image.open(pic_filename2)
        img2 = img1.resize((500, 500), Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(img2)
        self.pic.configure(image=img3)
        self.pic.image = img3

    def generate_tax_expenditures(self):
        
        # create Records object containing pit.csv and pit_weights.csv input data
        recs = Records()
        
        grecs = GSTRecords()
        
        crecs1 = CorpRecords(data=self.data_filename, weights=self.weights_filename)
        # Note: weights argument is optional
        assert isinstance(crecs1, CorpRecords)
        assert crecs1.current_year == 2017
        
        # create Policy object containing current-law policy
        pol = Policy()
        
        # specify Calculator objects for current-law policy
        calc1 = Calculator(policy=pol, records=recs, corprecords=crecs1,
                           gstrecords=grecs, verbose=False)
        assert isinstance(calc1, Calculator)
        assert calc1.current_year == 2017

        np.seterr(divide='ignore', invalid='ignore')

        # Produce DataFrame of results using cross-section
        calc1.calc_all()
        #sector=calc1.carray('sector')
        weight = calc1.carray('weight')
        
        dump_vars = ['CIT_ID_NO', 'legal_form', 'sector', 'province', 'small_business', 
                     'revenue', 'expenditure', 'income', 'tax_base_before_deductions', 
                     'deductions_from_tax_base',
                     'income_tax_base_after_deductions', 'citax']
        dumpdf = calc1.dataframe_cit(dump_vars)
        #create the weight variable
        dumpdf['weight']= weight
        dumpdf= dumpdf.rename(columns={'citax':"tax_collected_under_current_policy"})
        dumpdf['weighted_tax_collected_under_current_policy']= dumpdf['weight']*dumpdf['tax_collected_under_current_policy']
        dumpdf['ID_NO']= "A"+ dumpdf['CIT_ID_NO'].astype('str') 
        benchmark = Calculator.read_json_param_objects(self.benchmark_filename, None)
        base_year = list(benchmark['policy'].keys())[0]
        #reform = dict(benchmark)
        reform = copy.deepcopy(benchmark)
        with open('taxcalc/'+self.policy_filename) as f:
            current_law_policy = json.load(f)             
        ref_dict = benchmark['policy']
        var_list = []
        tax_expediture_list = []
        tax_expediture_list_polish = []
        for pkey, sdict in ref_dict.items():
                for k, s in sdict.items():
                    reform.pop("policy")
                    mydict={}
                    mydict[k]=s
                    mydict0={}
                    mydict0[pkey]=mydict
                    reform['policy']=mydict0            
                    pol2 = Policy()
                    pol2.implement_reform(reform['policy'])
                    calc2 = Calculator(policy=pol2, records=recs, corprecords=crecs1,
                                       gstrecords=grecs, verbose=False)
                    calc2.calc_all()
                    weight2 = calc2.carray('weight')                   
                    dump_vars = ['CIT_ID_NO', 'citax']     
                    dumpdf_2 = calc2.dataframe_cit(dump_vars)
                    dumpdf_2['weight']= weight2
                    dumpdf_2['ID_NO']= "A"+ dumpdf_2['CIT_ID_NO'].astype('int').astype('str')
                    dumpdf_2 = dumpdf_2.rename(columns={'citax':"tax_collected_under_benchmark"+ k})
                    dumpdf_2['weighted_tax_collected_under_benchmark'+ k]= dumpdf_2['weight']*dumpdf_2['tax_collected_under_benchmark'+ k]
                    dumpdf = pd.merge(dumpdf, dumpdf_2, how="inner", on="ID_NO")
                    #calculating expenditure
                    dumpdf['tax_expenditure_'+current_law_policy[k]['description']]= (dumpdf["weighted_tax_collected_under_benchmark"+ k]- dumpdf['weighted_tax_collected_under_current_policy'])/10**6
                    dumpdf['tax_expenditure_'+current_law_policy[k]['long_name']]= (dumpdf["weighted_tax_collected_under_benchmark"+ k]- dumpdf['weighted_tax_collected_under_current_policy'])/10**6            
                    var_list = var_list + [k]
                    tax_expediture_list = tax_expediture_list + ['tax_expenditure_'+current_law_policy[k]['description']]
                    tax_expediture_list_polish = tax_expediture_list_polish + ['tax_expenditure_'+current_law_policy[k]['long_name']]
                    
        #Summarize here
        tax_expenditure_df = dumpdf[tax_expediture_list].sum(axis = 0)
        tax_expenditure_df= tax_expenditure_df.reset_index()
        tax_expenditure_df.columns = ['Tax Expenditure', 'Million ']
        tax_expenditure_df.to_csv('tax_expenditures_sum.csv',index=False, float_format='%.0f')
        print("Tax Expenditures\n", tax_expenditure_df)
        tax_expenditure_df = dumpdf[tax_expediture_list_polish].sum(axis = 0)
        tax_expenditure_df= tax_expenditure_df.reset_index()
        tax_expenditure_df.columns = ['Wydatki Podatkowe', 'Milion ']
        tax_expenditure_df.to_csv('tax_expenditures_sum_polish.csv', encoding='utf-8', index=False, float_format='%.0f')
        tax_expenditure_df.to_csv('tax_expenditures_sum_polish.txt', encoding='utf-8', sep=',', index=False)       
                
        # This is the Overall Tax Expenditures
        pol3 = Policy()
        reform = Calculator.read_json_param_objects(self.benchmark_filename, None)
        pol3.implement_reform(reform['policy'])
        
        calc2 = Calculator(policy=pol3, records=recs, corprecords=crecs1,
                           gstrecords=grecs, verbose=False)
        # popup window for the Results
        window = tk.Toplevel()
        window.geometry("700x600+140+140")
        label = tk.Label(window, text="Tax Expenditures", font=self.fontStyle_sub_title)
        label.place(relx = 0.40, rely = 0.02)
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.fontStyle)         
        button_close = ttk.Button(window, text="Close", style='my.TButton', command=window.destroy)
        button_close.place(relx = 0.50, rely = 0.90)
        
        total_revenue_text={}
        reform_revenue_text={}
        tax_expenditure_text = {}        
        revenue_dict={}
        revenue_amount_dict = {}
        tax_expenditure = {}
        num = 1
        #for year in range(years[0], years[-1]+1):            
        for year in range(2019, 2024):  
            calc1.advance_to_year(year)        
            calc2.advance_to_year(year)
            # NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
            #       so we can continue to use pol and recs in this script without any
            #       concern about side effects from Calculator method calls on calc1.
    
            # Produce DataFrame of results using cross-section
            calc1.calc_all()
            
            dump_vars = ['CIT_ID_NO', 'legal_form', 'sector', 'province', 'small_business', 'revenue', 'expenditure', 'income', 'tax_base_before_deductions', 'deductions_from_tax_base',
                         'income_tax_base_after_deductions', 'citax']
            dumpdf_1 = calc1.dataframe_cit(dump_vars)
            dumpdf_1.to_csv('app00_poland1.csv', index=False, float_format='%.0f')
            
            Business_Profit1 = calc1.carray('income')
            Tax_Free_Incomes1 = calc1.carray('tax_free_income_total')
            Tax_Base_Before_Deductions1 = calc1.carray('tax_base_before_deductions')
            Deductions1 = calc1.carray('deductions_from_tax_base')
            Tax_Base_After_Deductions1 = calc1.carray('income_tax_base_after_deductions')
            citax1 = calc1.carray('citax')
            weight1 = calc1.carray('weight')
            etr1 = np.divide(citax1, Business_Profit1)
            weighted_etr1 = etr1*weight1.values
            weighted_etr_overall1 = (sum(weighted_etr1[~np.isnan(weighted_etr1)])/
                                     sum(weight1.values[~np.isnan(weighted_etr1)]))
            
            wtd_citax1 = citax1 * weight1
            
            citax_collection1 = wtd_citax1.sum()
            
            citax_collection_billions1 = citax_collection1/10**9
            
            citax_collection_str1 = '{0:.2f}'.format(citax_collection_billions1)
            
            print('\n\n\n')
            print('TAX COLLECTION UNDER CURRENT LAW FOR THE YEAR - '+str(year)+': ', citax_collection_billions1)
            
            total_revenue_text[year] = "TAX COLLECTION UNDER CURRENT LAW FOR THE YEAR - " + str(year)+" : "+str(citax_collection_str1)+" bill "
            #self.l6.config(text=total_revenue_text1)
            #self.l6.place(relx = 0.1, rely = 0.7+(num-1)*0.1, anchor = "w")
            # Produce DataFrame of results using cross-section
            calc2.calc_all()
            
            dump_vars = ['CIT_ID_NO', 'legal_form', 'sector', 'province', 'small_business', 'revenue', 'expenditure', 'income', 'tax_base_before_deductions', 'deductions_from_tax_base',
                         'income_tax_base_after_deductions', 'citax']
            dumpdf_2 = calc2.dataframe_cit(dump_vars)
            dumpdf_2.to_csv('app00_poland2.csv', index=False, float_format='%.0f')
            
            Business_Profit2 = calc2.carray('income')
            Tax_Free_Incomes2 = calc2.carray('tax_free_income_total')
            Tax_Base_Before_Deductions2 = calc2.carray('tax_base_before_deductions')
            Deductions2 = calc2.carray('deductions_from_tax_base')
            Tax_Base_After_Deductions2 = calc2.carray('income_tax_base_after_deductions')
            citax2 = calc2.carray('citax')
            weight2 = calc2.carray('weight')
            etr2 = np.divide(citax2, Business_Profit2)
            weighted_etr2 = etr2*weight2.values
            weighted_etr_overall2 = (sum(weighted_etr2[~np.isnan(weighted_etr2)])/
                                     sum(weight2.values[~np.isnan(weighted_etr2)]))
            
            wtd_citax2 = citax2 * weight2
            
            citax_collection2 = wtd_citax2.sum()
            
            citax_collection_billions2 = citax_collection2/10**9
            citax_expenditure_billions = citax_collection_billions2 -  citax_collection_billions1
            citax_collection_str2 = '{0:.2f}'.format(citax_collection_billions2)
            
            citax_expenditure_billions_str = '{0:.5f}'.format(citax_expenditure_billions)
            
            print('\n\n\n')
            print('TAX COLLECTION UNDER BENCHMARK POLICY FOR THE YEAR - '+str(year)+': ', citax_collection_billions2)
                 
            revenue_amount_dict[year]={}
            revenue_amount_dict[year]['current_law']={}            
            revenue_amount_dict[year]['current_law']['amount'] = citax_collection_billions1
            revenue_amount_dict[year]['benchmark']={}
            revenue_amount_dict[year]['benchmark']={}
            revenue_amount_dict[year]['benchmark']['amount'] = citax_collection_billions2
            
            revenue_amount_dict[year]['tax_expenditure']={}
            revenue_amount_dict[year]['tax_expenditure']={}                     
            revenue_amount_dict[year]['tax_expenditure']['amount'] = citax_expenditure_billions    
            
            reform_revenue_text[year] = "TAX COLLECTION UNDER BENCHMARK FOR THE YEAR - " + str(year)+" : "+str(citax_collection_str2)+" bill "

            tax_expenditure_text[year] = "TAX EXPENDITURES FOR THE YEAR - " + str(year)+" : "+citax_expenditure_billions_str+" bill "
            
            revenue_dict[year]={}
            revenue_dict[year]['current_law'] = {}
            revenue_dict[year]['current_law']['Label'] = Label(window, text=total_revenue_text[year], font=self.fontStyle)
            revenue_dict[year]['current_law']['Label'].place(relx = 0.05, rely = 0.1+(num-1)*0.2, anchor = "w") 
            revenue_dict[year]['benchmark'] = {}
            revenue_dict[year]['benchmark']['Label'] = Label(window, text=reform_revenue_text[year], font=self.fontStyle)
            revenue_dict[year]['benchmark']['Label'].place(relx = 0.05, rely = 0.13+(num-1)*0.2, anchor = "w") 
            revenue_dict[year]['tax_expenditure'] = {}
            revenue_dict[year]['tax_expenditure']['Label'] = Label(window, text=tax_expenditure_text[year], font=self.fontStyle)
            revenue_dict[year]['tax_expenditure']['Label'].place(relx = 0.05, rely = 0.16+(num-1)*0.2, anchor = "w")            
            num += 1
        
        #print(revenue_amount_dict)
        df_revenue_proj = pd.DataFrame(revenue_amount_dict)
        df_revenue_proj = df_revenue_proj.T
        df_revenue_proj['Current Law'] = df_revenue_proj['current_law'].apply(pd.Series)
        df_revenue_proj['Benchmark'] = df_revenue_proj['benchmark'].apply(pd.Series)
        df_revenue_proj = df_revenue_proj.drop(['current_law', 'benchmark'], axis=1)
        df_revenue_proj['Current Law'] = pd.to_numeric(df_revenue_proj['Current Law'])
        df_revenue_proj['Benchmark'] = pd.to_numeric(df_revenue_proj['Benchmark'])
        print("Revenue Projections2\n", df_revenue_proj)
        ax = df_revenue_proj.plot(y=["Current Law", "Benchmark"], kind="bar", rot=0,
                            figsize=(8,8))
        ax.set_ylabel('(billion )')
        ax.set_xlabel('')
        ax.set_title('CIT - Tax Collection under Current Law vs. Benchmark', fontweight="bold")
        pic_filename3 = 'CIT - Current Law and Benchmark.png'
        plt.savefig(pic_filename3)
        
        img1 = Image.open(pic_filename3)
        img2 = img1.resize((500, 500), Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(img2)
        self.pic.configure(image=img3)
        self.pic.image = img3
    
    
    def newselection1(self, event):
        print('selected1:', event.widget.get())
    
    def newselection2(self, event):
        print('selected2:', event.widget.get())
    
    def input_data_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file')
        #self.master.update()
        #filename_path = tk.splitlist(filez)[0]
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.data_filename = filename_list[-1]
        self.entry_data_filename.delete(0,END)
        self.entry_data_filename.insert(0,self.data_filename)
    
    def input_weights_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file')
        #print(filez[0])
        #self.master.update()        
        #filename_path = tk.splitlist(filez)[0]
        #filename_list = filename_path.split('/')
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.weights_filename = filename_list[-1]
        self.entry_weights_filename.delete(0,END)
        self.entry_weights_filename.insert(0,self.weights_filename)
    
    def input_policy_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file') 
        #self.master.update()
        #filename_path = tk.splitlist(filez)[0]
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.policy_filename = filename_list[-1]
        self.entry_policy_filename.delete(0,END)
        self.entry_policy_filename.insert(0,self.policy_filename)

    def input_benchmark_filename(self):
        filez = filedialog.askopenfilenames(title='Choose a file') 
        #self.master.update()
        #filename_path = tk.splitlist(filez)[0]
        filename_path = filez[0]
        filename_list = filename_path.split('/')
        self.benchmark_filename = filename_list[-1]
        self.entry_benchmark_filename.delete(0,END)
        self.entry_benchmark_filename.insert(0,self.benchmark_filename)
               
    
    def policy_options(self):
        self.sub_directory
        self.policy_filename
        with open(self.sub_directory+'/'+self.policy_filename) as f:
            current_law_policy = json.load(f)
        current_law_policy_sorted = dict(sorted(current_law_policy.items()))    
        policy_options_list = []
        for k, s in current_law_policy_sorted.items():
            #print(k)
            #print(current_law_policy[k]['description'])
            #policy_option_list = policy_option_list + [current_law_policy[k]['description']]
            policy_options_list = policy_options_list + [k[1:]]
        return (current_law_policy, policy_options_list)
    
    def policy_reform():
        self.reform={}
        self.reform['policy']={}
        self.reform['policy']['_'+self.selected_item]={}
        self.updated_year = self.block_widget_dict[1][2].get()
        self.updated_value = self.block_widget_dict[1][3].get()
        self.reform['policy']['_'+selected_item][self.updated_year]=[self.updated_value]
        print("Reform2: ", self.reform)
    
        
    def show_policy_selection(self, event):
        active_widget_number = int(str(event.widget)[1:])
        print("active_widget_number: ", active_widget_number)
        num = active_widget_number
        #for num in range(1, self.num_reforms):
        self.selected_item = self.block_widget_dict[num][1].get()
        self.selected_value = self.current_law_policy['_'+ self.selected_item]['value'][0]
        self.selected_year = self.current_law_policy['_'+ self.selected_item]['row_label'][0]
        self.block_selected_dict[num]['selected_item']= self.block_widget_dict[num][1].get()
        self.block_selected_dict[num]['selected_value']= self.current_law_policy['_'+ self.selected_item]['value'][0]
        self.block_selected_dict[num]['selected_year']= self.current_law_policy['_'+ self.selected_item]['row_label'][0]
        
        self.block_widget_dict[num][3].delete(0, END)
        self.block_widget_dict[num][3].insert(END, self.selected_value)
        self.block_widget_dict[num][2].delete(0, END)
        self.block_widget_dict[num][2].insert(END, self.selected_year)

        for num in range(1, self.num_reforms):        
            self.block_selected_dict[num]['selected_value']= self.block_widget_dict[num][3].get()
            self.block_selected_dict[num]['selected_year']= self.block_widget_dict[num][2].get()
        
        #print(self.block_selected_dict)
        return
    # --- main ---
    
 
def main():
    root = tk.Tk()
    root.geometry('1000x600')
    app = Application(root)
    app.mainloop()


if __name__ == '__main__':
    main()
    #main()

    
    
"""
    
    #button(row=6, column=1, sticky = W, pady = (0,25), padx = (0,0))
    root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.master.title("Sample application")
    app.mainloop()
    
 """   
