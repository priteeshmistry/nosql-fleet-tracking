import mysql.connector

print("Getting vehicles from MySQL...\n")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password123",
    database="fleet_sql"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM vehicles")
results = mycursor.fetchall()

print("VEHICLE ID\tLICENSE PLATE\tSTATUS")
print("----------------------------------------")

for row in results:
    print(f"{row[0]}\t\t{row[1]}\t{row[2]}")

mycursor.close()
mydb.close()