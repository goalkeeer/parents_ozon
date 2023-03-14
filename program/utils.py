def write_log(error_str):
    log_path = 'logs.log'

    with open(log_path, 'a+') as log_file:
        log_file.write("\n")
        log_file.write(f"{error_str}\n")

    return log_path


def write_interim_result(row):
    log_path = 'interim_result.txt'

    with open(log_path, 'a+') as log_file:
        log_file.write(f"{row}\n")

    return log_path