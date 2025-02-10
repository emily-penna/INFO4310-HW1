# Simple post-processing script to create a clean subset of tree data
#     - JRz, for personal use and not indended for real-world applications
 
#  NOTE: This is eliminating valid, useful data in lieu of something easier to visualize
#        It's possible that this will mask trends, as it is often VERY likely that missing data are non-randomly distributed (e.g. more missing data pre-1955 in this dataset)


import csv
import re

def passes_filter(row):
    # Filter criteria:
    #   Only listed trees that have full species name supplied
    if len(row['qSpecies']) < 3 or 'Tree(s) ::' in row['qSpecies']:
        return False
    #   Only trees that have a lat and lng provided
    elif len(row['Latitude']) < 2 or len(row['Longitude']) < 2:
        return False
    #   Only trees with valid SiteInfo
    elif len(row['qSiteInfo']) < 1 or row['qSiteInfo'] == ':':
        return False
    #   Only trees that have a DBH provided
    elif len(row['DBH']) < 1 or row['DBH'] == '0':
        return False
    elif len(row['PlotSize']) < 1:
        return False
    # elif len(row['PlantDate']) < 1:
    #     return False
    else:
        return True
    

    

def filterDate(row):
    if row['PlantDate'] == '' :
        row['PlantDate'] = 1955
    else:
        dates = re.findall('\d+', row['PlantDate'])
        # 3/29/18 0:00 becomes => ['3', '29', '18', '0', '00']
        year = int(dates[2])
        if (year >= 55): 
            row["PlantDate"] = "19" + dates[2]
        else:
            row['PlantDate'] = "20" + dates[2]

# import and run passes_filter
data = []
header = []
with open('Street_Tree_List-2022-01-30_RAW.csv','r') as f:
    reader = csv.DictReader(f)
    
    header = reader.fieldnames
    for row in reader:
        #if passes_filter(row):
        # you might consider doing some additional processing here
        filterDate(row)
        
        # e.g. splitting up qSpecies
        data.append(row)

print(len(data))

# export to new CSV       
with open('Street_Tree_List-2022-01-30_FILTERED_DATEONLY.csv','w', newline = '') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)
