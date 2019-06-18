# -StartPython.py *- coding: utf-8 -*-
from loaddata import load_data 
from loaddata import load_ip_sequence
import json
#%%
dataset = load_data('C:/Users/YI/Desktop/TUD/Cyber data analytics/LAB3/Sampling/capture20110811.pcap.netflow.labeled')
#%%
ip_data = load_ip_sequence(dataset,'147.32.84.229')