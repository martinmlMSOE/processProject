#Not sure if I need these from my project but I'll bring them in just in case
from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

from datetime import date, datetime, timedelta

import unittest

#this seems excessive but it works.
import project
from project import query_database
from project import cursor
from project import cnx
from project import queryResult
from project import connection
 

#Begin Test
class ProjectTestCase(unittest.TestCase):

	def setUp(self):
		self.expected = ("Vanderkelen, Geert was hired on 19 Feb 2015\n"
					"JJ, Cory was hired on 19 Feb 2015\n"
					"Peter, Madigan was hired on 20 Feb 2015\n"
					"Evan, Ronayne was hired on 21 Feb 2015\n")
					
		self.selectQuery = ("SELECT first_name, last_name, hire_date FROM employees "
				 "WHERE hire_date BETWEEN %s AND %s")
				 
		self.connection = True
		
		
	def test_select(self):
		self.assertEquals(queryResult, self.expected, "Test Failed. Query returned: \n " + queryResult)
		
	def test_connection(self):
		self.assertEquals(connection, self.connection, "Test Failed, not connected to database")
		
	def test_dates(self):
		print("placeholder")
		#queryResult = query_database(cursor, self.selectQuery, date(1999, 1, 1), date(2015, 2, 18))
		#self.assertEquals(queryResult, self.expected, "Test Failed. Query returned: \n " + queryResult)
		
	def tearDown(self):
		cursor.close()
		cnx.close()
	
if __name__ == '__main__':
	unittest.main()