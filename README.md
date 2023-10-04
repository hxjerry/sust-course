# sust-course
Autoscript for sustech course on tencent MOOC platform

# usage
1. Download this repo and install requests library in your python environment: pip install requests
2. Login to **lexiangla.com** and use chrome extension **https://cookie-editor.com/** to dump the cookies of your session into a json file.
3. Launch script.py
4. Enjoy

# how does it work
This work is based on basic reverse engineering of the protocol used by the server to track its users, which works as follows:
1. The client obtains an additional token on login which is used to post data to a tracking endpoint.
2. Javascipt from the client's browser posts a 1 at the begining of each course to the course's endpoint and then posts a 2 every about 30 seconds, the server sets up a timer that begins on the on and is kept alive by the 2.
3. When the timer hits the duration of the course, the couse is marked as completed on the server.

Therefore, this code simulates this hearbeat protocol to achieve what it does.
