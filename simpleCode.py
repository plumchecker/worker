import re
from json import dumps as jsonify

def is_valid_mail(email):
    EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")  # simple regex for emails validation
    return EMAIL_REGEX.match(email) is not None

def main():
    logpass = []
    try:
        with open('passwords.txt', 'r') as f:
            for line in f:
                line = line.strip()
                login, password = re.split(";|,|:", line)
                logpass.append({"login": login, "password": password})
    except FileNotFoundError:
        print("Cannot find \"passwords.txt\"!")
    print(jsonify(logpass))

if __name__ == "__main__":    
    main()
