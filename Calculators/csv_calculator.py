import polars as pl

class CsvCalculator:
    def calculate(self, data):
        if len(data) < 3:
            raise ValueError("Not enough control rows in the data. Must have at least 3 control rows.")
        
        control_data = data[:3]
        
        for row in data[3:]:
            if len(row) != 3:
                raise ValueError(f"Invalid number of readings in formulation row: {row}. Expected 3 readings.")
        
        avg_control = sum(control_data) / len(control_data)
        
        results = []
        
        for row in data[3:]:
            formulation_readings = row
            avg_formulation = sum(formulation_readings) / len(formulation_readings)
            
            normalized_value = avg_formulation / avg_control
            
            if normalized_value > 0:
                results.append((row[0], normalized_value))
            
        return results
