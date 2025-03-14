import json
import os
from typing import Any, Dict

from jinja2 import BaseLoader, Environment

from go2jinja import convert
from tests.command import Command


def get_test_directory() -> str:
    return os.path.join(".", "tests")


def load_data_file(json_file: str) -> Dict[str, Any]:
    # transforming all keys to be lower case as
    # - Go Templates (usually) use upper case variable names
    # - Jinja Templates (usually) use lower case variable names
    def transform_names(data: Any):
        if isinstance(data, list):
            for item in data:
                transform_names(item)
        if isinstance(data, dict):
            keys = [key for key in data.keys()]
            for key in keys:
                newKey = key.lower()
                data[newKey] = data[key]
                del data[key]
                if isinstance(data[newKey], dict) or isinstance(data[newKey], list):
                    transform_names(data[newKey])
        return data

    with open(json_file) as f:
        return transform_names(json.loads(f.read()))


def run_test(test_name: str, input_file: str, go_file: str = ""):
    data_file = os.path.join(get_test_directory(), test_name, "data", input_file)
    gotmpl_file = os.path.join(
        get_test_directory(),
        test_name,
        f"{test_name}.gotmpl" if go_file == "" else go_file,
    )

    gotmpl = ""
    with open(gotmpl_file, "r") as f:
        gotmpl = f.read()
    jinjatmpl = convert.go_to_jinja(gotmpl)

    go_out = Command(
        f"{os.path.join(get_test_directory(), 'gotemplate', 'gotemplate')}"
        f" -data-file={data_file} -go-template={gotmpl_file}"
    ).run()

    data = load_data_file(data_file)
    if len(data) != 1:
        raise Exception("Wrong number of test cases. Expected only 1.")

    jinja_out = ""
    for _, test_data in data.items():
        try:
            rtemplate = Environment(
                loader=BaseLoader, keep_trailing_newline=True
            ).from_string(jinjatmpl)
        except Exception as ex:
            print("Failed to load jinja template:")
            print(jinjatmpl)
            raise ex
        jinja_out = rtemplate.render(test_data)

    if go_out != jinja_out:
        print(f"[{test_name}]: Templates are not equal:")
        print(f"Go Output:\n'{go_out}'")
        print(f"Jinja Output:\n'{jinja_out}'")
        print()
        assert go_out == jinja_out
