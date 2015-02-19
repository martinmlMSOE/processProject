#Not sure if I need these from my project but I'll bring them in just in case
from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

from datetime import date, datetime, timedelta

import unittest

#this seems excessive but it works.
from project import calculate_weekly_wage
from project import connection
 

#Begin Test
class ProjectTestCase(unittest.TestCase):

	def setUp(self):
	
		self.connection = True
		
		
	#def test_select(self):
	#	self.assertEquals(queryResult, self.expected, "Test Failed. Query returned: \n " + queryResult)
		
	def test_connection(self):
		self.assertEquals(connection, self.connection, "Test Failed, not connected to database")
		
	#def test_employees(self):
	#	startDate = date(2015, 2, 19)
	#	endDate = date(2016, 12, 31)
	#	result = add_employees(cursor, "Matthew", "Martin", 1, startDate, 'M', endDate)
	#	assertEquals = (result, "Martin, Matthew, id#1 was hired on 19 Feb 2015", "Failed, returned " + result)
		#add_employees(cursor, firstName, lastName, emp_no, hire, gender, fire)
		
	#def test_salary(self):
	#	print ("place holder")
	
	def test_wage_calculator(self):
		calculation = calculate_weekly_wage(50)
		self.assertEquals(calculation, 250, "not working")
	
	#def test_dates(self):
		#queryResult = query_database(cursor, self.selectQuery, date(1999, 1, 1), date(2015, 2, 18))
		#self.assertEquals(queryResult, self.expected, "Test Failed. Query returned: \n " + queryResult)
		
	def tearDown(self):
		print("Ending test")
	
if __name__ == '__main__':
	unittest.main()