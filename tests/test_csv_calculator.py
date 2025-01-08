import sys
import os
import pytest
import polars as pl

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Calculators')))
from csv_calculator import CsvCalculator

VALID_CSV_FILE = "samples/zeta_valid.csv"
INVALID_CSV_FILE = "samples/zeta_invalid.csv"

@pytest.fixture
def calculator():
    return CsvCalculator()

def test_csv_file_exists():
    assert os.path.exists(VALID_CSV_FILE), f"File does not exist: {VALID_CSV_FILE}"

def test_csv_invalid_file_exists():
    assert os.path.exists(INVALID_CSV_FILE), f"File does not exist: {INVALID_CSV_FILE}"

def test_csv_calculate_invalid_data_raises_exception(calculator):
    data = pl.read_csv(INVALID_CSV_FILE)
    with pytest.raises(ValueError, match="Invalid Zeta potential value"):
        calculator.calculate(data)

def test_csv_calculate_valid_data(calculator):
    data = pl.read_csv(VALID_CSV_FILE)
    result = calculator.calculate(data)
    assert not result.empty, "Calculation result should not be empty"
    assert "Normalized Value" in result.columns, "Result should contain 'Normalized Value' column"
    assert all(result["Normalized Value"] > 0), "All normalized values should be positive"
