from .. import db

class Battalion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    battalion_number = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(150), nullable=False)
    district = db.Column(db.String(150))
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    commandant_name = db.Column(db.String(150))
    commandant_rank = db.Column(db.String(100))
    commandant_image = db.Column(db.String(255))
    ri_1 = db.Column(db.String(150))
    ri_2 = db.Column(db.String(150))
    ri_3 = db.Column(db.String(150))
    commandant_speech = db.Column(db.Text)
    organizational_structure = db.Column(db.Text)  # JSON data for additional officers
    history = db.Column(db.Text)  # Battalion history content
