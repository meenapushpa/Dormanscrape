import mysql.connector

mydb = mysql.connector.connect(
  host="172.31.53.216",
  user="admin",
  port=3306,
  password="test1234",
  database="dormandb"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE `dormantable` (`Product Name` VARCHAR(255),`Product Info` VARCHAR(255),`Product Summary` VARCHAR(255),`Cross` VARCHAR(255),`OE ref` VARCHAR(255),`Mfr Name` VARCHAR(255),`OEdetails` VARCHAR(255))")


mycursor1 = mydb.cursor()

sql = "INSERT INTO `dormantable` (`Product Name`, `Product Info`,`Product Summary`,`Cross`,`OE ref`,`Mfr Name`,`OEdetails`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
val = ('TI86080XL', 'Steering Tie Rod End','Application Summary: Ford 2020-14, Lincoln 2020-15','DIRECT INTERCHANGE CROSS','MEF315','FORD MOTOR COMPANY','FL3Z3280A:FORD MOTOR COMPANY')
mycursor1.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")

