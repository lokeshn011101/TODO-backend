import mysql.connector as mysql

mydb = mysql.connect(user='root', password='1234',
                     database='todoapp', host='localhost')

print("DB Connection: ", mydb.is_connected())

mycur = mydb.cursor()

mycur.execute("select * from todo")

res = mycur.fetchall()

for x in res:
    print(x)

sql = f"insert into todo(id, task, statuss) values (%s, %s, %s)"
val = (11, 'hello', 'not_started')
mycur = mydb.cursor()
mycur.execute(sql, val)


mycur.execute("select * from todo")

res = mycur.fetchall()

for x in res:
    print(x)
