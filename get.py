import Database

cdb = Database.Closings()
for entry in cdb.get_all():
  print entry
