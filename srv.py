from bottle import app, route, request, response, run
import cgi
import time

queue = []
who = []
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

@route('/who', method=['post'])
def updateWho():
	global who
	data = request.json
	user = data['user']
	ts = time.time()
	ip = request.remote_addr
	who.append(dict(user=user, ts=ts, ip=ip))	
	# Check timestamp from last update from user and purge.
	for u in who:
		lapse = time.time() - u['ts'] 
		# print lapse, u
		if lapse > 50:
			who.remove(u)
		else:
			for uu in who:
				if u != uu and u['user'] == uu['user'] and u['ip'] == uu['ip']:
					who.remove(uu)
	# print who
	return {"who": who}

run(host='0.0.0.0', port=8085)
