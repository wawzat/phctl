
# phctl & dnsflip

This project provides two tools to temporarily bypass or re-enable Pi-hole DNS blocking, each using a different approach:

---

## Overview: Two Ways to Control Pi-hole blocking

- **phctl.py**: A Python script that interacts directly with the Pi-hole API to disable or enable DNS blocking for a set period. It automatically re-enables blocking after the specified time.
- **dnsflip.ps1**: A PowerShell script that toggles your Windows network interface DNS settings between your Pi-hole server and public DNS (Google DNS). This script must be run manually each time you want to switch DNS servers and will not revert back to Pi-hole blocking automatically.

**Both tools accomplish the same goal—temporarily bypassing Pi-hole filtering—but in different ways:**

- `phctl.py` disables Pi-hole at the source (the Pi-hole server) and will automatically re-enable blocking after a timer.
- `dnsflip.ps1` changes your local computer's DNS settings to bypass Pi-hole, but **does not automatically revert**—you must run the script again to switch back to Pi-hole DNS. An advantage to this approach is blocking is disabled only for the local machine and not for the entire network.

---

## phctl.py

`phctl.py` is a simple Python script to control Pi-hole DNS blocking via its API.

### Features
- **Disable Pi-hole** for a specified number of minutes (default 5 minutes)
- **Enable Pi-hole** blocking
- Uses a config file for credentials and Pi-hole URL

### Requirements
- Python 3.7+
- `requests` library

Install dependencies:
```powershell
pip install -r requirements.txt
```

### Configuration
Create a `config.ini` file in the same directory with the following format:
 ```ini
 [auth]
 token = YOUR_PIHOLE_API_APP_PASSWORD
 
 [pihole]
 url = http://YOUR_PIHOLE_IP_ADDRESS
 ```
 
## Usage
Run the script from the command line:

- **Disable Pi-hole for N minutes:**
  ```powershell
  python phctl.py --disable N
  ```
  Replace `N` with the number of minutes or leave blank to use default 5 minutes.

- **Enable Pi-hole blocking:**
  ```powershell
  python phctl.py --enable
  ```

## Arguments
- `--disable N` or `-d N`: Disable Pi-hole for N minutes
- `--enable` or `-e`: Re-enable Pi-hole blocking

## Example
```powershell
python phctl.py --disable 10
python phctl.py --enable
```

## Notes
- The script authenticates using the password in `config.ini` and retrieves a session token for API requests.
- Make sure your Pi-hole instance is accessible from the machine running this script.

---

## dnsflip.ps1

`dnsflip.ps1` is a PowerShell script to quickly toggle your Windows network interface DNS settings between a Pi-hole server and public DNS (Google DNS).

### Features
- Checks if running as Administrator
- Detects current DNS configuration for the specified interface
- Prompts to switch between Pi-hole and public DNS servers

### Usage
1. Edit `$interfaceAlias`, `$piHoleAddress`, and `$publicDNS` at the top of the script to match your environment.
2. Run the script as Administrator in PowerShell:
   ```powershell
   .\dnsflip.ps1
   ```
3. Follow the prompts to switch DNS settings.

**Example:**
```
The current DNS server is Pi-hole. Do you want to change to public DNS servers? (Y/n)
```

**Note:**
- The script only affects the interface specified by `$interfaceAlias`.
- Useful for quickly switching DNS for troubleshooting or bypassing Pi-hole temporarily.
- **You must manually run the script again to restore your DNS settings to Pi-hole.**

---
## Features
- Reads configuration from `config.ini`
- Main script: `phctl.py`
- Easy setup with `requirements.txt`

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/wawzat/phctl.git
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration
Edit the `config.ini` file to customize the behavior of the script. This file is ignored by git for security and privacy.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Author
wawzat
