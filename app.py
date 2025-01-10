import streamlit as st  # type: ignore
import uuid
from main import parse_and_calculate, save_to_database
from database import Database
import pandas as pd  # type: ignore
import os

db = Database()

st.set_page_config(page_title="Lab Results Analyzer", layout="wide")
st.title("📊 Laboratory Results Management")
st.write(
    """
    Efficiently upload, process, and analyze laboratory results. 
    View stored data and compute essential statistics with ease.
    """
)



st.header("📤 Upload New Experiment Results 🔬")
uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"],
    help="Upload experiment results from TNS or Zeta Potential experiments",
)


if uploaded_file is not None:
    uuid_str = uuid.uuid4()
    temp_path = f"temp_{uuid_str}_{uploaded_file.name}"

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        result = parse_and_calculate(temp_path, uuid_str)
        
        if isinstance(result, pd.DataFrame):
            st.success("✅ File processed successfully!")
            st.dataframe(result)

            st.write("### 📈 Overall Statistics")
            numeric_cols = result.select_dtypes(include=["number"])
            if not numeric_cols.empty:
                st.write(f"- **Median**: \n{numeric_cols.median()}")
                st.write(f"- **Average**: \n{numeric_cols.mean()}")
                st.write(f"- **Standard Deviation**: \n{numeric_cols.std()}")
            else:
                st.warning("No numeric columns found for statistics computation.")

            save_to_database(result)
            st.success("📥 Results saved to the database.")
        else:
            st.error("❌ Error: The processed result is not a valid DataFrame.")

    except Exception as e:
        st.error(f"⚠️ An error occurred during processing: {e}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    st.header("📂 View Stored Results")

    try:
        data_df = db.fetch_all_data()

        if data_df.empty:
            st.info("🔍 The database is currently empty.")
        else:
            st.dataframe(data_df)
            st.write("### Summary Statistics")
            st.write(data_df.describe())

    except Exception as e:
        st.error(f"⚠️ Failed to load data from the database: {e}")
