import polars as pl

class ExcelCalculator:
    def calculate(self, data):        
        results = []
        control_rows = data[-1]

        for row in data[:-1]:
            formulation_readings = row[:3]
            avg_formulation = sum(formulation_readings) / len(formulation_readings)
            
            control_readings = control_rows[:4]
            avg_control = sum(control_readings) / len(control_readings)
            normalized_value = avg_formulation / avg_control
            
            if normalized_value > 10:
                results.append((row[0], normalized_value))
        return results
