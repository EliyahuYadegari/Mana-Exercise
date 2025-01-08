# Laboratory Data Processor

CLI utility for processing laboratory instrument data files for TNS and Zeta Potential experiments.

## Prerequisites
- Python 3.8 or higher  
- UV dependency management  
- SQLite3

## Installation

### Install UV
```bash
pip install uv
```

### Install Dependencies
```bash
uv sync
```

### Database Setup
```bash
python scripts/init_db.py
```

## Usage



## File Requirements
- **TNS (.xlsx)**: 96-well plate format, with triplicates and controls per row.  
- **Zeta (.csv)**: STD-labeled control rows, triplicate readings per formulation.  
