import uuid
import pytest
import pandas as pd
from src.calculators import CsvCalculator, ExcelCalculator
from src.interface import ExpirementResult

@pytest.fixture
def csv_data():
    return pd.read_csv("tests/samples/zeta_valid.csv")

@pytest.fixture
def excel_data():
    return pd.read_excel("tests/samples/tns_valid.xlsx")

def test_csv_calculator_length(csv_data):
    calculator = CsvCalculator()
    uuid_str = uuid.uuid4()
    results = calculator.calculate(csv_data, str(uuid_str))
    assert len(results) > 0

def test_csv_calculator_type(csv_data):
    calculator = CsvCalculator()
    uuid_str = uuid.uuid4()
    results = calculator.calculate(csv_data, str(uuid_str))
    assert isinstance(results[0], ExpirementResult)

def test_csv_calculator_experiment_id(csv_data):
    calculator = CsvCalculator()
    uuid_str = uuid.uuid4()
    results = calculator.calculate(csv_data, str(uuid_str))
    assert results[0].experiment_id == uuid_str

def test_excel_calculator_length(excel_data):
    calculator = ExcelCalculator()
    uuid_str = uuid.uuid4()
    results = calculator.calculate(excel_data, str(uuid_str))
    assert len(results) > 0

def test_excel_calculator_type(excel_data):
    calculator = ExcelCalculator()
    uuid_str = uuid.uuid4()
    results = calculator.calculate(excel_data, str(uuid_str))
    assert isinstance(results[0], ExpirementResult)

def test_excel_calculator_experiment_id(excel_data):
    calculator = ExcelCalculator()
    uuid_str = uuid.uuid4()
    results = calculator.calculate(excel_data, str(uuid_str))
    assert results[0].experiment_id == uuid_str
