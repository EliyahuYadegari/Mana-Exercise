import polars as pl

class CsvCalculator:
    def calculate(self, data: pl.DataFrame):
        # מחשבים את ממוצע הקריאות עבור STD
        std_data = data.filter(pl.col("Sample Name").str.contains("STD"))
        std_avg = std_data["Zeta Potential (mV)"].mean()

        # הפורמולציות
        formulations = data.filter(pl.col("Sample Name").str.contains("FORMULATION"))

        results = []

        # עבור כל פורמולציה, מחשבים את הממוצע של 3 הקריאות ומבצעים נרמול לפי ממוצע ה-STD
        unique_formulations = formulations["Sample Name"].unique()
        
        for formulation_name in unique_formulations:
            formulation_data = data.filter(pl.col("Sample Name") == formulation_name)
            avg_reading = formulation_data["Zeta Potential (mV)"].mean()
            normalized_value = avg_reading / std_avg

            if normalized_value > 0:
                results.append({
                    "Sample Name": formulation_name,
                    "Zeta Potential (mV)": avg_reading,
                    "Normalized Value": normalized_value
                })
            else:
                raise ValueError(f"Invalid Zeta potential value for {formulation_name}.")

        return results
