import csv
import sys
''' Convert the online-retail excel sheet to csv(OnlineRetail.csv) and feed as input to this program'''

''' THIS PROGRAM GENERATES ARFF format data that will be used to ''' 
''' find statistics about data set, using WEKA library'''

# READ FILENAME FROM COMMAND-LINE ARGUMENT
LINE_SEPERATOR = '\n'
# filePath = sys.argv[1]
filePath = 'Online_Retail.csv'
# filePath = 'G:\\Fall_2017\\Data_Mining\\Project\\update-2\\iceland_csv.csv'
# EXTRACT FILENAME WITHOUT EXTENSION TO BE USED AS RELATION
relationName = filePath.split('/')
relationName = relationName[len(relationName) - 1].split('.')[0]
# STORES FILEDATA
data = list()
# DICTIONARY OF COLUMNS AND THEIR TYPES
columnTypes = {}
numericColumns = set()
with open(filePath, newline='') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
# EXTRACT COLUMN HEADERS    
    header = next(csvReader)
    if(len(header) == 0):
        sys.exit()
    header = header[0].split(',')
    colLen = len(header)
    
    # Columns 0,1,5,6 are nominal
    nominalColumns = [0,1,5,6]
    
    columnTypes[0] = set()
    columnTypes[1] = set()
    columnTypes[5] = set()
    columnTypes[6] = set()
    
    # Columns 2,4 are numeric
    numericColumns.add(2)
    numericColumns.add(4)
    
    # Column 3 is date 
    
    for record in csvReader:
        line = ' '.join(record).split(',')
        if line[0].startswith('C'):
            continue
        if 'BANK CHARGES' in line[1]:
            line[1] = 'UNKNOWN_STOCK_CODE'
        line[3] = line[3].split(' ')[0]
        country = line[6]
        line[6] = country.replace(' ','_')
        if not bool(line[2].strip()):
            line[2] = -1
        if not bool(line[4].strip()):
            line[4] = -1
        if not bool(line[5].strip()):
            line[5] = 'UNKNOWN'
        for i in range(len(line)):
            # Numeric columns(2,4) and date column(3)
            if i==2 or i==4 or i==3:
                continue
            # Nominal
            elif (i == 0 or i==1 or i==5 or i==6) and bool(line[i]):
                columnTypes[i].add(line[i])
        data.append(line)
# COMPOSE ARFF FORMAT
# RELATION AS FILENAME
arffContent = '@RELATION ' + relationName
arffContent += LINE_SEPERATOR
# HEADER ATTRIBUTES
for i in range(len(header)):
    arffContent += '@ATTRIBUTE '
    arffContent += header[i]
    if(i in numericColumns):
        arffContent += ' NUMERIC'
    elif i in nominalColumns:    
        arffContent += ' {'
        arffContent += ','.join(sorted(columnTypes.get(i)))
        arffContent += '}'
    else:
#         arffContent+=" date dd-MM-yy HH:mm"    
        arffContent+=' date dd-MM-yy'
    arffContent += LINE_SEPERATOR
# DATA
arffContent += '@DATA'
for i in range(len(data)):
    arffContent += LINE_SEPERATOR
    arffContent += ','.join(data[i])
print(arffContent)