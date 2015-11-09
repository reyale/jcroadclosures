import datetime
import tornado.ioloop
import tornado.web
import json
from dateutil.parser import parse

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

class AddHandler(tornado.web.RequestHandler):
    def get(self):
        pass 

    def post(self, data=None):
        data = self.request.body
        json_data = json.loads(self.request.body)
        for entry in json_data:
          if 'date' not in entry:
            continue
          if 'origin' not in entry:
            continue
          if 'destination' not in entry:
            continue
          if 'comment' not in entry:
            continue
 
          try:
            date_string = entry['date'].encode('ascii', 'ignore')
            date_string = date_string[:10]
            date_string = datetime.datetime.strptime(date_string,'%Y-%m-%d').strftime('%Y%m%d')
          except:
            continue
          database.add(entry['origin'], entry['destination'], date_string, entry['comment'])

def make_app():
    return tornado.web.Application([
        (r"/get_data(.*)", DBHandler),
        (r"/entry(.*)", EntryHandler),
        (r"/add(.*)", AddHandler),
        (r"/", MainHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
