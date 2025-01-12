from src.interface import ExpirementResult
from src.database import Database

if __name__ == "__main__":
    db = Database()
    db.create_table_from_pydantic(ExpirementResult)
