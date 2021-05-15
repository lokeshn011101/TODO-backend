from flask import request, Flask
from flask_restplus import Api, Resource, fields
import datetime
from dbconfig import mydb
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
          description='A simple TodoMVC API',
          )

Api = api.namespace('todos', description='TODO operations')

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

    def execute_cursor(self, sql, val=None):
        mycur = mydb.cursor()
        if val != None:
            mycur.execute(sql, val)
        else:
            mycur.execute(sql)
        mydb.commit()

    def fetch_data(self):
        todos = []
        mycur = mydb.cursor()
        sql = "select * from todo"
        mycur.execute(sql)
        res = mycur.fetchall()
        for i in res:
            curt = {"id": i[0], "task": i[1], "due_by": i[2], "statuss": i[3]}
            todos.append(curt)
        self.counter = len(todos)
        return todos

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data, id=None):
        print(data)
        todo = data
        if(todo.get('id') == None and id == None):
            todo['id'] = self.counter = self.counter + 1
        elif(todo.get('id') == None and id != None):
            todo['id'] = id

        sql = ""
        val = ()

        if todo.get('statuss') == None:
            todo['statuss'] = 'not_started'

        if todo.get('due_by') == None or todo.get('due_by') == '':
            sql = f"insert into todo(id, task, statuss) values (%s, %s, %s)"
            val = (todo['id'], todo['task'], todo['statuss'])
        else:
            sql = f"insert into todo(id, task, due_by, statuss) values (%s, %s, %s, %s)"
            val = (todo['id'], todo['task'], todo['due_by'], todo['statuss'])

        self.execute_cursor(sql, val)
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
            self.execute_cursor(sql)
            self.todos = self.fetch_data()
            return {"message": "Successfully Deleted!"}
        else:
            return {"message": "No todo present!"}


DAO = TodoDAO()


@Api.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @Api.doc('list_todos')
    @Api.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @Api.doc('create_todo')
    @Api.expect(todo)
    @Api.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        print(api)
        DAO.create(api.payload)
        return DAO.todos


@Api.route('/<int:id>')
@Api.response(404, 'Todo not found')
@Api.param('id', 'The task identifier')
class TodoAdd(Resource):
    '''Show a single todo item and lets you delete them'''
    @Api.doc('get_todo')
    @Api.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @Api.doc('delete_todo')
    @Api.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        res = DAO.delete(id)
        if res['message'] == 'No todo present!':
            return '', 406
        else:
            return '', 204

    @Api.expect(todo)
    @Api.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


@Api.route('/due')
@Api.doc(params={'due_date': 'A string which is a date of format YYYY-MM-DD'})
class TodoGetOverdue(Resource):
    '''Show a todo items which are due to be finished on this date'''
    @Api.doc('get_todo_due')
    @Api.marshal_with(todo)
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


@Api.route('/overdue')
class TodoGetOverdue(Resource):
    '''Show a todo items which are overdue'''
    @Api.doc('get_todo_overdue')
    @Api.marshal_with(todo)
    def get(self):
        '''Fetch a given resource with status as overdue'''
        res = []
        for i in DAO.todos:
            date = i['due_by']
            if date < datetime.date.today():
                res.append(i)
        return res


@Api.route('/finished')
class TodoGetFinished(Resource):
    '''Show a single todo item which are finished'''
    @Api.doc('get_todo')
    @Api.marshal_with(todo)
    def get(self):
        '''Fetch a given resource with status as finished'''
        res = []
        for i in DAO.todos:
            stat = i['statuss']
            if stat == 'finished':
                res.append(i)
        return res


@Api.route('/authenticate')
@Api.doc(params={'username': 'Your username', 'password': 'Your password'})
class Authenticate(Resource):
    '''Authenticate users'''

    def post(self):
        username = request.args.get('username')
        password = request.args.get('password')
        mycur = mydb.cursor()
        mycur.execute('select * from users')
        res = mycur.fetchall()
        for i in res:
            if i[1] == username and i[2] == password:
                if i[1][0] == 'a':
                    return 'Admin'
                else:
                    return 'User'
        return 'Failure'


if __name__ == '__main__':
    app.run(debug=True)
