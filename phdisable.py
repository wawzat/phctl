import sys
import configparser
import requests
import argparse

CONFIG_FILE = 'config.ini'

def get_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        # This is your API password, not a session ID
        password = config['auth']['app_passsword']
        url = config['pihole']['url']
        return password, url
    except KeyError:
        print('Error: config.ini missing required sections or keys ([auth] app_password, [pihole] url).')
        sys.exit(1)

def get_sid(pihole_url, password):
    """Authenticates with the Pi-hole API to get a session ID."""
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


def main():
    parser = argparse.ArgumentParser(description="Control Pi-hole blocking.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--disable', type=int, metavar='MINUTES', help='Disable Pi-hole for MINUTES')
    group.add_argument('-e', '--enable', action='store_true', help='Re-enable Pi-hole blocking')
    args = parser.parse_args()
    password, pihole_url = get_config()
    sid = get_sid(pihole_url, password)
    if not sid:
        print("Failed to retrieve session ID. Check your password in config.ini.")
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