# Sites Monitoring Utility

Script to monitor sites health. It checks domain expiration date and if a website is answering with HTTP 200 code.

# Usage
1. Install requirements `pip install -r requirements.txt`
2. Create a text file with urls you want to check.
3. Run command `python3 check_sites_health.py path_to_a_file`

## Example of usage
**sites.txt**
```
devman.org
readthedocs.io
python.org
```
Run command
```
python3 check_sites_health sites.txt
```
Output:
```
Today is: 12.08.2017 17:19:19
Domain                        | Working  | Expiring |  Expire date
---------------------------------------------------------------------------
http://devman.org             |   YES    |    NO    |28.08.2018 11:49:42
---------------------------------------------------------------------------
http://readthedocs.io         |   YES    |   N/A    |      N/A
---------------------------------------------------------------------------
http://python.org             |   YES    |    NO    |28.03.2018 05:00:00
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
