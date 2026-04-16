from .. import db

class SDRFContent(db.Model):
    """Model for managing SDRF content"""
    __tablename__ = 'sdrf_content'
    
    id = db.Column(db.Integer, primary_key=True)
    # About SDRF page content (currently in sdrf.html)
    about_content = db.Column(db.Text)  # Main content for About SDRF page
    
    # PDF file paths
    about_pdf = db.Column(db.String(500))       # Path to About SDRF PDF file
    operations_pdf = db.Column(db.String(500))  # Path to operations PDF file
    training_pdf = db.Column(db.String(500))    # Path to training PDF file
    
    # Timestamps
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    def __repr__(self):
        return f'<SDRFContent {self.id}>'
