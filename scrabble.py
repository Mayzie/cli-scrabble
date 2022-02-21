#!/usr/bin/env python

import dictionary
import game
import network

import time

import readline

# Load the dictionary file.
dictionary = dictionary.Dictionary('dictionary.txt')

# ToDo: Make prompt and screen state prettier :-)
# It's all just a placeholder for now.
def main_menu():
    def prompt():
        print("Jessica's Scrabble:")
        print('\t1: Host a new game.')
        print('\t2: Join a game.')

        return input('Choose an option (1 or 2): ')

    result = None
    while result not in ['1', '2']:
        result = prompt()
        print()

    return result

def validate_ip_input(ip_details):
    if not len(ip_details) == 2:
        return None

    host, port = ip_details
    if host.count('.') != 3:
        return None

    try:
        int(port)
    except:
        return None

    return host, int(port)

def host_settings():
    def prompt():
        result = input('Enter your host server information [0.0.0.0:3123]: ')
        print()

        if result:
            return tuple(result.split(':'))
        else:
            return '0.0.0.0', '3123'

    result = None
    while not result:
        result = validate_ip_input(prompt())

    return result

def client_settings():
    def prompt():
        result = input('Enter the server ip:port to connect to: ')
        print()

        if result:
            return tuple(result.split(':'))

    result = None
    while not result:
        result = validate_ip_input(prompt())

    return result

def enter_name():
    return input('Please enter your display name: ')

def on_connect(client_addr):
    print(f'Client connected from {client_addr[0]}:{client_addr[1]}.')

if __name__ == '__main__':
    import sys

    if not(sys.version_info[0] >= 3 and sys.version_info[1] >= 6):
        print("Jessica's Scrabble requires at least Python 3.6 to run.")
        sys.exit(1)

    while True:
        is_host = True if main_menu() == '1' else False
        if is_host:
            host, port = host_settings()

            print(f'Starting server on {host}:{port}')
            net = network.Network(host, port, on_client_connect=on_connect)
            net.start_hosting()
        else:
            host, port = client_settings()

            print(f'Connecting to {host}:{port}')
            net = network.Network(host, port)
            net.establish_connection()

            display_name = enter_name()
            net.set_display_name(display_name)

    # scrabble = game.ScrabbleGame(dictionary)
    # scrabble.add_player('Jessica', 'jess')
    # scrabble.add_player('Christina', 'christina')
    # scrabble.select_first_player()
    # scrabble.take_turn('nonexistentword', (7, 7), 'D')
