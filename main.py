from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return "this is my blog!"

if __name__=="__main__":
    app.run(host = '127.0.0.1',port = 80,debug = True)
