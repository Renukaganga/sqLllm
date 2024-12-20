import mysql.connector

# Connect to MySQL (running in XAMPP)
connection = mysql.connector.connect(
    host="localhost",     # XAMPP MySQL host
    user="root",          # Default MySQL user in XAMPP
    password="",          # Default MySQL password is empty
    database="spring"      # Replace with your database name
)

# Create a cursor object
cursor = connection.cursor()

# Create the table
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""
cursor.execute(table_info)

# Insert some records
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Krish', 'Data Science', 'A', 90)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Sudhanshu', 'Data Science', 'B', 100)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Darius', 'Data Science', 'A', 86)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Vikash', 'DEVOPS', 'A', 50)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Dipesh', 'DEVOPS', 'A', 35)")

# Display all the records
print("The inserted records are:")
cursor.execute("SELECT * FROM STUDENT")
for row in cursor.fetchall():
    print(row)

# Commit the changes and close the connection
connection.commit()
connection.close()
