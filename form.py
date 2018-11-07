from tkinter import *
from tkinter import ttk
from collections import namedtuple

def is_number(string):
    return string.replace('.', '', 1).isdigit()

Field = namedtuple('Field', 'label entry data')
class Form:
    def __init__(self, frame):
        self.frame = frame
        self.fields = {}

    def insert_entry(self, text, key):
        label = ttk.Label(self.frame, text = text)
        data = StringVar()
        entry = ttk.Entry(self.frame, textvariable = data)
        self.fields[key] = Field(label, entry, data)

    def insert_combo(self, text, key, values):
        label = ttk.Label(self.frame, text = text)
        data = StringVar()
        entry = ttk.Combobox(self.frame, textvariable = data)
        entry['values'] = values 
        self.fields[key] = Field(label, entry, data)

    def pack_fields(self, keys):
        for key in keys:
            self.fields[key].label.pack()
            self.fields[key].entry.pack()

    def reset_data(self):
        for field in self.fields.values():
            field.data.set('')

    def data_with_key(self, key):
        return self.fields[key].data.get()
    
class TenderForm(Form):

    def __init__(self, frame):
        super().__init__(frame)

        self.insert_entry('Naziv', 'naziv');
        self.insert_combo('Tip:', 'tip', [
                'PROJEKTOVANJE',
                'REVIZIJA',
                'NADZOR',
                'IZVODJENJE']);
        self.insert_combo('Aktivan:', 'aktivan', ['', 'DA', 'NE']);
        self.insert_entry('Datum:', 'datum');
        self.insert_entry('Procenjena vrednost', 'proc_vred');
        self.insert_entry('Nasa vrednost:', 'nasa_vred');
        self.insert_entry('Narucilac:', 'narucilac');
        self.insert_combo('Odluka', 'odluka', [
            ' ',
            'NAJNIZA',
            'NAJVISA',
            'ZALBA']);
        self.insert_combo('Status:', 'status', [
             ' ',
            'DOBIJEN',
            'IZGUBLJEN',
            'ZALBA'])
        self.insert_entry('Napomena', 'napomena');

        # Order of items
        self.pack_fields(['naziv', 'tip', 'aktivan', 'datum', 'proc_vred', 
                         'nasa_vred', 'narucilac', 'odluka', 'status', 'napomena'])

    # Ubaci tender
    def get_data(self):
        naziv = self.data_with_key('naziv')
        tip = self.data_with_key('tip')
        aktivan = self.data_with_key('aktivan')
        proc_vred = self.data_with_key('proc_vred')
        nasa_vred = self.data_with_key('nasa_vred')
        narucilac = self.data_with_key('narucilac')
        odluka = self.data_with_key('odluka')
        status = self.data_with_key('status')
        napomena = self.data_with_key('napomena')
        datum = self.data_with_key('datum')

        msg_title = 'Poruka'
        if len(naziv) < 1:
            messagebox.showinfo(msg_title, 'Nije unet naziv!')
            return None
        elif not is_number(proc_vred):
            messagebox.showinfo(msg_title, 'Procenjena vrednost nije broj!')
            return None
        elif not is_number(nasa_vred):
            messagebox.showinfo(msg_title, 'Nasa vrednost nije broj!')
            return None
        elif len(datum) < 1:
            messagebox.showinfo(msg_title, 'Nije unet datum!')
            return None

        return {key : self.data_with_key(key) for key in self.fields.keys()}




