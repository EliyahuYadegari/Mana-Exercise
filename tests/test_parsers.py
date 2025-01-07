import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Parsers.csv_parser import CsvParser
from Parsers.excel_parser import ExcelParser

@pytest.mark.parametrize("parser_class, file_path", [
    (CsvParser, "samples/zeta_valid.csv"),
    (ExcelParser, "samples/tns_valid.xlsx"),
])
def test_parsers(parser_class, file_path):
    parser = parser_class()
    assert os.path.exists(file_path), f"File does not exist: {file_path}"
    assert parser.can_parse(file_path), f"{parser_class.__name__} should handle this file type"
    data = parser.parse(file_path)
    assert data is not None, f"Parsed data by {parser_class.__name__} should not be None"
    assert len(data) > 0, f"Parsed data by {parser_class.__name__} should not be empty"
