from Parsers.csv_parser import CsvParser
from Parsers.excel_parser import ExcelParser
import polars as pl
import sqlite3

parsers = {
    "csv": CsvParser(),
    "xlsx": ExcelParser(),
}

# Validation for zeta potential:
# 1. Calculate the average of the control readings (STD) and check if it's positive
# 2. Calculate the average of each formulation, normalized by the control average
# 3. display invalid results if the normalized result is not positive/
def validate_zeta_potential(df: pl.DataFrame) -> pl.DataFrame:
    # avg for the control sample
    control_avg = df.filter(pl.col("Sample Name") == "STD").select(pl.col("Zeta Potential (mV)")).mean().to_numpy()[0]
    
    if control_avg <= 0:
        print("Error: Control average must be positive")
        return pl.DataFrame()
    
    # avg for each formulation
    formulations = df.filter(pl.col("Measurement Type") == "Zeta").select("Sample Name", "Zeta Potential (mV)")
    
    # normalization (the average of the formulation / control_avg)
    formulations = formulations.with_columns(
        (pl.col("Zeta Potential (mV)") / control_avg).alias("normalized_value"))
    
    invalid_results = formulations.filter(pl.col("normalized_value") <= 0)
    
    if not invalid_results.is_empty():
        print("Invalid results detected:")
        print(invalid_results)
    
    # return the valid results
    return formulations.filter(pl.col("normalized_value") > 0)

# Validation for tns:
# 1. For each formulation, calculate the average of 3 readings
# 2. Calculate the average of the control readings in the same row.
# 3. Normalize and analyze if the result exceeds 10
def validate_tns(df: pl.DataFrame) -> pl.DataFrame:
    #  For each formulation row (representing a group of 3 readings)
    formulations = df.filter(pl.col("Instrument:").is_not_null()).select(pl.col("Instrument:")).unique()
    
    results = []
    
    for formulation in formulations["Instrument:"]:
        triplicate_avg = df.filter(pl.col("Instrument:") == formulation).select(pl.col("__UNNAMED__2").mean()).to_numpy()[0]
        control_avg = df.filter(pl.col("__UNNAMED__2").is_null()).select(pl.col("__UNNAMED__2").mean()).to_numpy()[0]
        
        # normalization (triplicate_avg / control_avg)
        normalized_value = triplicate_avg / control_avg
        
        results.append({
            "formulation": formulation,
            "triplicate_avg": triplicate_avg,
            "control_avg": control_avg,
            "normalized_value": normalized_value
        })
    
    invalid_results = [r for r in results if r["normalized_value"] <= 10]
    
    if invalid_results:
        print("Invalid results detected:")
        for result in invalid_results:
            print(result)
    
    # convert the valid results to data-frame
    return pl.DataFrame([r for r in results if r["normalized_value"] > 10])

# Checks if one of the parsers can analyze the file according to the type
def parse_file(file_path: str):
    for parser in parsers.values():
        if parser.can_parse(file_path):
            return parser.parse(file_path)
    raise ValueError(f"No suitable parser found for file: {file_path}")

# save the valid data to the database
def save_to_database(valid_data: pl.DataFrame, db_name: str = "data.db"):

    # connect to database and if the file not exist - create it
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # create a table for valid Zeta Potential data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ZetaResults (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_name TEXT,
            measurement_type TEXT,
            zeta_potential REAL,
            normalized_value REAL
        )
    """)
    
    # Insert valid data into the table
    for row in valid_data.iter_rows(named=True):
        cursor.execute("""
            INSERT INTO ZetaResults (sample_name, measurement_type, zeta_potential, normalized_value)
            VALUES (?, ?, ?, ?)
        """, (row["Sample Name"], row["Measurement Type"], row["Zeta Potential (mV)"], row["normalized_value"]))
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    file_path_csv = "samples/zeta_invalid.csv"
    file_path_excel = "samples/tns_invalid.xlsx"

    try:
        csv_data = parse_file(file_path_csv)
        print("CSV Data:")
        print(csv_data)
        valid_results = validate_zeta_potential(csv_data)
        save_to_database(valid_results)
    except ValueError as e:
        print(e)

    try:
        excel_data = parse_file(file_path_excel)
        print("Excel Data:")
        print(excel_data)
        valid_results = validate_tns(excel_data)
        save_to_database(valid_results)
    except ValueError as e:
        print(e)
