import pandas as pd
from parsers.parser_interface import BaseParser

class CsvParser(BaseParser):
    def can_parse(self, file_path: str) -> bool:
        return file_path.endswith('.csv')

    def parse(self, file_path: str):
        return pd.read_csv(file_path)
