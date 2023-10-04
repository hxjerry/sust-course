import requests
import json
import time

def filter_cookies(filename):
    with open(filename, 'r') as file:
        cookies = json.load(file)
    
    filtered_cookies = [{k: v for k, v in cookie.items() if k in ['name', 'value']} for cookie in cookies]
    
    return filtered_cookies

def send_request(url, payload, cookies):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url,data=json.dumps(payload),  cookies=cookies, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def load_lines(filename):
    with open(filename, 'r') as file:
        lines = [line.rstrip() for line in file]
    return lines

def convert_cookies(cookie_array):
    cookies = {}
    for cookie in cookie_array:
        cookies[cookie['name']] = cookie['value']
    return cookies

cookie=convert_cookies(filter_cookies('cookies.json'))
urls=load_lines('url.txt')
for i in range(0,len(urls)):
    R=send_request(urls[0],{"event":2},cookie)
    if R!=None and R['message']=='success':
        print("Register success:",i+1)
    else:
        exit(-1)
print('Register complete!')
while(len(urls)>0):
    i=0;
    remain=0;
    while(i<len(urls)):
        R=send_request(urls[i],{"event":2},cookie)
        if R!=None and R['message']=='success':
            #print("Update success:",i+1)
            if(R['data']['procedure']==100):
                print("Completed 1 lesson! Time:",R['data']['learn_time'])
                del urls[i]
                i-=1
            else:
                if(remain<R['data']['learn_time']*(100-R['data']['procedure'])/R['data']['procedure']):
                    remain=R['data']['learn_time']*(100-R['data']['procedure'])/R['data']['procedure'];
        else:
            exit(-1)
        i+=1
    print("Remaining time:",remain)
    time.sleep(10)
print("All Done!")
