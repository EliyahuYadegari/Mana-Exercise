import pandas as pd
import polars as pl

class ExcelCalculator:
    def calculate(self, data):
        if isinstance(data, pl.DataFrame):
            data = data.to_pandas()
        
        header = data.iloc[0]
        data = data[1:]

        column_names = ['Instrument'] + [f'Col-{i}' for i in range(1, len(data.columns))]
        data.columns = column_names

        data = data.dropna()

        formulation_columns = data.columns[1:-3]
        control_columns = data.columns[-3:]
        formulation_averages = data[formulation_columns].astype(float).mean(axis=1)
        control_averages = data[control_columns].astype(float).mean(axis=1)

        normalized_results = formulation_averages / control_averages

        valid_results = normalized_results[normalized_results > 10]

        return pd.DataFrame({'Valid Results': valid_results}).reset_index(drop=True)
