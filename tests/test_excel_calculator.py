import sys
import os
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Calculators')))
from excel_calculator import ExcelCalculator

VALID_EXCEL_FILE = "samples/tns_valid.xlsx"
INVALID_EXCEL_FILE = "samples/tns_invalid.xlsx"

@pytest.fixture
def calculator():
    return ExcelCalculator()

def test_excel_file_exists():
    assert os.path.exists(VALID_EXCEL_FILE), f"File does not exist: {VALID_EXCEL_FILE}"

def test_excel_invalid_file_exists():
    assert os.path.exists(INVALID_EXCEL_FILE), f"File does not exist: {INVALID_EXCEL_FILE}"

def test_excel_calculate_invalid_data_raises_exception(calculator):
    with pytest.raises(ValueError, match="Invalid data in Excel file: contains NaN values after cleaning"):
        calculator.calculate(INVALID_EXCEL_FILE)

def test_excel_calculate_valid_file_returns_dataframe(calculator):
    result = calculator.calculate(VALID_EXCEL_FILE)
    assert isinstance(result, pd.DataFrame), "The result is not a DataFrame for a valid Excel file"

def test_excel_calculate_valid_dataframe_not_empty(calculator):
    result = calculator.calculate(VALID_EXCEL_FILE)
    assert not result.empty, "The result DataFrame is empty for a valid Excel file"

def test_excel_calculate_formulation_column_exists(calculator):
    result = calculator.calculate(VALID_EXCEL_FILE)
    assert "Formulation" in result.columns, "The result DataFrame does not contain a 'Formulation' column"

def test_excel_calculate_result_column_exists(calculator):
    result = calculator.calculate(VALID_EXCEL_FILE)
    assert "Result" in result.columns, "The result DataFrame does not contain a 'Result' column"

def test_excel_calculate_normalized_values_greater_than_ten(calculator):
    result = calculator.calculate(VALID_EXCEL_FILE)
    assert all(result["Result"] > 10), "Some normalized values are not greater than 10"

def test_excel_calculate_formulations_are_sequential(calculator):
    result = calculator.calculate(VALID_EXCEL_FILE)
    formulation_numbers = [int(f.split(" ")[1]) for f in result["Formulation"]]
    assert formulation_numbers == list(range(1, len(formulation_numbers) + 1)), "Formulation numbers are not sequential"
