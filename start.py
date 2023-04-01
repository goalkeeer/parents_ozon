import traceback

from program.main import run_program
from program.utils import write_log

if __name__ == '__main__':
    try:
        run_program()
    except Exception as error:
        print(error)
        tb = traceback.format_exc()
        write_log(str(tb))
