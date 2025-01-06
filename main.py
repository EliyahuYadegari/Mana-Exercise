import os
from Parsers.csv_parser import CsvParser
from Parsers.excel_parser import ExcelParser
from Calculators.csv_calculator import CsvCalculator
from Calculators.excel_calculator import ExcelCalculator
from database import Database
import polars as pl
import pandas as pd

db = Database()
db.create_table()

parsers = {
    "csv": CsvParser(),
    "xlsx": ExcelParser(),
}

calculators = {
    "csv": CsvCalculator(),
    "xlsx": ExcelCalculator(),
}

def parse_file(file_path: str):
    file_extension = file_path.split('.')[-1]
    if file_extension not in parsers:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    parser = parsers[file_extension]
    
    if not parser.can_parse(file_path):
        raise ValueError(f"Parser cannot handle file: {file_path}")
    
    data = parser.parse(file_path)
    
    calculator = calculators[file_extension]
    result = calculator.calculate(data)
    
    return result

def save_to_database(results_df):
    db.store_results(results_df)

if __name__ == "__main__":
    
    file_path_csv = "samples/zeta_valid.csv"
    result_csv = parse_file(file_path_csv)
    print(f"Processed CSV file: {result_csv}")
    save_to_database(pd.DataFrame(result_csv))

    file_path_excel = "samples/tns_valid.xlsx"
    result_excel = parse_file(file_path_excel)
    print(f"Processed Excel file: {result_excel}")
    save_to_database(result_excel)
