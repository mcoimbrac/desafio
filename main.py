from lib import list_files, read_file, write_file
import os

from app import App

def main():
    base_files_list = list_files()
    for file in base_files_list:
        filepath = os.path.join(os.getcwd(), file)
        data = read_file(filepath)

        app = App(data)
        data = app.generate_template()
        write_file(file, data)
        # app.generate_template()
        # app.print_template()


if __name__ == '__main__':
    main()