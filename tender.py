#!usr/bin/python
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

from peewee import MySQLDatabase, Model, CharField, AutoField, IntegerField, DateField,\
                    DoubleField
from tkinter import *
from tkinter import ttk, LEFT, RIGHT
from tkinter import messagebox
import numpy as np
from table import Table
from form import TenderForm

from collections import namedtuple

host = 'localhost'
username = 'root'
password = 'jovanovic92'
database = 'tenderdb'

select_query = 'SELECT * FROM tender'

con = pymysql.connect(host, username, password, database)
cur = con.cursor()
cur.execute(select_query)
rows = cur.fetchall()

db = MySQLDatabase(database, user=username, passwd=password, host=host)

class BaseModel(Model):
    class Meta:
        database = db

class Tender(BaseModel):
    idtender = AutoField()
    naziv = CharField()
    tip = CharField()
    aktivan = CharField()
    datum = DateField(formats=['%d.%m.%Y'])
    proc_vred = DoubleField()
    nasa_vred = DoubleField()
    narucilac = CharField()
    odluka = CharField()
    status = CharField()
    napomena = CharField()

    @staticmethod
    def insert_tender(form):
        fields = form.get_data()
        if fields is None:
            return

        msg_title = 'Poruka'
        try:
            Tender.create(naziv = fields['naziv'], 
                          tip = fields['tip'], 
                          aktivan = fields['aktivan'], 
                          proc_vred = fields['proc_vred'],
                          nasa_vred = fields['nasa_vred'], 
                          narucilac = fields['narucilac'], 
                          odluka = fields['odluka'], 
                          status = fields['status'],
                          napomena = fields['napomena'], 
                          datum = fields['datum'])

        except:
            messagebox.showinfo(msg_title, 'Nije unet tender: %s! Doslo je do greske' % fields['naziv'])
            return

        messagebox.showinfo(msg_title, 'Uspesno unet tender: %s' % fields['naziv'])
        form.reset_data()
        table.show(Tender._meta.fields, Tender.select())

    def __str__(self):
        return '{};{};{};{};{};{};{};{};{};{};{}'.format(
                self.idtender, self.naziv, self.tip, self.aktivan, self.datum,
                self.proc_vred, self.nasa_vred, self.narucilac, self.odluka,
                self.status, self.napomena)

db.connect()
db.create_tables([Tender])
root = Tk()
root.title('Tender')
root.geometry('1000x1000')
#root.attributes("-fullscreen", True) 
#root.maxsize(1000, 1000)

# in root
content = ttk.Frame(root, padding=(3,3,12,12), width = 1000, height = 1000)
# in content
table = Table(content)
insert_frame = ttk.Frame(content, borderwidth = 5) #,width = 100, height = 300)
# in insert
button_frame = ttk.Frame(insert_frame, borderwidth = 2) #, width = 100, height = 200)
form_frame = ttk.Frame(insert_frame, borderwidth = 2)

# Position in root
content.pack()

# Position in content
table.pack(side = LEFT)
insert_frame.pack()
button_frame.pack()
form_frame.pack()

form = TenderForm(insert_frame)

all_records = Tender.select()
table.show(Tender._meta.fields, all_records)

insert_button = ttk.Button(button_frame, text = 'Ubaci', command  = lambda: Tender.insert_tender(form))
reset_button = ttk.Button(button_frame, text = 'Reset', command = form.reset_data)

insert_button.pack(side=LEFT)
reset_button.pack(side = LEFT)


mainloop()
