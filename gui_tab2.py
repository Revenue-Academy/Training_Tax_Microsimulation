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
from super_combo import super_combo
#from taxcalc import *

from PIL import Image,ImageTk
   
def tab2(self, tax_type):
    self.year_value_pairs_policy_dict = 1
    self.vars[tax_type+'_display_revenue_table'] = 1
    self.save_inputs()
    self.tab_generate_revenue_policy = super_combo(self.TAB2, self.current_law_policy, 'row_label', 'value', 0.01, 0.20, editable_field_year=1, num_combos=1)
    (self.button_generate_revenue_policy, self.block_widget_dict) = self.tab_generate_revenue_policy.display_widgets(self.TAB2)
    self.button_generate_revenue_policy.configure(command=self.clicked_generate_policy_revenues)
      
    return
