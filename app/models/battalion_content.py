from app import db
from datetime import datetime

class BattalionEvent(db.Model):
    __tablename__ = 'battalion_events'
    
    id = db.Column(db.Integer, primary_key=True)
    battalion_id = db.Column(db.Integer, db.ForeignKey('battalion.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.String(100))
    location = db.Column(db.String(200))
    image_file = db.Column(db.String(255))
    pdf_file = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'battalion_id': self.battalion_id,
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'location': self.location,
            'image_file': self.image_file,
            'pdf_file': self.pdf_file,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class BattalionAnnouncement(db.Model):
    __tablename__ = 'battalion_announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    battalion_id = db.Column(db.Integer, db.ForeignKey('battalion.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    date = db.Column(db.String(100))
    image_file = db.Column(db.String(255))
    pdf_file = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'battalion_id': self.battalion_id,
            'title': self.title,
            'content': self.content,
            'date': self.date,
            'image_file': self.image_file,
            'pdf_file': self.pdf_file,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class BattalionGallery(db.Model):
    __tablename__ = 'battalion_gallery'
    
    id = db.Column(db.Integer, primary_key=True)
    battalion_id = db.Column(db.Integer, db.ForeignKey('battalion.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'battalion_id': self.battalion_id,
            'image_path': self.image_path,
            'caption': self.caption,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
