import csv
import sys
''' Convert the online-retail excel sheet to csv(Online_Retail.csv) and feed as input to this program'''

filePath = "Online_Retail.csv"
invoice_stockcode_list = {}
stockcode_ids = {}

''' Prepare a map of invoice vs list of stock_codes '''
''' This is used to prepare a data with space separated stock codes for each invoice '''
''' This data will be used to generate sparse arff file '''
''' for analysis using Weka '''

with open(filePath) as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
    # EXTRACT COLUMN HEADERS    
    header = next(csvReader)
    if(len(header) == 0):
        sys.exit()
    for line in csvReader:
        data = ','.join(line).split(',')
        invoice = data[0]
        stock_code= data[1]
        # Skip Cancelled Invoices
        if 'C' in invoice:
            continue
        if stock_code not in stockcode_ids:
            id = len(stockcode_ids)
            stockcode_ids[stock_code] = id
        stock_code_id = stockcode_ids[stock_code]
        if invoice not in invoice_stockcode_list:
            invoice_stockcode_list[invoice] = list()
        invoice_stockcode_list[invoice].append(stock_code_id)

''' Iterate over the dictionary, and convert the list to a string of stock code ids '''
''' separated by space, for each invoice '''
stock_code_invoice_data = list()

for invoice in invoice_stockcode_list:
    delimeter = ''
    row = ''
    for stock_id in invoice_stockcode_list[invoice]:
        row+=delimeter
        delimeter = ' '
        row+=str(stock_id)
    stock_code_invoice_data.append(row)


def composeSpareRepresentation(features):
    sparse = '{'
    delimeter = ''
    numberSet = set(int(x) for x in features)
    for feature in sorted(numberSet):
        column = int(feature)
        sparse+=delimeter
        delimeter = ', '
        sparse+=str(column)
        sparse+=' '
        sparse+=str(1)
    sparse+='}'
    return sparse
maxFeatureColumn = -1
minFeatureColumn = sys.maxsize
data = list()

for line in stock_code_invoice_data:
        data_split = line.replace('\n','').split()
        features = list(int(f) for f in data_split)
        currentMaxFeature = int(max(features))
        currentMinFeature = int(min(features))
        maxFeatureColumn = max(currentMaxFeature, maxFeatureColumn)
        minFeatureColumn = min(minFeatureColumn, currentMinFeature)
        spareRepresentation = composeSpareRepresentation(features)
        data.append(spareRepresentation)

relationName = 'Online_Retail'

# COMPOSE ARFF FORMAT
# RELATION AS FILENAME

RELATION_HEADER = '@RELATION '
ATTRIBUTE_HEADER= '@ATTRIBUTE '
DATA_HEADER = '@DATA'
DEFAULT_FEATURE_NOMINALS = ' {0, 1}'
LINE_SEPERATOR = '\n'
arffContent =  RELATION_HEADER + relationName+LINE_SEPERATOR

# HEADER ATTRIBUTES

for i in range(minFeatureColumn, maxFeatureColumn+1):
    arffContent+=ATTRIBUTE_HEADER
    arffContent+='i'
    arffContent+= str(i)
    arffContent+=DEFAULT_FEATURE_NOMINALS
    arffContent+=LINE_SEPERATOR
arffContent+=DATA_HEADER
for i in range(len(data)):
    arffContent += LINE_SEPERATOR
    arffContent += (data[i])
print(arffContent)