#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np


# In[2]:


POS = [ 'W','N','E','S','C' ]    # position of IJ
MAT = [ 0,1,2 ]    # material with IJ
ARROW = [ 0,1,2,3 ]    # number of arrows
STATE = [ 'D','R' ]    # ready and dormant state of MM
HEALTH = [ 0,25,50,75,100 ]    # MM’s health
ACTION = [ 'UP','LEFT','DOWN','RIGHT','STAY','SHOOT','HIT','CRAFT','GATHER','NONE' ]    # POSSIBLE ACTIONS OF IJ

TEAM = 25

ARR = [ 0.5, 1, 2 ]
Y = ARR[TEAM % 3]
STEPCOST = -10/Y

GAMMA = 0.999
DELTA = 0.001

BLADEHITDAMAGE = 50
ARROWHITDAMAGE = 25

FINALREWARD = 50
NEGATEREWARD = 40
os.makedirs('outputs', exist_ok=True)


# In[3]:


all_state = []
for pos in POS:
    for mat in MAT:
        for arrow in ARROW:
            for state in STATE:
                for health in HEALTH:
                    all_state.append((pos,mat,arrow,state,health))


# In[4]:


state_actions = {} # state actions in dict.
for s in all_state:
    if s[-1]==0:
        state_actions[s] = ['NONE']
    elif s[0]=='W':
        state_actions[s] = [ 'RIGHT','STAY']
        if s[2]!=0:
            state_actions[s].append('SHOOT')
    elif s[0]=='N':
        state_actions[s] = [ 'DOWN','STAY']
        if (s[1]>0) and (s[2]<3):
                state_actions[s].append('CRAFT')
    elif s[0]=='E':
        state_actions[s] = [ 'LEFT','STAY','HIT' ]
        if s[2]!=0:
            state_actions[s].append('SHOOT')
    elif s[0]=='S':
        state_actions[s] = [ 'UP','STAY' ]
        if s[1]<2:
            state_actions[s].append('GATHER')
    else:
        state_actions[s] = [ 'UP','LEFT','DOWN','RIGHT','STAY','HIT' ]
        if s[2]>0:
            state_actions[s].append('SHOOT')


# In[5]:


utility = {}
policy = {}
for s in all_state:
    utility[s]=0
    if s[-1]!=0:
        policy[s]=""


# In[6]:


def get_pfsb(current_state, action):
    pfsb = []
    (pos,mat,arrow,state,health) = current_state
    if state=='D':
        
        if action == 'UP':
            if pos=='C':
                pfsb.append(('N',mat,arrow,'D',health,0.85*0.8))
                pfsb.append(('N',mat,arrow,'R',health,0.85*0.2))
            else:
                pfsb.append(('C',mat,arrow,'D',health,0.85*0.8))
                pfsb.append(('C',mat,arrow,'R',health,0.85*0.2))
            pfsb.append(('E',mat,arrow,'D',health,0.15*0.8))
            pfsb.append(('E',mat,arrow,'R',health,0.15*0.2))
            
        elif action == 'DOWN':
            if pos=='C':
                pfsb.append(('S',mat,arrow,'D',health,0.85*0.8))
                pfsb.append(('S',mat,arrow,'R',health,0.85*0.2))
            else:
                pfsb.append(('C',mat,arrow,'D',health,0.85*0.8))
                pfsb.append(('C',mat,arrow,'R',health,0.85*0.2))
            pfsb.append(('E',mat,arrow,'D',health,0.15*0.8))
            pfsb.append(('E',mat,arrow,'R',health,0.15*0.2))
            
        elif action == 'LEFT':
            if pos=='C':
                pfsb.append(('W',mat,arrow,'D',health,0.85*0.8))
                pfsb.append(('W',mat,arrow,'R',health,0.85*0.2))
                pfsb.append(('E',mat,arrow,'D',health,0.15*0.8))
                pfsb.append(('E',mat,arrow,'R',health,0.15*0.2))
            else:
                pfsb.append(('C',mat,arrow,'D',health,1*0.8))
                pfsb.append(('C',mat,arrow,'R',health,1*0.2))
        
        elif action == 'RIGHT':
            if pos=='C':
                pfsb.append(('E',mat,arrow,'D',health,1*0.8))
                pfsb.append(('E',mat,arrow,'R',health,1*0.2))
            else:
                pfsb.append(('C',mat,arrow,'D',health,1*0.8))
                pfsb.append(('C',mat,arrow,'R',health,1*0.2))
        
        elif action == 'STAY':
            if pos in ['C','S','N']:
                pfsb.append((pos,mat,arrow,'R',health,0.85*0.2))
                pfsb.append((pos,mat,arrow,'D',health,0.85*0.8))
                pfsb.append(('E',mat,arrow,'R',health,0.15*0.2))
                pfsb.append(('E',mat,arrow,'D',health,0.15*0.8))
            else:
                pfsb.append((pos,mat,arrow,'R',health,1*0.2))
                pfsb.append((pos,mat,arrow,'D',health,1*0.8))
                
        elif action == 'HIT':
            if pos=='C':
                pfsb.append((pos,mat,arrow,'D',max(health-BLADEHITDAMAGE,0),0.1*0.8))
                pfsb.append((pos,mat,arrow,'D',health,0.9*0.8))
                pfsb.append((pos,mat,arrow,'R',max(health-BLADEHITDAMAGE,0),0.1*0.2))
                pfsb.append((pos,mat,arrow,'R',health,0.9*0.2))
            else:
                pfsb.append((pos,mat,arrow,'D',max(health-BLADEHITDAMAGE,0),0.2*0.8))
                pfsb.append((pos,mat,arrow,'D',health,0.8*0.8))
                pfsb.append((pos,mat,arrow,'R',max(health-BLADEHITDAMAGE,0),0.2*0.2))
                pfsb.append((pos,mat,arrow,'R',health,0.8*0.2))

        elif action == 'SHOOT':
            if arrow==0:
                pfsb.append((pos,mat,arrow,'D',health,1*0.8))
                pfsb.append((pos,mat,arrow,'R',health,1*0.2))
            else:
                if pos=='W':
                    pfsb.append((pos,mat,arrow-1,'D',max(health-ARROWHITDAMAGE,0),0.25*0.8))
                    pfsb.append((pos,mat,arrow-1,'R',max(health-ARROWHITDAMAGE,0),0.25*0.2))
                    pfsb.append((pos,mat,arrow-1,'D',health,0.75*0.8))
                    pfsb.append((pos,mat,arrow-1,'R',health,0.75*0.2))
                elif pos=='C':
                    pfsb.append((pos,mat,arrow-1,'D',max(health-ARROWHITDAMAGE,0),0.5*0.8))
                    pfsb.append((pos,mat,arrow-1,'R',max(health-ARROWHITDAMAGE,0),0.5*0.2))
                    pfsb.append((pos,mat,arrow-1,'D',health,0.5*0.8))
                    pfsb.append((pos,mat,arrow-1,'R',health,0.5*0.2))
                else:
                    pfsb.append((pos,mat,arrow-1,'D',max(health-ARROWHITDAMAGE,0),0.9*0.8))
                    pfsb.append((pos,mat,arrow-1,'R',max(health-ARROWHITDAMAGE,0),0.9*0.2))
                    pfsb.append((pos,mat,arrow-1,'D',health,0.1*0.8))
                    pfsb.append((pos,mat,arrow-1,'R',health,0.1*0.2))
        
        elif action == 'GATHER':
            if mat<2:
                pfsb.append((pos,mat+1,arrow,'D',health,0.75*0.8))
                pfsb.append((pos,mat+1,arrow,'R',health,0.75*0.2))
                pfsb.append((pos,mat,arrow,'D',health,0.25*0.8))
                pfsb.append((pos,mat,arrow,'R',health,0.25*0.2))
            else:
                pfsb.append((pos,mat,arrow,'D',health,1*0.8))
                pfsb.append((pos,mat,arrow,'R',health,1*0.2))
        
        elif action == 'CRAFT':
            if (mat>0):
                if arrow==0:
                    pfsb.append((pos,mat-1,1,'D',health,0.5*0.8))
                    pfsb.append((pos,mat-1,2,'D',health,0.35*0.8))
                    pfsb.append((pos,mat-1,3,'D',health,0.15*0.8))
                    pfsb.append((pos,mat-1,1,'R',health,0.5*0.2))
                    pfsb.append((pos,mat-1,2,'R',health,0.35*0.2))
                    pfsb.append((pos,mat-1,3,'R',health,0.15*0.2))
                elif arrow==1:
                    pfsb.append((pos,mat-1,2,'D',health,0.5*0.8))
                    pfsb.append((pos,mat-1,3,'D',health,0.5*0.8))
                    pfsb.append((pos,mat-1,2,'R',health,0.5*0.2))
                    pfsb.append((pos,mat-1,3,'R',health,0.5*0.2))
                elif arrow in [2,3]:
                    pfsb.append((pos,mat-1,3,'R',health,1*0.2))
                    pfsb.append((pos,mat-1,3,'D',health,1*0.8))
            else:
                pfsb.append((pos,mat,arrow,'D',health,1*0.8))
                pfsb.append((pos,mat,arrow,'R',health,1*0.2))
                    
    else:
        
        if action == 'UP':
            if pos=='C':
                pfsb.append((pos,mat,0,'D',min(health+25,100),0.5))
                pfsb.append(('N',mat,arrow,'R',health,0.85*0.5))
                pfsb.append(('E',mat,arrow,'R',health,0.15*0.5))
            else:
                pfsb.append(('C',mat,arrow,'D',health,0.5))
                pfsb.append(('C',mat,arrow,'R',health,0.85*0.5))
                pfsb.append(('E',mat,arrow,'R',health,0.15*0.5))

        elif action == 'DOWN':
            if pos=='C':
                pfsb.append((pos,mat,0,'D',min(health+25,100),0.5))
                pfsb.append(('S',mat,arrow,'R',health,0.85*0.5))
                pfsb.append(('E',mat,arrow,'R',health,0.15*0.5))
            else:
                pfsb.append(('C',mat,arrow,'R',health,0.85*0.5))
                pfsb.append(('E',mat,arrow,'R',health,0.15*0.5))
                pfsb.append(('C',mat,arrow,'D',health,0.85*0.5))
                pfsb.append(('E',mat,arrow,'D',health,0.15*0.5))
            
        elif action == 'LEFT':
            pfsb.append((pos,mat,0,'D',min(health+25,100),0.5))
            if pos=='C':
                pfsb.append(('W',mat,arrow,'R',health,0.85*0.5))
                pfsb.append(('E',mat,arrow,'R',health,0.15*0.5))
            else:
                pfsb.append(('C',mat,arrow,'R',health,1*0.5))
        
        elif action == 'RIGHT':
            if pos=='C':
                pfsb.append((pos,mat,0,'D',min(health+25,100),0.5))
                pfsb.append(('E',mat,arrow,'R',health,1*0.5))
            else:
                pfsb.append(('C',mat,arrow,'R',health,1*0.5))
                pfsb.append(('C',mat,arrow,'D',health,1*0.5))

        elif action == 'STAY':
            if pos=='C':
                pfsb.append((pos,mat,0,'D',min(health+25,100),0.5))
                pfsb.append((pos,mat,arrow,'R',health,0.85*0.5))
                pfsb.append(('E',mat,arrow,'R',health,0.15*0.5))
            
            elif pos=='E':
                pfsb.append((pos,mat,0,'D',min(health+25,100),0.5))
                pfsb.append(('E',mat,arrow,'R',health,1*0.5))
                
            elif pos in ['S','N']:
                pfsb.append((pos,mat,arrow,'R',health,0.85*0.5))
                pfsb.append(('E',mat,arrow,'R',health,0.15*0.5))
                pfsb.append((pos,mat,arrow,'D',health,0.85*0.5))
                pfsb.append(('E',mat,arrow,'D',health,0.15*0.5))
                
            else:
                pfsb.append((pos,mat,arrow,'R',health,1*0.5))
                pfsb.append((pos,mat,arrow,'D',health,1*0.5))
                
        elif action == 'HIT':
            pfsb.append((pos,mat,0,'D',min(health+25,100),0.5))
            if pos=='C':
                pfsb.append((pos,mat,arrow,'R',max(health-BLADEHITDAMAGE,0),0.1*0.5))
                pfsb.append((pos,mat,arrow,'R',health,0.9*0.5))
            else:
                pfsb.append((pos,mat,arrow,'R',max(health-BLADEHITDAMAGE,0),0.2*0.5))
                pfsb.append((pos,mat,arrow,'R',health,0.8*0.5))

        elif action == 'SHOOT':
            if arrow==0:
                pfsb.append((pos,mat,arrow,'R',health,1*0.5))
                if pos=='W':
                    pfsb.append((pos,mat,arrow,'D',health,1*0.5))
                else:
                    pfsb.append((pos,mat,0,'D',min(health+25,100),1*0.5))
            else:
                if pos=='W':
                    pfsb.append((pos,mat,arrow-1,'R',max(health-ARROWHITDAMAGE,0),0.25*0.5))
                    pfsb.append((pos,mat,arrow-1,'R',health,0.75*0.5))
                    pfsb.append((pos,mat,arrow-1,'D',max(health-ARROWHITDAMAGE,0),0.25*0.5))
                    pfsb.append((pos,mat,arrow-1,'D',health,0.75*0.5))
                elif pos=='C':
                    pfsb.append((pos,mat,0,'D',min(health+25,100),0.5))
                    pfsb.append((pos,mat,arrow-1,'R',max(health-ARROWHITDAMAGE,0),0.5*0.5))
                    pfsb.append((pos,mat,arrow-1,'R',health,0.5*0.5))
                else:
                    pfsb.append((pos,mat,0,'D',min(health+25,100),0.5))
                    pfsb.append((pos,mat,arrow-1,'R',max(health-ARROWHITDAMAGE,0),0.9*0.5))
                    pfsb.append((pos,mat,arrow-1,'R',health,0.1*0.5))
        
        elif action == 'GATHER':
            if mat<2:
                pfsb.append((pos,mat+1,arrow,'R',health,0.75*0.5))
                pfsb.append((pos,mat,arrow,'R',health,0.25*0.5))
                pfsb.append((pos,mat+1,arrow,'D',health,0.75*0.5))
                pfsb.append((pos,mat,arrow,'D',health,0.25*0.5))
            else:
                pfsb.append((pos,mat,arrow,'R',health,1*0.5))
                pfsb.append((pos,mat,arrow,'D',health,1*0.5))

        elif action == 'CRAFT':
            if (mat>0):
                if arrow==0:
                    pfsb.append((pos,mat-1,1,'R',health,0.5*0.5))
                    pfsb.append((pos,mat-1,2,'R',health,0.35*0.5))
                    pfsb.append((pos,mat-1,3,'R',health,0.15*0.5))
                    pfsb.append((pos,mat-1,1,'D',health,0.5*0.5))
                    pfsb.append((pos,mat-1,2,'D',health,0.35*0.5))
                    pfsb.append((pos,mat-1,3,'D',health,0.15*0.5))
                elif arrow==1:
                    pfsb.append((pos,mat-1,2,'R',health,0.5*0.5))
                    pfsb.append((pos,mat-1,3,'R',health,0.5*0.5))
                    pfsb.append((pos,mat-1,2,'D',health,0.5*0.5))
                    pfsb.append((pos,mat-1,3,'D',health,0.5*0.5))
                elif arrow in [2,3]:
                    pfsb.append((pos,mat-1,3,'D',health,1*0.5))
                    pfsb.append((pos,mat-1,3,'R',health,1*0.5))
            else:
                pfsb.append((pos,mat,arrow,'R',health,1*0.5))
                pfsb.append((pos,mat,arrow,'D',health,1*0.5))
    return pfsb


# In[7]:


def get_action_utility(current_state, action, current_utility):
    pfsb = get_pfsb(current_state,action)   
    next_utility = 0
    for ft in pfsb:
        net_reward = STEPCOST
        (pos,mat,arrow,state,health, prob) = ft
        pfstate = (pos,mat,arrow,state,health)
        if pfstate[-1]==0:
            net_reward += FINALREWARD
        elif ((pfstate[0]==current_state[0]) and
              (pfstate[1]==current_state[1]) and
              (pfstate[2]==0) and
              (pfstate[3]=='D' and current_state[3]=='R') and
              ((pfstate[4]==current_state[4]+25) or ((pfstate[4]==100)and(current_state[4]==100)))
             ):
            net_reward -= NEGATEREWARD
        next_utility += (prob*(net_reward + (GAMMA*current_utility[pfstate])))
    return next_utility


# In[8]:


def log_trace(iteration,utility,policy):
    with open("outputs/part_2_trace.txt",'a+') as write_file:
        write_file.write(f"iteration={iteration}\n")
        for i in sorted (utility):
            (pos,mat,arrow,state,health) = i
            write_file.write(f"({pos},{mat},{arrow},{state},{health}):")
            if i[-1]!=0:
                write_file.write(f"{policy[i]}=[")
                write_file.write("%0.3f"%utility[i])
                write_file.write("]\n")
            else:
                write_file.write("NONE=[0]\n")
        write_file.close()


# In[9]:


def value_iteration():
    with open("outputs/part_2_trace.txt",'w+') as write_file:
        write_file.write("")
        write_file.close()
    iteration = -1
    converge = False
    while not converge:
        iteration+=1
        
        max_deviation = 0
        current_utility = utility
        temp_utility = {}
        
        for s in all_state:
            
            if s[-1]==0:
                continue
            max_action_utility = -100000000
            
            temp_utility[s]=utility[s]            
            for a in state_actions[s]:
                temp = get_action_utility(s,a,current_utility)
                if (max_action_utility <= temp):
                    max_action_utility = temp
                    policy[s] = a
                    temp_utility[s] = temp
                    
            current_deviation = abs(temp_utility[s]-current_utility[s])
            if (max_deviation < current_deviation):
                max_deviation = current_deviation 
        
        if max_deviation < DELTA:
            converge = True
            
        for k in temp_utility.keys():
            utility[k] = temp_utility[k]
        
        log_trace(iteration, utility, policy)
    return utility, policy


# In[10]:


final_utility, final_policy = value_iteration()


# In[38]:


def log_simulation(cs,action,pfs,file):
    with open(file,'a+') as write_file:
        write_file.write(f"current_state = {cs} action_taken = {action} reached_state = {pfs}\n")
        write_file.close()


# In[40]:


# start_state1 = ('W',0,0,'D',100)
# start_state2 = ('C',2,0,'R',100)

# file_sim = "outputs/simulations/2_2.txt"
# for k in range(10):
#     cs = start_state2
#     while cs[-1]!=0:
#         action = final_policy[cs]
#         pfstate = get_pfsb(cs, action)
#         weight = [ ts[-1] for ts in pfstate ]
#         fs = np.random.choice([ i for i in range(len(pfstate))],1,p = weight)
#         (pos,mat,arrow,state,health,prob) = pfstate[fs[0]]
#         pfs = (pos,mat,arrow,state,health)
#         log_simulation(cs,action,pfs,file_sim)
#         cs = pfs
#     with open(file_sim,'a+') as write_file:
#         write_file.write(f"\n-----------------------------------------------------------------------------------------------------\n\n")
#         write_file.close()


# In[ ]:




