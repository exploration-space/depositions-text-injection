import re
import os
import sys

from lxml import etree
from datetime import datetime



def check_arguments(arguments):
    if len(arguments) != 3:
        raise Exception("ERROR: Invalid number of arguments. Function takes 2 arguments.")

    arguments = arguments[1:]

    for argument in arguments:
        if not os.path.isdir(argument):
            raise ValueError("ERROR: '{0}' isn't correct directory.".format(argument))


def inject_original_text(dir_files_to_extend, dir_files_to_inject):
    files_to_extend = os.listdir(dir_files_to_extend)
    files_to_inject = os.listdir(dir_files_to_inject)

    dir_parent = os.path.abspath(os.path.join(dir_files_to_extend, os.pardir))

    head, tail = os.path.split(dir_files_to_extend)
    head, dirname_files_to_extend = os.path.split(head)

    result_directory_name = dirname_files_to_extend + "_injected"

    dir_result = os.path.join(dir_parent, result_directory_name)

    files_to_process = get_files_to_process(files_to_extend, files_to_inject)

    errors = []

    for i, filename in enumerate(files_to_process):
        source_text = load_text(dir_files_to_extend, filename)

        encoding_line, text_to_parse = separate_encoding_line(source_text)

        extracted_original_name = extract_original_name(filename)

        text_to_inject = load_text(dir_files_to_inject, extracted_original_name)
        text_to_inject = replace_carriage_return(text_to_inject)

        new_element = etree.Element("div", type="original")

        try:
            parser = etree.XMLParser(strip_cdata=False)
            xml_tree = etree.fromstring(text_to_parse, parser=parser)
            insert_element(xml_tree, new_element)

            text_to_write = etree.tostring(xml_tree, encoding="unicode")
            text_to_write = inject(text_to_write, text_to_inject)
            text_to_write = join_encoding_line(encoding_line, text_to_write)

            save_file(text_to_write, filename, dir_result)

        except etree.XMLSyntaxError as ex:
            error_message = {'file': filename, 'message': ex}
            errors.append(error_message)

        print("Processing: {0}/{1}".format(i + 1, len(files_to_process)), end='\r')

    print("")
    print("Processing: Done")
    print("Total errors: {0}".format(len(errors)))

    if errors:
        save_errors(errors, dir_result)


def save_errors(errors, dir_files_to_extend):
    errors_to_write = []

    for i, error in enumerate(errors):
        error_to_write = "{0}. {1}: {2}".format(i + 1, error['file'], error['message'])
        errors_to_write.append(error_to_write)

    write_directory = os.path.join(dir_files_to_extend, "extended")

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "Errors ({0})".format(time)

    text_to_write = '\n'.join(errors_to_write)

    save_file(text_to_write, filename, dir_files_to_extend)

    print("Errors list in: {0}".format(os.path.join(write_directory, filename)))


def extract_original_name(filename):
    extracted_original_name = filename.replace("dep_", "")
    extracted_original_name = extracted_original_name.replace("_tei", "")

    return extracted_original_name


def replace_carriage_return(text_to_inject):
    new_text = text_to_inject.replace('&#xD;', '&#13;')

    return new_text


def inject(text_to_write, text_to_inject):
    text_to_replace = '<div type="original"/>'
    text_to_inject = '<div type="original">' + text_to_inject + '</div>'
    text_with_injection = text_to_write.replace(text_to_replace, text_to_inject)

    return text_with_injection


def get_files_to_process(files_to_extend, files_to_inject):
    files_dep = []

    for filename in files_to_extend:
        if filename.startswith("dep_"):
            files_dep.append(filename)

    files_to_process = []

    for filename in files_dep:
        extracted_original_name = filename.replace("dep_", "")
        extracted_original_name = extracted_original_name.replace("_tei", "")

        if extracted_original_name in files_to_inject:
            files_to_process.append(filename)

    return sorted(files_to_process)


def load_text(directory, filename):
    file_path = os.path.join(directory, filename)

    with open(file_path, "r") as file_path:
        text = file_path.read()

    return text


def separate_encoding_line(xml_text):
    text_in_lines = xml_text.splitlines()

    encoding_line = text_in_lines[0]

    regex = r'encoding=".*?"'
    match = re.search(regex, encoding_line)

    if match:
        text_to_parse = '\n'.join(text_in_lines[1:])
    else:
        text_to_parse = xml_text

    return encoding_line, text_to_parse


def insert_element(xml_tree, element):
    namespaces = {'default': "http://www.tei-c.org/ns/1.0"}

    div_deposition = xml_tree.find('.//default:div[@type="deposition"]', namespaces=namespaces)
    div_deposition_parent = div_deposition.getparent()

    injection_position = div_deposition_parent.index(div_deposition) + 1
    div_deposition_parent.insert(injection_position, element)


def join_encoding_line(encoding_line, xml_text):
    final_xml = '\n'.join((encoding_line, xml_text))

    return final_xml


def save_file(text_to_write, filename, directory):


    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

    with open(os.path.join(directory, filename), 'w') as file:
        file.write(text_to_write)


def main(argv):

    check_arguments(argv)

    dir_files_to_extend = argv[1]
    dir_files_to_inject = argv[2]

    inject_original_text(dir_files_to_extend, dir_files_to_inject)


if __name__ == '__main__':
    main(sys.argv)

