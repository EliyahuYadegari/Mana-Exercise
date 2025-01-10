import sqlite3
import pandas as pd # type: ignore
import streamlit as st  # type: ignore


class Database:
    def __init__(self, db_name="results.db"):
        self.db_name = db_name

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS data_table (
                            "Sample Name" TEXT,
                            "Result" REAL,
                            "Experiment_ID" TEXT,
                            "Experiment_type" TEXT
                        )''')
        conn.commit()
        conn.close()

    def store_results(self, results_df):
        if results_df.empty:
            st.warning("No data to store.")
            return

        conn = sqlite3.connect(self.db_name)
        
        st.write("---זה מופיע---")

        results_df.to_sql('data_table', conn, if_exists='append', index=False)

        st.write("---זה לא מופיע---")
        conn.close()



    def fetch_all_data(self):
        conn = sqlite3.connect(self.db_name)
        query = "SELECT * FROM data_table"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

