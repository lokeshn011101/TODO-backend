import mysql.connector as mysql
from flask import Flask
from flask import request
from flask_restplus import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import datetime

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
          description='A simple TodoMVC API',
          )

mydb = mysql.connect(user='uoepyus8kbgfjsbu', password='yfZh18m7INgjupjSioA3',
                     database='blrnqpxk1qyh5kjvauti', host='blrnqpxk1qyh5kjvauti-mysql.services.clever-cloud.com')
print("DB Connection: ", mydb.is_connected())

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'due_by': fields.Date(required=False, description='Due by Date'),
    'statuss': fields.String(required=False, description='Status of the task')
})


class TodoDAO(object):
    def __init__(self):
        self.todos = self.fetch_data()
        self.counter = len(self.todos)

    def fetch_data(self):
        todos = []
        mycur = mydb.cursor()
        sql = "select * from todo"
        mycur.execute(sql)
        res = mycur.fetchall()
        for i in res:
            curt = {"id": i[0], "task": i[1], "due_by": i[2], "statuss": i[3]}
            todos.append(curt)
        return todos

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data, id=None):
        todo = data
        if(todo.get('id') == None and id == None):
            todo['id'] = self.counter = self.counter + 1
        elif(todo.get('id') == None and id != None):
            todo['id'] = id

        sql = ""
        val = ()

        if todo.get('statuss') == None:
            todo['statuss'] = 'not_started'

        if todo.get('due_by') == None:
            sql = f"insert into todo(id, task, statuss) values (%s, %s, %s)"
            val = (todo['id'], todo['task'], todo['statuss'])
        else:
            sql = f"insert into todo(id, task, due_by, statuss) values (%s, %s, %s, %s)"
            val = (todo['id'], todo['task'], todo['due_by'], todo['statuss'])

        mycur = mydb.cursor()
        mycur.execute(sql, val)
        mydb.commit()
        self.todos = self.fetch_data()

        return self.todos

    def update(self, id, data):
        self.delete(id)
        return self.create(data, id)

    def delete(self, id):
        flag = 0
        for i in self.todos:
            if i['id'] == id:
                flag = 1
                break
        if flag == 1:
            sql = f"DELETE FROM todo WHERE id = {id}"
            mycur = mydb.cursor()
            mycur.execute(sql)
            mydb.commit()
            self.todos = self.fetch_data()
            return {"message": "Successfully Deleted!"}
        else:
            return {"message": "No todo present!"}


DAO = TodoDAO()


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        DAO.create(api.payload)
        return DAO.todos


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class TodoAdd(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        res = DAO.delete(id)
        if res['message'] == 'No todo present!':
            return '', 406
        else:
            return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


@ns.route('/due')
class TodoGetOverdue(Resource):
    '''Show a todo items which are due to be finished on this date'''
    @ns.doc('get_todo_due')
    @ns.marshal_with(todo)
    def get(self):
        '''Fetch a given resource which are due to be finished on this date'''
        res = []
        gdate = request.args.get('due_date')
        dt = gdate.split('-')
        year = int(dt[0])
        month = int(dt[1])
        day = int(dt[2])
        gdate = datetime.date(year, month, day)
        for i in DAO.todos:
            date = i['due_by']
            if date == gdate:
                res.append(i)
        return res


@ ns.route('/overdue')
class TodoGetOverdue(Resource):
    '''Show a todo items which are overdue'''
    @ ns.doc('get_todo_overdue')
    @ ns.marshal_with(todo)
    def get(self):
        '''Fetch a given resource with status as overdue'''
        res = []
        for i in DAO.todos:
            date = i['due_by']
            if date < datetime.date.today():
                res.append(i)
        return res


@ ns.route('/finished')
class TodoGetFinished(Resource):
    '''Show a single todo item which are finished'''
    @ ns.doc('get_todo')
    @ ns.marshal_with(todo)
    def get(self):
        '''Fetch a given resource with status as finished'''
        res = []
        for i in DAO.todos:
            stat = i['statuss']
            if stat == 'finished':
                res.append(i)
        return res


if __name__ == '__main__':
    app.run(debug=True)
