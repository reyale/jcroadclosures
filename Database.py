import os
import sqlite3
import json

#TODO - good enough for now
_rel = os.path.dirname(__file__)
if not _rel:
  _const_db_file = './closings.db'
else:
  _const_db_file = _rel + '/closings.db'

def _create_or_get_db(fname):
  if not os.path.exists(fname):
    conn = sqlite3.connect(fname)
    c = conn.cursor()
    c.execute("CREATE table closings (INTEGER PRIMARY KEY, origin, destination, date, text, active BOOLEAN)")
    conn.commit()
    return conn 
  return sqlite3.connect(fname)

def db_to_json(closing_db, date):
  closings = closing_db.get(date)
  results = [ ]
  for closing in closings:
    entry = { }
    entry['origin'] = closing[1] 
    entry['destination'] = closing[2]
    entry['text'] = closing[4].encode('ascii', 'ignore') #no more unicode
    results.append(entry) 
  return json.dumps(results)

class Closings:
  def __init__(self):
    self.conn = _create_or_get_db(_const_db_file) 

  def __del__(self):
    self.conn.close()

  def add(self, origin, destination, date, text):
    c = self.conn.cursor()
    c.execute("INSERT INTO closings VALUES(NULL, '%s', '%s', '%s', '%s', 1)" % (origin, destination, date, text))
    self.conn.commit() 

  def get(self, date):
    c = self.conn.cursor()
    return c.execute("SELECT * FROM closings WHERE date='%s' and active=1" % date) 

#c = Closings()
#c.add("40.720072, -74.045233", "40.718852, -74.045898", "20150101", "test closing 1")
#c.add("40.71905, -74.043095", "40.717548, -74.044103", "20150101", "test closing 2")
#for d in c.get('20150101'):
#  print d
