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
    batch_size = 100000

    with open(file_name, 'r') as file:
        while True:
            lines = [next(file).strip() for _ in range(batch_size)]
            if not lines:
                break

            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = [executor.submit(process_line, line) for line in lines]
                for future in concurrent.futures.as_completed(results):
                    login, password = future.result()
                    logins[login] = password

            with open(file_name + '.json', 'w') as file:
                json.dump(logins, file)

            logins = {}

txt_to_json("1.txt")

#TODO:
# 1)check for another separators (optional)
# 2)realize checker for EOF in while(true) cycle
# 3)check for bugs
# 4)add login/domain separation
