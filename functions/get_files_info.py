import os
from google.genai import types 
      
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
def get_files_info(working_directory, directory="."):
    try:
        target_path = os.path.join(working_directory, directory)
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(target_path)

        if not (abs_target == abs_working or abs_target.startswith(abs_working + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_target):
            return f'Error: "{directory}" is not a directory'
        
      

        names = os.listdir(abs_target)
        lines = []
        for name in names:
            full_path = os.path.join(abs_target, name)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path)
            lines.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"