# NoIPUpdater
Command-line tool for updating a No-IP hostname

## Introduction
I created this script because I was bothered by the fact that [No-IP](www.noip.com) sends email about your domain name expiring after more than 30 days without a change.  To remedy this, I decided to write this script in Python and run it into a scheduled job every 15 days using `crontab` so this problem is solved automatically.
The script replaces the current hostname IP with a fake one, and then, gets the current public IP from an external API and again, replace the fake IP with the new public IP in the No-IP hostname so the expiring countdown will reset.

## Dependencies
You need to satisfy the following dependencies in order to compile the project

* Python 2.7 with [pip](https://pip.pypa.io/en/stable/) tool installed.
* Python modules installed: [requests](http://docs.python-requests.org/en/master/).

## Configuration
The script configuration is made in the `noip_updater.conf` file. You can open and modify it with a plain text editor. This file must be in the same path where the NoIPUpdater is stored.

## Run
### Update hostname
Just execute the script issuing the command `python noip_updater.py` to update the hostname indicated in the configuration file.

## Reporting issues
Issues can be reported via the [Github issue tracker](https://github.com/imartinezmateu/noipupdater/issues).

Please take the time to review existing issues before submitting your own to prevent duplicates. Incorrect or poorly formed reports are wasteful and are subject to deletion.

## Submitting fixes and improvements
Fixes and improvements are submitted as pull requests via Github.

