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


				
add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")
				

select_query = ("SELECT emp_no, first_name, last_name, hire_date FROM employees "
				 "WHERE hire_date BETWEEN %s AND %s")
				 
salary_query = ("SELECT emp_no, salary FROM salaries ")

hire_start = date(1999, 1, 1)
hire_end = date(2016, 12, 31)

#Create database stuff, mostly from the connector
def create_database(cursor):
	try:
		cursor.execute(
		"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
	except mysql.connector.Error as err:
		print("Failed creating database: {}".format(err))
		exit(1)
	
#Used to print out employees	
def query_database(cursor, query, startDate, endDate):
	try:		 
		cursor.execute(query, (startDate, endDate))
		result = "";
		for (first_name, last_name, emp_no, hire_date) in cursor:
			result += "{}, {}, id#{} was hired on {:%d %b %Y}".format(
			emp_no, last_name, first_name, hire_date) + "\n"
		#print(result) for testing purposes
		return result
	except mysql.connector.Error as err:
		print("Failed querying database: {}".format(err))
		exit(1)
		
#Used to print out employees	
def query_salaries(cursor, query):
	try:		 
		cursor.execute(query)
		result = "";
		for (emp_no, salary) in cursor:
			result += "{}'s weekly salary is {}".format(
			emp_no, salary) + "\n"
		#print(result) for testing purposes
		return result
	except mysql.connector.Error as err:
		print("Failed querying database: {}".format(err))
		exit(1)

#Starts fresh at the end of the program, gets rid of all the tables
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

def add_employees(cursor, firstName, lastName, emp_no, hire, gender, fire):
	add_employee = ("INSERT into EMPLOYEES "
				"(first_name, last_name, emp_no, hire_date, gender, birth_date)"
				"VALUES (%s, %s, %s, %s, %s, %s)")
	
	data_employee = (firstName, lastName, emp_no, hire, gender, fire)
	cursor.execute(add_employee, data_employee)
	
	queryString = "{}, {}, id#{} was hired on {:%d %b %Y}".format(
			emp_no, lastName, firstName, hire)
	return queryString
	
def add_salaries(cursor, emp_no, salary, from_date, to_date):

	add_salary = ("INSERT into SALARIES "
				"(emp_no, salary, from_date, to_date)"
				"VALUES (%s, %s, %s, %s)")
				
	data_salary = (emp_no, salary, from_date, to_date)
	cursor.execute(add_salary, data_salary)
	
	return salary
	
def calculate_weekly_wage(daily):
	weekly = daily * 5
	return weekly
		
# HERE for all intents and purposes is main

def main():

	#Connect to the DB
	try:
		cnx.database = DB_NAME
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_BAD_DB_ERROR:
			create_database(cursor)
			cnx.database = DB_NAME
		else:
			print(err)
			exit(1)

	#Create all the tables
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
			
	#Put in some basic IO. Raw input or no? Gonna try raw first
	running = True

	while running:

		print ("1. Add an Employee")
		print ("2. Calculate and Set an Employee's Weekly Wage")
		print ("3. Exit")
		response = int(raw_input("Select an action: ")) 

		if response == 1:
			notDone = True;
			while notDone:
				enteredLast = raw_input("Please enter the employee's last name: ")
				enteredFirst = raw_input("Please enter the employee's first name: ")
				enteredId = raw_input("Please enter the employee's id number: ")
				#enteredHiredDate = raw_input("Please enter the employee's name: ")
				#enteredGender = raw_input("Please enter the employee's gender: ")
				#enteredFireDate raw_input("Please enter the employee's name: ")

				add_employees(cursor, enteredFirst, enteredLast, enteredId, tomorrow, 'M', date(1997, 6, 14))
				
				response = str(raw_input("Would you like to enter another user? (Y/N): ")).upper()

				if response == "N":
					notDone = False
		elif response == 2:
			emp_no = int(raw_input("Please enter the employee's id: "))
			salary = int(raw_input("Please enter the desired daily pay: "))
			add_salaries(cursor, emp_no, salary, tomorrow, date(1997, 6, 14))
		elif response == 3:
			running = False


			


	emp_no = cursor.lastrowid

	#Insert salary information


	#data_salary = {
	 # 'emp_no': emp_no,
	  #'salary': 50000,
	  #'from_date': tomorrow,
	  #'to_date': date(9999, 1, 1),
	#}

	#cursor.execute(add_salary, data_salary)

	queryResult = query_database(cursor,select_query,hire_start,hire_end)
	print("for testing purposes")
	print(queryResult)
	queryResult = query_salaries(cursor, salary_query)
	print(queryResult)
	drop_tables(cursor)
		

	cnx.commit()
	cursor.close()
	cnx.close()
	
if __name__ == '__main__':	
	main()
else:
	print("Testing...")