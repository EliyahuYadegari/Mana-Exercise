import streamlit as st  # type: ignore
import uuid
from main import parse_file, save_to_database
from database import Database
import pandas as pd  # type: ignore

db = Database()

st.set_page_config(page_title="Lab Results Analyzer", layout="wide")

st.title("📊 Laboratory Results Management")

st.header("📂 View Stored Results")

try:
    data_df = db.fetch_all_data()
    if data_df.empty:
        st.info("The database is currently empty.")
    else:
        st.dataframe(data_df)
except Exception as e:
    st.error(f"Failed to load data from the database: {e}")

st.header("📤 Upload New Experiment Results 🔬")
uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"],
    help="Upload experiment results from TNS or Zeta Potential experiments",
)

if uploaded_file is not None:
    temp_path = f"temp_{uuid.uuid4()}_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        result = parse_file(temp_path)
        st.success("File processed successfully!")
        st.write(result)
        
        if isinstance(result, pd.DataFrame):
            save_to_database(result)
            st.success("Results saved to database.")
        else:
            st.error("Error: The result is not a valid DataFrame.")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
