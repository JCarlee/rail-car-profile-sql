# Rail Car Profile SQL Generator

A Python GUI application that generates SQL insert statements for rail car profiles. The application handles different measurement units and converts them to metric values for database storage.

## Features

- Graphical user interface for data entry
- Supports multiple measurement units:
  - Meters
  - Feet
  - US Survey Feet
- Automatic conversion to metric units
- Generates SQL insert statements
- Saves output to SQL files
- Handles envelope dimensions with width/height pairs

## Requirements

- Python 3.x
- tkinter (usually included with Python)

## Fields

The application collects the following rail car data:
- ID
- Name
- Description
- Cabin Length
- Wheel Length
- Wheel Anchor
- Track Gauge
- Envelope Dimensions
- Units
- User ID
- URL ID
- Additional Information

## Usage

1. Run the application:
```python
python rail-sql.py