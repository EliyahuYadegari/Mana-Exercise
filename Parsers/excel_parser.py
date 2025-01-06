import polars as pl
from base_parser import BaseParser

class ExcelParser(BaseParser):
    def can_parse(self, file_path: str) -> bool:
        return file_path.endswith('.xlsx')

    def parse(self, file_path: str):
        return pl.read_excel(file_path)
