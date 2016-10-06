from main import db

class Posts(db.Model):

    __tablename__='Posts'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

    def __init__(self,title,content):
        self.title=title
        self.content=content

    def __repr__(self):
        return '{}--{}'.format(self.title,self.content)
