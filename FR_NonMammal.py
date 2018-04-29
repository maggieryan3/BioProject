#imports
import pandas as pd
import xlrd
from scipy import stats

##  Non-Mammal:
##      1. How do the 3 site types of degraded, restored, and intact differ in terms of vegetation,
##      insects, nematodes and soil characteristics?
##      2. How do nematodes cluster and what characteristics do the different types of nematodes
##      prefer?

#import excel file & data
myfile = pd.ExcelFile('Field_Restoration.xlsx')
mydata = pd.ExcelFile(myfile)

#extracting data from the first sheet as a dataframe
dataframe = myfile.parse('NonMammal')

def runTestOnAll(dataFrame):
    file = open("results.txt", "w")
    file.write("RESULTS\n")
    categories = list(dataFrame.columns.values)
    reducedCategories = []
    print("_______________ANOVA TEST STARTING____________________")
    for cat in categories:
        if cat != "site.type" and cat != "site" and cat != "station":
            testResults = anovaTest(dataFrame, cat)
            if testResults != None:
                reducedCategories.append(testResults)
            #print(cat + ": F-value = " + str(testResults.statistic) + " P-value = " + str(testResults.pvalue))
    print("______________ANOVA COMPLETE, TTEST STARTING__________")
    passCount = 0
    file.write("TTEST: The following passed a ttest with a p-value greater than 0.05, meaning that we are 95% confident that there is a statistical significance.\n")
    file.close()
    for cat in reducedCategories:
        passCount += tTest(dataFrame, cat)
    print("Number of tests passed: " + str(passCount))
    file = open("results.txt", "a")
    file.write("Number of tests passed: " + str(passCount)+"\n")
    print("________TTEST COMPLETE, CORRELATION TEST STARTING_______")
    nematodes = dataFrame[['nem.total.av']]
    file.write("\n\nThe following results will tell us which variables have a certain effect on the number of nematodes and how they cluster.\n")
    file.close()
    for cat in categories:
        if cat != "site.type" and cat != "site" and cat != "station" and cat != "nem.total.av":
            correlationTest(nematodes, cat, dataFrame)
    print("The rest of the variables were not statistically significant and/ or had a weak correlation")
    print("________________CORRELATION TEST COMPLETE_______________")
    return

def tchecker(type1, type2, pval, cat):
    strength = .05
    file = open("results.txt", "a")
    if pval < strength:
        
        print("PASS - Since the pvalue of " + str(pval) + " is less than " + str(strength) + ", we are " + str(100 - (strength*100)) + "% confident that there is a statistical significance between sites: " + type1 + " and " + type2 + " for " + cat)
        file.write("PASS - " + cat + " for " + type1 + " vs. " + type2+"\n")
        file.close()
        return 1
    else:
        print("FAIL - Since the p-value of " + str(pval) + " is greater than " + str(strength) + " we cannot say there is a significance difference between sites: " + type1 + " and " + type2 + " for " + cat)
        file.close()
        return 0

def tTest(dataFrame, category):
    
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
    temp = 0
    t1 = stats.ttest_ind(dArray, iArray, equal_var = False)
    temp += tchecker("degrated", "intact", t1.pvalue, category)
    t2 = stats.ttest_ind(dArray, rArray, equal_var = False)
    temp += tchecker("degrated", "restored", t2.pvalue, category)
    t3 = stats.ttest_ind(iArray, rArray, equal_var = False)
    temp += tchecker("intact", "restored", t3.pvalue, category)

    return temp

def anovaTest(dataFrame, category):

    strength = .05

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
    if anova.pvalue < strength:
        print("PASS - " + category + " P-Value= " + str(anova.pvalue) + " we will continue with a t-test...")
        return category
    else:
        print("FAIL - " + category + "P-Value= " + str(anova.pvalue))
        return None

'''
This function tests the correlation between nematodes and other variables
in order to see how nematodes cluster, using Spearman's correlation.
'''
def correlationTest(list, category, dataFrame):
    file = open("results.txt", "a")
    reducedDF = dataFrame[[category]]
    spearman = stats.spearmanr(list, reducedDF)
    if spearman.pvalue <= 0.05: #only consider statistically significant ones
        if spearman.correlation > .79:
            print("There is a VERY STRONG POSITIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation))
            file.write("There is a VERY STRONG POSITIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation)+"\n")
        elif spearman.correlation > .59:
            print("There is a STRONG POSITIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation))
            file.write("There is a STRONG POSITIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation)+"\n")
        elif spearman.correlation > .39:
            print("There is a MODERATE POSITIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation))
            file.write("There is a MODERATE POSITIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation)+"\n")
        elif spearman.correlation < -.79:
            print("There is a VERY STRONG NEGATIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation))
            file.write("There is a VERY STRONG NEGATIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation)+"\n")
        elif spearman.correlation < -.59:
            print("There is a STRONG NEGATIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation))
            file.write("There is a STRONG NEGATIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation)+"\n")
        elif spearman.correlation < -.39:
            print("There is a MODERATE NEGATIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation))
            file.write("There is a MODERATE NEGATIVE correlation between the number of nematodes and " + category + " Correlation = " + str(spearman.correlation)+"\n")
    file.close()
    return

#MAIN
runTestOnAll(dataframe)
