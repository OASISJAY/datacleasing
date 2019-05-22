'''
COMP9321 Assignment One Code Template 2019T1
Name: Shuai JI
Student ID: z5189630
'''
import csv
import sys
import os.path
import pandas as pd
import re
import matplotlib
import matplotlib.pyplot as plt

def remove_unknown(df):
    remove_value = ['Unknown','--']
    for col in list(df.columns.values):
        df = df.loc[~df[col].isin(remove_value)]
    return df

def title_style_with_exception(string):
    string = string.strip().title()
    string = string.replace(' De ',' de ').replace('De ','de ').replace(' La ',' la ').\
             replace("La ","la ").replace(" L'"," l'").replace(" D'"," d'")
    if re.search("^L'.*",string):
        string = 'l'+string[1:]
    if re.search("^D'.*",string):
        string = 'd'+string[1:]
    return string

def float_to_int(row):
    for j in [6,7,9,10,11,12]:
        row[j] = int(row[j])
    for i in range(len(row)):
        if isinstance(row[i],str):
            row[i] = title_style_with_exception(row[i])
    return row

def q1():
    filename = 'accidents_2017.csv'
    with open(filename) as datafile:
        data = csv.reader(datafile)
        i = 11
        data = list(data)
        for lines in data:
            for x in range(len(lines)-1):
                lines[x] = lines[x].strip()
                if lines[x] not in data[0]:
                    lines[x] = title_style_with_exception(lines[x]) 
                if ' ' in lines[x]:
                    lines[x] = '"' + lines[x] + '"'
                print(lines[x],end = ' ')
            print(lines[len(lines)-1])
            i -= 1
            if (i < 1):
                break

def q2():
    filename = 'accidents_2017.csv'
    with open(filename) as datafile:
        data = csv.reader(datafile,quotechar='"',quoting = csv.QUOTE_NONNUMERIC)
        with open('result_q2.csv','w') as csvfile:
            csvwriter = csv.writer(csvfile,delimiter=',',quotechar='"',\
                                   quoting = csv.QUOTE_NONNUMERIC)
            i = 0
            for lines in data:
                if i == 0:
                    csvwriter.writerow(lines)
                    i += 1
                else:
                    if 'Unknown' not in lines:
                        lines = float_to_int(lines)
                        csvwriter.writerow(lines)

def q3():
    q2()
    data = pd.read_csv('result_q2.csv').drop_duplicates()
    gb = data.groupby(by=['District Name'])['Id'].count().reset_index(name= 'Total')
    gb = gb.sort_values(by=['Total'],ascending=False)
    print('"District Name"',end = ' ')
    print('"Total numbers of accidents"')
    for lines in gb.values:
        if ' ' in lines[0]:
            lines[0] = '"'+lines[0]+'"'
        print(lines[0]+' '+str(lines[1]))


def q4():
    result = list()
    data = pd.read_csv('air_stations_Nov2017.csv',usecols=['Station','District Name'])
    for lines in data.values:
        if ' ' in lines[0]:
            lines[0] = '"'+lines[0]+'"'
        if ' ' in lines[1]:
            lines[1] = '"'+lines[1]+'"'
        dic = {"Station":lines[0], "District Name":lines[1]}
        result.append(dic)
    print(result)
    data = pd.read_csv('air_stations_Nov2017.csv')
    data = data.applymap(lambda x:title_style_with_exception(x) if isinstance(x,str) else x)

    data2 = pd.read_csv('air_quality_Nov2017.csv',quoting = csv.QUOTE_NONNUMERIC)
    data2['Air Quality'] = data2['Air Quality'].dropna()
    data2 = data2.loc[data2['Air Quality']!='Good']
    data2 = data2.loc[data2['Air Quality']!='--']
    data2 = data2.applymap(lambda x:title_style_with_exception(x) if isinstance(x,str) else x)
    printing = data2.head(10)
    header = list(printing)
    for i in range(len(header)):
        if ' ' in header[i]:
            header[i] = '"'+header[i]+'"'
    print(' '.join(header))
    printing = printing.applymap(lambda x:str(x))
    printing =printing.applymap(lambda x:'"'+x+'"' if (' ' in x) else x)
    for lines in printing.values:
        print(' '.join(lines))
    data2['Generated']= pd.to_datetime(data2['Generated'],format='%d/%m/%Y %H:%M')
    data = data[['Station','District Name']]
    data2 = data2[['Station','Generated']]
    output = data.merge(data2,left_on='Station',right_on='Station',how = 'inner',suffixes=('','_x'))
    data3 = pd.read_csv('accidents_2017.csv',quoting=csv.QUOTE_NONNUMERIC)
    data3 = data3.dropna()
    data3 = remove_unknown(data3)
    data3 = data3.applymap(lambda x:title_style_with_exception(x) if isinstance(x,str) else x)
    
    
    output = data3.merge(output,left_on='District Name',right_on='District Name'\
                         ,how='inner',suffixes=('','_y'))
    #output.to_csv('result.csv',index=False)
    month = {'October':10,'September':9,'December':12,'July':7,'June':6,'May':5,'August':8,\
             'February':2,'March':3,'November':11,'April':4,'January':1}
    output['Month']=output['Month'].map(month)
    output['Day']=output['Day'].apply(lambda x : int(x))
    output['Hour']=output['Hour'].apply(lambda x :int(x))
    
    output = output[(output['Month']==output['Generated'].dt.month)&(output['Day']==output['Generated'].dt.day)&\
                    (output['Hour']==output['Generated'].dt.hour)]
    output = output[list(data3.columns.values)]
    invert_month = dict([[v,k] for k,v in month.items()])
    output['Month']=output['Month'].map(invert_month)
    output = output.apply(float_to_int,axis=1)
    output.to_csv('result_q4.csv',index=False,quoting=csv.QUOTE_NONNUMERIC)


def q5():
    data = pd.read_csv('accidents_2017.csv',quoting = csv.QUOTE_NONNUMERIC,\
                       usecols=['Longitude','Latitude'])
    data = data.loc[(data['Longitude']>=1.9168051389)&\
                    (data['Longitude']<=2.423210210)&\
                    (data['Latitude']>=41.28291)&\
                    (data['Latitude']<=41.493609)]
    img = plt.imread('Map.png')
    plt.rcParams['figure.figsize']=(9.46,5.75)
    plt.rcParams['figure.dpi']=100
    plt.imshow(img)
    length=0.5064050711
    width=0.2166989999
    plt.axis('off')
    data['Longitude'] = data['Longitude'].\
                        apply(lambda x : (x-1.9168051389)*946/length-1)
    data['Latitude'] = data['Latitude'].\
                       apply(lambda x : 575-(x-41.28291)*575/width)
    s = [[1.590,0],[0,1.50]]
    data = data.values.dot(s)
    plt.xlim((0,946))
    plt.ylim((575,0))
    plt.scatter(data.T[0]-278,data.T[1]-155,c='lightblue',s=2,alpha = 0.2)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1,bottom=0,right=1,left=0,hspace=0,wspace=0)
    plt.margins(0,0)
    plt.savefig('plot.png',transparent=True,dpi=100,pad_inches = 0)


