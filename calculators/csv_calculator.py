import pandas as pd  # type: ignore
from interface import ExpirementResult
from typing import List

class CsvCalculator:
    def calculate(self, data: pd.DataFrame, uuid_str) -> List[ExpirementResult]:
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
                results.append(ExpirementResult(sample_name=formulation_name,
                                                result=normalized_value,
                                                experiment_id=uuid_str,
                                                experiment_type="Zeta_potential"))
            else:
                results.append(ExpirementResult(sample_name=formulation_name,
                                                result=None,
                                                experiment_id=uuid_str,
                                                experiment_type="Zeta_potential"))

        return results
