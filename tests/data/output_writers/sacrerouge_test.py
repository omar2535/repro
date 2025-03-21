import unittest

from repro2.data.output_writers import SacreROUGEOutputWriter
from repro2.common import TemporaryDirectory
from repro2.common.io import read_jsonl_file


class TestSacreROUGEOutputWriter(unittest.TestCase):
    def test_sacrerouge_output_writer(self):
        writer = SacreROUGEOutputWriter()
        with TemporaryDirectory() as temp:
            output_file = f"{temp}/output.jsonl"

            instances = [
                {"instance_id": "1"},
                {"instance_id": "2", "reference": "ref"},
                {"instance_id": "3", "references": ["ref1", "ref2"]},
            ]
            predictions = ["summary1", "summary2", "summary3"]
            writer.write(instances, predictions, output_file, "test-model")

            outputs = read_jsonl_file(output_file)
            assert outputs == [
                {
                    "instance_id": "1",
                    "summarizer_id": "test-model",
                    "summarizer_type": "peer",
                    "summary": {"text": "summary1"},
                },
                {
                    "instance_id": "2",
                    "summarizer_id": "test-model",
                    "summarizer_type": "peer",
                    "summary": {"text": "summary2"},
                    "reference": {"text": "ref"},
                },
                {
                    "instance_id": "3",
                    "summarizer_id": "test-model",
                    "summarizer_type": "peer",
                    "summary": {"text": "summary3"},
                    "references": [{"text": "ref1"}, {"text": "ref2"}],
                },
            ]

    def test_unequal_number_of_instances_predictions(self):
        writer = SacreROUGEOutputWriter()
        with TemporaryDirectory() as temp:
            output_file = f"{temp}/output.jsonl"

            instances = [
                {"instance_id": "1"},
                {"instance_id": "2", "reference": "ref"},
                {"instance_id": "3", "references": ["ref1", "ref2"]},
            ]
            predictions = ["summary1", "summary2", "summary3", "summary4"]
            with self.assertRaises(Exception):
                writer.write(instances, predictions, output_file, "test-model")

            instances = [
                {"instance_id": "1"},
                {"instance_id": "2", "reference": "ref"},
                {"instance_id": "3", "references": ["ref1", "ref2"]},
                {"instance_id": "4"},
            ]
            predictions = ["summary1", "summary2", "summary3"]
            with self.assertRaises(Exception):
                writer.write(instances, predictions, output_file, "test-model")
