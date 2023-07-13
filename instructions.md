# Data Science Workshop

## Source Code

### Copy and paste this code onto your main.py program then click ***Run***.

```python
'''
Mercer on Mission 2023
Data Science Workshop: Cape Town Historical Loadshedding 2020-2023
Designed by: Ervin Pangilinan
'''

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import sys

# Functions
        
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
    
    for year in years:
        # Get all data for given year and area.
        query = data[(data['Date'].dt.year == year) & 
                     (data['Area'] == str("Area " + str(area)))]
        
        total = 0
        for index, row in query.iterrows():
            # Calculate the average for each year.
            total = total + int(row["Duration"])
            
        average = round(float(total / query.shape[0]), 2)
        historicAverages[year] = average
        
    return historicAverages

def makeBarGraph(graphDataDict, area):
    # PRE: Dictionary containing year-average pairs is filled.
    # POST: Creates a bar graph based on the dictionary pairs.
    
    # Customize styling of the graph
    plt.style.use('_mpl-gallery')
    titleFont = {'family':'serif', 'size':'18'}
    axesFont = {'family':'serif', 'size':'14'}
    fig = plt.figure(figsize = (5, 4))
    
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
    
    # Sort the dictionary.
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
            ['r', 'g', 'b', 'c', 'm', 'y'], autopct = '%1.1f%%', radius = 0.9)
    plt.title("Area " + 
              str(area) + " Loadshedding Stage Percentages in " 
              + str(year), fontdict = titleFont)
    plt.show()
    
def areaQuery(data, area):
    # PRE: DataFrame and area number is passed in.
    # POST: Returns a DataFrame containing frequencies for each year.
    
    years = [2020, 2021, 2022, 2023]
    amCounts = []
    pmCounts = []
        
    for year in years:
        # Get all records about an area for specified year.
        query = data[(data['Date'].dt.year == year) & 
                     (data['Area'] == str("Area " + str(area)))]

        # Count how many are AM or PM loadshedding times.
        amCount = 0
        pmCount = 0
        for index, row in query.iterrows():
            parsedTime = dt.datetime.strptime(row['Time'], '%H:%M')
            noon = dt.datetime.strptime('12:00', '%H:%M')
            if parsedTime.time() < noon.time():
                amCount += 1
            else:
                pmCount += 1

        # Add each count to a seperate list.
        amCounts.append(amCount)
        pmCounts.append(pmCount)
        
    # Create a dictionary where each list is a value.
    areaDict = {'Year' : years, 'AM Frequency' : amCounts,
                'PM Frequency' : pmCounts}
    
    # Create a DataFrame based on the dictionary that was just created.
    areaDF = pd.DataFrame.from_dict(areaDict)
        
    return areaDF
            
def makeFrequencyBarGraph(data, area):  
    # PRE: Smaller DataFrame was created and area number is passed in.
    # POST: Outputs the table for AM and PM frequencies.
    
    # Customize styling of the graph
    plt.style.use('_mpl-gallery')
    
    # Create the bar graph.
    data.plot(x = "Year", y = ["AM Frequency", "PM Frequency"], kind = "bar") 
    plt.show()
    
def queryRecords(data):
    # PRE: CSV file is read in and converted into a DataFrame.
    # POST: Returns a DataFrame that matches the specified filters.
        
    # Prompt the user to input the search filters.
    filters = {}
    print("\nJust press ENTER to not specify a filter.\n")
    for field in ["Date", "Time", "Stage", "Area", "Duration"]:
        if field == "Date":
            message = "Enter Date in YYYY-MM-DD format (Ex: 2020-01-01): "
        elif field == "Time":
            message = "Enter Time (24-hour clock, HH:MM): "
        else:
            message = "Enter " + field + ": "
            
        # Check to see if there is a response for each prompt.
        response = input(message)
        if len(response) == 0:
            filters[field] = False
        elif field == "Stage" or field == "Area":
            filters[field] = str(field + " " + response).strip()
        elif field == "Duration":
            filters[field] = int(response)
        else:
            filters[field] = response.strip()
            
    # Apply the filters.
    madeNewDataFrame = False
    query = pd.DataFrame()
    for field in filters:
        # If-else branches account for fields with no response.
        if filters[field] == False:
            continue
        elif madeNewDataFrame == False and field == "Date":
                query = data[data["Date"] == pd.Timestamp(filters[field])]
                madeNewDataFrame = True
        elif madeNewDataFrame == False and field != "Date":
            query = data[data[field] == filters[field]]
            madeNewDataFrame = True
        else:
            query = query[query[field] == filters[field]]
        
    if query.empty:
        print("\nNo results...\n")
    else:
        print("\nFound the following", query.shape[0] ,"record(s)...\n")
        print(query.head(query.shape[0]))
        print()
        
##############################################################################

# Main Program
pd.options.display.max_columns = 6
df = pd.read_csv('loadsheddingData.csv', index_col = 0)
df["Date"] = pd.to_datetime(df["Date"], format = '%Y-%m-%d')

print("\t\t Cape Town Historical Loadshedding Data Records Program")
print("\t\tThis program contains records from Jan 2020 to May 2023.\n")
showMenu()
option = input("\nEnter an option: ")

while option != "5":
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
        area = int(input("\nEnter the area number (1-18 only): "))
        result = areaQuery(df, area)
        print("\n\tData Points for Area", area, "\n\n", result)
        makeFrequencyBarGraph(result, area)
        print()
    elif option == "4":
        queryRecords(df)
    elif option == "5":
        sys.exit()
    else:
        print("Invalid option. Please try again.\n")
        
    showMenu()
    option = input("\nEnter an option: ")
```

### If you want to get started with making your own queries, copy and paste this:
```python
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import sys

pd.options.display.max_columns = 6
df = pd.read_csv('loadsheddingData.csv', index_col = 0)
df["Date"] = pd.to_datetime(df["Date"], format = '%Y-%m-%d')

```


## Guided Questions

### 1.) How can we write a query to gather all of the data of a single area?

### 2.) We can actually write out some of these queries as for-loops. Let's apply our knowledge of for-loops to rewrite a query using for-loops instead of using Pandas' style of querying data.

  