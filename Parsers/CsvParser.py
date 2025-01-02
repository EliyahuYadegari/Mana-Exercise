from Parsers import BaseParser
import polars as pl # type: ignore

class CsvParser(BaseParser):
    def can_parse(self, file_path: str) -> bool:
        return file_path.endswith('.csv')

    def parse(self, file_path: str):
        return pl.read_csv(file_path)
