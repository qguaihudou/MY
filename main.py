#-*- coding: utf-8 -*-
#encoding=utf-8
from flask import abort,Flask,render_template,session,url_for,redirect,request,flash
import json,os
from flask_sqlalchemy import SQLAlchemy
import sys,time
reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)
app.debug = True
app.secret_key = 'it is a my fucking blog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['username']='qguaihudou'
app.config['password']=''
# create sqlalchemy object
db = SQLAlchemy(app)

from model import *



#To get the abstrct post first image
def getimg(text):
    t=0
    while t<len(text)-4:
        if text[t:t+4] == "<img":
            u=t
            while text[t] != ">" and t<len(text):
                t=t+1
            return text[u:t+1]
        t=t+1
    return ''

#clean the code
def cleanthecode(text):
    t=0
    while t<len(text):
        if text[t:t+5] == "<code":
            u=t
            while text[t:t+7] != "</code>":
                t=t+1
            return text[:u]+text[t+7:]
        t=t+1
    return text

#To get the abstract of the post
def getabstr(text):
    img = getimg(text)
    text=cleanthecode(text)
    text=text[:1200]
    text=text.replace('&nbsp;',' ')
    text=text.replace('</p','#$%^&<')
    text=text.replace('</b','#$%^&<')
    text=text.replace('</h','#$%^&<')
    text=text.replace('<br>','#$%^&')
    text = text.replace('</li','#$%^&<')
    def fn(x, y):
        if x[-1] == "<" and y != ">":
            return x
        else:
            return x+y
    text=reduce(fn,text)
    text=text.replace('<>','')
    text=text.replace('\n\n\n','\n')
    text=text.replace('\n\n','\n')
    text=text.replace('#$%^&','</p><p>')
    text=img+'<hr>'+text[:220]
    return text

#for administrator check how many users he has
@app.route('/checkusers',methods=['GET'])
def checkusers():
    users=Users.query.all()
    return render_template('checkusers.html',users=users)

#manage blog（after administor login）
@app.route('/admin',methods=['GET'])
def admin():
    post=db.session.query(Posts).all()
    return render_template('admin.html',post=post)

#Asure to delete blog(after administor login)
@app.route('/delete/<int:pid>',methods=['GET'])
def delete(pid):
    pos=Posts.query.filter_by(id=pid).first()
    return render_template('delete.html',pos=pos)


#delete blog(after administor login)
@app.route('/deletepost/<int:pid>',methods=['GET'])
def deletepost(pid):
    pos=Posts.query.filter_by(id=pid).first()
    db.session.delete(pos)
    db.session.commit()
    flash('删除文章成功！')
    return redirect(url_for('hello'))

#the menu of the blog(ordered by time)
@app.route('/blogs',methods=['GET'])
def blogs():
    post = Posts.query.order_by(Posts.id.desc())
    return render_template('blogs.html',post=post)



#edit blog(after administrator login)
@app.route('/edit/<int:pid>',methods=['GET','POST'])
def edit(pid):
    if session.get('admin'):
        if request.method == 'POST':
            content=request.form['content']
            title=request.form['title']
            tag=request.form['tag']
            pos = Posts.query.filter_by(id=pid).first()
            pos.title = title
            pos.content = content
            pos.abstr=getabstr(pos.content)
            pos.tag=tag
            db.session.commit()
            flash('文章修改成功！')
            return redirect(url_for('hello'))
        tags=Tags.query.all()
        pos = Posts.query.filter_by(id=pid).first()
        return render_template('edit.html',pos=pos,tags=tags)
    return redirect(url_for('hello'))


#select by tag
@app.route('/select/<tag>',methods=['GET'])
def select(tag):
    post=Posts.query.filter_by(tag=tag).order_by(Posts.id.desc())
    return render_template('select.html',post=post)

#mannage tags
@app.route('/tag',methods=['GET','POST'])
def tags():
    tag=Tags.query.all()
    if request.method=='POST':
        T=request.form['tag']
        db.session.add(Tags(T))
        db.session.commit()
        flash('标签添加成功')
        return redirect(url_for('tags'))
    return render_template('tag.html',tags=tag)



#change tag name
@app.route('/change/<int:pid>',methods=['GET','POST'])
def change(pid):
    if session.get('admin'):
        T = Tags.query.filter_by(tag_id = pid).first()
        if request.method=='POST':
            post=Posts.query.filter_by(tag = T.tag_name).all()
            for pos in post:
                pos.tag=request.form['tag']
            T.tag_name = request.form['tag']
            db.session.commit()
            flash('tag修改成功')
            return redirect(url_for('tags'))
        return render_template('change.html',tag=T)
    else:
        return redirect(url_for('hello'))



#the homepage
@app.route('/',methods=['GET','POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
def hello(page = 1):
    db.create_all()
    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']
        Time=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        tag=request.form['tag']
        abstr=getabstr(content)
        db.session.add(Posts(title,content,Time,tag,abstr))
        db.session.commit()
    post = Posts.query.order_by(Posts.id.desc()).paginate(page, 6, False)
    return render_template('homepage.html', post = post)



#for users to login
@app.route('/sign',methods=['GET','POST'])
def sign():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if username or password:
            if username == app.config['username'] and password == app.config['password']:
                session['username'] = username
                session['admin'] = True
                flash('登陆成功，欢迎回来！')
                return redirect(url_for('hello'))
            t = Users.query.filter_by(username=username).first()
            if t is  None or t.password != password:
                flash('你输入的用户名和密码有误')
                return redirect(url_for('sign'))
            session['username']=username
            flash('登陆成功，欢迎回来！')
            return redirect(url_for('hello'))
        flash('您输入的信息不完整，请重新输入')
        return redirect(url_for('sign'))
    return render_template('sign.html')

#for users to register
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        if request.form['username'] !='' and request.form['password'] !='' and request.form['passwordr'] !='':
            if Users.query.filter_by(username=request.form['username']).first() is not None:
                flash('该用户名已存在，请重新注册。')
                return render_template('signup.html')
            if  request.form['password'] != request.form['passwordr']:
                flash('两次输入的密码不一样，请重新输入。')
                return render_template('signup.html')
            db.session.add(Users(request.form['username'], request.form['password']))
            db.session.commit()
            flash('恭喜你注册成功。')
            session['username']=request.form['username']
            return redirect(url_for('hello'))
        flash('您的信息不完整，请重新输入。')
        return render_template('signup.html')
    return render_template('signup.html')

#post articles if you are admin
@app.route('/posts',methods=['GET'])
def posts():
    if session.get('admin'):
        tags=Tags.query.all()
        return render_template('posts blog.html',tags=tags)
    else:
        return redirect(url_for('hello'))

#read the whole article
@app.route('/article/<int:pid>',methods=['GET'])
def read(pid):
    pos=Posts.query.filter_by(id = pid).first()
    if pos is None:
        abort(404)
    else:
        return render_template('article.html',pos=pos)

#logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session['admin']=False
    flash('你已经登出')
    return redirect(url_for('hello'))













if __name__=="__main__":
    app.run(host = '127.0.0.1',port = 80,debug = True)

