import pytest

from tests.helper import run_test

GO_TEMPLATE_FILE = "falcon-instruct.gotmpl"


@pytest.mark.parametrize("file", ["empty.json", "simple.json"])
def test_falcon_instruct(file: str):
    run_test("falcon-instruct", file)
