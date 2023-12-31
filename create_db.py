import sqlite3

# db initializer
conn = sqlite3.connect('data.db')
print("Opened database successfully")

# raw data
task = ["'Water', 'Plants', 'False'", "'Homework', 'basic API', 'False'", "'Make food', 'Belgian Fries with Pork tenderloin with mushroom sauce', 'False'"]

# create tables
conn.execute("CREATE TABLE task (taskId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, taskTitle TEXT, taskDescription TEXT, taskDone BOOL);")
print("Created tables successfully")

# insert data
for x in task:
    conn.execute("INSERT INTO task (taskTitle, taskDescription, taskDone) VALUES (" + x + ");")

print("Inserted data successfully")

# commit all changes to the database, otherwise they will be lost
conn.commit()

# close the connection
conn.close()
print("Database created successfully")