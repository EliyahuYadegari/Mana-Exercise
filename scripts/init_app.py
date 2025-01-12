import os
from subprocess import call

if not os.path.exists('results.db'):
    call(['python', 'scripts/init_db.py'])

if __name__ == "__main__":
    call(['streamlit', 'run', 'app.py'])
