from .. import db
import json

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    # Add more fields as needed


class ContactInfo(db.Model):
    """Model for storing website contact information (admin-managed)"""
    __tablename__ = 'contact_info'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_numbers = db.Column(db.Text)  # JSON array of phone numbers
    email_addresses = db.Column(db.Text)  # JSON array of email addresses
    office_address = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    def get_phone_numbers(self):
        """Returns list of phone numbers"""
        if self.phone_numbers:
            try:
                return json.loads(self.phone_numbers)
            except:
                return []
        return []
    
    def set_phone_numbers(self, phones):
        """Set phone numbers from list"""
        self.phone_numbers = json.dumps(phones)
    
    def get_email_addresses(self):
        """Returns list of email addresses"""
        if self.email_addresses:
            try:
                return json.loads(self.email_addresses)
            except:
                return []
        return []
    
    def set_email_addresses(self, emails):
        """Set email addresses from list"""
        self.email_addresses = json.dumps(emails)

