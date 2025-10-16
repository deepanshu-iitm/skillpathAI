import subprocess
import sys
import time
import streamlit as st

# Start the FastAPI backend
backend_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"])
time.sleep(3) 

exec(open('app.py').read())