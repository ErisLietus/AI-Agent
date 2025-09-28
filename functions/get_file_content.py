from config import MAX_CHARS
import os
from google.genai import types 
      
schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Accesses the File Content and keeps it under 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                type=types.Type.STRING,
                description="Accesses the File Content and keeps it under 10000 characters, constrained to the working",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(working_directory, file_path))

        if not (abs_target == abs_working or abs_target.startswith(abs_working + os.sep)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_target, "r") as f:
            content = f.read(MAX_CHARS + 1)

        if len(content) == MAX_CHARS + 1:
            return content[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
        return content

    except Exception as e:
        return f"Error: {e}"