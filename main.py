'''
Mercer on Mission 2023
Data Science Workshop: Cape Town Historical Loadshedding 2020-2023
Designed by: Ervin Pangilinan
'''

import pandas as pd
import matplotlib.pyplot as plt
import sys
from os import system, name

# Functions

def clearScreen():
    # POST: Clears the console screen. 
    
    # For Windows
    if name == 'nt':
        _ = system('cls')
    # For Mac and Linux (here, os.name is 'posix')
    else:
        _ = system('clear')
        
def showMenu():
    # POST: Outputs all of the menu options. 
    
    print("Type in a number (1-5) of the option below:")
    print("1.) Get Yearly Average Loadshedding Data by Area")
    print("2.) Get Yearly Loadshedding Stage Percentages by Area")
    print("3.) Get Day vs. Night Yearly Frequencies by Area")
    print("4.) Query records")
    print("5.) Exit Program")

def historicAveragesQuery(area, data):
    # PRE: Valid area name and DataFrame are passed in.
    # POST: Returns a dictionary of year and average duration pairs.
    
    historicAverages = {}
    years = [2020, 2021, 2022, 2023]
    
    for i in years:
        query = data[(data['Date'].dt.year == i) & 
                     (data['Area'] == str("Area " + str(area)))]
        
        total = 0
        for index, row in query.iterrows():
            total = total + int(row["Duration"])
            
        average = round(float(total / query.shape[0]), 2)
        historicAverages[i] = average
        
    return historicAverages

def makeBarGraph(graphDataDict, area):
    # PRE: Dictionary containing year-average pairs is filled.
    # POST: Creates a bar graph based on the dictionary pairs.
    
    # Customize styling of the graph
    plt.style.use('_mpl-gallery')
    titleFont = {'family':'serif', 'size':'18'}
    axesFont = {'family':'serif', 'size':'14'}
    fig = plt.figure(figsize = (8, 8))
    
    # Make a new, smaller DataFrame based on the passed dictionary.
    graphData = {"Year" : graphDataDict.keys(), 
                 "Average Duration" : graphDataDict.values()}
    graphDF = pd.DataFrame(data = graphData)
    
    # Create the graph and show it.
    plt.bar(graphDF["Year"], graphDF["Average Duration"])
    plt.xticks([2020, 2021, 2022, 2023])
    plt.xlabel("Year", fontdict = axesFont)
    plt.ylabel("Minutes", fontdict = axesFont)
    plt.title("Average Loadshedding Duration in Area " + str(area), 
              fontdict = titleFont)
    plt.show()

    # Output the data points to the console.
    print("\n\tData Points for Area", area, "\n")
    print(graphDF)
    
def historicStageQuery(area, data, year):
    # PRE: Valid area name, DataFrame, and year are passed in.
    # POST: Returns a dictionary of Stage-Frequency pairs.
    
    # Get all data for given year and area.
    query = data[(data['Date'].dt.year == year) & 
                 (data['Area'] == str("Area " + str(area)))]
    stageCount = {}
    
    # Extract the Stage data from each row.
    for index, row in query.iterrows():
        if row["Stage"] not in stageCount:
            stageCount[row["Stage"]] = 0
        else:
            stageCount[row["Stage"]] = stageCount[row["Stage"]] + 1
    
    # Sort the dictionary
    keys = list(stageCount.keys())
    keys.sort()
    sortedStageCount = {i : stageCount[i] for i in keys}
    
    return sortedStageCount

def makePieChart(graphDataDict, area, year):
    # PRE: Valid area number is passed in and data has been queried.
    # POST: Creates a pie chart based on the dictionary pairs.
    
    # Seperate the dictionary pairs.
    stages = list(graphDataDict.keys())
    frequencies = list(graphDataDict.values())
    total = sum(frequencies)
    
    # Output the data points.
    print("\n\tData Points for Area", area, "in", year, "\n")
    for i in range(len(stages)):
        print("\t" + stages[i] + "\t\t" + 
              str(round(frequencies[i] / total, 3) * 100) + "%")
    
    # Customize styling.
    plt.style.use('_mpl-gallery')
    titleFont = {'family':'serif', 'size':'24'}
    plt.figure(figsize = (16, 9))
    plt.pie(frequencies, labels = stages, colors = 
            ['r', 'g', 'b', 'c', 'm', 'y'], autopct = '%1.1f%%', 
            radius = 0.9)
    plt.title("Area " + 
              str(area) + " Loadshedding Stage Percentages in " 
              + str(year), fontdict = titleFont)
    plt.show()
      
#######################################################################

# Main Program
pd.options.display.max_columns = 6
df = pd.read_csv('loadsheddingData.csv', index_col = 0)
df["Date"] = pd.to_datetime(df["Date"], format = '%Y-%m-%d')

clearScreen()
print("\t\t Cape Town Historical Loadshedding Data Records Program\n")
showMenu()
option = input("\nEnter an option: ")

while option != 5:
    if option == "1":
        area = int(input("\nEnter the area number (1-18 only): "))
        queryDataDict = historicAveragesQuery(area, df)
        makeBarGraph(queryDataDict, area)
        print()
    elif option == "2":
        area = int(input("\nEnter the area number (1-18 only): "))
        year = int(input("Enter the year (2020-2023 only): "))
        queryDataDict = historicStageQuery(area, df, year)
        makePieChart(queryDataDict, area, year)
        print()
    elif option == "3":
        print("Still in progress...\n")
    elif option == "4":
        print("Still in progress...\n")
    elif option == "5":
        sys.exit()
    else:
        print("Invalid option. Please try again.\n")
        
    showMenu()
    option = input("\nEnter an option: ")

