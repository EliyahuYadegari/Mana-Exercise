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

