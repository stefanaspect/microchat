from bottle import app, route, request, response, run
import cgi
import time

queue = []
tmpl = None
MAX = 10

@route('/')
def index():
    global tmpl
    if tmpl is None:
        with file('index.html', 'r') as fh:
            tmpl = fh.read()
    return tmpl

@route('/message', method=['get', 'post'])
def message():
    global queue
    if request.method == "POST":
        data = request.json
        ts = time.time()
        date = time.ctime()
        user = data['user']
        mesg = data.get('mesg')
        code = data.get('code')
        # only store the last MAX items in the queue...
        if len(queue) > MAX:
            tmp = len(queue) - MAX
            queue = queue[tmp:len(queue)]
        queue.append(dict(user=user, ts=ts, date=date, mesg=mesg, code=code))
        return {"queue": queue}
    else:
        return {"queue": queue}


run(host='0.0.0.0', port=8085)
