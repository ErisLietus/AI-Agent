from functions.write_file import write_file

def show(wd, file_path, content):
    print(write_file(wd, file_path, content))

if __name__ == "__main__":
    show("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    show("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    show("calculator", "/tmp/temp.txt", "this should not be allowed")
    
   