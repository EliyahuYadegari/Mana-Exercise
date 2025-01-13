from database import Database
from interface import ExpirementResult

if __name__ == "__main__":
    db = Database()
    db.init_db_file()
    db.create_table_from_pydantic(ExpirementResult)
