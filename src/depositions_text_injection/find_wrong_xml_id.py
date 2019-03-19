import os
import re
import sys
from datetime import datetime
from typing import List, Tuple, Set


def find_wrong_ids(directory_with_files_to_check: str):
    files_to_check = list_files(directory_with_files_to_check)
    wrong_ids = list_wrong_ids(files_to_check)

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    wrong_ids_to_file(directory_with_files_to_check, wrong_ids, time)

    tags_with_wrong_id, tags_with_wrong_id_without_id_declarations = search_for_tags_with_wrong_ids(files_to_check,
                                                                                                    wrong_ids)

    tags_with_wrong_ids_to_file(directory_with_files_to_check, tags_with_wrong_id,
                                tags_with_wrong_id_without_id_declarations, time)


def tags_with_wrong_ids_to_file(directory_with_files_to_check: str, tags_with_wrong_id: Tuple[str],
                                tags_with_wrong_id_without_id_declarations: Tuple[str], time):
    filename_to_write = "Tags with wrong ids ({}).txt".format(time)
    with open(os.path.join(directory_with_files_to_check, filename_to_write), 'w') as file:
        file.writelines(tags_with_wrong_id)
    filename_to_write = "Tags with wrong ids (without id declarations) ({}).txt".format(time)
    with open(os.path.join(directory_with_files_to_check, filename_to_write), 'w') as file:
        file.writelines(tags_with_wrong_id_without_id_declarations)


def search_for_tags_with_wrong_ids(files_to_check: Tuple[str], wrong_ids: Tuple[str]) -> Tuple[Tuple[str], Tuple[str]]:
    files_number = len(files_to_check)
    wrong_ids_number = len(wrong_ids)
    tags_with_wrong_id: Set[str] = set()
    tags_with_wrong_id_without_id_declarations: Set[str] = set()
    for i, filepath in enumerate(reversed(sorted(files_to_check))):
        print("file {}/{}: {}".format(i + 1, files_number, filepath), end='\r')
        with open(filepath) as file:
            file_text = file.read()

        regex = r'<.*?>'
        tags = set(re.findall(regex, file_text))

        for j, id in enumerate(wrong_ids):
            print("searched id: {}/{}".format(j + 1, wrong_ids_number), end='\r')
            tags_with_wrong_id.union({tag for tag in tags if id in tag})
            tags_with_wrong_id_without_id_declarations.union(
                {tag for tag in tags if (id in tag) and ('xml:id="' not in tag)})

    return tuple(sorted(tags_with_wrong_id)), tuple(sorted(tags_with_wrong_id_without_id_declarations))


def wrong_ids_to_file(directory_with_files_to_check: str, wrong_ids: Tuple[str], time: str) -> None:
    filename_to_write = "Wrong ids ({}).txt".format(time)
    with open(os.path.join(directory_with_files_to_check, filename_to_write), 'w') as file:
        file.writelines(wrong_ids)


def list_wrong_ids(files_to_check: Tuple[str]) -> Tuple[str]:
    wrong_ids: Set[str] = set()
    regex = r'xml:id="([0-9].*?)"'

    for filepath in files_to_check:
        with open(filepath) as file:
            file_text = file.read()
        wrong_ids.update(re.findall(regex, file_text))

    return tuple(sorted(wrong_ids))


def list_files(directory_with_files_to_check: str) -> Tuple[str]:
    directory_file_list = os.listdir(directory_with_files_to_check)
    directory_file_list = [os.path.join(directory_with_files_to_check, item) for item in directory_file_list]
    files_to_check = [str(filepath) for filepath in directory_file_list if os.path.isfile(filepath)]
    return tuple(sorted(files_to_check))


def main(argv: List[str]) -> None:
    assert len(argv) == 2, "Wrong number of parameters given"

    directory_with_files_to_check = argv[1]

    find_wrong_ids(directory_with_files_to_check)


if __name__ == '__main__':
    main(sys.argv)
