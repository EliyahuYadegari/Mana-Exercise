from typing import List

import pandas as pd

from src.interface import ExpirementResult

ZETA_VALIDATION = 0
TNS_VALIDATION = 10


class BaseCalculator:
    def calculate(self, data: pd.DataFrame, uuid: str) -> List[ExpirementResult]:
        raise NotImplementedError("Subclasses must implement this method.")


class CsvCalculator(BaseCalculator):
    def calculate(self, data: pd.DataFrame, uuid: str) -> List[ExpirementResult]:
        std_data = data[data["Sample Name"].str.contains("STD", na=False)]
        std_avg = std_data["Zeta Potential (mV)"].mean()

        formulations = data[data["Sample Name"].str.contains("FORMULATION", na=False)]

        results = []

        unique_formulations = formulations["Sample Name"].unique()
        for formulation_name in unique_formulations:
            formulation_data = formulations[
                formulations["Sample Name"] == formulation_name
            ]

            avg_reading = formulation_data["Zeta Potential (mV)"].mean()

            normalized_value = avg_reading / std_avg

            if normalized_value > ZETA_VALIDATION:
                results.append(
                    ExpirementResult(
                        sample_name=formulation_name,
                        result=normalized_value,
                        experiment_id=uuid,
                        experiment_type="Zeta_potential",
                    )
                )
            else:
                results.append(
                    ExpirementResult(
                        sample_name=formulation_name,
                        result=None,
                        experiment_id=uuid,
                        experiment_type="Zeta_potential",
                    )
                )

        return results


class ExcelCalculator(BaseCalculator):
    def calculate(self, data: pd.DataFrame, uuid: str) -> List[ExpirementResult]:

        if data.empty:
            raise ValueError("The Excel file is empty.")

        header_row_idx = data.apply(
            lambda row: row.astype(str).str.contains("<>").any(), axis=1
        ).idxmax()

        header = data.iloc[header_row_idx]
        data = data.iloc[header_row_idx + 1 :]

        data.columns = header

        data = data.dropna()
        data.drop(columns="<>", inplace=True)

        if data.isnull().values.any():
            raise ValueError(
                "Invalid data in Excel file: contains NaN values after cleaning."
            )

        control_columns = data.columns[-3:]
        formulation_columns = data.columns[:-3]

        results = []

        formulation_count = 1

        for _, row in data.iterrows():
            triplet_start = 0
            while triplet_start + 3 <= len(formulation_columns):
                triplet_columns = formulation_columns[triplet_start : triplet_start + 3]

                triplet_average = row[triplet_columns].mean()
                control_average = row[control_columns].mean()

                if control_average == 0:
                    raise ValueError(
                        "Control averages contain zeros, causing division by zero."
                    )

                normalized_result = triplet_average / control_average

                if normalized_result > TNS_VALIDATION:
                    results.append(
                        ExpirementResult(
                            sample_name=f"Formulation {formulation_count}",
                            result=normalized_result,
                            experiment_id=uuid,
                            experiment_type="TNS",
                        )
                    )
                else:
                    results.append(
                        ExpirementResult(
                            sample_name=f"Formulation {formulation_count}",
                            result=None,
                            experiment_id=uuid,
                            experiment_type="TNS",
                        )
                    )

                triplet_start += 3
                formulation_count += 1

        if not results:
            raise ValueError("No valid results were calculated.")

        return results
