import sqlite3
import pandas as pd # type: ignore
import streamlit as st  # type: ignore
from pydantic import BaseModel


class Database:
    def __init__(self, db_name="results.db"):
        self.db_name = db_name

    def create_table_from_pydantic(self, model: BaseModel):
        # Start building the SQL CREATE TABLE statement
        create_statement = "CREATE TABLE IF NOT EXISTS data_table ("

        # Map Pydantic types to SQLite column types
        type_mapping = {
            str: 'TEXT',
            int: 'INTEGER',
            float: 'REAL',
            bool: 'BOOLEAN'  # SQLite stores BOOLEAN as INTEGER 0 or 1
        }

        # Loop through the fields in the Pydantic model
        fields = []
        # st.write(type(model.model_fields))
        for field_name, field_type in model.model_fields.items():
            sqlite_type = type_mapping.get(field_type.annotation, 'TEXT')
            fields.append(f'"{field_name}" {sqlite_type}')

        # Join all field definitions into the CREATE TABLE statement
        create_statement += ", ".join(fields) + ")"

        # Connect to the SQLite database and execute the CREATE TABLE statement
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(create_statement)
        conn.commit()
        conn.close()

    # def create_table_from_pydantic(self, model: BaseModel):
    #     # Start building the SQL CREATE TABLE statement
    #     create_statement = "CREATE TABLE IF NOT EXISTS data_table ("

    #     # Map Pydantic types to SQLite column types
    #     type_mapping = {
    #         str: 'TEXT',
    #         int: 'INTEGER',
    #         float: 'REAL',
    #         bool: 'BOOLEAN'  # SQLite stores BOOLEAN as INTEGER 0 or 1
    #     }

    #     # Loop through the fields in the Pydantic model
    #     fields = []
    #     for field_name, field_type in model._annotations_.items():
    #         sqlite_type = type_mapping.get(field_type, 'TEXT')
    #         fields.append(f'"{field_name}" {sqlite_type}')

    #     # Join all field definitions into the CREATE TABLE statement
    #     create_statement += ", ".join(fields) + ")"

    #     # Connect to the SQLite database and execute the CREATE TABLE statement
    #     conn = sqlite3.connect(self.db_name)
    #     cursor = conn.cursor()
    #     cursor.execute(create_statement)
    #     conn.commit()
    #     conn.close()

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

        # Convert unsupported data types to string or a supported type
        for col in results_df.columns:
            if results_df[col].dtype == 'object' or pd.api.types.is_datetime64_any_dtype(results_df[col].dtype):
                results_df[col] = results_df[col].astype(str)

        conn = sqlite3.connect(self.db_name)

        st.write("---Before storing data---")
        st.dataframe(results_df)

        try:
            results_df.to_sql('data_table', conn, if_exists='append', index=False)
            st.write("---Data successfully stored---")
        except Exception as e:
            st.error(f"An error occurred during SQL operation: {e}")
        finally:
            conn.close()

    # def store_results(self, results_df):
    #     if results_df.empty:
    #         st.warning("No data to store.")
    #         return

    #     conn = sqlite3.connect(self.db_name)
        
    #     st.write("---עד כאן מופיע---")

    #     st.dataframe(results_df)

    #     results_df.to_sql('data_table', conn, if_exists='append', index=False)

    #     st.write("---זה כבר לא מופיע---")

    #     conn.close()



    def fetch_all_data(self):
        conn = sqlite3.connect(self.db_name)
        query = "SELECT * FROM data_table"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

