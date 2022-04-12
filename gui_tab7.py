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

def tab7(self):
    self.year_value_pairs_growfactors_dict = len(self.growfactors[list(self.growfactors.keys())[0]]['Year'])
    self.tab_growfactors = super_combo(self.TAB7, self.growfactors, 'Year', 'Value', 0.03, 0.20)
    (self.button_growfactors, self.growfactors_widget_dict) = self.tab_growfactors.display_widgets(self.TAB7)
    self.button_growfactors.configure(command=self.clicked_generate_policy_revenues)
    return
     