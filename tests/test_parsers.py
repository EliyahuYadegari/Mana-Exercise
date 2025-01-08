import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Parsers.csv_parser import CsvParser
from Parsers.excel_parser import ExcelParser

test_cases = [
    (CsvParser, "samples/zeta_valid.csv"),
    (ExcelParser, "samples/tns_valid.xlsx"),
]

@pytest.mark.parametrize("parser_class, file_path", test_cases)
def test_file_exists(parser_class, file_path):
    assert os.path.exists(file_path), f"File does not exist: {file_path}"

@pytest.mark.parametrize("parser_class, file_path", test_cases)
def test_parser_can_handle_file_type(parser_class, file_path):
    parser = parser_class()
    assert parser.can_parse(file_path), f"{parser_class.__name__} cannot handle this file type"

@pytest.mark.parametrize("parser_class, file_path", test_cases)
def test_parser_returns_data(parser_class, file_path):
    parser = parser_class()
    data = parser.parse(file_path)
    assert data is not None, f"Parsed data by {parser_class.__name__} is None"

@pytest.mark.parametrize("parser_class, file_path", test_cases)
def test_parsed_data_not_empty(parser_class, file_path):
    parser = parser_class()
    data = parser.parse(file_path)
    assert len(data) > 0, f"Parsed data by {parser_class.__name__} is empty"
