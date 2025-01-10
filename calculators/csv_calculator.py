import pandas as pd  # type: ignore

class CsvCalculator:
    def calculate(self, data: pd.DataFrame, uuid_str):
        std_data = data[data["Sample Name"].str.contains("STD", na=False)]
        std_avg = std_data["Zeta Potential (mV)"].mean()

        formulations = data[data["Sample Name"].str.contains("FORMULATION", na=False)]

        results = []

        unique_formulations = formulations["Sample Name"].unique()
        for formulation_name in unique_formulations:
            formulation_data = formulations[formulations["Sample Name"] == formulation_name]

            avg_reading = formulation_data["Zeta Potential (mV)"].mean()

            normalized_value = avg_reading / std_avg

            if normalized_value > 0:
                results.append({
                    "Sample Name": formulation_name,
                    "Result": normalized_value,
                    "Experiment_ID": uuid_str,
                    "Experiment_type": "Zeta_potentiol"
                })
            else:
                results.append({
                    "Sample Name": formulation_name,
                    "Result": None,
                    "Experiment_ID": uuid_str,
                    "Experiment_type": "Zeta_potentiol"
                })

        return pd.DataFrame(results)
