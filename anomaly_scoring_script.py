# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 22:49:22 2021

@author: Abhishek Mukherjee
"""

import csv

master_row=[]
with open('C:/Users/Abhishek Mukherjee/Downloads/input_data1.csv', 'r') as file:
    my_reader = csv.reader(file, delimiter=',')
    for row in my_reader:
        master_row.append(row)

#function to computer the neighbours 
#of a point at 'epsilon' distance
#from the point.
def range_query(db,p,eps):    
    N=[]
    for i in db:
        if abs(i-p) <=eps:
            N.append(i)
    return N

# the main dbscan function
def dbscan(db,min_pts,eps):
    
    #Giving an initial label to all the points
    label=dict()
    for p in db:
        label.update({p:'undefined'})
    
    c=1  #Initial cluster label
    S=[] #initial seed set
    
    #Main algorithm begins    
    for p in db:
        if label[p]!='undefined':
            continue
        
        N=range_query(db,p,eps)
        
        if len(N)<min_pts:
            label[p]='Noise'
            continue
        
        #starting a new cluster:
        c+=1
        
        #assigning cluster label to the point:
        label[p]=c
        
        #Seed-set:
        S=N.copy()
        
        #Neighbourhood expanding:
        for q in S: 
            
            if label[q]=='Noise':
                label[q]=c
                
            if label[q]!='undefined':
                continue
            
            N=range_query(db,q,eps)
            
            label[q]=c #re-assigning of labels to
                        #neighbourhood points.
                        
            if len(N)<min_pts:
                continue
            
            S.extend(N) #adding points which form border
            
    #Computing the sum of
    #the non-anamoulous points
    temp_total=[]
    for nums in db:
        if label[nums]!='Noise':
            temp_total.append(nums)
    
    #Average without taking the outliers
    #into account:
    temp_average=sum(temp_total)/len(temp_total)
    
    #Num. of cluster memebers:
    #For every element belonging 
    #this dictionary will have
    #the num. of members in its cluster/class. 
    temp_dict=dict()

    temp_label=[]
    for ele in db:
        temp_label.append(label[ele])
    
    for element,class_mem in zip(db,temp_label):
        num_mems=temp_label.count(class_mem)
        temp_dict.update({element:[num_mems,element]})
                
    #computing the score:
    score=dict()
    
    alpha=0.1 #Base score.
    beta=0.01 #penalizing parameter. 
    for keys,values in temp_dict.items():
        temp_score=alpha+(beta*(abs((values[1]-temp_average)/(values[0]))))
        score.update({keys:temp_score})
        
    return label,score

anamoly_score=dict() #dictionary containing the anamoly scores
for temp_row in master_row[1:]:
    user_name=temp_row[0]
    db=temp_row[1:] 
    db=list(map(lambda a:int(a),db))
    label,temp_score=dbscan(db,min_pts=2,eps=3)
    anamoly_score.update({user_name:list(map(lambda val:temp_score[val],db))})
    

    
    
    

    