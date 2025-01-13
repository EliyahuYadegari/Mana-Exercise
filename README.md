# Laboratory Data Processor

Application for processing laboratory instrument data files for TNS and Zeta Potential experiments.

## Prerequisites
- Python 3.8 or higher  
- UV dependency management  
- SQLite3
- Streamlit

## Installation

### Install UV
```bash
pip install uv
```

### Install Dependencies
```bash
uv sync
```

## Usage
### Initialize the DataBase
```bash
python scripts/init_db.py
```

### Run the "Laboratory Data Processor" app
```bash
streamlit run src/app.py
```


## File Requirements
- **TNS (.xlsx)**: 96-well plate format, with triplicates and controls per row.  
- **Zeta (.csv)**: STD-labeled control rows, triplicate readings per formulation.  
