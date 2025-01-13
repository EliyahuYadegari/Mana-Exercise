import os
import uuid

import pandas as pd
import streamlit as st

from calculators import CsvCalculator, ExcelCalculator
from database import Database
from parsers import CsvParser, ExcelParser


def parse_and_calculate(file_path: str, uuid_str) -> pd.DataFrame:
    parsers = {"csv": CsvParser(), "xlsx": ExcelParser()}
    calculators = {"csv": CsvCalculator(), "xlsx": ExcelCalculator()}
    file_extension = file_path.split(".")[-1]
    if file_extension not in parsers:
        raise ValueError(f"Unsupported file type: {file_extension}")

    parser = parsers[file_extension]

    if not parser.can_parse(file_path):
        raise ValueError(f"Parser cannot handle file: {file_path}")

    data = parser.parse(file_path)
    calculator = calculators[file_extension]
    result = calculator.calculate(data, uuid_str)

    df = pd.DataFrame([{**item.model_dump(), "experiment_id": str(item.experiment_id)} for item in result])
    return df


def display_statistics(numeric_cols, result):
    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 📊 Key Metrics")
        if not numeric_cols.empty:
            st.metric("Median", f"{numeric_cols.median()['result']:.2f}")
            st.metric("Average", f"{numeric_cols.mean()['result']:.2f}")
            st.metric("Standard Deviation", f"{numeric_cols.std()['result']:.2f}")
        else:
            st.warning("No numeric columns found for statistics computation.")

    with col2:
        st.write("#### 🎯 Experiment Status")
        valid_experiments = result["result"].notna().sum()
        total_experiments = len(result)
        invalid_experiments = total_experiments - valid_experiments

        valid_percentage = (valid_experiments / total_experiments) * 100
        invalid_percentage = (invalid_experiments / total_experiments) * 100

        st.metric(
            "Valid Experiments", f"{valid_experiments}", f"{valid_percentage:.1f}%"
        )
        st.metric(
            "Invalid Experiments",
            f"{invalid_experiments}",
            f"{invalid_percentage:.1f}%",
        )


def main():
    st.set_page_config(page_title="Lab Results Analyzer", layout="wide")
    st.title("🔬 Laboratory Results Management")

    db = Database()

    st.header("📤 Upload New Experiment Results")
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

                st.subheader("📊 New Data Statistics")
                numeric_cols = result.select_dtypes(include=["number"])
                display_statistics(numeric_cols, result)

                st.subheader("📋 Uploaded Data Preview")
                st.dataframe(result)

                db.store_results(result)
                st.success("📥 Results saved to the database.")

            else:
                st.error("❌ Error: The processed result is not a valid DataFrame.")

        except Exception as e:
            st.error(f"⚠️ An error occurred during processing: {e}")

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    try:
        data_df = db.fetch_all_data()
        if not data_df.empty:
            st.header("📈 Overall Laboratory Statistics")

            experiment_types = data_df["experiment_type"].unique()
            selected_type = st.selectbox(
                "Select Experiment Type", ["All"] + list(experiment_types)
            )

            if selected_type != "All":
                data_df = data_df[data_df["experiment_type"] == selected_type]

            data_df["result"] = pd.to_numeric(data_df["result"], errors="coerce")
            numeric_cols = data_df[["result"]].dropna()
            display_statistics(numeric_cols, data_df)

            st.subheader("📋 Data Overview")
            st.dataframe(data_df)
        else:
            st.info(
                "📭 No data available yet. Upload your first experiment results below!"
            )
    except Exception as e:
        st.error(f"⚠️ Failed to load data from the database: {e}")


if __name__ == "__main__":
    main()
