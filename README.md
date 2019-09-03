# dr-range
Tools for analyzing Texas Hold'em hand ranges

## Hand Range Visualization and Organization
Draw and save ranges to a sqlite3 database
### Features
* Drag mouse to select multiple squares at once
* Rename actions by right-clicking the buttons
* Add filters and notes to find and understand your ranges better
* Database of ranges can be maintained through "Browse Ranges"

## Usage
`python range_db.py` to initialize the database
`python main.py` to run RangeViewer (the main part of the app)

## Dependencies
* Sqlite3
* Tkinter (?)
* PIL and Ghostscript (in the future)

## TODOs
* Postflop hand ranges and card removal effects
  * Differentiate between suits postflop
* Fractional actions
* Keyboard shortcuts to commands
* Add and remove actions/colors
* Custom action colors
