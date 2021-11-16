#SFM November, 2021
import sqlite3
import re

defaultFileName = 'mbox.txt'
count = dict()
connectedToDatabase = False

try:
    # Try to connect in the database
    conn = sqlite3.connect('countOrg.sqlite')
    cur = conn.cursor()
    connectedToDatabase = True
except Exception as e:
   
    print(e)

if connectedToDatabase:
    #Make sure the table is deleted before start the execution
    cur.execute(""" DROP TABLE IF EXISTS Counts """)

    #Create the table
    cur.execute("""CREATE TABLE Counts (org TEXT, count INTEGER)""")


#Request file to be opened
fileName = input("Enter file name:")
print (fileName)
if len(fileName) <1:
    print('The user did not provide a file name using the default file', defaultFileName)
    fileName = defaultFileName

#Open the file
fileHandle = open(fileName)

#process in memory the number of organization email
print("Processing file")
for line in fileHandle:
    line = line.rstrip()
    '''
        extact the organization:
        Get all emails that starts with From and after @ sign get anything that is between a-z A-Z 0-9 and it is before the first . sign
    '''
    #emails = re.findall('^From:.+@([a-zA-Z0-9]+)[.]?', line) working, but if incomplete domain
    emails = re.findall('^From:.+@([a-zA-Z0-9.]+)', line) 

    if len(emails) > 0:
        #the result is a list, get the first item only
        count[emails[0]] = count.get(emails[0],0) +1
        #print(email)
            
#convert dictionary values to import to sql
keyvalues = ', '.join("'" + str(x).replace('/','_')  + "'" for x in count.keys())
values = ', ' .join( str(y) for y in count.values())
#print (values)
#print(keyvalues) 

#if sql connection exists, add the data into sql table
if  connectedToDatabase:
    print("Inserting the data into database...")
    for key, value in count.items():
        #print('key ->', key, 'value->' , value)
        #sqlInsert = 'INSERT INTO Counts(org, count) VALUES (?, ?)', (key,value)
        cur.execute('INSERT INTO Counts(org, count) VALUES (?, ?)', (key,value))
   
    
conn.commit()
cur.close()
