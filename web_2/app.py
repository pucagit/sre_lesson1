from flask import Flask, request, render_template # type: ignore

app = Flask(__name__)

def client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    return ip

@app.route('/')
def index():
    ip = client_ip()
    method = request.method
    url = request.url
    return render_template('index.html',  ip=ip, method=method, url=url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)