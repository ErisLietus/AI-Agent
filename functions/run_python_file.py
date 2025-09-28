import os
import subprocess
import sys
from google.genai import types 
      
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python Files with Optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                type=types.Type.STRING,
                description="Execute Python Files with Optional arguments, constrained to the working directory.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_target.startswith(abs_working + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_target):
            return f'Error: File "{file_path}" not found.'

        if not abs_target.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        args = args or []
        cmd = [sys.executable, abs_target, *args]
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=abs_working,
            timeout=30,
        )

        if not completed.stdout and not completed.stderr:
            return "No output produced."

        result = f"STDOUT:\n{completed.stdout}STDERR:\n{completed.stderr}"
        if completed.returncode != 0:
            result += f"\nProcess exited with code {completed.returncode}"
        return result

    except Exception as e:
        return f"Error: executing Python file: {e}"