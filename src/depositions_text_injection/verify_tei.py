import sys

from lxml import etree as et
import os
from shutil import copy
from typing import Dict

ErrorDict = Dict[str, str]


def verify_tei(path_to_check: str) -> ErrorDict:
    if not os.path.isdir(path_to_check):
        raise TypeError("Invalid path. File is not directory or path does not exist.")

    correct_files_dir = os.path.join(path_to_check, "correct")

    try:
        os.makedirs(correct_files_dir)
    except FileExistsError:
        pass
    except PermissionError:
        raise PermissionError("Cannot create directory {}, check write permissions.".format(correct_files_dir))

    incorrect_files = dict()
    files = list(os.path.join(path_to_check, p) for p in os.listdir(path_to_check))
    files = list(p for p in files if p[-4:] == ".xml" and os.path.isfile(p))

    i, success = 0, 0
    for fpath in files:
        try:
            et.parse(fpath)
        except et.XMLSyntaxError as e:
            incorrect_files[fpath] = str(e)
        else:
            copy(fpath, correct_files_dir)
            success += 1
        i += 1
        print("Checking {}".format(i), end='\r')
    print("{} correct files copied.".format(success))
    return incorrect_files


def dump_errors(path_to_check: str, errors: ErrorDict) -> None:  # Not catching exceptions, as it should only be used
    with open(os.path.join(os.getcwd(), path_to_check, "correct", "verify_log.txt"), "w") as F:  # after successful
        F.writelines("{}:\t{}\n".format(k, v) for k, v in errors.items())                        # usage of verify_tei.


if __name__ == '__main__':
    assert len(sys.argv) == 2, "Invalid number of arguments. Please provide only path to directory with files to check."
    errors = verify_tei(sys.argv[1])
    if errors:
        dump_errors(sys.argv[1], errors)
