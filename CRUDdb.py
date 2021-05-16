from dbconfig import MySQLDatabase


class CRUDdb():

    def __init__(self):
        self.mydb = MySQLDatabase()

    def execute_cursor(self, sql, val=None):
        self.mydb.connectDB()
        mycur = self.mydb.mydb.cursor()
        if val != None:
            mycur.execute(sql, val)
        else:
            mycur.execute(sql)
        self.mydb.mydb.commit()
        self.mydb.disconnectDB()

    def fetch_data(self):
        self.mydb.connectDB()
        todos = []
        mycur = self.mydb.mydb.cursor()
        sql = "select * from todo"
        mycur.execute(sql)
        res = mycur.fetchall()
        for i in res:
            curt = {"id": i[0], "task": i[1], "due_by": i[2], "statuss": i[3]}
            todos.append(curt)
        self.mydb.disconnectDB()
        return todos, len(todos)

    def get_all(self):
        return self.fetch_data()

    def get(self, id):
        self.mydb.connectDB()
        todos, length = self.fetch_data()
        for todo in todos:
            if todo['id'] == id:
                return todo
        self.mydb.disconnectDB()
        return None

    def insert(self, data):
        todo = data
        sql = ""
        val = ()

        if todo.get('statuss') == None:
            todo['statuss'] = 'not_started'

        if todo.get('due_by') == None or todo.get('due_by') == '':
            sql = f"insert into todo(task, statuss) values (%s, %s)"
            val = (todo['task'], todo['statuss'])
        else:
            sql = f"insert into todo(task, due_by, statuss) values (%s, %s, %s)"
            val = (todo['task'], todo['due_by'], todo['statuss'])

        self.execute_cursor(sql, val)
        todos, length = self.fetch_data()

        return todos

    def update(self, id, data):
        sql = ''
        val = ()
        print(data)
        if data.get('task') != None:
            sql = f'update todo set task=%s where id=%s'
            val = (data['task'], id)
            self.execute_cursor(sql, val)
            return "Success"
        if data.get('statuss') != None:
            sql = f'update todo set statuss=%s where id=%s'
            val = (data['statuss'], id)
            self.execute_cursor(sql, val)
            return "Success"
        if data.get('due_by') != None:
            sql = f'update todo set due_by=%s where id=%s'
            val = (data['due_by'], id)
            self.execute_cursor(sql, val)
            return "Success"
        return "Failure"

    def delete(self, id):
        todos, length = self.fetch_data()
        flag = 0
        for i in todos:
            if i['id'] == id:
                flag = 1
                break
        if flag == 1:
            sql = f"delete from todo where id = {id}"
            self.execute_cursor(sql)
            todos, length = self.fetch_data()
            return {"message": "Successfully Deleted!"}
        else:
            return {"message": "No todo present!"}


# no = CRUDdb()
# print(no.get_all())
# print(no.delete(4))
# print(no.get_all())
# no.insert({'id': 4, 'task': 'sdfds'})
# print(no.get_all())
