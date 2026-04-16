from .. import db

class Commandant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    rank = db.Column(db.String(100))
    image = db.Column(db.String(255))
    battalion_id = db.Column(db.Integer, db.ForeignKey('battalion.id'))
