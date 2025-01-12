from src.database import Database
from src.interface import ExpirementResult

if __name__ == "__main__":
    db = Database()
    db.create_table_from_pydantic(ExpirementResult)
