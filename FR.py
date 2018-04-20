#imports
import pandas as pd
import xlrd
from scipy import stats

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
#print(mydata.sheet_names)

#extracting data from the first sheet as a dataframe
'''
dataframe = myfile.parse('Mammals')
print(dataframe)
'''

dataframe = myfile.parse('NonMammal')

def runTestOnAll(dataFrame):
    categories = list(dataframe.columns.values)
    for cat in categories:
        if cat != "site.type" and cat != "site" and cat != "station":
            testResults = anovaTest(dataFrame, cat)
            print(cat + ": F-value = " + str(testResults.statistic) + " P-value = " + str(testResults.pvalue))
    return

def anovaTest(dataFrame, category):

    reducedDF = dataFrame[['site.type', category]]

    dArray = []
    rArray = []
    iArray = []
    for index, row in reducedDF.iterrows():
        site = row['site.type']
        val = row[category]
        if site== 'D':
            dArray.append(val)
        elif site == 'R':
            rArray.append(val)
        elif site == 'I':
                iArray.append(val)
        else:
            print("ERROR\n")

    anova = stats.f_oneway(dArray, rArray, iArray)
    return anova

#function calls
runTestOnAll(dataframe)
#n = anovaTest(dataframe, "av.bac")


#printing out the sheet names in the excel file
print(mydata.sheet_names)

#extracting data from NonMammals sheet for dataframe
nonmammal = myfile.parse('NonMammal')
df = pd.DataFrame(nonmammal)
groups = df.groupby("site.type")
print(groups.count())

#extracting data from Mammals sheet for dataframe
dataframe = myfile.parse('Mammals')
#print(dataframe)
