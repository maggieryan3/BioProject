#imports
import pandas as pd
import xlrd

##  Non-Mammal:
##      1. How do the 3 site types of degraded, restored, and intact differ in terms of vegetation,
##      insects, nematodes and soil characteristics?
##      2. How do nematodes cluster and what characteristics do the different types of nematodes
##      prefer?
##  Mammal:
##      1. Do mammals differ among the different sites and/or site types? How so?

#import excel file & data
myfile = pd.ExcelFile('Field_Restoration.xlsx')
mydata = pd.ExcelFile(myfile)

#printing out all the sheet names in the excel file
print(mydata.sheet_names)

#extracting data from the first sheet as a dataframe
dataframe = myfile.parse('Mammals')
print(dataframe)

dataframe = myfile.parse('NonMammal')
print(dataframe)
