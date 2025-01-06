import os
from Parsers.csv_parser import CsvParser
from Parsers.excel_parser import ExcelParser
from Calculators.csv_calculator import CsvCalculator
from Calculators.excel_calculator import ExcelCalculator
import polars as pl
import sqlite3

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


# def save_to_database(valid_data: pl.DataFrame, db_name: str = "data.db"):

#     # connect to database and if the file not exist - create it
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()

#     # create a table for valid Zeta Potential data
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS ZetaResults (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             sample_name TEXT,
#             measurement_type TEXT,
#             zeta_potential REAL,
#             normalized_value REAL
#         )
#     """)
    
#     # Insert valid data into the table
#     for row in valid_data.iter_rows(named=True):
#         cursor.execute("""
#             INSERT INTO ZetaResults (sample_name, measurement_type, zeta_potential, normalized_value)
#             VALUES (?, ?, ?, ?)
#         """, (row["Sample Name"], row["Measurement Type"], row["Zeta Potential (mV)"], row["normalized_value"]))
    
#     conn.commit()
#     conn.close()


if __name__ == "__main__":
    file_path_csv = "samples/zeta_invalid.csv"
    file_path_excel = "samples/tns_invalid.xlsx"
