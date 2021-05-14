import mysql.connector as mysql
mydb = mysql.connect(user='uoepyus8kbgfjsbu', password='yfZh18m7INgjupjSioA3',
                     database='blrnqpxk1qyh5kjvauti', host='blrnqpxk1qyh5kjvauti-mysql.services.clever-cloud.com')
print("DB Connection: ", mydb.is_connected())
