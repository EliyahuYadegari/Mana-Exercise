# Interface for all the posible parsers

class BaseParser:
    # Checks if the parser matches the file
    def can_parse(self, file_path: str) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")

    # Decrypts the file
    def parse(self, file_path: str):
        raise NotImplementedError("Subclasses must implement this method.")
