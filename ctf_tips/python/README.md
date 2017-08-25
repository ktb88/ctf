# Python tricks :P

## requests

HTTP 통신 관련 모듈

### requests - Install

```
$ sudo pip install requests
```

### requests - Basic Usage

```python
import requests

url = "http://target_url/index.php"

headers = {
    "Cookie": "Something",
    "Usert-Agent": "Something"
}

params = {
    "id": "id",
    "pw": "pw"
}

# GET REQUEST
# http://target_url/index.php?id=id&pw=pw
r = requests.get(url, params=params, headers=headers)
print r.headers
print r.content

data = {
    "data": "data"
}
r = requests.post(url, data=data, headers=headers)
print r.headers
print r.content
```

## PIL (known as Pillow)

그림 파일 처리 관련 모듈

### PIL - install

```
$ sudo pip install Pillow
```

### PIL - Basic Usage

PNG 읽고, 쓰기

```python
from PIL import Image
import sys

target_name = sys.argv[1]
img = Image.open(target, "r").convert("RGB") # or RGBA

width ,height = img.size
data = img.load()

# READ Process
for w in range(0, width):
    for h in range(0, height):
        (r, g, b) = data[w, h]

new_target_name = sys.argv[2]
new_img = Image.new("RGB", (width, height))
new_img_data = new_img.load()

# WRITE Process
for w in range(0, width):
    for h in range(0, height):
        (r, g, b) = data[w, h]

        # convert RED to 0xff
        new_img_data[w, h] = (255, g, b)

new_img.save(new_target_name)
```

