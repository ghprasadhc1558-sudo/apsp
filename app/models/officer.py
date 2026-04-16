from .. import db

class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    location = db.Column(db.String(100))
    image_file = db.Column(db.String(100), default='default.jpg')
    priority = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'rank': self.rank,
            'designation': self.designation,
            'phone': self.phone,
            'email': self.email,
            'location': self.location,
            'image_file': self.image_file,
            'priority': self.priority
        }
