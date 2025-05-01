"""
Rail Car Profile SQL Generator

A GUI application that generates SQL insert statements for rail car profiles.
Handles different measurement units (Meters, Feet, US Survey Feet) and converts
them to metric values. Creates SQL files for database insertion.

Author: John Carlee
"""
from tkinter import filedialog
from tkinter import *
from tkinter import ttk

# Constants
WINDOW_SIZE = "400x660"
DEFAULT_PADDING = 5
DEFAULT_ENTRY_PADDING = 10
DECIMAL_PRECISION = 9
UNITS = ['Meters', 'Feet', 'US Survey Feet']

FIELD_NAMES = ['Id', 'Name', 'Description', 'Cabin Length', 'Wheel Length', 'Wheel Anchor', 'Track Gauge',
               'Envelope', 'Units', 'User ID', 'URL Id', 'More Info']

DEFAULT_VALUES = {
    'id': '000',
    'name': '**CTA Series 2600**',
    'cabin_length': '0.00',
    'wheel_length': 'Distance between wheel axles',
    'wheel_anchor': 'Full length between inner rails (0.00)',
    'track_gauge': 'Length between rail center',
    'envelope': 'Width\tHeight (no header)',
    'user_id': '1',
    'url_id': '12',
    'more_info': 'www.website.com'
}


def try_input(value) -> str:
    """Convert input value to SQL-compatible string format.

    Args:
        value: The input value to convert (can be string, number, or empty)

    Returns:
        str: SQL-formatted string:
            - 'NULL' if input is empty
            - quoted string if input is non-NULL string
            - string representation of value otherwise
    """
    if value == '':
        return "NULL"
    if isinstance(value, str) and value != "NULL":
        return f"'{value}'"
    return str(value)


def make_sql_report() -> None:
    """Generate SQL insert statement for rail car dimensions and save to file.

    Collects values from all input fields, converts measurements to meters,
    and writes an SQL insert statement to a user-specified file.
    All dimensional values are converted to meters regardless of input unit.
    """
    filename = filedialog.asksaveasfilename(
        defaultextension=".sql",
        filetypes=(("sql", "*.sql"), ("all files", "*.*"))
    )
    if not filename:
        return

    sql_values = {
        'objectid': try_input(int(e1.get())),
        'name': try_input(str(e2.get())),
        'desc': try_input(str(e3.get())),
        'cabin_length': conversion_check(float(e4.get())),
        'wheel_length': conversion_check(float(e5.get())),
        'wheel_anchor': try_input(f"{conversion_check(float(e6.get())) / 2},0"),
        'track_gauge': conversion_check(float(e7.get())),
        'envelope': try_input(str(convert_envelope())),
        'user_id': try_input(int(e10.get())),
        'url_id': try_input(int(e11.get())),
        'more_info': try_input(str(e12.get()))
    }

    sql_template = (
        "Insert into [RailCar]([Id], [Name], [Description], [CabinLength], "
        "[WheelLength], [WheelAnchor], [TrackGauge], [Envelope], [UserId], "
        "[UrlId], [MoreInfo])\n\tValues({objectid}, {name}, {desc}, "
        "{cabin_length}, {wheel_length}, {wheel_anchor}, {track_gauge}, "
        "{envelope}, {user_id}, {url_id}, {more_info});\n"
    )

    with open(filename, 'w') as sql_file:
        sql_file.write(sql_template.format(**sql_values))


def feet_to_meters(ft: float) -> float:
    """Convert feet to meters with specified precision.

    Args:
        ft: Length in feet

    Returns:
        float: Length in meters, rounded to DECIMAL_PRECISION places
    """
    return round(ft * 0.3048, DECIMAL_PRECISION)


def us_survey_feet_to_meters(us_survey_feet: float) -> float:
    """Convert US survey feet to meters with specified precision.

    Args:
        us_survey_feet: Length in US survey feet

    Returns:
        float: Length in meters, rounded to DECIMAL_PRECISION places
    """
    return round(us_survey_feet * (1200 / 3937), DECIMAL_PRECISION)


def read_envelope() -> list:
    """Parse envelope dimensions from text area input.

    Reads tab-separated width/height pairs, one pair per line.
    If units are not meters, converts string values to float.

    Returns:
        list: Flattened list of envelope dimensions
    """
    env_text = e8.get("1.0", 'end-1c')
    env_split = env_text.splitlines()
    flat_list = []

    for line in env_split:
        values = line.split('\t')
        if e9.get() != 'Meters':
            flat_list.extend(float(item) for item in values)
        else:
            flat_list.extend(values)

    return flat_list


def convert_envelope() -> str:
    """Convert envelope measurements to meters and format as comma-separated string.

    Reads envelope dimensions from input, converts to meters if necessary,
    and joins values with commas for SQL insertion.

    Returns:
        str: Comma-separated string of measurements in meters.
            Empty string if unit type is invalid.
    """
    env_list = read_envelope()
    unit = e9.get()

    if unit not in UNITS:
        return ''

    if unit == 'Meters':
        return ','.join(str(val) for val in env_list)

    converter = us_survey_feet_to_meters if unit == 'US Survey Feet' else feet_to_meters
    return ','.join(str(converter(val)) for val in env_list)


def conversion_check(value: float) -> float:
    """Convert measurement value to meters based on selected unit.

    Args:
        value: The measurement value to convert

    Returns:
        float: Value converted to meters if input unit is feet or US survey feet.
            Original value if input unit is meters.
    """
    unit = e9.get()
    if unit == 'US Survey Feet':
        return us_survey_feet_to_meters(value)
    if unit == 'Feet':
        return feet_to_meters(value)
    return value

# Initialize main window
master = Tk()
master.title("Rail Car Dimensions")
master.geometry(WINDOW_SIZE)

# Create and place labels
for idx, name in enumerate(FIELD_NAMES):
    Label(master, text=name).grid(row=idx, padx=DEFAULT_PADDING)

# Create entry widgets
entries = []
for idx in range(12):
    if idx == 7:  # Special case for envelope text area
        entry = Text(master)
    elif idx == 8:  # Special case for units combo box
        entry = ttk.Combobox(master, values=UNITS)
        entry.set('Meters')
    else:
        entry = Entry(master)

    entry.grid(row=idx, column=1, sticky=W + E, padx=DEFAULT_ENTRY_PADDING)
    entries.append(entry)

# Add save button
Button(master, text='Save', command=make_sql_report).grid(
    row=len(FIELD_NAMES) + 1,
    column=1,
    sticky=W + E,
    pady=4,
    padx=DEFAULT_ENTRY_PADDING
)

# Configure grid
master.columnconfigure(1, weight=1)

# Initialize entry values
e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12 = entries

e1.insert(END, DEFAULT_VALUES['id'])
e2.insert(END, DEFAULT_VALUES['name'])
e4.insert(END, DEFAULT_VALUES['cabin_length'])
e5.insert(END, DEFAULT_VALUES['wheel_length'])
e6.insert(END, DEFAULT_VALUES['wheel_anchor'])
e7.insert(END, DEFAULT_VALUES['track_gauge'])
e8.insert(END, DEFAULT_VALUES['envelope'])
e10.insert(END, DEFAULT_VALUES['user_id'])
e11.insert(END, DEFAULT_VALUES['url_id'])
e12.insert(END, DEFAULT_VALUES['more_info'])

# Ensure text boxes expand with window
master.columnconfigure(1, weight=1)

mainloop()