from .. import db

class Content(db.Model):
    """Model for managing editable website content"""
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(50), nullable=False, unique=True)  # home, about, sdrf, etc.
    title = db.Column(db.String(200))
    content = db.Column(db.Text)  # Main content/description
    section_data = db.Column(db.Text)  # JSON data for additional sections
    meta_description = db.Column(db.String(500))
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
