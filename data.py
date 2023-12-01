import sqlite3
from tkinter import messagebox

class Database:

    patient_table = """ CREATE TABLE IF NOT EXISTS patient (
                        id INTEGER PRIMARY KEY,
                        name text NOT NULL,
                        age integer,
                        address text,
                        details text
                    ); """
    insert_row = "INSERT INTO patient(name, age, address, details) VALUES (?, ?, ?, ?)"
    get_row_by_id = "SELECT * FROM patient WHERE id=?"
    get_all_patient = "SELECT id, name, age, address FROM patient"
    get_searched_patient = "SELECT * FROM patient WHERE name LIKE (?)"
    update_row_basic = "UPDATE patient SET name=?, age=?, address=? WHERE id=?"
    update_row_details = "UPDATE patient SET details=? WHERE id=?"
    info = "Update completed successfully!"

    def create_table(self):
        try:
            self.conn = sqlite3.connect('clinic.db')
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(self.patient_table)
        except Exception as e:
            messagebox.showerror(message=str(e))

    def get_patients(self):
        all_patients = []
        try:
            cur = self.conn.cursor()
            all_patients = cur.execute(self.get_all_patient).fetchall()
        except Exception as e:
            messagebox.showerror(message=str(e))
        return all_patients

    def get_searched(self, patient_name):
        searched_patients = []
        pat_name = "%{}%".format(patient_name)
        try:
            cur = self.conn.cursor()
            searched_patients = cur.execute(self.get_searched_patient, (pat_name,)).fetchall()
        except Exception as e:
            messagebox.showerror(message=str(e))
        return searched_patients

    def insert_patient(self, pat_name, pat_age, pat_address, pat_details):
        try:
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(self.insert_row, (pat_name, pat_age, pat_address, pat_details))
                return cur.lastrowid
        except Exception as e:
            messagebox.showerror(message=str(e))
            return 0

    def get_patient(self, pat_id):
        one_patient = []
        try:
            cur = self.conn.cursor()
            one_patient = cur.execute(self.get_row_by_id, (pat_id,)).fetchall()
        except Exception as e:
            messagebox.showerror(message=str(e))
        return one_patient

    def update_patient_basic(self, pat_name, pat_age, pat_address, pat_id):
        try:
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(self.update_row_basic, (pat_name, pat_age, pat_address, pat_id))
                messagebox.showinfo(message=self.info)
        except Exception as e:
            messagebox.showerror(message=str(e))

    def update_patient_details(self,pat_details, pat_id):
        try:
            with self.conn:
                cur = self.conn.cursor()
                cur.execute(self.update_row_details, (pat_details, pat_id))
                #messagebox.showinfo(message=self.info)
        except Exception as e:
            messagebox.showerror(message=str(e))