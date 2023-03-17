import os
import wget
from tempfile import mkstemp
from shutil import move, copymode


def createConf(TEMP_FILE, CONF_FILE, WHITELIST_FILE):
    try:
        with open(TEMP_FILE, 'r') as file:
            with open(CONF_FILE, 'w') as input_file:
                for line in file:
                    if line.startswith('0.0.0.0'):
                        split_line = line.split()
                        domain = split_line[1]
                        if not checkWhitelist(domain, WHITELIST_FILE):
                            input_file.write(
                                f'local-zone: "{domain}" redirect\nlocal-data: "{domain} A 0.0.0.0"\n')
    finally:
        file.close()
        input_file.close()


def checkWhitelist(domain, WHITELIST_FILE):
    try:
        whitelisted = False
        with open(WHITELIST_FILE,) as file:
            if domain in file.read():
                whitelisted = True
    finally:
        file.close()
        return whitelisted


def checkLastUpdate(TEMP_FILE, WHITELIST_FILE, DATE_STRING_START):
    update = False
    try:
        with open(TEMP_FILE, 'r') as tempfile:
            for line in tempfile:
                if line.startswith(DATE_STRING_START):
                    lastUpdated = line.strip()
                    break
        with open(WHITELIST_FILE, 'r+') as file:
            for line in file:
                # check if the date string is in the line
                if line.startswith(DATE_STRING_START):
                    if line.strip() != lastUpdated:
                        update = True
                        fh, abs_path = mkstemp()
                        with os.fdopen(fh, 'w') as new_file:
                            with open(WHITELIST_FILE) as old_file:
                                for line in old_file:
                                    if line.startswith(DATE_STRING_START):
                                        new_file.write(line.replace(
                                            line.strip(), lastUpdated))
                                    else:
                                        new_file.write(line)
                        # Copy the file permissions from the old file to the new file
                        copymode(WHITELIST_FILE, abs_path)
                        # Remove original file
                        os.remove(WHITELIST_FILE)
                        # Move new file
                        move(abs_path, WHITELIST_FILE)
    finally:
        file.close()
        tempfile.close()
        return update


def restartService(SERVICE):
    try:
        # restart unbound service
        os.popen("sudo systemctl restart " + SERVICE)
        print("Unbound service restarted successfully...")

    except OSError as ose:
        print("Error while running the command", ose)

    pass


if __name__ == "__main__":
    URL = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts'
    CONF_FILE = '/etc/unbound/unbound.conf.d/fakenews-gambling-porn-social.conf'
    WHITELIST_FILE = 'whitelist.txt'
    DATE_STRING_START = '# Date:'
    SERVICE = 'unbound'
    TEMP_FILE = 'blacklist'
    try:
        wget.download(URL, TEMP_FILE)
        if checkLastUpdate(TEMP_FILE, WHITELIST_FILE, DATE_STRING_START):
            createConf(TEMP_FILE, CONF_FILE, WHITELIST_FILE)
            restartService(SERVICE)
    finally:
        os.remove(TEMP_FILE)
