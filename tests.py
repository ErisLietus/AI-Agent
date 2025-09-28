from functions.run_python_file import run_python_file

def show(working_directory, file_path, args=None):
    if args is None:
        args = []
    print(run_python_file(working_directory, file_path, args))

if __name__ == "__main__":
    show("calculator", "main.py")                 # no args
    show("calculator", "main.py", ["3 + 5"])      # with args
    show("calculator", "tests.py")
    show("calculator", "../main.py")
    show("calculator", "nonexistent.py")
    
   