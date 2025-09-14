from functions.get_files_info import get_files_info

def show(title, wd, dir_):
    result = get_files_info(wd, dir_)
    print(f"Result for {title}:")
    for line in result.splitlines():
        print(f"  {line}")

if __name__ == "__main__":
    show("current directory", "calculator", ".")
    show("'pkg' directory", "calculator", "pkg")
    show("'/bin' directory", "calculator", "/bin")
    show("'../' directory", "calculator", "../")