from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import csv

# Function to parse tabular data
# Function to convert units of measurement

master = Tk()
master.title("Rail Car Dimensions")
master.geometry("400x660")

field_names = ['Id', 'Name', 'Description', 'Cabin Length', 'Wheel Length', 'Wheel Anchor', 'Track Guage',
               'Envelope', 'Units', 'User ID', 'URL Id', 'More Info']


# Verify input from user
def try_input(f):
    if f == '':
        return "NULL"
    elif type(f) is str and f != "NULL":
        return "'" + f + "'"
    else:
        return f


def make_sql_report():
    master.filename = filedialog.asksaveasfilename(defaultextension=".sql",
                                                   filetypes=(("sql", "*.sql"), ("all files", "*.*")))
    objectid = try_input(int(e1.get()))
    name = try_input(str(e2.get()))
    desc = try_input(str(e3.get()))
    cabin_length = try_input(float(e4.get()))
    wheel_length = try_input(float(e5.get()))
    wheel_anchor = try_input(float(e6.get()))
    track_guage = try_input(float(e7.get()))
    user_id = try_input(int(e10.get()))
    url_id = try_input(int(e11.get()))
    more_info = try_input(str(e12.get()))
    # input_values = [objectid, name, desc, cabin_length, wheel_length, wheel_anchor, track_guage, envelope, user_id,
    #                url_id, more_info]
    sql_file = open(master.filename, 'w')
    sql_file.write("Insert into [RailCar]([Id], [Name], [Description], [CabinLength], [WheelLength], [WheelAnchor], "
                   "[TrackGuage], [Envelope], [UserId], [UrlId], [MoreInfo])\n\t")
    sql_file.write(
        "Values({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10});\n".format(
            objectid, name, desc, cabin_length, wheel_length, wheel_anchor, track_guage, None, user_id, url_id,
            more_info))
    sql_file.close()

# m to ussft m * 1200/3937
# ft to ussft 1 = 0.999998000004
#


def transpose():
    env = e8.get("1.0", 'end-1c')
    lol = csv.reader(env, delimiter='\t')
    print(lol)
#    for line in lol:
#       print(line)


def envelope():
    env = e8.get("1.0", 'end-1c')
    if e9.get() == 'm':
        pass
    elif e9.get() == 'ft':
        pass
    elif e9.get() == 'ussft':
        pass
    print(env)


for i in field_names:
    Label(master, text=i).grid(row=field_names.index(i), padx=5)


# Define values from entries
e1 = Entry(master)  # Id
e1.insert(END, '000')

e2 = Entry(master)  # Name
e2.insert(END, '**CTA Series 2600**')

e3 = Entry(master)  # Description
e3.insert(END, '**Desc**')

e4 = Entry(master)  # CabinLength
e4.insert(END, '0.00')

e5 = Entry(master)  # WheelLength
e5.insert(END, '0.00')

e6 = Entry(master)  # WheelAnchor
e6.insert(END, '0.00')

e7 = Entry(master)  # TrackGuage
e7.insert(END, '0.00')

e8 = Text(master)  # Envelope
e8.insert(END, '**Copy and Paste**')

units = ['m', 'ft', 'ussft']

e9 = ttk.Combobox(master, values=units)  # Unit of measurement
e9.set('m')

e10 = Entry(master)  # UserID
e10.insert(END, '1')

e11 = Entry(master)  # URL Id
e11.insert(END, '12')

e12 = Entry(master)  # MoreInfo
e12.insert(END, 'www.website.com')

e_list = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12]

for i in e_list:
    i.grid(row=e_list.index(i), column=1, sticky=W + E, padx=10)

# Create Save button
Button(master, text='Save', command=make_sql_report).grid(row=13, column=1, sticky=W+E, pady=4, padx=(0, 10))
Button(master, text='Envelope', command=transpose).grid(row=13, column=0, sticky=W+E, pady=4, padx=10)

# Ensure text boxes expand with window
master.columnconfigure(1, weight=1)

mainloop()
