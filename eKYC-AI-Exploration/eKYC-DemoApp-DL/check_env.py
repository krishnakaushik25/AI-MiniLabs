import sys
import os

def get_python_environment_info():
    # Get the path of the current Python interpreter
    python_interpreter = sys.executable
    
    # Get the Python version
    python_version = sys.version
    
    # Determine if a virtual environment is being used
    venv = os.getenv('VIRTUAL_ENV', None)
    if venv:
        venv_path = venv
    else:
        venv_path = "Not using a virtual environment"
    
    return python_interpreter, python_version, venv_path

if __name__ == "__main__":
    python_interpreter, python_version, venv_path = get_python_environment_info()
    
    print(f"Python Interpreter: {python_interpreter}")
    print(f"Python Version: {python_version}")
    print(f"Virtual Environment Path: {venv_path}")
