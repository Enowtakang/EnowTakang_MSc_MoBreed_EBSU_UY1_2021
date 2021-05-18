from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import mysql.connector
import csv
import os
from ttkthemes import themed_tk as tk


"""
Connect to database
"""

my_database = mysql.connector.connect(host="localhost",
                                      user="root",
                                      passwd="MyMScThesisProject",  # Insert your password
                                      database="THESIS",
                                      auth_plugin="mysql_native_password")

my_database_CURSOR = my_database.cursor()   # create cursor


"""
Create a table in your database

Once the table is created, remove the code, so as not
to get an error when re-running the script
"""

create_TABLE_variables = """CREATE TABLE variables(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                      Genotype_Name VARCHAR(20),
                      v1 INT (20),
                      v2 INT (20),
                      v3 INT (20),
                      v4 INT (20),
                      v5 INT (20),
                      v6 INT (20),
                      v7 INT (20));"""

my_database_CURSOR.execute(create_TABLE_variables)
my_database.commit()


"""
The global variable below is CREATED, with function to KEEP ALL OF THE DATA
"""

my_data = []


"""
Functions to be executed using the GUI buttons                                                     
"""


def update(rows):

    global my_data
    my_data = rows

    tree_view.delete(*tree_view.get_children())

    for i in rows:
        tree_view.insert('', 'end', values=i)


def search():

    q2 = q.get()

    query = "SELECT id, Genotype_Name, v1, v2, v3, v4, v5, v6, v7 FROM variables WHERE " \
            "id LIKE '%"+q2+"%' OR Genotype_Name LIKE '%"+q2+"%' OR v1 LIKE '%"+q2+"%' " \
            "OR v2 LIKE '%"+q2+"%' OR v3 LIKE '%"+q2+"%' OR v4 LIKE '%"+q2+"%' OR v5 LIKE '%"+q2+"%'" \
            "OR v6 LIKE '%"+q2+"%' OR v7 LIKE '%"+q2+"%'"

    my_database_CURSOR.execute(query)

    rows = my_database_CURSOR.fetchall()

    update(rows)


def clear():

    query = "SELECT id, Genotype_Name, v1, v2, v3, v4, v5, v6, v7 FROM variables"

    my_database_CURSOR.execute(query)

    rows = my_database_CURSOR.fetchall()

    update(rows)


def getrow(event):

    row_id = tree_view.identify_row(event.y)

    item = tree_view.item(tree_view.focus())

    t1.set(item['values'][0])
    t2.set(item['values'][1])
    t3.set(item['values'][2])
    t4.set(item['values'][3])
    t5.set(item['values'][4])
    t6.set(item['values'][5])
    t7.set(item['values'][6])
    t8.set(item['values'][7])
    t9.set(item['values'][8])


def clear_fields():

    entry_1.delete(0, END)
    entry_2.delete(0, END)
    entry_3.delete(0, END)
    entry_4.delete(0, END)
    entry_5.delete(0, END)
    entry_6.delete(0, END)
    entry_7.delete(0, END)
    entry_8.delete(0, END)
    entry_9.delete(0, END)


def add_row_variables():

    a2 = t2.get()
    a3 = t3.get()
    a4 = t4.get()
    a5 = t5.get()
    a6 = t6.get()
    a7 = t7.get()
    a8 = t8.get()
    a9 = t9.get()

    if messagebox.askyesno("Confirm Addition", "Are you sure you want to add a new row to the data?"):

        query = "INSERT INTO variables(id, Genotype_Name, v1, v2, v3, v4, v5, v6, v7) " \
                "VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)"

        my_database_CURSOR.execute(query, (a2, a3, a4, a5, a6, a7, a8, a9))

        my_database.commit()

        clear()


def update_row_variables():

    a2 = t2.get()
    a3 = t3.get()
    a4 = t4.get()
    a5 = t5.get()
    a6 = t6.get()
    a7 = t7.get()
    a8 = t8.get()
    a9 = t9.get()
    a1 = t1.get()

    if messagebox.askyesno("Confirm Update", "Are you sure you want to update this row?"):

        query = "UPDATE variables SET Genotype_Name = %s, v1 = %s, v2 = %s, v3 = %s, v4 = %s, v5 = %s," \
                "v6 = %s, v7 = %s WHERE id = %s"

        my_database_CURSOR.execute(query, (a2, a3, a4, a5, a6, a7, a8, a9, a1))

        my_database.commit()

        clear()


def delete_row_variables():

    row_id = t1.get()

    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this row?"):

        query = "DELETE FROM variables WHERE id = "+row_id

        my_database_CURSOR.execute(query)

        my_database.commit()

        clear()


def export_csv():

    if len(my_data) < 1:

        messagebox.showerror("No data", "No data available to export!")

        return False

    file_name = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                             title="Save CSV",
                                             filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

    with open(file_name, mode='w', newline='') as my_file:

        exp_writer = csv.writer(my_file, delimiter=',')  # < newline='' > prevents skipping of lines

        for i in my_data:

            exp_writer.writerow(i)

    messagebox.showinfo("Data Exported!",
                        " Your data has been exported to " + os.path.basename(file_name) + " successfully.")


def import_csv():

    my_data.clear()

    file_name = filedialog.askopenfilename(initialdir=os.getcwd(),
                                           title="Open CSV file",
                                           filetype=(("CSV File", "*.csv"), ("All Files", "*.*")))

    with open(file_name) as my_file:

        csv_read = csv.reader(my_file, delimiter=',')

        for i in csv_read:

            my_data.append(i)

    update(my_data)


def save_to_mysql():

    if messagebox.askyesno("Save to MySQL database", "Do you want to save this csv data to the database?"):

        for i in my_data:

            genotype_name = i[1]
            v1 = i[2]
            v2 = i[3]
            v3 = i[4]
            v4 = i[5]
            v5 = i[6]
            v6 = i[7]
            v7 = i[8]

            query = "INSERT INTO variables(id, Genotype_Name, v1, v2, v3, v4, v5, v6, v7) " \
                "VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)"

            my_database_CURSOR.execute(query, (genotype_name, v1, v2, v3, v4, v5, v6, v7))

        my_database.commit()

        clear()

        messagebox.showinfo("Data Saved!", "Your data has been saved to the database!")

    else:

        return False


def clear_entire_database():

    if messagebox.askyesno("CLEAR ENTIRE DATABASE!", "Do you want to DELETE all contents from the database? "
                                                     "This action cannot be reversed!"):
        query = "TRUNCATE TABLE variables"

        my_database_CURSOR.execute(query)

        my_database.commit()

        clear()

        messagebox.showinfo("Congratulations!", "Your database is now empty!")


"""
Initialize Tkinter
"""

root = tk.ThemedTk()
root.set_theme("black")

root.title('Data Management Assistant version 2021.0')
root.geometry(f"900x500")


"""
Create a notebook
"""

# Create notebook
root_notebook = ttk.Notebook(root)
root_notebook.pack(fill="both", expand="yes", padx=2, pady=10)  # Solves the expand problem

# Create a tab (which is a frame)
my_frame1 = ttk.Frame(root_notebook, width=900, height=500)

# Pack the tab
my_frame1.pack(fill="both", expand="yes")

# Put the tab in the notebook
root_notebook.add(my_frame1, text="Created by Enow Takang Achuo Albert")


"""
CREATE LABEL FRAMES IN THE TAB
"""

label_frame_1 = ttk.LabelFrame(my_frame1, text="Data")
label_frame_2 = ttk.LabelFrame(my_frame1, text="Explore data")
label_frame_3 = ttk.LabelFrame(my_frame1, text="Modify Data")

label_frame_1.place(relwidth=1, relheight=0.5, relx=0, rely=0)     # solves the expansion problem which I had
label_frame_2.place(relwidth=1, relheight=0.1, relx=0, rely=0.5)
label_frame_3.place(relwidth=1, relheight=0.4, relx=0, rely=0.6)

"""
CREATE TREE_VIEW AND PUT IN LABELFRAME 1 
"""

tree_view = ttk.Treeview(label_frame_1, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show="headings", height=5)

tree_view.place(relheight=1, relwidth=1)      # Fill the whole container with the tree view

tree_view.heading(1, text="id")
tree_view.heading(2, text="Genotype_Name")
tree_view.heading(3, text="B T C")
tree_view.heading(4, text="E P C")
tree_view.heading(5, text="M T C")
tree_view.heading(6, text="P S C")
tree_view.heading(7, text="T T P")
tree_view.heading(8, text="Y M V")
tree_view.heading(9, text="Y A D")


for column in range(0, 10):
    tree_view.column(column, anchor=CENTER, width=120, stretch=True)

# Event Listener

tree_view.bind('<Double 1>', getrow)


"""
SCROLLBARS FOR LABELFRAME 1
"""

scrollbar_y_axis = ttk.Scrollbar(label_frame_1, orient='vertical', command=tree_view.yview)
scrollbar_x_axis = ttk.Scrollbar(label_frame_1, orient='horizontal', command=tree_view.xview)
tree_view.configure(xscrollcommand=scrollbar_x_axis.set, yscrollcommand=scrollbar_y_axis.set)
scrollbar_x_axis.pack(side="bottom", fill='x')
scrollbar_y_axis.pack(side='right', fill='y')


"""
Create query to grab data from mysql database 'variables' table
"""

query = "SELECT id, Genotype_Name, v1, v2, v3, v4, v5, v6, v7 FROM variables"
my_database_CURSOR.execute(query)
rows = my_database_CURSOR.fetchall()
update(rows)

"""
MANIPULATE THE "EXPLORE DATA" SECTION
"""

# Search and clear SECTION

q = StringVar()
entry = Entry(label_frame_2, textvariable=q, bg="#696969", fg="white", bd=0, justify=CENTER)
entry.pack(side=LEFT, padx=10, pady=2)

search_button = ttk.Button(label_frame_2, text="   Search   ", command=search)
search_button.pack(side=LEFT, padx=3, pady=2)

clear_button = ttk.Button(label_frame_2, text="    Refresh    ", command=clear)
clear_button.pack(side=LEFT, padx=10, pady=2)

"""
MANIPULATE THE "MODIFY DATA" SECTION
"""

container = ttk.Frame(label_frame_3)
container.pack(fill=BOTH, expand=True)
canvas = Canvas(container)
canvas.configure(bg="#444444", bd=0, highlightthickness=0)
canvas.pack(side="left", fill=BOTH, expand=True, padx=15, pady=10)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)


"""
DATA COLLECTION SECTION
"""

label_1 = ttk.Label(scrollable_frame, text="id")
label_1.grid(row=0, column=0, padx=5, pady=3)

t1 = StringVar()
entry_1 = Entry(scrollable_frame, textvariable=t1, bg="#696969", fg="white", bd=0, justify=CENTER)
entry_1.grid(row=0, column=1, padx=5, pady=3)

label_2 = ttk.Label(scrollable_frame, text="Genotype_Name")
label_2.grid(row=0, column=2, padx=5, pady=3)

t2 = StringVar()
entry_2 = Entry(scrollable_frame, textvariable=t2, bg="#696969", fg="white", bd=0, justify=CENTER)
entry_2.grid(row=0, column=3, padx=5, pady=3)

label_3 = ttk.Label(scrollable_frame, text="B T C")
label_3.grid(row=2, column=0, padx=5, pady=25)

t3 = StringVar()
entry_3 = Entry(scrollable_frame, textvariable=t3, bg="#696969", fg="white", bd=0, justify=CENTER)
entry_3.grid(row=2, column=1, padx=5, pady=3)

label_4 = ttk.Label(scrollable_frame, text="E P C")
label_4.grid(row=2, column=2, padx=5, pady=3)

t4 = StringVar()
entry_4 = Entry(scrollable_frame, textvariable=t4, bg="#696969", fg="white", bd=0, justify=CENTER)
entry_4.grid(row=2, column=3, padx=5, pady=3)

label_5 = ttk.Label(scrollable_frame, text="M T C")
label_5.grid(row=2, column=4, padx=5, pady=3)

t5 = StringVar()
entry_5 = Entry(scrollable_frame, textvariable=t5, bg="#696969", fg="white", bd=0, justify=CENTER)
entry_5.grid(row=2, column=5, padx=5, pady=3)

label_6 = ttk.Label(scrollable_frame, text="P S C")
label_6.grid(row=2, column=6, padx=5, pady=3)

t6 = StringVar()
entry_6 = Entry(scrollable_frame, textvariable=t6, bg="#696969", fg="white", bd=0, justify=CENTER)
entry_6.grid(row=2, column=7, padx=5, pady=3)

label_7 = ttk.Label(scrollable_frame, text="T T P")
label_7.grid(row=2, column=8, padx=5, pady=3)

t7 = StringVar()
entry_7 = Entry(scrollable_frame, textvariable=t7, bg="#696969", fg="white", bd=0, justify=CENTER)
entry_7.grid(row=2, column=9, padx=5, pady=3)

label_8 = ttk.Label(scrollable_frame, text="Y M V")
label_8.grid(row=2, column=10, padx=5, pady=3)

t8 = StringVar()
entry_8 = Entry(scrollable_frame, textvariable=t8, bg="#696969", fg="white", bd=0, justify=CENTER)
entry_8.grid(row=2, column=11, padx=5, pady=3)

label_9 = ttk.Label(scrollable_frame, text="Y A D")
label_9.grid(row=2, column=12, padx=5, pady=3)

t9 = StringVar()
entry_9 = Entry(scrollable_frame, textvariable=t9, bg="#696969", fg="white", bd=0, justify=CENTER)
entry_9.grid(row=2, column=13, padx=5, pady=3)

"""
CRUD SECTION
"""

add_button = ttk.Button(scrollable_frame, text="   Add new row   ", command=add_row_variables)
add_button.grid(row=4, column=7, padx=5, pady=50)

update_button = ttk.Button(scrollable_frame, text="   Update row   ", command=update_row_variables)
update_button.grid(row=4, column=9, padx=5, pady=3)

delete_button = ttk.Button(scrollable_frame, text="   Delete row   ", command=delete_row_variables)
delete_button.grid(row=4, column=11, padx=5, pady=3)

clear_fields_button = ttk.Button(scrollable_frame, text="Clear all entries", command=clear_fields)
clear_fields_button.grid(row=4, column=13, padx=5, pady=3)

"""
IMPORT, SAVE, EXPORT, CLEAR and EXIT BUTTONS
"""

exit_button = ttk.Button(label_frame_2, text="     Exit", command=lambda: exit())
exit_button.pack(side=RIGHT, padx=5, pady=3)

clear_database_button = ttk.Button(label_frame_2, text="Clear entire database", command=clear_entire_database)
clear_database_button.pack(side=RIGHT, padx=5, pady=3)

export_button = ttk.Button(label_frame_2, text="Export to CSV", command=export_csv)
export_button.pack(side=RIGHT, padx=5, pady=3)

save2_mysql_button = ttk.Button(label_frame_2, text="Save to database", command=save_to_mysql)
save2_mysql_button.pack(side=RIGHT, padx=5, pady=3)

import_button = ttk.Button(label_frame_2, text="Import from CSV", command=import_csv)
import_button.pack(side=RIGHT, padx=5, pady=3)


root.mainloop()
