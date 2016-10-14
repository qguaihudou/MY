from main import db

class Posts(db.Model):

    __tablename__='Posts'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    time=db.Column(db.String, nullable=False)
    tag=db.Column(db.String,nullable=False)
    abstr=db.Column(db.String,nullable=False)
    def __init__(self,title,content,time,tag,abstr):
        self.title=title
        self.content=content
        self.time=time
        self.tag=tag
        self.abstr=abstr
    def __repr__(self):
        return '{}--{}'.format(self.title,self.content)

class Users(db.Model):
    __tablename__='Users'

    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self,username,password):
        self.username=username
        self.password=password

    def __repr__(self):
        return '{}--{}'.format(self.username,self.password)

class Tags(db.Model):
    __tablename__='Tags'

    tag_id = db.Column(db.Integer,primary_key=True)
    tag_name = db.Column(db.String , unique=True)

    def __init__(self,tag):
        self.tag_name=tag