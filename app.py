from flask import request, Flask
from flask_restplus import Api, Resource, fields
import datetime
from dbconfig import MySQLDatabase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from model import TodoDAO

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.wsgi_app = ProxyFix(app.wsgi_app)
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


DAO = TodoDAO()


@Api.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @Api.doc('list_todos')
    @Api.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos[0]

    @Api.doc('create_todo')
    @Api.expect(todo)
    @Api.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        DAO.create(api.payload)
        return DAO.todos[0]


@Api.route('/<int:id>')
@Api.response(404, 'Todo not found')
@Api.param('id', 'The task identifier')
class TodoAdd(Resource):
    '''Show a single todo item and lets you delete them'''
    @Api.doc('get_todo')
    @Api.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        for i in DAO.todos[0]:
            if i['id'] == id:
                return i
        return Api.abort(404)

    @Api.doc('delete_todo')
    @Api.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        res, todos = DAO.delete(id)
        if res['message'] == 'No todo present!':
            return '', 406
        else:
            return '', 204

    @Api.expect(todo)
    @Api.marshal_with(todo, code=201)
    def put(self, id):
        '''Update a task given its identifier'''
        print(id, api.payload)
        res = DAO.update(id, api.payload)
        if res == "Failure":
            Api.abort(400)
        else:
            return res


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
        for i in DAO.todos[0]:
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
        for i in DAO.todos[0]:
            date = i['due_by']
            if date != None and date.day < datetime.date.today().day and date.month <= datetime.date.today().month and date.year <= datetime.date.today().year:
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
        for i in DAO.todos[0]:
            stat = i['statuss']
            if stat == 'finished':
                res.append(i)
        return res


@Api.route('/authenticate')
@Api.doc(params={'username': 'Your username', 'password': 'Your password'})
class Authenticate(Resource):
    '''Authenticate users'''
    @Api.doc('authenticate_users')
    def post(self):
        q = request.get_json()
        username = q['params']['username']
        password = q['params']['password']
        # username = request.args.get('username')
        # password = request.args.get('password')
        obj = MySQLDatabase()
        obj.connectDB()
        mycur = obj.mydb.cursor()
        print(username, password)
        mycur.execute('select * from users')
        res = mycur.fetchall()
        for i in res:
            if i[1] == username and i[2] == password:
                if i[1][0] == 'a':
                    return 'Admin'
                else:
                    return 'User'
        obj.disconnectDB()
        return 'Failure'


if __name__ == '__main__':
    app.run(debug=True)


# heroku logs -a todo-backend-lokesh --tail
