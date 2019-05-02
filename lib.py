import glob, sys, time, logging

stdout_handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[stdout_handler]
)
logger = logging.getLogger('lib')

def get_param():
    if len(sys.argv) > 1:
        return sys.argv[1]

    return "Default"

def list_files():
    file_list = glob.glob("*.json")
    if len(file_list) < 1:
        error_message = "No JSON file found."
        # raise Exception(error_message)
        logger.error(error_message)
        return []

    return file_list

def read_file(filepath):
    logger.info("reading file {}".format(filepath))
    in_file = open(filepath, 'rb')
    data = in_file.read()
    in_file.close()
    return data

def write_file(filename, data):
    now = time.strftime("%Y%m%dT%H%M%S")
    new_filename = now + "_" + filename

    f = open(new_filename, 'a')
    f.write(data)
    f.close()
    logger.info("created file {}".format(new_filename))