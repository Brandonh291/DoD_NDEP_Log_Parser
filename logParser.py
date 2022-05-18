# -*- coding: utf-8 -*-
###############################################################################
# Python Parsing Code for Mission Planner Data Logs
# By: Brandon Hickey
# Date: 5/18/2022

# Description: This code will be used to convert a mission planner log file
#               to a comma separate values document containing
#               Vertical Position, Velocity, and Acceleration.

# IMPORTANT NOTE: You MUST convert the ".BIN" file logs from 
#                  Navio2 to a ".log" otherwise you will get an error.
###############################################################################


# Import Packages
import csv # Used for parsing CSV files
import tkinter as tk # Used for dialog boxes
from tkinter import filedialog as fd # sub module for dialog boxes

# Initialize dialog box object
root = tk.Tk() 

# Ask for ".log" file here to open
experimentalFile = fd.askopenfilename()

# Ask for the name of the final parsed log.
fileSaveName=fd.asksaveasfilename(defaultextension = '.csv')
# Make sure to include .csv
    
# Plotting Limits
startTimeOffset=0
stopTimeOffset=10000

# Initializing variables
experimentalData = []
expTimeArray=[]
expDataArray=[]
expTimePlot=[]
expDataPlot=[]
logArray=[]
innerArray=[]
dataSet1=[]
dataSet2=[]
dataSet3=[]




##############################################################################
############################ SEARCH TERMS ####################################
##############################################################################
#
# Here is the format how search terms are made:
#
#    ['ACC1',5,"Z-Acceleration (m/s/s)",3,1,"AccZ"]
#
#
# ACC1 : This is the Group that the specific data you are looking for is filed under.
#         Its like the folder that contains the list of related variables
#         In this case ACC (acceleration) would contain items 
#         like x,y, and z accelerations
#
# 5 : This is the column to pull data from in the ACC1 group.
#      Each group has a different number of columns that correspond to different
#      data like columns 3,4, and 5 would contain 
#      X, Y, and Z acceleration respectively.
#
# Z-Acceleration (m/s/s) : This is used as a label in the exported data to 
#                           tell you what data is represented.
#
# 3 : This is the column of data you want to pull from the OpenRocket simulation
#      to compare with your experiment. In this case, column 3 represents your
#      Z-Acceleration.
#
# 1 : This represents whether we are multiplying our simulated data values by
#      a "1" or "-1" because based on the orientation of the data from Navio2
#      it might interpret upward motion as a negative value while the OpenRocket
#      considers it a positive value so we just flip the sign to make the match.
#
# "AccZ" : This is label that tells you what data you are pulling from the
#         experimental data. Its user made so it's just for display purposes.
#         If you look at the experimental log you will see our z-accel is
#         Listed as ACC1.AccZ which tells you its group and the variable.
searchTermSet=['ACC1',5,"Z-Acceleration (m/s/s)",3,1,"AccZ"] # Z-Acceleration
searchTermSet2=['NKF1',11,"Altitude (m)",1,-1,"PD"] # Altitude (Z-Position)
searchTermSet3=['NKF1',7,"Downward Velocity (m/s)",2,-1,"VD"] # Z-Velocity
searchTermArray=[searchTermSet,searchTermSet2,searchTermSet3] # Combine 




##############################################################################
############################ MAIN CODE #######################################
##############################################################################

# Initialize Variables
firstTermTrigger=0
startTime=0


# Extract Experimental Data from Log File
with open(experimentalFile, 'r') as csvfile:
    csvreader = csv.reader(csvfile)      # creating a csv reader object
    for row in csvreader:                
        experimentalData.append(row)     # extracting each data row one by one
 
    
# Begin our for loop to go through each desired search term in the array
for row in experimentalData[:]:
    innerTimeArray=[]
    innerDataArray=[]
    
    # For each row of data, we will see if it matches any of our three search
    # terms, if it matches, record it in a column corresponding to the term 
    for x in range(len(searchTermArray)):
        searchRow=searchTermArray[x][1] # Desired Column
        searchValue=searchTermArray[x][0] # Set initial time
        # parsing each column of a row
        if row[0] == searchValue:
            if firstTermTrigger==0:
                startTime=float(row[1])
                firstTermTrigger=1
            if (float(row[1])-startTime)/1000000 > startTimeOffset and (float(row[1])-startTime)/1000000 < stopTimeOffset:    
                innerTimeArray.append((float(row[1])-startTime)/1000000)
                innerDataArray.append(searchTermArray[x][4]*float(row[searchRow]))
        else:
            innerTimeArray.append(0)
            innerDataArray.append(0)
    if (float(row[1])-startTime)/1000000 > startTimeOffset and (float(row[1])-startTime)/1000000 < stopTimeOffset:
        if len(innerTimeArray)>0:
            count=0
            for x in innerTimeArray:
                if x==0:
                    count=count+1
            if count!=len(innerTimeArray):
                expTimeArray.append(innerTimeArray)
                expDataArray.append(innerDataArray)


# Pair Data
for row in range(len(expDataArray)):
    if expTimeArray[row][0] != 0:
        timeDataPair=[expTimeArray[row][0],expDataArray[row][0]]
        dataSet1.append(timeDataPair)   
for row in range(len(expDataArray)):
    if expTimeArray[row][1] != 0:
        timeDataPair=[expTimeArray[row][1],expDataArray[row][1]]
        dataSet2.append(timeDataPair)    
for row in range(len(expDataArray)):
    if expTimeArray[row][2] != 0:
        timeDataPair=[expTimeArray[row][2],expDataArray[row][2]]
        dataSet3.append(timeDataPair)

# Combine Data Sets
combineData=[]
# Place Labels in log array
for row in range(len(searchTermArray)):
    combineData.append('Time (s)')
    combineData.append('Experimental '+str(searchTermArray[row][2]))
logArray.append(combineData)

# Organize all data sets to one log
for row in range(len(dataSet1)):
    combineData=[]
    if row < len(dataSet2):
        combineData.append(dataSet1[row][0])
        combineData.append(dataSet1[row][1])
        combineData.append(dataSet2[row][0])
        combineData.append(dataSet2[row][1])
        combineData.append(dataSet3[row][0])
        combineData.append(dataSet3[row][1])
    else:
        combineData.append(dataSet1[row][0])
        combineData.append(dataSet1[row][1])
        combineData.append('')
        combineData.append('')
        combineData.append('')
        combineData.append('')
    logArray.append(combineData)
        
# Write log to file
with open(fileSaveName, 'w') as file:
 for row in logArray:
     firstCheck=0
     for col in row:
         if firstCheck==0:
             file.write(str(col))
             firstCheck=1
         else:
             file.write(',')
             file.write(str(col))
     file.write('\r')
#############################################################################

root.destroy()
print("Parsing Finished")

