# depositions-text-injection
## Purpose
This script was designed to inject text from original deposition files to appropriate TEI files. 

It work only with files with UTF-8 encoding.

## Usage
To run script, type in console:
```
python depositions_text_injection.py /path/to/TEI/files/directory/ /path/to/original/deposition/files/directory/
```
Script writes all created files in `/path/to/TEI/files/directory/extended/` directory.

If script encounter some errors, write them to `Errors (current_date).txt` in `/path/to/TEI/files/directory/extended/` directory.

## Testing
All tests should be in `depositions-text-injection/tests` directory.

All tests should be write with `pytest` framework.

To correct import something from `/src` to file with test, you need to install this module locally:
1. In console go to directory ABOVE depositions-text-injection main directory.
2. Run in console:
```
pip install -e ./depositions-text-injection/
```
Then you can import something by:
```
from depositions-text-injection import something
```
