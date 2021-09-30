__version__ = '0.1.0'

from flask import Flask
app =Flask(__name__)

@app.route('/api/v1/hello-world/<name>')
def user(name):
    return '<h1>Hello World  %s!</h1>' % name

if __name__ == '__main__':
    app.run(debug=True)