import pandas as pd


#linking to database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("leaving-cert-database-a27d6-firebase-adminsdk-fbsvc-7c9e2b0b52.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://leaving-cert-database-a27d6-default-rtdb.europe-west1.firebasedatabase.app/'})



#opening csv file using pandas
df = pd.read_csv('mentalillnessspreadsheet.csv',encoding = 'ANSI') # opens csv file same way youd read it normally and stores it as a dataframe (df)

columns = str(df.columns) # stores names of columns (keys of the table dictionary)
print(columns)


# shortening/simplifying column names using the rename function
df = df.rename(columns={'Entity' : 'Country',
                        'Schizophrenia disorders (share of population) - Sex: Both - Age: Age-standardized' : 'Schizophrenia disorders',
                        'Depressive disorders (share of population) - Sex: Both - Age: Age-standardized' : 'Depressive disorders',
                        'Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized' : 'Anxiety disorders',
                        'Bipolar disorders (share of population) - Sex: Both - Age: Age-standardized' : 'Bipolar disorders',
                        'Eating disorders (share of population) - Sex: Both - Age: Age-standardized' : 'Eating disorders'})
columns = str(df.columns) # saving the changes to the columns variable
print(columns)
print('')



# checking for missing data
print(df.isnull().any()) # to see what rows contain missing data
print(df.isnull().sum()) # to see how many empty values in each row
print('')



#to deal with missing data in 'Code' column
CodeRows = list(df['Code']) # list of all values in 'Code' column
CodeRowsCheck = list(df['Code'].isnull()) # list containing boolean values for all the rows in the 'Code' column, returning whether data is missing or not
print(CodeRowsCheck)

CodeEmptyRows = [] # in this list i will store the indexes of the empty rows in the 'Code' column so i can deal with them 

for x in range(len(CodeRowsCheck)): # using a for loop to add the indexes of all empty rows to a list
    if CodeRowsCheck[x] == True:
        CodeEmptyRows.append(x)

useless = []
emptycountries = ['Australia'] # a list containting the names of the countries / states with no Code values
countries = list(df['Country'])
for x in CodeEmptyRows: 
    current = str(countries[x])
    if countries[x] not in emptycountries and 'IHME' in current:
        emptycountries.append(countries[x])
    else:
        useless.append(countries[x])
'''
I used the above loop to check what countries were missing a code. After reading through the
 results, i found that the only rows missing a code were ones with information for continents, the 
 European Union and income classifiactions (High income countries, low income, lower-middle and upper-middle).
I decided to store the continents alongside the country of Australia seperately from the countries (to show continent data in a seperate chart) ,
 and to drop the rest of the rows.
'''

def datastoring(dic): # a function that returns the data in each row in a dictionary with the corresponding headers
    if dic[0] in emptycountries:
        ccode = 'NaN'
    else:
        ccode = dic[1]
    f1 = 0.0
    f2 = 0.0
    f3 = 0.0
    f4 = 0.0
    f5 = 0.0
    f6 = 0.0
    
    f1 += dic[2]
    f2 += dic[3]
    f3 += dic[4]
    f4 += dic[5]
    f5 += dic[6]
    f6 += dic[7]
    out = {'Country'                 : dic[0],
           'Code'                    : ccode,
           'Year'                    : f1,
           'Schizophernia disorders' : f2,
           'Depressive disorders'    : f3,
           'Anxiety disorders'       : f4,
           'Bipolar disorders'       : f5,
           'Eating disorders'        : f6}
    return out

rows = [] # a list to store the values in each row in order to seperate them

for x in range(len(countries)): #adding the values to the list. i used the length of the column 'countries' to get the amount of rows
    rows.append(df.loc[x])




''' --------------------------------------------------------------------------------STORING-------------------------------------------------------------------------------------------'''



''' storing the filtered data properly:
      i decided to store the data by year, then store the
      data in each year by country/continent '''

years = {}

for y in range(30): # runs once for every yer
    world = {}
    continents = {}
    countries = {}
    currentyear = y + 1990
    
    for x in range(len(rows)): # runs for every value in 'rows' but only operates on current year
        
        if rows[x][2] == (currentyear): # operates only on current year eg: 1990, then 1991, 1992... until 2019
#             print(rows[x]) # prints all the countries in the current years
            
            if 'World' == rows[x][0]: 
                world = datastoring(rows[x]) # passes the information into the function that returns it stored as a dictionary
                
                # to check that the data from the function is returned properly
#                 for key,value in world.items():
#                     print(key, ':', value)
            
            elif rows[x][0] in emptycountries: #if the current series (rows[x]) is a continent, add to the dictionary with continent data
                continents[rows[x][0]] = datastoring(rows[x])
            
            elif rows[x][0] not in useless:
                countries[rows[x][0]] = datastoring(rows[x])
    
    #adding the information obtained for the current year to the dictionary with the data for each year
    years[currentyear] = {'World'      : world,
                          'Continents' : continents,
                          'Countries'  : countries}
#     print('-----------------')


print('done')
print(years)
# ----------------------------------- cleaning and filtering done -----------------------------------


''' --------------------------------------------------------------------------------UPLOADING TO FIREBASE-------------------------------------------------------------------------------------------'''
ref = db.reference("/years") # creating a reference to the database
ref.set(years) #uploading the data to said reference