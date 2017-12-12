To execute the ipython notebook code or the python programs, following input files should be placed in the same directory as the programs:

1) Online_Retail.xlsx : the dataset in excel format
2) Online_Retail.csv : csv version of the dataset, with the 'description' column deleted


- AssociationRulesArffGenerator.py 
 This program generates stock code data for each invoice to arff format. Weka library is then used to identify association rules with the output file of the program.
 
- DataStatistics.py
 This program generates arff format data from the dataset. Statistics about data are found using Weka library. 


The ipython notebook 'project.ipynb' contains code and results for the following:
- Data exploration of the dataset
- K-Means clustering
- Agglomerative clustering
- Time series analysis 