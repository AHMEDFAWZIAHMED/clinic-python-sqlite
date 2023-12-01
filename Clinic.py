import tkinter as tk
from tkinter import font, ttk
from tkinter import messagebox
from data import Database
from patient import Patient

class Clinic(tk.Tk):

    advice = "Select one patient form the table to add details"
    warning = """*You can find patients that already in database on the right window ->"""
    tip = """*After entering name, age and address for NEW PATIENT.
    press SAVE button to save and go to new window for patient details."""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        self.configure(background="gray")
        self.wm_title("Main page: Clinic")

        self.database = Database()
        self.database.create_table()

        self.left_panel()


    def left_panel(self):

        bolded = font.Font(family='Helvetica', size=15, weight='bold')

        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT, padx=15, pady=10, fill='y', expand=False)

        inside_frame = tk.Frame(left_frame,borderwidth=3, relief=tk.GROOVE)
        inside_frame.pack(padx=10, pady=10, fill="y", expand=True)

        title_label = tk.Label(inside_frame, text="New patient", font=bolded)
        title_label.pack(side=tk.TOP, padx=10, pady=50)

        name_frame = tk.Frame(inside_frame)
        name_frame.pack(side=tk.TOP, padx=15, pady=10, fill="x")

        entry_name_label = tk.Label(name_frame, text="Name:    ", font=bolded)
        entry_name_label.pack(side=tk.LEFT,padx=10, pady=5)

        name_text = tk.StringVar()
        self.entry_name = tk.Entry(name_frame, textvariable=name_text, width=40, bd=2)
        self.entry_name.pack(side=tk.LEFT)

        age_frame = tk.Frame(inside_frame)
        age_frame.pack(side=tk.TOP, padx=15, pady=10, fill="x")

        entry_age_label = tk.Label(age_frame, text="Age:       ", font=bolded)
        entry_age_label.pack(side=tk.LEFT, padx=10, pady=5)

        age_text = tk.StringVar()
        self.entry_age = tk.Entry(age_frame, textvariable=age_text, width=40, bd=2)
        self.entry_age.pack(side=tk.LEFT)

        address_frame = tk.Frame(inside_frame)
        address_frame.pack(side=tk.TOP, padx=15, pady=10, fill="x")

        entry_address_label = tk.Label(address_frame, text="Address:", font=bolded)
        entry_address_label.pack(side=tk.LEFT, padx=10, pady=5)

        address_text = tk.StringVar()
        self.entry_address = tk.Entry(address_frame, textvariable=address_text, width=40, bd=2)
        self.entry_address.pack(side=tk.LEFT)

        insert_button = tk.Button(inside_frame, text="SAVE", font=bolded,
                                   bd=2, command=self.details_new_window)
        insert_button.config(anchor=tk.S)
        insert_button.pack(side=tk.TOP, padx=10, pady=30)

        info_label = tk.Label(inside_frame, text=self.warning, fg='red')
        info_label.pack(side=tk.TOP)

        tip_label = tk.Label(inside_frame, text=self.tip, fg='green')
        tip_label.pack(side=tk.TOP, pady=10)

        self.right_panel()


    def right_panel(self):

        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.LEFT, pady=10, padx=10, fill="both", expand=True)

        search_frame = tk.Frame(right_frame,borderwidth=2, relief=tk.GROOVE)
        search_frame.pack(side=tk.TOP, fill="x", padx=15, pady=15)

        advice_label = tk.Label(search_frame, text=self.advice, fg='blue')
        advice_label.pack(side=tk.LEFT, padx=15, pady=10)
        search_text = tk.StringVar()
        self.entry_search = tk.Entry(search_frame, textvariable=search_text, foreground="gray")
        self.entry_search.pack(side=tk.LEFT, padx=5, pady=10)
        self.entry_search.bind("<Button-1>", lambda e: self.empty_entry_search("black"))

        search_button = tk.Button(search_frame, text="Search", command=self.search_database)
        search_button.pack(side=tk.LEFT, padx=5, pady=10)

        all_button = tk.Button(search_frame, text="All patients", command=self.get_patients)
        all_button.pack(side=tk.LEFT, padx=5, pady=10)

        tree_border = tk.Frame(right_frame, bd=1, relief="sunken", background="white")
        tree_border.pack(side=tk.TOP, padx=15, pady=5, fill="both", expand=True)

        self.tree = ttk.Treeview(tree_border)
        header = ['Name', 'Age', 'Address']
        self.tree["columns"] = header
        self.tree.column("#0",width=100, anchor=tk.CENTER)
        for i, h in enumerate(header):
            self.tree.heading(i, text=h)
            self.tree.column(i, anchor=tk.CENTER)
        self.get_patients()

        vsb = tk.Scrollbar(tree_border, orient="vertical")
        vsb.config(command=self.tree.yview)
        hsb = tk.Scrollbar(tree_border, orient="horizontal")
        hsb.config(command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind('<ButtonRelease-1>', self.selectItem)

    def search_database(self):
        if len(self.entry_search.get()) == 0 or self.entry_search.get() == " Type to search..":
            messagebox.showerror(message="Please type a name in search bar")
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        entered_search = "%{}%".format(self.entry_search.get())
        search_patients = self.database.get_searched(entered_search)
        if search_patients:
            self.get_patients(search_patients)
        else:
            messagebox.showinfo(message="Can't find the name in the database")

    def get_patients(self, search=None):
        if search:
            patients = search
        else:
            patients = self.database.get_patients()
            self.empty_entry_search("gray")
            self.entry_search.insert(0, " Type to search..")
        if not patients:
            messagebox.showinfo(message="Database is empty! Add new patient")
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        for single_patient in patients:
            items = [single_patient[1], single_patient[2], single_patient[3]]
            self.tree.insert("", int(single_patient[0]),text=single_patient[0], values=items)

    def empty_entry_search(self, color):
        self.entry_search.delete(0, 'end')
        self.entry_search.config(foreground=color)

    def selectItem(self, event):
        curItem = self.tree.focus()
        id = self.tree.item(curItem)['text']
        details = self.database.get_patient(int(float(id)))[0][4]
        values = self.tree.item(curItem)['values']# name, age, address
        self.open_patient_window(id, values[0], values[1], values[2], details, self.database)


    def details_new_window(self):
        name = self.entry_name.get()
        age = self.entry_age.get()
        address = self.entry_address.get()
        details = ""
        if name == "" or age == "" or address == "":
            messagebox.showerror(message=" Please fill in all fields to save new patient")
            return
        if not age.isnumeric():
            messagebox.showerror(message="Please type a number in the age fields")
            return
        p_id = self.database.insert_patient(name, int(age), address, details)
        if p_id != 0:
            self.entry_name.delete(0, 'end')
            self.entry_age.delete(0, 'end')
            self.entry_address.delete(0, 'end')
            self.open_patient_window(p_id, name, int(age), address, details, self.database)
        else:
            messagebox.showerror(message="Something went wrong. Please try again")

    def open_patient_window(self, id, name, age, address, details, data):
        new_patient = Patient(self, id, name, age, address, details, data)
        new_patient.show_patient_details()



if __name__ == "__main__":
    clinic = Clinic()
    clinic.mainloop()