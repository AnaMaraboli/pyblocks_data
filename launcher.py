import subprocess
import sys
import os

# Ruta de tu app.py
app_path = os.path.join(os.path.dirname(__file__), "app.py")

# Ejecutar Streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
