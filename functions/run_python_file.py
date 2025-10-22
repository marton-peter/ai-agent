import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    fullpath = os.path.abspath(os.path.join(working_directory, file_path))
    if not fullpath.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(fullpath):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(
            ["python3", fullpath, *args],
            capture_output=True,
            timeout=30,
            cwd=os.path.abspath(working_directory)
            )
        if not completed_process.stdout and not completed_process.stderr:
            if completed_process.returncode != 0:
                return f"No output produced.\nProcess exited with code {completed_process.returncode}"
            else:
                return "No output produced."
        output = f"STDOUT: {completed_process.stdout.decode()}\nSTDERR: {completed_process.stderr.decode()}"
        if completed_process.returncode != 0:
            output += f"\nProcess exited with code {completed_process.returncode}"
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    return output

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file with the specified arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the specific file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to pass to the Python file.",
            )
        },
    ),
)