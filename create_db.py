import sqlite3

# db initializer
conn = sqlite3.connect('data.db')
print("Opened database successfully")

# raw data
user = ["'John'", "'Jane'", "'Bob'"]
item = ["'Dino'", "'Boat'", "'Octopus'"]
order = ["'1', '1', '1'", "'2', '1', '2'", "'3', '2', '1'"]

# create tables
conn.execute("CREATE TABLE user (userId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, userName TEXT);")
conn.execute("CREATE TABLE item (itemId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, itemName TEXT);")
conn.execute("CREATE TABLE orders (orderId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, itemId TEXT, userId TEXT, amount TEXT);")
print("Created tables successfully")

# insert data
for x in user:
    conn.execute("INSERT INTO user (userName) VALUES (" + x + ");")

for x in item:
    conn.execute("INSERT INTO item (itemName) VALUES (" + x + ");")

for x in order:
    conn.execute("INSERT INTO orders (itemId, userId, amount) VALUES (" + x + ");")

print("Inserted data successfully")

# commit all changes to the database, otherwise they will be lost
conn.commit()

# close the connection
conn.close()
print("Database created successfully")