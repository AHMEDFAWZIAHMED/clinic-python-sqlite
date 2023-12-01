import tkinter as tk
from tkinter import messagebox

class Patient(tk.Toplevel):

    def __init__(self, parent, p_id, p_name, p_age, p_address, p_details, data):
        tk.Toplevel.__init__(self, parent)

        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        self.title("Second page: patient")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.p_id = p_id
        self.p_name = p_name
        self.p_age = p_age
        self.p_address = p_address
        self.p_details = p_details
        self.database = data


    def show_patient_details(self):
        frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE)
        frame.grid(row=0, column=0, pady=30)

        name_lable = tk.Label(frame, text="Name: "+str(self.p_name))
        name_lable.pack(side=tk.LEFT, padx=20, pady=10)
        age_lable = tk.Label(frame, text="Age: "+str(self.p_age))
        age_lable.pack(side=tk.LEFT, padx=20, pady=10)
        address_lable = tk.Label(frame, text="Address: "+str(self.p_address))
        address_lable.pack(side=tk.LEFT, padx=20, pady=10)

        update_button = tk.Button(frame, text='Update', command=self.start_dialog)
        update_button.pack(side=tk.LEFT, padx=20)

        frame1 = tk.Frame(self, borderwidth=2,relief=tk.SUNKEN)
        frame1.grid(row=1, column=0)

        details_lable = tk.Label(frame1, text="Details:", font='Helvetica 15 bold')
        details_lable.pack(side=tk.LEFT, padx=50, pady=5)
        details_button = tk.Button(frame1, text='Save', font='Helvetica 15 bold',
                                    borderwidth=3, command=self.save_patient_details)
        details_button.pack(side=tk.LEFT, padx=50, pady=5)

        frame2 = tk.Frame(self, borderwidth=3,relief=tk.SUNKEN)
        frame2.grid(row=2, column=0, padx=40)

        self.my_text = tk.Text(frame2, width=150, height=27)
        self.my_text.insert('1.0', str(self.p_details))
        self.my_text.focus()

        v_scrollbar = tk.Scrollbar(frame2, orient='vertical')
        v_scrollbar.config(command=self.my_text.yview)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar = tk.Scrollbar(frame2, orient='horizontal')
        h_scrollbar.config(command=self.my_text.xview)
        h_scrollbar.pack(side='bottom', fill='x')

        self.my_text.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.my_text.pack(side='left', fill='y')


    def save_patient_details(self):
        patient_details = ""
        for line in self.my_text.get('1.0', 'end-1c').splitlines():
            if line:
                patient_details += line
                patient_details += '\n'
        self.database.update_patient_details(patient_details, self.p_id)

    def on_closing(self):
        if messagebox.askokcancel("Exit", "Do you want to exit?", parent=self):
            self.save_patient_details()
            self.destroy()


    def start_dialog(self):
        self.dialog = Update_dialog(self, self.p_id, self.p_name,
                                     self.p_age, self.p_address, self.database)
        self.dialog.show_dialog()



class Update_dialog(tk.Toplevel):
    def __init__(self, parent, p_id, p_name, p_age, p_address, data):
        tk.Toplevel.__init__(self, parent)
        self.geometry("250x300")

        self.p_id = p_id
        self.p_name = p_name
        self.p_age = p_age
        self.p_address = p_address
        self.data = data

        #self.show_dialog()

    def show_dialog(self):
        entry_frame = tk.Frame(self)
        entry_frame.grid(row=0, column=0, pady=20, padx=20)

        address_text = tk.StringVar()
        self.entry_address = tk.Entry(entry_frame, textvariable=address_text)
        self.entry_address.insert(0, str(self.p_address))
        self.entry_address.pack(side=tk.BOTTOM, pady=10)
        entry_address_label = tk.Label(entry_frame, text="Address:")
        entry_address_label.pack(side=tk.BOTTOM)
        age_text = tk.StringVar()
        self.entry_age = tk.Entry(entry_frame, textvariable=age_text)
        self.entry_age.insert(0, str(self.p_age))
        self.entry_age.pack(side=tk.BOTTOM, pady=10)
        entry_age_label = tk.Label(entry_frame, text="Age:")
        entry_age_label.pack(side=tk.BOTTOM)
        name_text = tk.StringVar()
        self.entry_name = tk.Entry(entry_frame, textvariable=name_text)
        self.entry_name.insert(0, str(self.p_name))
        self.entry_name.pack(side=tk.BOTTOM, pady=10)
        entry_name_label = tk.Label(entry_frame, text="Name:")
        entry_name_label.pack(side=tk.BOTTOM)

        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, pady=30, padx=20)

        b_update = tk.Button(button_frame, text='Update', command=self.update_changes)
        b_update.pack(side=tk.LEFT, padx=20)
        b_update = tk.Button(button_frame, text='Close', command=self.dismiss)
        b_update.pack(side=tk.LEFT, padx=20)

    def dismiss(self):
        self.grab_release()
        self.destroy()

    def update_changes(self):
        name = self.entry_name.get()
        age = self.entry_age.get()
        address = self.entry_address.get()
        if name == "" or age == "" or address == "":
            messagebox.showerror(message=" Please fill in all fields to update")
            return
        if not age.isnumeric():
            messagebox.showerror(message="Please type a number in the age fields")
            return
        self.data.update_patient_basic(name, int(age), address, self.p_id)
        self.dismiss()