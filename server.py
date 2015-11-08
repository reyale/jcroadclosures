import tornado.ioloop
import tornado.web
import json

import Database

database = Database.Closings()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class DBHandler(tornado.web.RequestHandler):
    def get(self, date=None):
        date = self.get_argument("DATE", None) 
        if not date:
          self.write(json.dumps([]))
          return

        self.write(Database.db_to_json(database, date))

class EntryHandler(tornado.web.RequestHandler):
    def get(self, data=None):
        self.render("entry.html")

def make_app():
    return tornado.web.Application([
        (r"/get_data(.*)", DBHandler),
        (r"/entry(.*)", EntryHandler),
        (r"/", MainHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
