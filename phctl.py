import sys
import configparser
import requests
import argparse

"""
phdisable.py

A command-line utility to control Pi-hole DNS blocking via its API. This script allows you to temporarily disable or re-enable Pi-hole blocking by authenticating with the Pi-hole API using credentials stored in a config file.

Features:
- Disable Pi-hole for a specified number of minutes
- Re-enable Pi-hole blocking
- Reads configuration from config.ini
- Handles authentication and session management

Usage:
    python phdisable.py --disable MINUTES
    python phdisable.py --enable
"""

CONFIG_FILE = 'config.ini'

def get_config():
    """
    Reads the Pi-hole API credentials and URL from the config.ini file.
    Returns:
        tuple: (password, url) from the config file.
    Exits if required keys are missing.
    """

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        # This is your Pi-hole API app password, not a session ID
        password = config['auth']['app_passsword']
        url = config['pihole']['url']
        return password, url
    except KeyError:
        print('Error: config.ini missing required sections or keys ([auth] app_password, [pihole] url).')
        sys.exit(1)

def get_sid(pihole_url, password):
    """
    Authenticates with the Pi-hole API to obtain a session ID (sid).
    Args:
        pihole_url (str): The base URL of the Pi-hole instance.
        password (str): The Pi-hole API app password.
    Returns:
        str: The session ID (sid) if authentication is successful.
    Exits if authentication fails.
    """
    api_url = pihole_url.rstrip('/') + '/api/auth'
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(api_url, json={'password': password}, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        sid = data.get("session", {}).get("sid")
        if sid:
            return sid
    except requests.RequestException as e:
        print(f"Error getting session ID: {e}")
        if e.response:
            print(f"Response: {e.response.text}")
        sys.exit(1)

def disable_pihole(minutes, sid, pihole_url):
    """
    Disables Pi-hole DNS blocking for a specified number of minutes.
    Args:
        minutes (int): Number of minutes to disable blocking.
        sid (str): Session ID for authentication.
        pihole_url (str): The base URL of the Pi-hole instance.
    Exits if the API request fails.
    """
    seconds = minutes * 60
    api_url = pihole_url.rstrip('/') + '/api/dns/blocking'
    headers = {"Content-Type": "application/json", "sid": sid}
    payload = {
        "blocking": False,
        "timer": seconds
    }
    try:
        response = requests.post(api_url, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        print(f"Pi-hole disabled for {minutes} minutes.")
    except requests.RequestException as e:
        print(f"Error disabling Pi-hole: {e}")
        if e.response:
            print(f"Response: {e.response.text}")
        sys.exit(1)

def enable_pihole(sid, pihole_url):
    """
    Re-enables Pi-hole DNS blocking.
    Args:
        sid (str): Session ID for authentication.
        pihole_url (str): The base URL of the Pi-hole instance.
    Exits if the API request fails.
    """
    api_url = pihole_url.rstrip('/') + '/api/dns/blocking'
    headers = {"Content-Type": "application/json", "sid": sid}
    payload = {"blocking": True}
    try:
        response = requests.post(api_url, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        print(f"Pi-hole enabled")
    except requests.RequestException as e:
        print(f"Error enabling Pi-hole: {e}")
        if e.response:
            print(f"Response: {e.response.text}")
        sys.exit(1)

def parse_args():
    """
    Parses command-line arguments for disabling or enabling Pi-hole blocking.
    Returns:
        argparse.Namespace: Parsed arguments with either --disable or --enable set.
    """
    parser = argparse.ArgumentParser(description="Control Pi-hole blocking.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--disable', type=int, metavar='MINUTES', help='Disable Pi-hole for MINUTES')
    group.add_argument('-e', '--enable', action='store_true', help='Re-enable Pi-hole blocking')
    return parser.parse_args()

def main():
    """
    Main entry point for the script. Parses arguments, authenticates, and calls the appropriate function to disable or enable Pi-hole blocking.
    """
    args = parse_args()
    password, pihole_url = get_config()
    sid = get_sid(pihole_url, password)
    if not sid:
        print("Failed to retrieve Pi-hole Session ID. Check your password in config.ini.")
        sys.exit(1)
    if args.disable is not None:
        if args.disable <= 0:
            print("Minutes must be a positive integer.")
            sys.exit(1)
        disable_pihole(args.disable, sid, pihole_url)
    elif args.enable:
        enable_pihole(sid, pihole_url)

if __name__ == '__main__':
    main()