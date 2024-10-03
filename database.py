#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################

'''
Connect to the database using the connection string
'''
def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    userid = "y24s2c9120_xihe0498"
    passwd = "Hxy5463060432&"
    myHost = "awsprddbs4836.shared.sydney.edu.au"


    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=userid,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    
    # return the connection to use
    return conn

'''
Validate staff based on username and password
'''
def checkLogin(login, password):
    # acquire the connection from database
    conn = openConnection()
    cursor = conn.cursor()
    # querying the user information from database
    SQL_query = "select username, firstname, lastname, email \
        from Administrator where username = %s and password = %s"
    cursor.execute(SQL_query, (login, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    # check if the submitting details can match the user information from 
    # the database and return the user information
    if result:
        return [result[0], result[1], result[2], result[3]]
    else:
        return None

'''
List all the associated admissions records in the database by staff
'''
def findAdmissionsByAdmin(login):
    # acquire the connection from database
    conn = openConnection()
    cursor = conn.cursor()
    # querying the related admission list 
    SQL_query = "select * from findAdmissionsByadmin(%s)"
    cursor.execute(SQL_query, (login,))
    result = cursor.fetchall()
    # Acquire the column_names
    column_name = []
    for every_row in cursor.description:
        column_name.append(every_row[0])
    display_list = []
    cursor.close()
    conn.close()
    # Transfer every row into dictionary
    for row in result:
        dictionary = {}
        for i in range(len(column_name)):
            # choose the column_name as the index and every row of the query 
            # result as its value
            dictionary[column_name[i]] = row[i]
        display_list.append(dictionary)
    return display_list

'''
Find a list of admissions based on the searchString provided as parameter
See assignment description for search specification
'''
def findAdmissionsByCriteria(searchString):

    return


'''
Add a new addmission 
'''
def addAdmission(type, department, patient, condition, admin):
    
    return


'''
Update an existing admission
'''
def updateAdmission(id, type, department, dischargeDate, fee, patient, condition):
    

    return
