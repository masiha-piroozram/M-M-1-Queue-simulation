import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# set seed for replication
#np.random.seed(0)

# M/M/1 queue simulation

Lambda = 1/5 # average number of arrivals per minute
mu = 1/3 # average number of people served per minute
ncust = 100 # number of customers
s = 1 # number of servers
service_times = [] # list of service times once they reach the front

 #generating inter arrival times using exponential distribution

if s==1:
    inter_arrival_times = list(np.random.exponential(scale=1/Lambda,size=ncust))
for i in range(0,ncust):
    inter_arrival_times[i] = round(inter_arrival_times[i],4)
    
    
    
arrival_times= []# list of arrival times of a person joining the queue
finish_times = [] # list of finish times after waiting and being served
        
arrival_times = [0 for i in range(ncust)]
finish_times = [0 for i in range(ncust)]
        
arrival_times[0]=round(inter_arrival_times[0],4)#arrival of first customer
        
        #Generate arrival times
      
for i in range(1,ncust):
    arrival_times[i]=round((arrival_times[i-1]+inter_arrival_times[i]),4)
        
    
        # Generate random service times for each customer 
if s==1:
    service_times = list(np.random.exponential(scale=1/mu,size=ncust))
for i in range(0,ncust):
    service_times[i] = round(service_times[i],4)
    
    
             #Generate finish times
finish_times[0]= round((arrival_times[0]+service_times[0]),4)
for i in range(1,ncust):
    previous_finish=finish_times[:i]
    previous_finish.sort(reverse=True)
    previous_finish=previous_finish[:s]
    if i< s:
        finish_times[i] = round(arrival_times[i] + service_times[i],4)
    else:
        finish_times[i]=round((max(arrival_times[i],min(previous_finish))+service_times[i]),4)
    
    
           # Total time spent in the system by each customer
total_times =[abs(round((finish_times[i]-arrival_times[i]),4)) for i in range(ncust)]
    
    
    
         # Time spent waiting before being served (time spent in the queue)
wait_times = [abs(round((total_times[i] - service_times[i]),4)) for i in range(ncust)]
     
    
        #creating a dataframe with all the data of the model
data = pd.DataFrame(list(zip(arrival_times,finish_times,service_times,total_times,wait_times,inter_arrival_times)), 
columns =['arrival_times','finish_times', 'service_times','total_times','wait_times','inter_arrival_times'])

    
print(data)
data.to_csv('Queueing Simulation.csv', sep='\t', encoding='utf-8')



#generating the timeline , and their description (arrivals, departures)
    
tbe=list([0])
timeline=['simulation starts']
for i in range(0,ncust):
    tbe.append(data['arrival_times'][i])
    tbe.append(data['finish_times'][i])
    timeline.append('customer ' +str(i+1)+' arrived')
    timeline.append('customer ' +str(i+1)+' left')
        
    
    #generating a dataframe with the timeline and description of events
    
timeline = pd.DataFrame(list(zip(tbe,timeline)), 
columns =['time','Timeline']).sort_values(by='time').reset_index()
timeline=timeline.drop(columns='index')
    
    #generating the number of customers inside the system at any given time of the simulation
    # and recording idle and working times
    
timeline['n']=0
x=0
for i in range(1,(2*ncust)-1):
    if len(((timeline.Timeline[i]).split()))>2:
        z=str(timeline['Timeline'][i]).split()[2]
    else:
        continue
    if z =='arrived':
        x = x+1
        timeline['n'][i]=x
    else:
        x=x-1
        if x==-1:
            x=0
        timeline['n'][i]=x
        
    
    
    #computing time between events
t= list()
for i in timeline.index:
    if i == (2*ncust) -2 :
        continue
    if i < 2*ncust:
        x=timeline.time[i+1]
    else:
        x=timeline.time[i]
    y=timeline.time[i]
    t.append(round((x-y),4))
    
t.append(0) 
timeline['tbe']=t

    #computing the probability of 'n' customers being in the system
    
Pn=timeline.groupby('n').tbe.agg(sum)/sum(t)
Tn=timeline.groupby('n').tbe.agg('count')
    
      
    #checking central tendency measures and dispersion of the data
timeline.n.describe()
    
    
    #computing expected number of customers in the system
Ls=(sum(Pn*Pn.index))
    
    
    #computing expected customers waiting in line
Lq=sum((Pn.index[s+1:]-1)*(Pn[s+1:]))

print('\nFull overview of arrivals and exits :\n' , timeline)

timeline.to_csv('Timeline.csv', sep='\t', encoding='utf-8')
print('\nLs(expected number of customers in the system) = ' , Ls ,
      '\nLq(expected customers waiting in the queue) = ' , Lq)

