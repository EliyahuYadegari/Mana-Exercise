import pandas as pd

from parsers import CsvParser, ExcelParser


def test_csv_parser_can_parse():
    csv_parser = CsvParser()
    result = csv_parser.can_parse("test.csv")
    assert result == True


def test_csv_parser_cannot_parse():
    csv_parser = CsvParser()
    result = csv_parser.can_parse("test.xlsx")
    assert result == False


def test_excel_parser_can_parse():
    excel_parser = ExcelParser()
    result = excel_parser.can_parse("test.xlsx")
    assert result == True


def test_excel_parser_cannot_parse():
    excel_parser = ExcelParser()
    result = excel_parser.can_parse("test.csv")
    assert result == False


def test_csv_parser_parse():
    csv_parser = CsvParser()
    test_data = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    test_data.to_csv("test.csv", index=False)
    result = csv_parser.parse("test.csv")
    assert result.shape == (2, 2)


def test_excel_parser_parse():
    excel_parser = ExcelParser()
    test_data = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    test_data.to_excel("test.xlsx", index=False)
    result = excel_parser.parse("test.xlsx")
    assert result.shape == (2, 2)
