import os

def write_file(working_directory, file_path, content):

    try:
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(working_directory, file_path))

        if not (abs_target == abs_working or abs_target.startswith(abs_working + os.sep)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
    
        parent = os.path.dirname(abs_target)
        os.makedirs(parent, exist_ok= True)

        
        with open(abs_target, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        

    except Exception as e:
        return f"Error: {e}"