import json

def txt_to_json(file_name):
    logins = {}

    with open(file_name, 'r') as file:
        for line in file:
            if ';' in line:
                login, password = line.strip().split(';')
            elif ':' in line:
                login, password = line.strip().split(':')
            else:
                raise ValueError("Invalid separator in line: {}".format(line))
            logins[login] = password

    with open(file_name + '.json', 'w') as file:
        json.dump(logins, file)

txt_to_json("1.txt")

#TODO: 
# 1)check for separator in password
# 2)check for separator in login // UPD: no ':' or ';' symbols in login
# 3)add regular expressions