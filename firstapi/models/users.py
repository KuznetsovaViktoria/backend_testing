from db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, )
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def find_by_username(username):
        user = User.query.filter_by(username=username).first()
        return user

    @staticmethod
    def find_by_id(_id):
        user = User.query.filter_by(id=_id).first()
        return user

    @staticmethod
    def post(username, password):
        db.session.add(User(username=username, password=password))
        db.session.commit()
