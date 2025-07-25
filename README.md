# phdisable
 
 # phdisable
 
 A simple Python script to control Pi-hole DNS blocking via its API.
 
 ## Features
 - **Disable Pi-hole** for a specified number of minutes
 - **Enable Pi-hole** blocking
 - Uses a config file for credentials and Pi-hole URL
 
 ## Requirements
 - Python 3.7+
 - `requests` library
 
 Install dependencies:
 ```powershell
 pip install -r requirements.txt
 ```
 
 ## Configuration
 Create a `config.ini` file in the same directory with the following format:
 ```ini
 [auth]
 token = YOUR_PIHOLE_API_PASSWORD
 
 [pihole]
 url = http://YOUR_PIHOLE_URL
 ```
 
 ## Usage
 Run the script from the command line:
 
 - **Disable Pi-hole for N minutes:**
   ```powershell
   python phdisable.py --disable N
   ```
   Replace `N` with the number of minutes.
 
 - **Enable Pi-hole blocking:**
   ```powershell
   python phdisable.py --enable
   ```
 
 ## Arguments
 - `--disable N` or `-d N`: Disable Pi-hole for N minutes
 - `--enable` or `-e`: Re-enable Pi-hole blocking
 
 ## Example
 ```powershell
 python phdisable.py --disable 10
 python phdisable.py --enable
 ```
 
 ## Notes
 - The script authenticates using the password in `config.ini` and retrieves a session token for API requests.
 - Make sure your Pi-hole instance is accessible from the machine running this script.
 - SSL verification is disabled for API requests (`verify=False`).
 
 ## License
 See `LICENSE` for details.
## Features
- Reads configuration from `config.ini`
- Main script: `phdisable.py`
- Easy setup with `requirements.txt`

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/wawzat/phdisable.git
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Run the main script:
```sh
python phdisable.py
```

## Configuration
Edit the `config.ini` file to customize the behavior of the script. This file is ignored by git for security and privacy.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Author
wawzat
