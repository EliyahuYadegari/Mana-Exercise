from Parsers.csv_parser import CsvParser
from Parsers.excel_parser import ExcelParser

parsers = {
    "csv": CsvParser(),
    "xlsx": ExcelParser(),
}

def parse_file(file_path: str):
    for parser in parsers.values():
        if parser.can_parse(file_path):
            return parser.parse(file_path)
    raise ValueError(f"No suitable parser found for file: {file_path}")

if __name__ == "__main__":
    file_path_csv = "samples/zeta_valid.csv"
    file_path_excel = "samples/tns_valid.xlsx"

    try:
        csv_data = parse_file(file_path_csv)
        print("CSV Data:")
        print(csv_data)
    except ValueError as e:
        print(e)

    try:
        excel_data = parse_file(file_path_excel)
        print("Excel Data:")
        print(excel_data)
    except ValueError as e:
        print(e)
