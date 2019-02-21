
import os
import re
import sys
from datetime import datetime


def find_wrong_ids(directory_with_files_to_check):
    directory_content = os.listdir(directory_with_files_to_check)

    files_to_check = []

    for item in directory_content:
        path = os.path.join(directory_with_files_to_check, item)

        if os.path.isfile(path):
            files_to_check.append(item)

    # finding wrong ids

    wrong_ids = set()
    regex = r'xml:id="([0-9].*?)"'

    for filename in files_to_check:
        with open(os.path.join(directory_with_files_to_check, filename), 'r') as file:
            text_to_check = file.read()
        wrong_ids.update(re.findall(regex, text_to_check))

    sorted_wrong_ids = sorted(wrong_ids)
    print("List of wrong ids in all files:")
    for id in sorted_wrong_ids:
        print(id)

    # write wrong ids to file

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename_to_write = "Wrong ids ({0}).txt".format(time)

    write_directory = os.path.join(directory_with_files_to_check, "search results")

    try:
        os.makedirs(write_directory)
    except FileExistsError:
        pass

    with open(os.path.join(write_directory, filename_to_write), 'w') as file:
        file.writelines(sorted_wrong_ids)

    files_number = len(files_to_check)
    wrong_ids_number = len(wrong_ids)

    # find tags with wrong ids

    tags_with_wrong_id = []
    tags_with_wrong_ids_without_id_declarations = []

    for i, filename in enumerate(reversed(sorted(files_to_check))):

        if i == 10:
            break

        print("file {0}/{1}: {2}".format(i + 1, files_number, filename))

        filename_core = filename.replace('dep_', '')
        filename_core = filename_core.replace('_tei.xml', '')

        # print("filename core: ", filename_core)

        with open(os.path.join(directory_with_files_to_check, filename), 'r') as file:
            text_to_check = file.read()

        regex = r'<.*?>'
        tags = re.findall(regex, text_to_check)

        tags = set(tags)

        for i, id in enumerate(wrong_ids):
            print("searched id: {0}/{1}".format(i + 1, wrong_ids_number), end='\r')

            for tag in tags:
                if (id in tag):
                    tags_with_wrong_id.append(tag)

                if (id in tag) and ('xml:id="' not in tag):
                    print(tag)

                    tags_with_wrong_ids_without_id_declarations.append(tag)


    # write tags with wrong isd to file

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename_to_write = "Tags with wrong ids ({0}).txt".format(time)

    write_directory = os.path.join(directory_with_files_to_check, "search results")

    text_to_write = '\n'.join(tags_with_wrong_id)

    try:
        os.makedirs(write_directory)
    except FileExistsError:
        pass

    with open(os.path.join(write_directory, filename_to_write), 'w') as file:
        file.write(text_to_write)


    # write tags with wrong isd to file

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename_to_write = "Tags with wrong ids (without id declarations) ({0}).txt".format(time)

    write_directory = os.path.join(directory_with_files_to_check, "search results")

    text_to_write = '\n'.join(tags_with_wrong_ids_without_id_declarations)

    try:
        os.makedirs(write_directory)
    except FileExistsError:
        pass

    with open(os.path.join(write_directory, filename_to_write), 'w') as file:
        file.write(text_to_write)



















def check_arguments(arguments):
    if len(arguments) != 2:
        raise Exception("ERROR: Incorrect number of arguments.")



def main(argv):

    check_arguments(argv)

    directory_with_files_to_check = argv[1]

    find_wrong_ids(directory_with_files_to_check)


if __name__ == '__main__':
    main(sys.argv)







