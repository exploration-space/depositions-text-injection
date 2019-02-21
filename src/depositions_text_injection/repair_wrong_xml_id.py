import re
import os
import sys

def repair_ids(text: str) -> str:
    # replace id's in tags with explixit xml:id value, if it starts with digit
    text = re.sub('<([a-zA-Z_][A-Za-z-_.]*?) ([^<^>]?xml:id=")([0-9].*?")', "<\g<1> \g<2>\g<1>\g<3>", text)

    # replace id's in text @corresp tags, if it starts with digit
    text = re.sub('(<text.*?)#id([0-9].*?")', "\g<1>#p\g<2>", text)
    return text


def check_arguments(arguments):
    if len(arguments) != 2:
        raise Exception("ERROR: Incorrect number of arguments.")


def repair(files_to_repair):
    files = os.listdir(files_to_repair)


    for filename in files:
        if os.path.isfile(os.path.join(files_to_repair, filename)):
            source_text = load_text(files_to_repair, filename)

            text_to_write = repair_ids(source_text)

            save_xml(text_to_write, filename, files_to_repair)




def load_text(directory, filename):
    file_path = os.path.join(directory, filename)

    with open(file_path, "r") as file_path:
        text = file_path.read()

    return text


def save_xml(text_to_write, filename, directory_with_files_to_extend):
    # filename_to_write = filename + "_id_corected" + ".xml"
    filename_to_write = filename

    write_directory = os.path.join(directory_with_files_to_extend, "id_corrected")

    try:
        os.makedirs(write_directory)
    except FileExistsError:
        pass

    with open(os.path.join(write_directory, filename_to_write), 'w') as file:
        file.write(text_to_write)


def main(argv):
    check_arguments(argv)

    files_to_repair = argv[1]

    repair(files_to_repair)


if __name__ == '__main__':
    main(sys.argv)