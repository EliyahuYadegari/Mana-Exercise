import pandas as pd  # type: ignore

class ExcelCalculator:
    def calculate(self, data: pd.DataFrame, uuid_str):

        print("Loaded data:", data)

        if data.empty:
            raise ValueError("The Excel file is empty.")
        
        header_row_idx = data.apply(lambda row: row.astype(str).str.contains('<>').any(), axis=1).idxmax()
        
        header = data.iloc[header_row_idx]
        data = data.iloc[header_row_idx + 1:]

        print("Header row:", header)
        print("Data after trimming:", data)

        data.columns = header

        data = data.dropna()
        data.drop(columns='<>', inplace=True)

        # data = data.apply(pd.to_numeric, errors='coerce')
        
        if data.isnull().values.any():
            raise ValueError("Invalid data in Excel file: contains NaN values after cleaning.")

        control_columns = data.columns[-3:]
        formulation_columns = data.columns[:-3]

        results = []

        formulation_count = 1
        
        for _, row in data.iterrows():
            triplet_start = 0
            while triplet_start + 3 <= len(formulation_columns):  # חלוקה לשלשות
                triplet_columns = formulation_columns[triplet_start:triplet_start + 3]

                triplet_average = row[triplet_columns].mean()
                control_average = row[control_columns].mean()

                if control_average == 0:
                    raise ValueError("Control averages contain zeros, causing division by zero.")

                normalized_result = triplet_average / control_average

                if normalized_result > 10:
                    results.append({
                        "Sample Name": f"Formulation {formulation_count}",
                        "Result": normalized_result,
                        "Experiment_ID": uuid_str,
                        "Experiment_type": "TNS"
                    })
                else:
                    results.append({
                        "Sample Name": f"Formulation {formulation_count}",
                        "Result": -1,
                        "Experiment_ID": uuid_str,
                        "Experiment_type": "TNS"
                    })

                triplet_start += 3
                formulation_count += 1

        if not results:
            raise ValueError("No valid results were calculated.")

        return pd.DataFrame(results)
