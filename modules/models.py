from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from modules import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean,nullable=False, default=0)

    def get_reset_token(self, expires_secs=1800):
        s=Serializer(app.config['SECRET_KEY'], expires_secs)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def get_file_download_token(fileName,expires_secs=1800):
        s=Serializer(app.config['SECRET_KEY'], expires_secs)
        return s.dumps({'file_name':fileName}).decode('utf-8')
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    @staticmethod
    def get_download_file(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            fileName = s.loads(token)['file_name']
        except:
            return None
        return fileName

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
