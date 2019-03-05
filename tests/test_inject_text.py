import pytest
from depositions_text_injection import inject_text

import os
import shutil


test_data_check_arguments__invalid_number_of_arguments__exception = [
    ("", "path_1"),
    ("", "path_1", "path_2")
]


@pytest.mark.parametrize("arguments", test_data_check_arguments__invalid_number_of_arguments__exception)
def test_check_arguments__invalid_number_of_arguments__exception(arguments):
    with pytest.raises(Exception) as error:
        inject_text.check_arguments(arguments)

    message = error.value.args[0]

    assert message == "ERROR: Invalid number of arguments. Function takes 3 arguments."


test_data_check_arguments__invalid_path_in_argument__exception = [
    (("", "/home/tei_wrong/", "/home/original/"), "/home/tei_wrong/"),
    (("", "/home/tei/", "/home/original_wrong/"), "/home/original_wrong/"),

]


@pytest.mark.parametrize("arguments, wrong_path", test_data_check_arguments__invalid_path_in_argument__exception)
def test_check_arguments__invalid_path_in_argument__exception(arguments, wrong_path, tmpdir):
    home_dir = tmpdir.mkdir("home")
    home_dir.mkdir("tei")
    home_dir.mkdir("original")

    arguments = (
        "",
        os.path.join(str(tmpdir), arguments[1][1:]),
        os.path.join(str(tmpdir), arguments[2][1:]),
        "original"
    )

    wrong_path = os.path.join(str(tmpdir), wrong_path[1:])

    with pytest.raises(ValueError) as error:
        inject_text.check_arguments(arguments)

    error_message = error.value.args[0]

    assert error_message == "ERROR: '" + wrong_path + "' isn\'t correct directory."


def test_inject_original_text__xml_parsing_error__write_error_file(tmpdir):
    home_dir = tmpdir.mkdir("home")
    tei_dir = home_dir.mkdir("tei")
    original_dir = home_dir.mkdir("original")

    dirname = os.path.dirname(__file__)
    dir_tei_invalid_id = os.path.join(dirname, "test_inject_text_files", "tei_invalid_id")
    dir_original = os.path.join(dirname, "test_inject_text_files", "original")


    files_tei_invalid_id = os.listdir(dir_tei_invalid_id)
    for file in files_tei_invalid_id:
        path_to_file = os.path.join(dir_tei_invalid_id, file)
        if (os.path.isfile(path_to_file)):
            shutil.copy(path_to_file, str(tei_dir))

    files_in_tei = os.listdir(str(tei_dir))
    print("\n")
    print(files_in_tei)


    files_original = os.listdir(dir_original)
    for file in files_original:
        path_to_file = os.path.join(dir_original, file)
        if (os.path.isfile(path_to_file)):
            shutil.copy(path_to_file, str(original_dir))

    files_in_original = os.listdir(str(original_dir))
    print("\n")
    print(files_in_original)


    inject_text.inject_text_div(str(tei_dir), str(original_dir))

    files_in_tei = os.listdir(str(tei_dir))
    print("\n")
    print(files_in_tei)

    # TODO: Finish writing this test by check if file with errors was created and  it had correct content and refactor this test

    assert 'a' == 'b'


































