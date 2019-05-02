from lib import list_files, read_file, write_file
import os, logging, sys

from app import App

stdout_handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[stdout_handler]
)
logger = logging.getLogger('main')

def main():
    logger.info("tropo started")

    base_files_list = list_files()
    for file in base_files_list:
        filepath = os.path.join(os.getcwd(), file)
        data = read_file(filepath)

        app = App(data)
        data = app.generate_template()
        write_file(file, data)
        # app.generate_template()
        # app.print_template()

    logger.info("tropo finished")


if __name__ == '__main__':
    main()