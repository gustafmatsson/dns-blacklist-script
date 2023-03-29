
# DNS-BLACKLIST-SCRIPT

Script to create a configurationfile for redirecting requests from non allowed domains.

## Prerequisites

- Python 3
- wget
## Run

```bash
python3 blacklist.py
```

## Whitelist

When whitelisting a new domain simply add the new domain as a newline in the whitelist.txt and remove delete the text after "# Date:" 
and run the script. This will generate a new config with the given domain whitelisted.

Ex:
```bash
# Date: 
#### ADD WHITELISTED DOMAIN BELOW ####
example.com
```

## Cronjob
 The script is automatically runned everyday for update checks using a [cronjob](https://linuxhandbook.com/crontab/) in linux.
```bash
sudo crontab -e

0 0 * * * python3 /path/to/script/blacklist.py

```

## Documentation

The script downloads list of domains from Steve Blacks [fakenews-gambling-porn-social](https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts) collection. Then it checks from the whitelist.txt the date when the configuration was last updated. If the newly downloaded list is newer, it creates a new configuration using the latest list.

The script also has an whitelist functionality where you add the domain you want to whitelist to whitelist.txt.
The script will do a check towards the whitelist everytime it adds a new domain to the configuration.

The script is then ran everyday using a cronjob in linux. 
