import re
import os
import sys
from lxml import etree as et
from datetime import datetime
from typing import List, Dict, Tuple


def check_arguments(arguments: List[str]) -> None:
    assert len(arguments) == 4, "ERROR: Invalid number of arguments. Function takes 3 arguments."
    for argument in arguments[1:2]:
        if not os.path.isdir(argument):
            raise ValueError("ERROR: '{}' isn't correct directory.".format(argument))


def inject_text_div(dir_files_to_extend: str, dir_files_to_inject: str, div_type: str) -> None:
    files_to_extend = os.listdir(dir_files_to_extend)
    files_to_inject = os.listdir(dir_files_to_inject)

    dir_result = create_target_dir(dir_files_to_extend)

    files_to_process = get_files_to_process(files_to_extend, files_to_inject)

    errors = []

    for i, filename in enumerate(files_to_process):
        source_text = load_text(dir_files_to_extend, filename)

        encoding_line, text_to_parse = separate_encoding_line(source_text)

        extracted_original_name = extract_original_name(filename)

        text_to_inject = load_text(dir_files_to_inject, extracted_original_name)
        text_to_inject = replace_carriage_return(text_to_inject)

        new_element = et.Element("div", type=div_type)

        try:
            parser = et.XMLParser(strip_cdata=False)
            xml_tree = et.fromstring(text_to_parse, parser=parser)
            insert_element(xml_tree, new_element)

            text_to_write = et.tostring(xml_tree, encoding="unicode")
            text_to_write = inject(text_to_write, text_to_inject, div_type)
            text_to_write = join_encoding_line(encoding_line, text_to_write)

            save_file(text_to_write, filename, dir_result)

        except et.XMLSyntaxError as ex:
            error_message = {'file': filename, 'message': ex}
            errors.append(error_message)

        print("Processing: {0}/{1}".format(i + 1, len(files_to_process)), end='\r')

    print("")
    print("Processing: Done")
    print("Total errors: {}".format(len(errors)))

    if errors:
        save_errors(errors, dir_result)


def create_target_dir(dir_files_to_extend: str) -> str:
    while dir_files_to_extend[-1] == '/':
        dir_files_to_extend = dir_files_to_extend[:-1]

    dir_parent = os.path.abspath(os.path.join(dir_files_to_extend, os.pardir))
    _, tail = os.path.split(dir_files_to_extend)
    result_directory_name = (tail + "_injected")
    dir_result = os.path.join(dir_parent, result_directory_name)

    try:
        os.makedirs(dir_result)
    except FileExistsError:
        pass
    except PermissionError:
        raise PermissionError("Cannot create directory {} due to lack of required permissions.".format(dir_result))

    return dir_result


def save_errors(errors: List[Dict[str, Exception]], dir_files_to_extend: str) -> None:
    errors_to_write = []

    for i, error in enumerate(errors):
        error_to_write = "{}. {}: {}".format(i + 1, error['file'], error['message'])
        errors_to_write.append(error_to_write)

    write_directory = os.path.join(dir_files_to_extend, "extended")

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "Errors ({})".format(time)

    text_to_write = '\n'.join(errors_to_write)
    save_file(text_to_write, filename, dir_files_to_extend)

    print("Errors list in: {}".format(os.path.join(write_directory, filename)))


def extract_original_name(filename: str) -> str:
    return filename.replace("dep_", "").replace("_tei", "")


def replace_carriage_return(text_to_inject: str) -> str:
    return text_to_inject.replace('&#xD;', '&#13;').replace('&xd;', '&#13;')


def inject(text_to_write: str, text_to_inject: str, div_type: str) -> str:
    text_to_replace = '<div type="{}"/>'.format(div_type)
    text_to_inject = '<div type="{}">{}</div>'.format(div_type, text_to_inject)

    return text_to_write.replace(text_to_replace, text_to_inject)


def get_files_to_process(files_to_extend: List[str], files_to_inject: List[str]) -> List[str]:
    files_dep = [filename for filename in files_to_extend if filename.startswith("dep_")]
    files_to_process = [filename for filename in files_dep if
                        filename.replace("dep_", "").replace("_tei", "") in files_to_inject]

    return sorted(files_to_process)


def load_text(directory: str, filename: str) -> str:
    file_path = os.path.join(directory, filename)
    with open(file_path) as file:
        text = file.read()

    return text


def separate_encoding_line(xml_text: str) -> Tuple[str, str]:
    text_in_lines = xml_text.splitlines()

    encoding_line = text_in_lines[0]

    regex = r'encoding=".*?"'
    match = re.search(regex, encoding_line)

    text_to_parse = '\n'.join(text_in_lines[1:]) if match else xml_text

    return encoding_line, text_to_parse


def insert_element(xml_tree: et, element: et.Element) -> None:
    namespaces = {'default': "http://www.tei-c.org/ns/1.0"}

    div_deposition = xml_tree.find('.//default:div[@type="deposition"]', namespaces=namespaces)
    div_deposition_parent = div_deposition.getparent()

    injection_position = div_deposition_parent.index(div_deposition) + 1
    div_deposition_parent.insert(injection_position, element)


def join_encoding_line(encoding_line: str, xml_text: str) -> str:
    final_xml = '\n'.join((encoding_line, xml_text))
    return final_xml


def save_file(text_to_write: str, filename: str, directory: str) -> None:
    with open(os.path.join(directory, filename), 'w') as file:
        file.write(text_to_write)


def main(argv: List[str]) -> None:
    check_arguments(argv)

    dir_files_to_extend = argv[1]
    dir_files_to_inject = argv[2]
    div_type = argv[3]

    inject_text_div(dir_files_to_extend, dir_files_to_inject, div_type)


if __name__ == '__main__':
    main(sys.argv)
