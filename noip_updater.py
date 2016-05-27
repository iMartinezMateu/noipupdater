#!/usr/bin/env python
#
# Copyright (c) 2016 Ivan Martinez Mateu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import ConfigParser
import logging
import os
import random
import sys
import time
import urllib2

import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S')
logger = logging.getLogger(__name__)
config = ConfigParser.RawConfigParser()

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config.read(os.path.join(application_path, 'noip_updater.conf'))

noip_hostname = config.get('noip_updater', 'Hostname')
noip_username = config.get('noip_updater', 'Username')
noip_password = config.get('noip_updater', 'Password')
ip_bag = config.get('noip_updater', 'IPBag').split(',')

old_ip = ip_bag[random.randrange(0, len(ip_bag) - 1)]
new_ip = urllib2.urlopen('http://api.enlightns.com/tools/whatismyip/?format=text').read().strip()
noip_api_endpoint = 'https://dynupdate.no-ip.com/nic/update?hostname={hostname}&myip={ip}'

logger.info('Updating www.noip.com account ...')
logger.info('OLD IP: {ip}'.format(ip=old_ip))
logger.info('NEW IP: {ip}'.format(ip=new_ip))

# Update no-ip with the fake old IP from the IP bag
logger.info('Updating hostname with fake old IP ...')
url_called = noip_api_endpoint.format(hostname=noip_hostname, ip=old_ip)
noip_api_request = requests.get(url_called, auth=(noip_username, noip_password))
print noip_api_request.content  # Print the response from the No-IP API

# Print operation result
if noip_api_request.status_code == 200:
    logger.info('Hostname ' + noip_hostname + ' from www.no-ip.com was updated successfully with a fake IP!')
else:
    logger.error('Hostname ' + noip_hostname + ' from www.no-ip.com was NOT updated successfully!. Check if the auth '
                                               'settings are correct in the configuration file.')
    sys.exit(1)

logger.info('Waiting 60 seconds in order to avoid No-IP blocking the following API request...')
time.sleep(60)

# Update no-ip with the current public IP
logger.info('Updating hostname with current public IP ...')
url_called = noip_api_endpoint.format(hostname=noip_hostname, ip=new_ip)
noip_api_request = requests.get(url_called, auth=(noip_username, noip_password))
print noip_api_request.content  # Print the response from the No-IP API

while 'nochg' in noip_api_request.content:
    logger.info('It appears that No-IP did not process the previous API request. Trying again...')
    logger.info('Waiting 120 seconds in order to avoid No-IP blocking the following API request...')
    time.sleep(120)
    noip_api_request = requests.get(url_called, auth=(noip_username, noip_password))
    print noip_api_request.content  # Print the response from the No-IP API

# Print operation result
if noip_api_request.status_code == 200:
    logger.info('Hostname ' + noip_hostname + ' from www.no-ip.com was updated successfully with the current IP!')
else:
    logger.error('Hostname ' + noip_hostname + ' from www.no-ip.com was NOT updated successfully!. Check if the auth '
                                               'settings are correct in the configuration file.')
    sys.exit(1)
