#automated report generator from the trimatrix device.
import pandas as pd
import re
import sys
import os
import pathlib
import matplotlib.pyplot as plt
import random
import matplotlib.patches as mpatches

# read the csv file
file_name = sys.argv[1]
data_1 = pd.read_csv(file_name, encoding='utf-8')
#filter the unrequired columns from the data
l= data_1.filter(regex='unit').columns.tolist()
l.extend(['Spectrum ID','Date and Time','Measurement Description','Corporate Account','Application Product Code','Campaign Name'])
#try to remove date and time and instead used measurement ID
data_1 = data_1.drop(columns=l)
#bifurcation of samples and then their devices
s1 = set(data_1['Device'])
s2 = set(data_1['Sample ID'])
l1 = [*s1,]
l2 = [*s2,]
def plot_save(df,t1,x,y):
    cl = df.filter(regex ='^[0-9]').columns.tolist()
    df = df[cl].transpose()
    d_plot = df.plot(figsize =(16,8),title = t1 ,xlabel = x,ylabel = y)
    fig_d_plot = d_plot.get_figure()
    # directory to save file
    d1  = 'C:\\Users\\Admin\\Desktop\\samples_report\\'
    d2 = file_name[:-4].split('\\')[-1]
    pathlib.Path(d1+d2).mkdir(parents=True,exist_ok=True)
    dirt = d1+d2+t1+'.png'
    fig_d_plot.savefig(dirt)

for i in range(len(l1)):
    # collecting data per device for commodity and taking only the wavelength columns for plot
    # data_c_2_1_5 is for 5 csv of each scan
    # data_2 is for the device specific 
    data_2 = data_1[(data_1['Device'] == str(l1[i]))]
    s3 = set(data_2['Measurement ID'])
    l3 = [*s3,]
    data_c_2_1_5 = data_2[data_2['Measurement ID']==l3[0]]
    
    # xaxis and y axix
    x_ax = data_2.iat[0,4]
    y_ax = data_2.iat[0,5]
    
    #to plot data_c_2_1_5
    plot_save(df = data_c_2_1_5,x = x_ax, y = y_ax,t1 =  '\\5 spectra plot of 1 %s sample in device ID %s'% (data_1['Sample'][0],l1[i]))
       
    # data_c_mean is for mean of each 
    data_c_mean = pd.DataFrame(columns = data_2.columns)
    for j in l3:
        d_1 = data_2[data_2['Measurement ID']==j]
        d_2 = d_1.filter(regex = '^[A-Za-z]').iloc[0].to_dict()
        d_3 = d_1.filter(regex = '^[0-9]').mean().to_dict()
        d_2.update(d_3)
        data_c_mean = data_c_mean.append(d_2,ignore_index = True)
        
    plot_save(df = data_c_mean,x = x_ax, y = y_ax,t1 =  '\\mean spectra plot of each scan of %s sample in device ID %s'% (data_1['Sample'][0],l1[i]))   

for i in range(len(l1)):
    data_2 = data_1[(data_1['Device'] == str(l1[i]))]
    s3 = set(data_2['Measurement ID'])
    l3 = [*s3,]
    fig = plt.figure(figsize = (16,8))
    ax = fig.add_subplot(1,1,1)
    for j in l3:
        d_1 = data_2[data_2['Measurement ID']==j]
        d_1 = d_1.filter(regex = '^[0-9]')
        clr = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        for k in range(d_1.shape[0]):
            d_1.iloc[k][1:].plot.line(ax=ax,color=clr,label = str(j))
    fig_d_plot = fig.get_figure()
    # directory to save file
    d1  = 'C:\\Users\\Admin\\Desktop\\samples_report\\'
    d2 = file_name[:-4].split('\\')[-1]
    pathlib.Path(d1+d2).mkdir(parents=True,exist_ok=True)
    dirt = d1+d2+'\\1 color for each scan for device %s'%(l1[i])+'.png'
    fig_d_plot.savefig(dirt)


data_1_t = data_1.filter(regex = '^[0-9]|^Device')
fig = plt.figure(figsize = (16,8))
ax = fig.add_subplot(1,1,1)
for i in range(data_1_t.shape[0]):
    if(data_1_t.iloc[i][0]==l1[0]):
        data_1_t.iloc[i][1:].plot.line(ax=ax,color='red',label = str(l1[0]))
    else:
        data_1_t.iloc[i][1:].plot.line(ax=ax,color='green',label = str(l1[1]))

red_patch = mpatches.Patch(color='red', label=l1[0])
blue_patch = mpatches.Patch(color='green', label=l1[1])
ax.legend(handles=[red_patch, blue_patch])
fig_d_plot = fig.get_figure()
# directory to save file
d1  = 'C:\\Users\\Admin\\Desktop\\samples_report\\'
d2 = file_name[:-4].split('\\')[-1]
dirt = d1+d2+'\\d1 and d2'+'.png'
fig_d_plot.savefig(dirt)