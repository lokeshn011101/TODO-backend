from CRUDdb import CRUDdb


class TodoDAO(object):
    def __init__(self):
        self.cruddb = CRUDdb()
        self.todos = self.cruddb.fetch_data()
        self.counter = len(self.todos)

    def get_all(self):
        return self.cruddb.get_all()

    def get(self, id):
        res = self.cruddb.get(id)
        if res == None:
            return 'No data found'
        return res

    def create(self, data):
        self.cruddb.insert(data)
        self.todos = self.cruddb.fetch_data()
        return self.todos

    def update(self, id, data):
        self.cruddb.update(id, data)
        self.todos = self.cruddb.fetch_data()

    def delete(self, id):
        res = self.cruddb.delete(id)
        self.todos = self.cruddb.fetch_data()
        return res, self.todos


# o = TodoDAO()
# print(o.delete(4))
# print(o.create({'id': 4, 'task': 'sdfds'}))
