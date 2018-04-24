#imports
import pandas as pd
import xlrd
from scipy import stats

##  Mammal:
##      1. Do mammals differ among the different sites and/or site types? How so?

#import excel file & data
myfile = pd.ExcelFile('Field_Restoration.xlsx')
mydata = pd.ExcelFile(myfile)

#extracting data from the mammal sheet as a dataframe
dataframe = myfile.parse('Mammals')
