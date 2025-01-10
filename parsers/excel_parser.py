import pandas as pd # type: ignore
from parsers.parser_interface import BaseParser

class ExcelParser(BaseParser):
    def can_parse(self, file_path: str) -> bool:
        return file_path.endswith('.xlsx')

    def parse(self, file_path: str):
        return pd.read_excel(file_path)
