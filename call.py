"""
call.py - Telemarketing script that displays the next name 
          and phone number of a Customer to call.

          This script is used to drive promotions for 
          specific customers based on their order history.
          We only want to call customers that have placed
          an order of over 20 Watermelons.

"""

import sqlite3
from time import strftime

DB = None
CONN = None

# Class definition to store our customer data
class Customer(object):
	def __init__(self, id=None, first=None, last=None, telephone=None):
		self.first = first
		self.last = last
		self.telephone = telephone
		pass

	def __str__(self):
		output = " Name: %s, %s\n" % (self.last, self.first)
		output += "Phone: %s" % self.telephone

		return output

# Connect to the Database
def connect_to_db():
	global DB, CONN
	CONN = sqlite3.connect('my_melons.db')

	DB = CONN.cursor()

def initialize_query():
	query = """SELECT Customers.customer_id, first_name, last_name, telephone FROM Customers 
			INNER JOIN Orders on Orders.customer_id = Customers.customer_id WHERE Orders.num_watermelons > 20"""
	DB.execute(query)

# Retrieve the next uncontacted customer record from the database.
# Return the data in a Customer class object.
#
# Remember: Our telemarketers should only be calling customers
#           who have placed orders of 20 melons or more.
def get_next_customer():
	row = DB.fetchone()

	while row[0] == 'customer_id': #Prevent any column headers from appearing as customer result
		row = DB.fetchone()

	print 'id ' + str(row[0]) + ' first ' + row[1] + ' last ' + row[2] + ' telephone ' + row[3]
	c = Customer(id=row[0], first=row[1], last=row[2], telephone=row[3])
	print c 
	return c 


def display_next_to_call(customer):
	print "---------------------"
	print "Next Customer to call"
	print "---------------------\n"
	print customer
	print "\n"


# Update the "last called" column for the customer
#   in the database.
def update_customer_called(customer):
	customer_id, user_answer = id_was_called
	date = strftime("%m/%d/%y")
	if user_answer == "y":
		query = """Update Customers SET called = ? WHERE customer id = ?"""
		DB.execute(query, (date, customer_id))
		CONN.commit()
		print "You called! How thoughtful!"
		update_customer_called(display_next_to_call(get_next_customer()))	
	
	elif user_answer == "n":
		print "Call someone else then!"
		update_customer_called(display_next_to_call(get_next_customer))
	else:
		print "Go home then."

def main():
	connect_to_db()
	initialize_query()
	done = False

	while not done:
		customer = get_next_customer()
		display_next_to_call(customer)

		print "Mark this customer as called?"
		user_answer = raw_input('(y/n) > ')

		if user_answer.lower() == 'y':
			update_customer_called(customer)
		else:
			done = True


if __name__ == '__main__':
	main()