from tkinter import filedialog
from tkinter import *

master = Tk()
master.title("Rail Car Dimensions")
master.geometry("300x267")

field_names = ['Id', 'Name', 'Description', 'Cabin Length', 'Wheel Length', 'Wheel Anchor', 'Track Guage',
               'Envelope', 'User ID', 'URL Id', 'More Info']


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
    envelope = try_input(str(e8.get()))
    user_id = try_input(int(e9.get()))
    url_id = try_input(int(e10.get()))
    more_info = try_input(str(e11.get()))
    input_values = [objectid, name, desc, cabin_length, wheel_length, wheel_anchor, track_guage, envelope, user_id,
                    url_id, more_info]
    sql_file = open(master.filename, 'w')
    sql_file.write("Insert into [RailCar]([Id], [Name], [Description], [CabinLength], [WheelLength], [WheelAnchor], "
                   "[TrackGuage], [Envelope], [UserId], [UrlId], [MoreInfo])\n\t")
    sql_file.write(
        "Values({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10});\n".format(
            objectid, name, desc, cabin_length, wheel_length, wheel_anchor, track_guage, envelope, user_id, url_id,
            more_info))
    sql_file.close()


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

e8 = Entry(master)  # Envelope
e8.insert(END, '**Copy and Paste**')

e9 = Entry(master)  # UserID
e9.insert(END, '1')

e10 = Entry(master)  # URL Id
e10.insert(END, '12')

e11 = Entry(master)  # MoreInfo
e11.insert(END, 'google.com')

e_list = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11]

for i in e_list:
    i.grid(row=e_list.index(i), column=1, sticky=W + E)

# Create Save button
Button(master, text='Save', command=make_sql_report).grid(row=12, column=1, sticky=W+E, pady=4, padx=10)

# Ensure text boxes expand with window
master.columnconfigure(1, weight=1)

mainloop()
