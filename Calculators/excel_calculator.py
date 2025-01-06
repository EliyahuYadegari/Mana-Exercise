import pandas as pd
import polars as pl

class ExcelCalculator:
    def calculate(self, data):
        # אם data הוא DataFrame מ-polars, להמיר אותו ל-pandas
        if isinstance(data, pl.DataFrame):
            data = data.to_pandas()
        
        # הדפסת מספר העמודות והנתונים לפני העדכון
        print(f"Columns before update: {data.columns.tolist()}")
        print(f"Initial data shape: {data.shape}")
        print("Initial data (first few rows):")
        print(data.head())

        # דילוג על שורת הכותרת אם יש צורך
        header = data.iloc[0]  # שורת כותרת היא השורה הראשונה
        data = data[1:]  # דלג על שורת הכותרת

        # הדפסת שורת הכותרת
        print("Header row:")
        print(header)

        # השגת שם ה-"Instrument" מהשורה הראשונה
        instrument = header[0]  # נניח ש-"Instrument" נמצא בעמודה הראשונה בשורה הראשונה

        # יצירת שמות דינמיים לכל העמודות
        column_names = [f"Instrument ({instrument})"] + [chr(65 + i) for i in range(1, len(data.columns))]
        print(f"Dynamic column names: {column_names}")

        # עדכון שמות העמודות
        data.columns = column_names

        # הצגת הנתונים לאחר עדכון
        print(f"Data after column update: shape: {data.shape}")
        print("Data after column update (first few rows):")
        print(data.head())

        # בדיקת ערכים חסרים
        if data.isnull().values.any():
            print("Warning: There are missing values in the data.")
            print("Rows with NaN values:")
            print(data[data.isnull().any(axis=1)])  # הדפסת שורות עם NaN

        # טיפול במידע חסר (לדוגמה, הסרת שורות עם ערכים חסרים או מילוי שלהן)
        data = data.dropna()  # ניתן גם למלא ערכים חסרים באמצעות `data.fillna(value)`

        # חישוב ממוצע של כל פורמולציה (שלושה קריאות עוקבות)
        formulation_averages = []
        print("Calculating formulation averages:")
        for col in range(1, len(data.columns), 3):  # כל פורמולציה עם שלושה ערכים (מתחילים מ־B)
            try:
                formulation_avg = (data.iloc[:, col].astype(float) +
                                   data.iloc[:, col + 1].astype(float) +
                                   data.iloc[:, col + 2].astype(float)) / 3
                formulation_averages.append(formulation_avg)
            except Exception as e:
                print(f"Error in column {col}-{col+2}: {e}")
        
        # הדפסת הממוצעים המחושבים
        print("Formulation averages:")
        for idx, avg in enumerate(formulation_averages):
            print(f"Formulation {idx + 1}:")
            print(avg)

        # חישוב ממוצע לכל תצפית וממוצע בקרה
        formulation_averages_df = pd.DataFrame(formulation_averages).T
        print("Formulation averages DataFrame (first few rows):")
        print(formulation_averages_df.head())

        control_averages = formulation_averages_df.mean(axis=0)
        print("Control averages:")
        print(control_averages)

        # נורמליזציה של התוצאות
        normalized_results = formulation_averages_df / control_averages
        print("Normalized results (first few rows):")
        print(normalized_results.head())

        # פילוח התוצאות לתוקף אם הן יותר מ־10
        valid_results = normalized_results[normalized_results > 10]
        print("Valid results (values > 10):")
        print(valid_results)

        # החזרת הנתונים כ-DataFrame של pandas
        return valid_results
