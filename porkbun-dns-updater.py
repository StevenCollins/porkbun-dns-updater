#!/usr/bin/python3

import os
import requests
import datetime

from dotenv import load_dotenv
load_dotenv()

# constants
SECRET_API_KEY = os.getenv('SECRET_API_KEY')
API_KEY = os.getenv('API_KEY')
ID = os.getenv('ID')
DOMAIN = os.getenv('DOMAIN')
LOG = os.path.realpath(__file__) + '.log'

# initialize variables (so they can be verified)
error = False
current_ip = ''
a_record_ip = ''

# get current IP using API ping
ping_data = {'secretapikey': SECRET_API_KEY, 'apikey': API_KEY}
try:
    ping_response = requests.post('https://porkbun.com/api/json/v3/ping', json = ping_data).json()
    current_ip = ping_response['yourIp']
except:
    error = True

# get current A record using API retrieve
retrieve_data = {'secretapikey': SECRET_API_KEY, 'apikey': API_KEY}
try:
    retrieve_response = requests.post('https://porkbun.com/api/json/v3/dns/retrieve/' + DOMAIN, json = retrieve_data).json()
    for record in retrieve_response['records']:
        if record['id'] == ID:
            a_record_ip = record['content']
except:
    error = True

# if different, update A record using API edit
if error == False and current_ip != '' and a_record_ip != '':
    if current_ip != a_record_ip:
        edit_data = {'secretapikey': SECRET_API_KEY, 'apikey': API_KEY, 'type': 'A', 'content': current_ip, 'ttl': '600'}
        edit_response = requests.post('https://porkbun.com/api/json/v3/dns/edit/' + DOMAIN + '/' + ID, json = edit_data).json()
        log = open(LOG, 'a')
        log.write(datetime.datetime.now().isoformat() + ' ' + 'current ip: ' + current_ip + ' a record ip: ' + a_record_ip + '\n\t' + str(edit_response) + '\n')
        log.close()
else:
    log = open(LOG, 'a')
    log.write(datetime.datetime.now().isoformat() + ' error retriving IPs: current ip: ' + current_ip + ' a record ip: ' + a_record_ip + '\n')
    log.close()
