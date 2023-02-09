import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")  # simple regex for emails validation


def is_valid_mail(email):
    if EMAIL_REGEX.match(email):
        return True
    else:
        return False
      

def main_fuck():
    with open('passwords.txt', 'r') as f:
        logpass = []
        for line in f:
            line = line.strip()
            login, password = re.split(";|,|:", line)
            logpass.append([login, password])

    print(logpass)
    
main_fuck()
