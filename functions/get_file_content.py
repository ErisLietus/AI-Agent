def get_file_content(working_directory, directory="."):
    try:
        target_path = os.path.join(working_directory, directory)
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(target_path)

        if not (abs_target == abs_working or abs_target.startswith(abs_working + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_target):
            return f'Error: "{directory}" is not a directory'
        except Exception as e:
            return f"Error: {e}"