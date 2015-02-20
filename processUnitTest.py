#Not sure if I need these from my project but I'll bring them in just in case
from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

from datetime import date, datetime, timedelta

import unittest

#this seems excessive but it works.
from project import calculate_weekly_wage
from project import calculate_monthly_wage
from project import calculate_yearly_wage
from project import connection
 

#Begin Test
class ProjectTestCase(unittest.TestCase):

	def setUp(self):
	
		self.connection = True
		
		
	#def test_select(self):
	#	self.assertEquals(queryResult, self.expected, "Test Failed. Query returned: \n " + queryResult)
		
	def test_connection(self):
		print("Testing connection...")
		self.assertEquals(connection, self.connection, "Test Failed, not connected to database")
		print("Passed\n")
		
	#def test_employees(self):
	#	startDate = date(2015, 2, 19)
	#	endDate = date(2016, 12, 31)
	#	result = add_employees(cursor, "Matthew", "Martin", 1, startDate, 'M', endDate)
	#	assertEquals = (result, "Martin, Matthew, id#1 was hired on 19 Feb 2015", "Failed, returned " + result)
		#add_employees(cursor, firstName, lastName, emp_no, hire, gender, fire)
		
	#def test_salary(self):
	#	print ("place holder")
	
	def test_weekly_calculator(self):
		print("Testing Weekly Wage Calculator...")
		calculation = calculate_weekly_wage(50)
		self.assertEquals(calculation, 250, "not working")
		print("Passed\n")
		
	def test_monthly_calculator(self):
		print("Testing Monthly Wage Calculator...")
		
		calculation = calculate_monthly_wage(50,1)
		self.assertEquals(calculation, 1550, "Incorrectly calculated monthly wage for January, returned " + str(calculation) )
		calculation = calculate_monthly_wage(50,2)
		self.assertEquals(calculation, 1400, "Incorrectly calculated monthly wage for February" )
		calculation = calculate_monthly_wage(50,3)
		self.assertEquals(calculation, 1550, "Incorrectly calculated monthly wage for March" )
		calculation = calculate_monthly_wage(50,4)
		self.assertEquals(calculation, 1500, "Incorrectly calculated monthly wage for April" )
		calculation = calculate_monthly_wage(50,5)
		self.assertEquals(calculation, 1550, "Incorrectly calculated monthly wage for May" )
		calculation = calculate_monthly_wage(50,6)
		self.assertEquals(calculation, 1500, "Incorrectly calculated monthly wage for June" )
		calculation = calculate_monthly_wage(50,7)
		self.assertEquals(calculation, 1550, "Incorrectly calculated monthly wage for July" )
		calculation = calculate_monthly_wage(50,8)
		self.assertEquals(calculation, 1550, "Incorrectly calculated monthly wage for August" )
		calculation = calculate_monthly_wage(50,9)
		self.assertEquals(calculation, 1500, "Incorrectly calculated monthly wage for September" )
		calculation = calculate_monthly_wage(50,10)
		self.assertEquals(calculation, 1550, "Incorrectly calculated monthly wage for October" )
		calculation = calculate_monthly_wage(50,11)
		self.assertEquals(calculation, 1500, "Incorrectly calculated monthly wage for November" )
		calculation = calculate_monthly_wage(50,12)
		self.assertEquals(calculation, 1550, "Incorrectly calculated monthly wage for December" )
		calculation = calculate_monthly_wage(50,13)
		self.assertEquals(calculation, 0, "Incorrectly calculated monthly wage for December" )
		

		print("Passed")
		
	def test_yearly_calculator(self):
		print("Testing Yearly Wage Calculator...")
		calculation = calculate_yearly_wage(50)
		self.assertEquals(calculation, 16700, "Incorrectly calculated yearly wage.")
		print("Passed\n")

	
	#def test_dates(self):
		#queryResult = query_database(cursor, self.selectQuery, date(1999, 1, 1), date(2015, 2, 18))
		#self.assertEquals(queryResult, self.expected, "Test Failed. Query returned: \n " + queryResult)
		
	def tearDown(self):
		print("Ending test")
	
if __name__ == '__main__':
	unittest.main()