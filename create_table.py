import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,   \
                                          username text,             \
                                          password text,             \
                                          first_name text,           \
                                          last_name text,            \
                                          address text,              \
                                          phone integer,             \
                                          role  text)"
cursor.execute(query)

query = "CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY,                   \
                                           order_id,                                  \
                                           order_no INTEGER,                          \
                                           username text,                             \
                                           order_date text,                           \
                                           delivery_date text,                        \
                                           product_id text,                           \
                                           quantity INTEGER,                          \
                                           price real)"

cursor.execute(query)

query = "CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY,                 \
                                             product_id,                              \
                                             name text,                               \
                                             price real)"
cursor.execute(query)

connection.commit()
connection.close()

                                          

                                          
                                          
