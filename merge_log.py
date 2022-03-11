import os
import better_terminal
import datetime

LOG_DIR_LIST = [
    os.path.join(os.getcwd(), 'log.txt'),
    os.path.join(os.getcwd(), 'log2.txt'),
    os.path.join(os.getcwd(), 'log3.txt'),
]

def parse_log_line(line):
    date_str, time_str = line.split(' ')[-2:]
    date_list = [int(x) for x in date_str.split('-')]
    time_list = [int(x) for x in time_str.split(':')[:-1]]
    second, microsecond = [int(x) for x in time_str.split(':')[-1].split('.')]
    time_list.append(second)
    time_list.append(microsecond)
    time = datetime.datetime(date_list[0], date_list[1], date_list[2], time_list[0], time_list[1], time_list[2], time_list[3])
    return time, line
    

def load_log(log_dir):
    log = []

    with open(log_dir) as log_file:
        log_content = log_file.read().splitlines()

        for line in log_content:
            log.append(parse_log_line(line))
    
    return log

def merge_log(log_1, log_2):
    merged_log = []

    i = j = 0
    while (i < len(log_1) and j < len(log_2)):
        if (log_1[i][0] < log_2[j][0]):
            merged_log.append(log_1[i])
            i += 1
        else:
            merged_log.append(log_2[j])
            j += 1
    
    while (i < len(log_1)):
        merged_log.append(log_1[i])
        i += 1

    while (j < len(log_2)):
        merged_log.append(log_2[j])
        j += 1
    
    return merged_log


if __name__ == '__main__':
    logs = []
    for idx, log_dir in enumerate(LOG_DIR_LIST):
        new_log = load_log(log_dir)
        if idx == 0:
            logs = new_log
        else:
            logs = merge_log(logs, new_log)
    
    str_time = ''.join(['.' if x == ':' else x for x in list(str(datetime.datetime.now()))])
    merged_log_file_name = f'merged_log_{str_time}.txt'

    with open(merged_log_file_name, 'w') as file:
        for log in logs:
            file.write(f'{log[1]}\n')
    
    better_terminal.success(f'Succesfully merged log files into {merged_log_file_name}')

    
