import pandas as pd
import pytest

from calculators import CsvCalculator, ExcelCalculator
from interface import ExpirementResult


@pytest.fixture
def csv_data():
    return pd.read_csv("tests/resources/zeta_valid.csv")


@pytest.fixture
def excel_data():
    return pd.read_excel("tests/resources/tns_valid.xlsx")


def test_csv_calculator_length(csv_data):
    calculator = CsvCalculator()
    uuid = uuid.uuid4()
    results = calculator.calculate(csv_data, str(uuid))
    assert len(results) > 0


def test_csv_calculator_type(csv_data):
    calculator = CsvCalculator()
    uuid = uuid.uuid4()
    results = calculator.calculate(csv_data, str(uuid))
    assert isinstance(results[0], ExpirementResult)


def test_csv_calculator_experiment_id(csv_data):
    calculator = CsvCalculator()
    uuid = uuid.uuid4()
    results = calculator.calculate(csv_data, str(uuid))
    assert results[0].experiment_id == uuid


def test_excel_calculator_length(excel_data):
    calculator = ExcelCalculator()
    uuid = uuid.uuid4()
    results = calculator.calculate(excel_data, str(uuid))
    assert len(results) > 0


def test_excel_calculator_type(excel_data):
    calculator = ExcelCalculator()
    uuid = uuid.uuid4()
    results = calculator.calculate(excel_data, str(uuid))
    assert isinstance(results[0], ExpirementResult)


def test_excel_calculator_experiment_id(excel_data):
    calculator = ExcelCalculator()
    uuid = uuid.uuid4()
    results = calculator.calculate(excel_data, str(uuid))
    assert results[0].experiment_id == uuid
