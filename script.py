import requests
import json
import time

def filter_cookies(filename):
    with open(filename, 'r') as file:
        cookies = json.load(file)
    
    filtered_cookies = [{k: v for k, v in cookie.items() if k in ['name', 'value']} for cookie in cookies]
    
    return filtered_cookies

def send_request(url, payload, cookies, post=True):
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    if post:
        response = requests.post(url,data=json.dumps(payload),  cookies=cookies, headers=headers)
    if not post:
        response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print("failed url:",url)
        #print the response content
        print(response.content)
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

#loop

while True:
    #display a menu
    print("1. clear url list")
    print("2. add url")
    print("3. run")

    #read user input
    choice = input("Enter choice: ")

    #perform the desired action
    if choice == "1":
        with open('url.txt', 'w') as file:
            pass
    elif choice == "2":
        #Endpoint format: https://lexiangla.com/api/v1/teams/k100014/classes/076f6604168111ef97d2fef9eec64ed1/courses/51751d94168011ef9e2e06e5dcc45e88?with_source_detail=1
        #To be inputted: 076f6604168111ef97d2fef9eec64ed1 and 51751d94168011ef9e2e06e5dcc45e88
        #input the two ids
        team_id = input("Enter team id: ")
        course_id = input("Enter course id: ")
        url = f"https://lexiangla.com/api/v1/teams/k100014/classes/{team_id}/courses/{course_id}?with_source_detail=1"
        #send payload with cookie, no need to send any payload
        R=send_request(url,{},cookie,False)
        #result shound be in resp["class"]["chapters"]
        if R==None or "data" not in R:
            print("Failed request")
        else:
            R = R["data"]["class"]["chapters"]
            with open('url.txt', 'a') as file:
                for chapter in R:
                    course_id = chapter["courses"][0]["id"]
                    #construct target url
                    # https://lexiangla.com/tapi/class/study/teams/k100014/v1/classes/a7ed33fe585911ee9d7fe24daedc9d6b/courses/fbb0315435a911ed8b7dde87cc985f65/report-study
                    url = f"https://lexiangla.com/tapi/class/study/teams/k100014/v1/classes/{team_id}/courses/{course_id}/report-study"
                    file.write(url + '\n')
            print("Number of chapters added:", len(R))
    elif choice == "3":
        urls=load_lines('url.txt')
        for i in range(0,len(urls)):
            R=send_request(urls[0],{"event":2},cookie)
            if R!=None and R['message']=='success':
                print("Register success:",i+1)
            else:
                exit(-1)
        print('Register complete!')
        while(len(urls)>0):
            i=0
            remain=0
            while(i<len(urls)):
                R=send_request(urls[i],{"event":2},cookie)
                if R!=None and R['message']=='success':
                    #print("Update success:",i+1)
                    if(R['data']['procedure']==100):
                        print("Completed 1 lesson! Time:",R['data']['learn_time'])
                        del urls[i]
                        i-=1
                    else:
                        if(R['data']['procedure']>0 and remain<R['data']['learn_time']*(100-R['data']['procedure'])/R['data']['procedure']):
                            remain=R['data']['learn_time']*(100-R['data']['procedure'])/R['data']['procedure']
                else:
                    exit(-1)
                i+=1
            print("Remaining time:",remain)
            time.sleep(10)
    print("All Done!")
