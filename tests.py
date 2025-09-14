from functions.get_file_content import get_file_content

def show(title, wd, file_path):
    result = get_file_content(wd, file_path)
    print(f"Result for {title}:")
    for line in result.splitlines():
        print(f"  {line}")

if __name__ == "__main__":
    show("main", "calculator", "main.py")
    show("outside","calculator", "pkg/calculator.py")
    show("missing","calculator", "/bin/cat")
    show("error","calculator", "pkg/does_not_exist.py")
   