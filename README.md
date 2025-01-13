# Laboratory Data Processor

Application for processing laboratory instrument data files for TNS and Zeta Potential experiments.

## Prerequisites for Local Mode
- Python 3.11 or higher
- SQLite3
- Streamlit
- UV dependency management

### Install Dependencies
1. Install UV:
   ```bash
   pip install uv
   ```
2. Install project dependencies:
   ```bash
   uv sync
   ```

### Initialize the Database
Run the following command to initialize the database:
```bash
python scripts/init_db.py
```

## Start the Application

### To run the Streamlit application locally:
```bash
streamlit run src/app.py
```

### To run Using Docker

#### Build the Docker Image
To build the Docker image:
```bash
docker build -t lab-data-processor .
```

#### Run the Application with Docker
To run the application with Docker:
```bash
docker run -p 8501:8501 lab-data-processor
```

## File Requirements
- **TNS (.xlsx)**: 96-well plate format, with triplicates and controls per row.  
- **Zeta (.csv)**: STD-labeled control rows, triplicate readings per formulation.
