import psycopg2

#####################################################
# Database Connection
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
        """
        conn = psycopg2.connect(database=userid,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)
        """
        conn = psycopg2.connect(database='9120',
                                user='charles',
                                password='charles',
                                host='43.134.49.254')

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


def list_to_dict(data, decs):
    decs = (list(map(lambda x: x[0], decs)))
    result = [dict(zip(decs, row)) for row in data]
    return result


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
    try:
        # searchString = searchString.strip()
        conn = openConnection()
        cursor = conn.cursor()
        SQL_query = "SELECT * FROM findadmissionsbycriteria(%s)"
        cursor.execute(SQL_query, (searchString,))
        result = cursor.fetchall()
        return list_to_dict(result, cursor.description)
    except Exception as e:
        print(e)
        return []
    finally:
        cursor.close()
        conn.close()


'''
Add a new addmission
'''


def addAdmission(type_, department_, patient_, condition, admin):
    try:
        conn = openConnection()
        cursor = conn.cursor()
        SQL_query = """
        SELECT * FROM addadmission(%s, %s, %s, %s, %s)
        """
        cursor.execute(SQL_query, (type_, department_,
                       patient_, condition, admin))
        conn.commit()
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()


'''
Update an existing admission
'''
def updateAdmission(id, type, department, dischargeDate, fee, patient, condition):
    try:
        conn = openConnection()
        cursor = conn.cursor()

        SQL_query = """
        UPDATE Admission
        SET
            AdmissionType = (SELECT AdmissionTypeID FROM AdmissionType WHERE LOWER(AdmissionTypeName) = LOWER(%s)),
            Department = (SELECT DeptID FROM Department WHERE LOWER(DeptNAME) = LOWER(%s)),
            DischargeDate = %s,
            Fee = %s,
            Patient = (SELECT PatientID FROM Patient WHERE LOWER(PatientID) = LOWER(%s)),
            Condition = %s
        WHERE AdmissionID = %s
        """

        cursor.execute(SQL_query, (type, department, dischargeDate, fee, patient, condition, id))

        conn.commit()

        if cursor.rowcount > 0:
            print(f"Admission record with ID {id} updated successfully.")
            return True
        else:
            print(f"No admission record found with ID {id}.")
            return False

    except Exception as e:
        print(f"Error during admission update: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

