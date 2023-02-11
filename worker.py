import re
import json

def txt_to_json(file_name):
    logins = {}

    with open(file_name, 'r') as file:
        for line in file:
            match = re.search("^(.*)[;:]", line)
            if match:
                login = match.group(1)
                password = line[match.end():].strip()
                logins[login] = password
            else:
                raise ValueError("Invalid line format: {}".format(line))

    with open(file_name + '.json', 'w') as file:
        json.dump(logins, file)

txt_to_json("1.txt")

#TODO:
# 1)optimize with threads
# 2)optimize with chunks (optional)
# 3)check for another separators (optional)
