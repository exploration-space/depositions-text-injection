import re
import os
import sys
from typing import List


def repair_ids(text: str) -> str:
    # replace id's in tags with explicit xml:id value, if it starts with digit
    text = re.sub('<([a-zA-Z_][A-Za-z-_.]*?) ([^<^>]?xml:id=")([0-9].*?")', "<\g<1> \g<2>\g<1>\g<3>", text)

    # replace id's in text @corresp tags, if it starts with digit
    text = re.sub('(<text.*?)#id([0-9].*?")', "\g<1>#p\g<2>", text)
    return text


def check_arguments(arguments: List[str]) -> None:
    if len(arguments) != 2:
        raise Exception("ERROR: Incorrect number of arguments.")
    elif not type(arguments[1]) is str or not os.path.isdir(arguments[1]):
        raise TypeError("Expected directory path as command line argument.")


def repair(source_dir: str) -> None:
    files = os.listdir(source_dir)

    for filename in files:
        if os.path.isfile(os.path.join(source_dir, filename)):
            source_text = load_text(source_dir, filename)
            if source_text:
                text_to_write = repair_ids(source_text)
                save_xml(text_to_write, filename, source_dir)


def load_text(directory: str, filename: str) -> str:
    file_path = os.path.join(directory, filename)
    text = ""
    try:
        with open(file_path) as file:
            text = file.read()
    except OSError:
        print("Couldn't open {} file.".format(filename), file=sys.stderr)

    return text or None


def save_xml(text_to_write: str, filename: str, target_dir: str) -> None:
    # filename_to_write = filename + "_id_corected" + ".xml"
    write_directory = os.path.join(target_dir, "id_corrected")

    try:
        os.makedirs(write_directory)
    except FileExistsError:
        pass
    except PermissionError:
        raise PermissionError("Cannot create directory {}. Check permissions.".format(write_directory))

    try:
        with open(os.path.join(write_directory, filename), 'w') as file:
            file.write(text_to_write)
    except OSError:
        print("Couldn't open {} file.".format(filename), file=sys.stderr)


def main(argv: List[str]) -> None:
    check_arguments(argv)
    dir_to_repair = argv[1]
    repair(dir_to_repair)


if __name__ == '__main__':
    main(sys.argv)
