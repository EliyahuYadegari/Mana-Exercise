from parsers.csv_parser import CsvParser
from parsers.excel_parser import ExcelParser
from calculators.csv_calculator import CsvCalculator
from calculators.excel_calculator import ExcelCalculator
from database import Database
import pandas as pd # type: ignore
import streamlit as st  # type: ignore
# import uuid


# db = Database()


parsers = {
    "csv": CsvParser(),
    "xlsx": ExcelParser(),
}

calculators = {
    "csv": CsvCalculator(),
    "xlsx": ExcelCalculator(),
}

def parse_and_calculate(file_path: str, uuid_str)-> pd.DataFrame:
    file_extension = file_path.split('.')[-1]
    if file_extension not in parsers:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    parser = parsers[file_extension]
    
    if not parser.can_parse(file_path):
        raise ValueError(f"Parser cannot handle file: {file_path}")
    
    data = parser.parse(file_path)
    calculator = calculators[file_extension]
    if st.button("Show file"):
        st.write(data)
    result = calculator.calculate(data, uuid_str)
    df = pd.DataFrame([item.dict() for item in result])
    return df

    

# if __name__ == "__main__":
    
#     file_path_csv = "samples/zeta_valid.csv"
#     result_csv = parse_file(file_path_csv)
#     print(f"Processed CSV file: {result_csv}")
#     save_to_database(pd.DataFrame(result_csv))

#     file_path_excel = "samples/tns_valid.xlsx"
#     result_excel = parse_file(file_path_excel)
#     print(f"Processed Excel file: {result_excel}")
#     save_to_database(result_excel)
