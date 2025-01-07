import sqlite3
import pandas as pd

class Database:
    def __init__(self, db_name="results.db"):
        self.db_name = db_name

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS data_table (
                            "Sample Name" TEXT,
                            "Zeta Potential (mV)" REAL,
                            "Normalized Value" REAL
                        )''')

        conn.commit()
        conn.close()

    def store_results(self, results_df):
        
        conn = sqlite3.connect(self.db_name)
        results_df.to_sql('data_table', conn, if_exists='replace', index=False)
        conn.close()
