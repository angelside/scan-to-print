#!/usr/bin/env python
import socket
import sys
import platform
import datetime
import json
import os.path
from string import Template

from signal import signal, SIGINT
from sys import exit

# https://www.devdungeon.com/content/colorize-terminal-output-python
import colorama # poetry add colorama
colorama.init()

config = {
    'app_title': '=== Scan to Print ===',
    'message': 'IT zebra printer quality test',
    'printer_port': 9100,
    'socket_timeout': 3,
}


class CliColors:
    HEADER = '\033[95m'
    WHITE  = '\33[37m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def handler(signal_received, frame):
    # Handle any cleanup here
    print('\nSIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)
    
    # Not working: RuntimeError: can't re-enter readline
    #res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    #if res == 'y':
    #    exit(1)


def main():
    # Required data files
    label_file = 'label.txt'
    data_file = 'data.json'

    if not os.path.isfile(label_file):
        print()
        print(f'{CliColors.FAIL}[ERROR]{CliColors.ENDC} A required file is missing: {CliColors.OKCYAN}{label_file}{CliColors.ENDC}')
        print()
        os.system('pause') # Press any key to continue . . .
        exit()

    if not os.path.isfile(data_file):
        print()
        print(f'{CliColors.FAIL}[ERROR]{CliColors.ENDC} A required file is missing: {CliColors.OKCYAN}{data_file}{CliColors.ENDC}')
        print()
        os.system('pause') # Press any key to continue . . .
        exit()

    # TODO: Check if data.json is a valid json format

    # ZPL template
    with open(label_file, 'r') as file:
        zplTemplateSmall = file.read().strip()

    # Create a Template object from "ZPL template"
    template = Template(zplTemplateSmall)

    # Current time 19/06/2023 09:00
    current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    
    with open(data_file) as f:
       locations = json.load(f)

    while True: # Forever loop
        # Ask for input
        print()
        location = input('Location: ')

        if location not in locations:
            print(current_time, f'{CliColors.FAIL}[ERROR]{CliColors.ENDC} Location does not exist')
        else:
            print(current_time)

            # Substitute variables in the template
            templateResult = template.substitute(location=location, time=current_time, message=config['message'])
            # Formatted and encoded zpl template code
            fmt_zpl_code = f'{templateResult}'.encode()

            # Send a socket request
            print(location)
            print(locations[location])

            socket_request(
                ip_address = locations[location],
                port = config['printer_port'],
                timeout = config['socket_timeout'],
                zpl_code = fmt_zpl_code,
                location = location
            )


def socket_request(ip_address, port, timeout, zpl_code, location):
    """Socket request
        It will be print green "[OK]" at success, and red "[ERROR]" in the connection error

    Args:
        ip_address (str): IP address
        port (int): Port
        timeout (int): Timeout
        zpl_code (str): ZPL code to send
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((ip_address, port))
            sock.send(zpl_code)
            print(f'\r{CliColors.OKGREEN}[OK]{CliColors.ENDC} {CliColors.OKBLUE}{location} - {ip_address}{CliColors.ENDC}')
        except TimeoutError:
            #error_msg(f'Request timed out while connecting to remote host {ip_address}', True)
            print(f'{CliColors.FAIL}[ERROR]{CliColors.ENDC} {location} - {ip_address}')
        finally:
            sock.close()


# Entry point for CLI
if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    
    print(f"{CliColors.HEADER}{config['app_title']}{CliColors.ENDC}")

    main()