from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    uid = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'