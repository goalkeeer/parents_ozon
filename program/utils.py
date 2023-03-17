from pathlib import Path

from program import settings


def write_log(error_str):
    Path(settings.LOG_PATH).mkdir(parents=True, exist_ok=True)
    log_path = Path(settings.LOG_PATH, 'logs.log')

    with open(log_path, 'a+') as log_file:
        log_file.write("\n")
        log_file.write(f"{error_str}\n")

    return log_path


def write_interim_result(row):
    Path(settings.LOG_PATH).mkdir(parents=True, exist_ok=True)
    log_path = Path(settings.LOG_PATH, 'interim_result.txt')

    with open(log_path, 'a+') as log_file:
        log_file.write(f"{row}\n")

    return log_path
