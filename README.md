# depositions-text-injection
## Purpose
This scripts was designed to inject text from original deposition files to appropriate TEI files. 

It work only with files encoded in UTF-8.

## Usage
First, you need to correct wrong xml ids in TEI files, by running in console:
```
python3 repair_wrong_xml_id.py /path/to/TEI/files/directory/ 
```
Script writes all created files in `/path/to/TEI/files/directory/id_corrected/` directory.

After that, you need to inject original depositions text to appropriate TEI files with corrected ids:
```
python3 inject_text.py /path/to/TEI/files/directory/id_corrected/ /path/to/original/deposition/files/directory/ div_name
```
e.g.
```
python3 inject_text.py id_corrected original/ original
```

Script writes all created files in `/path/to/TEI/files/directory/id_corrected_injected/` directory.

If script encounters some incorrect IDs, those are written to `Errors (current_date).txt` in `/path/to/TEI/files/directory/id_corrected_injected/` directory.

If deposition files are incorrect, you can try repairing them by going into directory that contains those, creating "repaired" dir within, and running repair.sh.
It will try to repair some known issues and will write modified files to "repaired" directory. Remember to check those after, as it's not guaranteed, that this script will repair all or even any of those. 

## Testing
All tests should be in `depositions-text-injection/tests` directory.

All tests should be written with `pytest` framework.

To correctly import something from `/src` to file with test, you need to install this module locally:
1. In console go to depositions-text-injection main directory.
2. Run in console:
```
pip install -e .
```
Then you can import something by:
```
from depositions-text-injection import something
```
