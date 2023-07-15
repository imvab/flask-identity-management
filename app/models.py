from .extensions import db

class Identity(db.Model):
    __tablename__ = 'identity'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String)
    email = db.Column(db.String)
    linked_id = db.Column(db.Integer)
    link_precedence = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)