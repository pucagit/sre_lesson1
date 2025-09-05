from flask import Flask, request, render_template, redirect, url_for # type: ignore

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.remote_addr
    method = request.method
    url = request.url
    return render_template('index.html',  ip=ip, method=method, url=url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)