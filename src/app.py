from src.calculators import CsvCalculator, ExcelCalculator
from src.parsers import CsvParser, ExcelParser
from src.database import Database
from subprocess import call
import streamlit as st
import pandas as pd
import uuid
import os

db = Database()

parsers = {
    "csv": CsvParser(),
    "xlsx": ExcelParser(),
}

calculators = {
    "csv": CsvCalculator(),
    "xlsx": ExcelCalculator(),
}


def parse_and_calculate(file_path: str, uuid_str)-> pd.DataFrame:
    file_extension = file_path.split('.')[-1]
    if file_extension not in parsers:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    parser = parsers[file_extension]
    
    if not parser.can_parse(file_path):
        raise ValueError(f"Parser cannot handle file: {file_path}")
    
    data = parser.parse(file_path)
    calculator = calculators[file_extension]
    st.write(data)
    result = calculator.calculate(data, uuid_str)
    df = pd.DataFrame([item.dict() for item in result])
    return df

def statistics_value(numeric_cols, result):
    if not numeric_cols.empty:
        st.write(f"- **Median**: \n{numeric_cols.median()}")
        st.write(f"- **Average**: \n{numeric_cols.mean()}")
        st.write(f"- **Standard Deviation**: \n{numeric_cols.std()}")
    else:
        st.warning("No numeric columns found for statistics computation.")
    valid_experiments = result["result"].notna().sum()
    total_experiments = len(result)
    invalid_experiments = total_experiments - valid_experiments

    valid_percentage = (valid_experiments / total_experiments) * 100
    invalid_percentage = (invalid_experiments / total_experiments) * 100
    st.write(f"✅ **Valid experiments**: {valid_experiments} ({valid_percentage:.2f}%)")
    st.write(f"❌ **Invalid experiments**: {invalid_experiments} ({invalid_percentage:.2f}%)")

def main():
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

    if "data_saved" not in st.session_state:
        st.session_state["data_saved"] = False

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

                st.write("### 📈 File Statistics")
                numeric_cols = result.select_dtypes(include=["number"])
                statistics_value(numeric_cols, result)

                # Save the results for every uploaded file
                db.store_results(result)
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
                experiment_types = data_df["experiment_type"].unique()
                selected_type = st.selectbox("Select Experiment Type", ["All"] + list(experiment_types))

                if selected_type != "All":
                    data_df = data_df[data_df["experiment_type"] == selected_type]

                st.dataframe(data_df)

                st.write("### 📈 Overall Statistics")
                data_df["result"] = pd.to_numeric(data_df["result"], errors="coerce")
                numeric_cols = data_df[["result"]].dropna()
                numeric_cols.select_dtypes(include=["number"])
                statistics_value(numeric_cols, data_df)

        except Exception as e:
            st.error(f"⚠️ Failed to load data from the database: {e}")

if __name__ == "__main__":
    if not os.path.exists('results.db'):
        call(['python', 'scripts/init_db.py'])
    main()