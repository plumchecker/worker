import concurrent.futures
import re
import json
import requests
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_name>")
        return

    file_name = sys.argv[1]
    txt_to_json(file_name)

def send_request(ip, data_payloads):
    counter = 0
    hosts = {}
    resp = requests.post(ip, json={"leaks": data_payloads})
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
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
   
    ip_address = config['ip_address']
    batch_size = config['batch_size']
    
    payload = {}
    payloads = []
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
            
            send_request(ip_address, payloads)

            payload = {}
            payloads = []

if __name__ == '__main__':
    main()
