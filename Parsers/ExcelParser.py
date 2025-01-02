from Parsers import BaseParser
import polars as pl # type: ignore

class ExcelParser(BaseParser):
    def can_parse(self, file_path: str) -> bool:
        return file_path.endswith('.xlsx')

    def parse(self, file_path: str):
        return pl.read_excel(file_path)
