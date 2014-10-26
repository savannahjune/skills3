import sqlite3

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("my_melons.db")
    CONN.text_factory = str
    DB = CONN.cursor()

def read_customers(filename):
    file_text = open(filename)

    for line in file_text:
        line = line.strip()
        customer_id, first_name, last_name, email, telephone, called = line.split(',')
        query = """INSERT into Customers values (?, ?, ?, ?, ?, ?)"""
        DB.execute(query, (customer_id, first_name, last_name, email, telephone, called))
        CONN.commit()

    file_text.close()

def read_orders(filename):
    file_text = open(filename)

    for line in file_text:
        line = line.strip()
        order_id, order_date, status, customer_id, email, address, city, state, postalcode, num_watermelons, num_othermelons, subtotal, tax, order_total = line.split(',')
        query = """INSERT into Orders values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        DB.execute(query, (order_id, order_date, status, customer_id, email, address, city, state, postalcode, num_watermelons, num_othermelons, subtotal, tax, order_total))
        CONN.commit()

    file_text.close()

def main():
    connect_to_db()

    read_customers("customers.csv")
    read_orders("orders.csv")

if __name__ == "__main__":
    main()

# CREATE TABLE Orders (order_id integer(30), order_date varchar(15), status varchar(15), 
# customer_id integer(10), email varchar(60), address varchar(200), city varchar(50), 
# state varchar(5), postalcode varchar(20), num_watermelons integer(100), num_othermelons integer(100), 
# subtotal decimal(5,2), tax decimal(5,2), order_total decimal(5,2));  

# CREATE TABLE Customers (customer_id integer(20), first_name varchar(30), last_name varchar(40), 
# email varchar(80), telephone varchar(20), called bool(10));  

