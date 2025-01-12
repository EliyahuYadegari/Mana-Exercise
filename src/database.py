import sqlite3
import pandas as pd
import streamlit as st
from pydantic import BaseModel


class Database:
    def __init__(self, db_name="results.db"):
        self.db_name = db_name

    def create_table_from_pydantic(self, model: BaseModel):
        create_statement = "CREATE TABLE IF NOT EXISTS data_table ("

        type_mapping = {
            str: 'TEXT',
            int: 'INTEGER',
            float: 'REAL',
            bool: 'BOOLEAN'
        }

        fields = []
        for field_name, field_type in model.model_fields.items():
            sqlite_type = type_mapping.get(field_type.annotation, 'TEXT')
            fields.append(f'"{field_name}" {sqlite_type}')

        create_statement += ", ".join(fields) + ")"

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(create_statement)
        conn.commit()
        conn.close()


    def store_results(self, results_df):
        if results_df.empty:
            st.warning("No data to store.")
            return

        for col in results_df.columns:
            if results_df[col].dtype == 'object' or pd.api.types.is_datetime64_any_dtype(results_df[col].dtype):
                results_df[col] = results_df[col].astype(str)

        conn = sqlite3.connect(self.db_name)

        try:
            results_df.to_sql('data_table', conn, if_exists='append', index=False)
        except Exception as e:
            st.error(f"An error occurred during SQL operation: {e}")
        finally:
            conn.close()



    def fetch_all_data(self):
        conn = sqlite3.connect(self.db_name)
        query = "SELECT * FROM data_table"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

