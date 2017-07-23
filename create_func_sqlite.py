import sqlite3
import datetime


import dateutil.parser

def isoweek_text(texte):
    ladate = dateutil.parser.parse(texte)
    return str(ladate.isocalendar()[1])

def isoweek(text):
    return "pouet"



db = sqlite3.connect(':memory:',detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
c = db.cursor()
db.create_function("isoweek", 1, isoweek)
c.execute('''create table t (id INTEGER PRIMARY KEY, created_at DATE)''')
today = datetime.date.today()
c.execute('''insert into t(created_at)  VALUES (?) ''', (today,))
db.commit()
c.execute('''select created_at from t''')
row = c.fetchone()

print("preuve que format ok: la date est un format date{0} et la date est {1}".format(type(row[0]), row[0]))

print(isoweek(datetime.date(2014,1,1)))
db.close()

db = sqlite3.connect(':memory:')
c = db.cursor()
db.create_function("isoweek", 1, isoweek)
c.execute('''create table t (id INTEGER PRIMARY KEY, created_at DATE)''')
today = datetime.date.today()
c.execute('''insert into t(created_at)  VALUES (?) ''', (today,))
db.commit()
c.execute('''select created_at from t''')
row = c.fetchone()

print("pareil sans les decls de type en mem: la date est un format date{0} et la date est {1}".format(type(row[0]), row[0]))


db = sqlite3.connect(':memory:')
c = db.cursor()
db.create_function("isoweek", 1, isoweek)
c.execute('''create table t (id INTEGER PRIMARY KEY, created_at TEXT )''')
today = datetime.date.today()
c.execute('''insert into t(created_at)  VALUES (date(?)) ''', (today,))
db.commit()
c.execute('''select created_at, typeof(created_at) from t''')
row = c.fetchone()

print("pareil sans les decls de type en mem et avec des types natifs et les transpileurs entree sqlite (sortie pas nécess pour txt): la date est un format date{0} et la date est {1}, le type annoncé par sqlite est {2}".format(type(row[0]), row[0], row[1]))


#c.execute(""" select isoweek((? as [date]))""", (datetime.date(2016,1,1),)).fetchall()
#c.execute("""select ('? as [date]')""", (datetime.datetime(2016,1,1),)).fetchall()
#sqlite3.OperationalError: user-defined function raised exception


db = sqlite3.connect(':memory:')
c = db.cursor()
db.create_function("isoweek", 1, isoweek)
c.execute('''create table t (id INTEGER PRIMARY KEY, created_at REAL )''')
now = datetime.datetime.now()
c.execute('''insert into t(created_at)  VALUES (julianday(?)) ''', (now,))
db.commit()
c.execute('''select created_at, typeof(created_at) from t''')
row = c.fetchone()

print("pareil sans les decls de type en mem et avec des types natifs et les transpileurs entree sqlite (transpileur sortie nécess pour real: sortie pas human readable. preuve): la date est un format date{0} et la date est {1}, le type annoncé par sqlite est {2}".format(type(row[0]), row[0], row[1]))



db = sqlite3.connect(':memory:')
c = db.cursor()
db.create_function("isoweek", 1, isoweek)
c.execute('''create table t (id INTEGER PRIMARY KEY, created_at REAL )''')
now = datetime.datetime.now()
c.execute('''insert into t(created_at)  VALUES (julianday(?)) ''', (now,))
db.commit()
c.execute('''select created_at, typeof(created_at), date(created_at), typeof(date(created_at)) from t''')
row = c.fetchone()

print(""" created_at est de format {} pour python et vaut {} non human readable, annoncé de format {} par sqlite""".format(type(row[0]), row[0], row[1]))
print(""" date(created_at) est de format {} pour python et vaut {} human readable annoncé de format {} par sqlite""".format(type(row[2]), row[2], row[3]))



# experience avec isoweek claquant du natif:

db = sqlite3.connect(':memory:')
c = db.cursor()
db.create_function("isoweek_text", 1, isoweek_text)
c.execute('''create table t (id INTEGER PRIMARY KEY, created_at DATE)''')
today = datetime.date.today()
c.execute('''insert into t(created_at)  VALUES (?) ''', (today,))
db.commit()
c.execute('''select created_at, isoweek_text(created_at) from t''')
row = c.fetchone()

print("""experience de create_func avec les types natifs (sans les decls de type en mem): la date est un format date{0} et la date est {1}. isoweek_text {2} doit renvoyer du texte {3} pour python""".format(type(row[0]), row[0], row[1], type(row[1])))





          
