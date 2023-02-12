import concurrent.futures
import re
import json
import requests

def send_request(data_payloads):
    counter = 0
    hosts = {}

    resp = requests.post("http://25.68.246.17:30001/api/leaks",json={"leaks": data_payloads})
    print(resp.json())

def process_line(line):
    match = re.search("^(.*)[;:]", line)
    if match:
        login = match.group(1)
        password = line[match.end():].strip()
        return (login, password)
    else:
        raise ValueError("Invalid line format: {}".format(line))

def txt_to_json(file_name):
    payload = {}
    payloads = []
    batch_size = 100
    last_iter = False
    
    with open(file_name, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        file_size = len(lines)

    with open(file_name, 'r', encoding="utf-8") as file:
        while not last_iter:
            
            lines = [next(file).strip() for _ in range(batch_size)]
            file_size = file_size - batch_size
            
            if batch_size > file_size:
                batch_size = file_size

            if file_size == 0:
                last_iter = True

            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = [executor.submit(process_line, line) for line in lines]
                for future in concurrent.futures.as_completed(results):
                    login, password = future.result()
                    email = login.split("@")[0]
                    domain = login.split("@")[1]
                    payload = {"email": email, "domain": domain, "password": password}
                    payloads.append(payload)
            
            send_request(payloads)
            #with open(file_name + '.json', 'w', encoding="utf-8") as file1:
            #    json.dump(payload, file1)

            payload = {}
            payloads = []

txt_to_json("1.txt")
