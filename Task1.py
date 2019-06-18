# -StartPython.py *- coding: utf-8 -*-
from loaddata import load_data 
import json

dataset = load_data('C:/Users/YI/Desktop/TUD/Cyber data analytics/LAB3/Sampling/capture20110811.pcap.netflow.labeled')

#with open('botnet-capture-20110819-bot.json', 'r',encoding="utf8", errors='ignore') as csvDataFile:
#    csvReader = json.load(csvDataFile)