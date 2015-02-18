from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

from datetime import date, datetime, timedelta

DB_NAME = 'projecttest'

TABLES = {}

TABLES['employees'] = (
	"CREATE TABLE `employees` ("
	"`emp_no` int(11) NOT NULL AUTO_INCREMENT,"
	"`birth_date` date NOT NULL,"
	"`first_name` varchar(14) NOT NULL,"
	"`last_name` varchar(16) NOT NULL,"
	"`gender` enum('M', 'F') NOT NULL,"
	"`hire_date` date NOT NULL,"
	"PRIMARY KEY (`emp_no`)"
	") ENGINE=InnoDB")

TABLES['departments'] = (
	"CREATE TABLE `departments` ("
	"`dept_no` char(4) NOT NULL,"
	"`dept_name` varchar(40) NOT NULL,"
	"PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
	") ENGINE=InnoDB")
	
TABLES['salaries'] = (
    "CREATE TABLE `salaries` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `salary` int(11) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
    "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")
	
connection = False;


cnx = mysql.connector.connect(user='root',password='password', database='projecttest')
cursor = cnx.cursor()

connection = True;

queryResult = ""

tomorrow = datetime.now().date() + timedelta(days=1)
dayAfter = datetime.now().date() + timedelta(days=2)
oneDayMore = datetime.now().date() + timedelta(days=3)

add_employee = ("INSERT into EMPLOYEES "
				"(first_name, last_name, hire_date, gender, birth_date)"
				"VALUES (%s, %s, %s, %s, %s)")
				
add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")
				
data_employee1 = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))
data_employee2 = ('Cory', 'JJ', tomorrow, 'M', date(1993, 5, 11))
data_employee3 = ('Madigan', 'Peter', dayAfter, 'M', date(1993, 11, 14))
data_employee4 = ('Ronayne', 'Evan', oneDayMore, 'M', date(1987, 4, 14))

select_query = ("SELECT first_name, last_name, hire_date FROM employees "
				 "WHERE hire_date BETWEEN %s AND %s")

hire_start = date(1999, 1, 1)
hire_end = date(2016, 12, 31)

def create_database(cursor):
	try:
		cursor.execute(
		"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
	except mysql.connector.Error as err:
		print("Failed creating database: {}".format(err))
		exit(1)
		
def query_database(cursor, query, startDate, endDate):
	try:		 
		cursor.execute(query, (startDate, endDate))
		result = "";
		for (first_name, last_name, hire_date) in cursor:
			result += "{}, {} was hired on {:%d %b %Y}".format(
			last_name, first_name, hire_date) + "\n"
		#print(result) for testing purposes
		return result
	except mysql.connector.Error as err:
		print("Failed querying database: {}".format(err))
		exit(1)
		
def drop_tables(cursor):
	try:
		query1 = ("drop table if exists employees")
		query2 = ("drop table if exists departments")
		query3 = ("drop table if exists salaries")
		
		cursor.execute(query3)
		cursor.execute(query2)
		cursor.execute(query1)
		
	except mysql.connector.Error as err:
		print("Failed dropping tables: {}".format(err))
		exit(1)
try:
	cnx.database = DB_NAME
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_BAD_DB_ERROR:
		create_database(cursor)
		cnx.database = DB_NAME
	else:
		print(err)
		exit(1)

for name, dd1 in TABLES.iteritems ():
	try:
		print("Creating table {}: ".format(name), end='')
		cursor.execute(dd1)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
			print("already exists.")
		else:
			print(err.msg)
	else:
		print("OK")
		
#Insert new employee
cursor.execute(add_employee, data_employee1)
cursor.execute(add_employee, data_employee2)
cursor.execute(add_employee, data_employee3)
cursor.execute(add_employee, data_employee4)

emp_no = cursor.lastrowid

#Insert salary information


data_salary = {
  'emp_no': emp_no,
  'salary': 50000,
  'from_date': tomorrow,
  'to_date': date(9999, 1, 1),
}

cursor.execute(add_salary, data_salary)

queryResult = query_database(cursor,select_query,hire_start,hire_end)
print("for testing purposes")
print(queryResult)
drop_tables(cursor)
	

cnx.commit()
cursor.close()
cnx.close()