#-*- coding: utf-8 -*-
#encoding=utf-8
from flask import Flask,render_template,session,url_for,redirect,request,flash
import json,os
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.debug = True
app.secret_key = 'it is a my fucking blog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Posts.db'

# create sqlalchemy object
db = SQLAlchemy(app)

from model import *




@app.route('/',methods=['GET','POST'])
def hello():
    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']
        db.create_all()
        db.session.add(Posts(title,content))
        db.session.commit()
    post = db.session.query(Posts).all()
    return render_template('homepage.html', post = post)

@app.route('/upload/', methods=['GET', 'POST'])
def ueditor():
    action = request.args.get("action", "")
    if 'config' == action:
        return json.dumps(get_config())
    if 'uploadimage' == action:
        return json.dumps(upload_image())


@app.route('/sign',methods=['GET','POST'])
def sign():
    return render_template('sign.html')

@app.route('/posts',methods=['GET'])
def posts():
    return render_template('posts blog.html')


def get_config():
    return {"imageActionName": "uploadimage",
            "imageFieldName": "upfile",
            "imageMaxSize": 2048000,
            "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif"],
            "imageCompressEnable": True,
            "imageCompressBorder": 1600,
            "imageInsertAlign": "none",
            "imageUrlPrefix": "",
            "imagePathFormat": "upload/photo"}


def upload_image():
    import hashlib
    file_storage = request.files['upfile']
    name, extension = os.path.splitext(file_storage.filename)
    m = hashlib.md5()
    m.update(name)
    name = m.hexdigest()
    filename = name + extension
    file_path = os.path.join("static/upload/", filename)
    file_storage.save(file_path)
    return {"state": "SUCCESS",
            "url": '/'+file_path,
            "title": file_storage.filename,
            "original": file_storage.filename,
            "type": extension,
            "size": ""}










if __name__=="__main__":
    app.run(host = '127.0.0.1',port = 80,debug = True)

