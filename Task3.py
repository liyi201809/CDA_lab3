# -*- coding: utf-8 -*-
from loaddata import load_data 
from loaddata import host_ip
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import pyplot
#%% load two features from infected host relecant flows
dataset1 = load_data('C:/Users/YI/Desktop/TUD/Cyber data analytics/LAB3/Sampling/capture20110818.pcap.netflow.labeled')
host_address = host_ip(dataset1)

#%
def load_feature_data(df, host_ip):
    
    def filter_ip(row):
        if row['src_ip'] == host_ip:
            return row['dst_ip']
        else:
            return row['src_ip']
    
    feature1 = 'Prot'
    feature2 = 'Packets'    
    # Filter out rows without host_ip
    df = df[['src_ip', 'dst_ip', feature1, feature2]]
    df = df[(df['src_ip'] == host_ip) | (df['dst_ip'] == host_ip)]
    
    return df[feature1].tolist(), df[feature2].tolist()


feature1, feature2 = load_feature_data(dataset1, '147.32.84.170')

#%% visualize the first feature ---categorical
names1 = np.unique(feature1).tolist()
count = [0,0,0]

f1 = []
for i in range(len(feature1)):
    if feature1[i] == 'ICMP':
        f1.append(0)
        count[0]+=1
    elif feature1[i] == 'TCP':
        f1.append(1)
        count[1]+=1
    elif feature1[i] == 'UDP':
        f1.append(2)
        count[2]+=1
    else:
        f1.append(3)
        

plt.bar(names1, count, align='center', alpha=0.5)
plt.title('Port feature of scenario 10')

#%% visualize the second feature --- sequential
plt.subplot(1, 2, 1)
np.unique(feature2)
plt.plot(feature2)
plt.title('Packets feature of scenario 10')
plt.xlabel('values')
plt.ylabel('occurrence')

#% histogram 
plt.subplot(1, 2, 2)
x = np.array(feature2)
plt.hist(x, range=[0, 50], density=True, bins=50)
plt.title('Histogram of Packets feature of scenario 10')
plt.xlabel('values')
plt.ylabel('percentage')
plt.show()

#%% attribute mapping for discretization 

# discretize the second feature
f2 = []
count2 = [0,0,0,0,0]
for i in range(len(feature2)):
    if feature2[i]==1:
        f2.append(1)
        count2[0]+=1
    elif feature2[i]>1 and feature2[i]<=3:
        f2.append(2)
        count2[1]+=1
    elif feature2[i]>3 and feature2[i]<=5:
        f2.append(3)
        count2[2]+=1
    elif feature2[i]>5 and feature2[i]<=10:
        f2.append(4)
        count2[3]+=1
    else:
        f2.append(0)
        count2[4]+=1
#%% combine the two features
dis_value = []
code = 0
spacesize = 3*5
for i in range(len(f1)):
    code = (f1[i] * spacesize / 3) + (f2[i] * spacesize / 3 / 5) 
    dis_value.append(code)

plt.plot(dis_value)