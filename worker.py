import concurrent.futures
import re
import json

def process_line(line):
    match = re.search("^(.*)[;:]", line)
    if match:
        login = match.group(1)
        password = line[match.end():].strip()
        return (login, password)
    else:
        raise ValueError("Invalid line format: {}".format(line))

def txt_to_json(file_name):
    logins = {}

    with open(file_name, 'r') as file:
        lines = file.readlines()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(process_line, line) for line in lines]
        for future in concurrent.futures.as_completed(results):
            login, password = future.result()
            logins[login] = password

    with open(file_name + '.json', 'w') as file:
        json.dump(logins, file)

txt_to_json("1.txt")

#TODO:
# 1)optimize with chunks (optional)
# 2)check for another separators (optional)
