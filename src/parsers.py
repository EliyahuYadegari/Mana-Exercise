import pandas as pd


class BaseParser:
    def can_parse(self, file_path: str) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")

    def parse(self, file_path: str):
        raise NotImplementedError("Subclasses must implement this method.")


class CsvParser(BaseParser):
    def can_parse(self, file_path: str) -> bool:
        return file_path.endswith(".csv")

    def parse(self, file_path: str):
        return pd.read_csv(file_path)


class ExcelParser(BaseParser):
    def can_parse(self, file_path: str) -> bool:
        return file_path.endswith(".xlsx")

    def parse(self, file_path: str):
        return pd.read_excel(file_path)
