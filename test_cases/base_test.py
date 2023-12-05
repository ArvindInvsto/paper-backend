import requests
import json
import traceback 
url = 'https://a87eyqankc.us-east-2.awsapprunner.com/strategy/view-signals?strategy_id=71'

try:
    res = requests.get(url)
except:
    print()
# json_res = json.loads(res.text)
print("### TEST case 1 ###")
print('==================================================================================')
if res.status_code == 200:
    print("API response 200")
    print("Test case 1: Passed")
else:
    print("Test case 1: Failed")
    print("Invalid status code "+ str(res.status_code))
print('==================================================================================')


print('==================================================================================')
print("### TEST case 2 ###")
try:
    json_res = json.loads(res.text)
    print("API response Valid json")
    print("Test case 2: Passed")
except:
    print("Test case 2: Failed")
    print("Fail to response convert to json")
print('==================================================================================')


url = "https://a87eyqankc.us-east-2.awsapprunner.com/compile"
import os
cur_d =os.path.dirname(os.path.abspath(__file__))
cur_d = cur_d + '/hello.py'
payload = {}
files=[
  ('file',('file',open(cur_d,'rb'),'application/octet-stream'))
]
headers = {
  'accept': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

if response.status_code == 200:
    print("API response 200")
    print("Test case 3: Passed")
else:
    print("Test case 3: Failed")
    print("Invalid status code "+ str(response.status_code))
print('==================================================================================')

if str(response.text) == '\"hello\"':
    print("API response as expected")
    print("Test case 4: Passed")
else:
    print("Test case 4: Failed")
    print("API response not as expected")
    print(response.text)
print('==================================================================================')



if int(response.elapsed.total_seconds()) < 100:
    print("API response time ok")
    print("Test case 5: Passed")
else:
    print("Test case 5: Failed")
    print("high response time")
print('==================================================================================')



url = "https://a87eyqankc.us-east-2.awsapprunner.com/compile"
import os
cur_d =os.path.dirname(os.path.abspath(__file__))
cur_d = cur_d + '/hello_2.py'
payload = {}
files=[
  ('file',('file',open(cur_d,'rb'),'application/octet-stream'))
]
headers = {
  'accept': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

if response.status_code == 200:
    print("API response 200")
    print("Test case 6: Passed")
else:
    print("Test case 6: Failed")
    print("Invalid status code "+ str(response.status_code))
print('==================================================================================')

try:
    num = int(response.text.replace('\"',''))
    print("API response as expected")
    print("Test case 7: Passed")
except:
    print("Test case 7: Failed")
    print("API response not as expected")
    print(response.text)
print('==================================================================================')

if int(response.text.replace('\"','')) in [5,6,7,8,9]:
    print("API response as expected")
    print("Test case 8: Passed")
else:
    print("Test case 8: Failed")
    print("API response not as expected")
    print(response.text)
print('==================================================================================')

if int(response.elapsed.total_seconds()) < 100:
    print("API response time ok")
    print("Test case 9: Passed")
else:
    print("Test case 9: Failed")
    print("high response time")
print('==================================================================================')

'''


for i in range(200):

    url = "https://a87eyqankc.us-east-2.awsapprunner.com/compile"
    import os
    cur_d =os.path.dirname(os.path.abspath(__file__))
    cur_d = cur_d + '/hello.py'
    payload = {}
    files=[
    ('file',('file',open(cur_d,'rb'),'application/octet-stream'))
    ]
    headers = {
    'accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    if str(response.text) == '\"hello\"':
        print("API response as expected")
        print("Test case stress: Passed")
    else:
        print("Test case stress: Failed")
        print("API response not as expected")
        print(response.text)
    print('==================================================================================')

'''