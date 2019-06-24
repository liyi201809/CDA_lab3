# -StartPython.py *- coding: utf-8 -*-
from loaddata import load_data 
from loaddata import load_ip_sequence

dataset = load_data('C:/Users/YI/Desktop/TUD/Cyber data analytics/LAB3/Sampling/capture20110811.pcap.netflow.labeled')
ip_data = load_ip_sequence(dataset,'147.32.84.229')
#%%
def top10freq(lst):
    from collections import Counter
    d = {}
    for i in lst:
        if d.get(i):
            d[i] += 1
        else:
            d[i] = 1
    occurence = dict(Counter(d).most_common(10))        
    frequency = occurence
    for i in frequency:
        frequency[i] = occurence[i]/len(lst)
    return frequency
#
def reservoir_sampling(stream, k): 
    import random 
    i=0;  
    n = len(stream)
    reservoir = [0]*k; 
    for i in range(k): 
        reservoir[i] = stream[i]; 
    # Iterate from the (k+1)th 
    while(i < n):  
        j = random.randrange(i+1);     
        # then replace the element with new element from stream 
        if(j < k): 
            reservoir[j] = stream[i]; 
        i+=1;  
    return reservoir
#%%
freq_data = top10freq(ip_data)

# try different sizes    
sampled_data1 = reservoir_sampling(ip_data,30000)
freq_data1 = top10freq(sampled_data1)
sampled_data2 = reservoir_sampling(ip_data,100000)
freq_data2 = top10freq(sampled_data2)
sampled_data3 = reservoir_sampling(ip_data,500000)
freq_data3 = top10freq(sampled_data3)
sampled_data4 = reservoir_sampling(ip_data,1000000)
freq_data4 = top10freq(sampled_data4)
sampled_data5 = reservoir_sampling(ip_data,2000000)
freq_data5 = top10freq(sampled_data5)

#%% CMS
import time
start_time = time.time()             # count the compute time           
from probables import (CountMinSketch)
cms = CountMinSketch(width=500, depth=100)
cms.clear
for i in ip_data:
    cms.add(i)
time_spend = time.time() - start_time
#
cms.error_rate
cms.elements_added

