# Interface for all the posible parsers

class BaseParser:

    def can_parse(self, file_path: str) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")

    def parse(self, file_path: str):
        raise NotImplementedError("Subclasses must implement this method.")
