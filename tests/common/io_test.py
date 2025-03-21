import unittest

from repro2.common.io import read_jsonl_file, write_to_jsonl_file, write_to_text_file
from repro2.common import TemporaryDirectory


class TestIO(unittest.TestCase):
    def test_write_to_text_file(self):
        with TemporaryDirectory() as temp:
            file_path = f"{temp}/file.txt"

            items = ["1", "2", "3"]
            write_to_text_file(items, file_path)
            assert open(file_path, "r").read().splitlines() == ["1", "2", "3"]

            items = [["1a", "1b"], ["2"], "3"]
            write_to_text_file(items, file_path)
            assert open(file_path, "r").read().splitlines() == ["1a 1b", "2", "3"]

            items = [["1a", "1b"], ["2"], "3"]
            write_to_text_file(items, file_path, separator="-")
            assert open(file_path, "r").read().splitlines() == ["1a-1b", "2", "3"]

    def test_read_write_jsonl(self):
        with TemporaryDirectory() as temp:
            file_path = f"{temp}/file.txt"

            items = ["1", "2", "3"]
            write_to_jsonl_file(items, "item", file_path)
            assert read_jsonl_file(file_path) == [
                {"item": "1"},
                {"item": "2"},
                {"item": "3"},
            ]

            items = [["1a", "1b"], ["2"], "3"]
            write_to_jsonl_file(items, "item", file_path)
            assert read_jsonl_file(file_path) == [
                {"item": ["1a", "1b"]},
                {"item": ["2"]},
                {"item": "3"},
            ]

            items = [["1a", "1b"], ["2"], "3"]
            write_to_jsonl_file(items, "item", file_path, flatten=True)
            assert read_jsonl_file(file_path) == [
                {"item": "1a 1b"},
                {"item": "2"},
                {"item": "3"},
            ]

            items = [["1a", "1b"], ["2"], "3"]
            write_to_jsonl_file(items, "item", file_path, flatten=True, separator="-")
            assert read_jsonl_file(file_path) == [
                {"item": "1a-1b"},
                {"item": "2"},
                {"item": "3"},
            ]

    def test_read_jsonl_single_line(self):
        with TemporaryDirectory() as temp:
            file_path = f"{temp}/file.txt"

            with open(file_path, "w") as out:
                out.write('{"item": "1"}{"item": "2"}{"item": "3"}')

            assert read_jsonl_file(file_path, single_line=True) == [
                {"item": "1"},
                {"item": "2"},
                {"item": "3"},
            ]
