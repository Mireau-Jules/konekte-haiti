from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationships
    service_providers = db.relationship('ServiceProvider', back_populates='user', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    
    # Association proxy - get all service providers this user has reviewed
    reviewed_services = association_proxy('reviews', 'service_provider')
    
    # Serialization rules - prevent infinite recursion
    serialize_only = ('id', 'name', 'email', 'created_at')
    
    # Validations
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(name) > 100:
            raise ValueError("Name must be less than 100 characters")
        return name.strip()
    
    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError("Must provide a valid email address")
        if len(email) > 120:
            raise ValueError("Email must be less than 120 characters")
        return email.lower().strip()
    
    def to_dict_with_relations(self):
        """Custom serialization with relationships"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'service_providers': [sp.to_dict() for sp in self.service_providers],
            'reviews': [r.to_dict() for r in self.reviews]
        }
    
    def __repr__(self):
        return f'<User {self.id}: {self.name}>'


class ServiceProvider(db.Model, SerializerMixin):
    __tablename__ = 'service_providers'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    hours = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='service_providers')
    reviews = db.relationship('Review', back_populates='service_provider', cascade='all, delete-orphan')
    
    # Association proxy - get all users who reviewed this service
    reviewers = association_proxy('reviews', 'user')
    
    # Serialization rules - prevent infinite recursion
    serialize_only = ('id', 'name', 'category', 'description', 'location', 'phone', 'hours', 'created_at', 'user_id')
    
    # Validations
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 3:
            raise ValueError("Service name must be at least 3 characters long")
        if len(name) > 150:
            raise ValueError("Service name must be less than 150 characters")
        return name.strip()
    
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = [
            'Medical/Health',
            'Education',
            'Water & Sanitation',
            'Community Centers',
            'Emergency Services'
        ]
        if category not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category
    
    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description.strip()) < 10:
            raise ValueError("Description must be at least 10 characters long")
        if len(description) > 1000:
            raise ValueError("Description must be less than 1000 characters")
        return description.strip()
    
    @validates('location')
    def validate_location(self, key, location):
        if not location or len(location.strip()) < 5:
            raise ValueError("Location must be at least 5 characters long")
        if len(location) > 200:
            raise ValueError("Location must be less than 200 characters")
        return location.strip()
    
    @validates('phone')
    def validate_phone(self, key, phone):
        if phone:
            # Remove spaces and dashes for validation
            clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not clean_phone.isdigit():
                raise ValueError("Phone number must contain only digits, spaces, dashes, or parentheses")
            if len(clean_phone) < 8 or len(clean_phone) > 15:
                raise ValueError("Phone number must be between 8 and 15 digits")
        return phone
    
    def to_dict_with_reviews(self):
        """Custom serialization with reviews"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'location': self.location,
            'phone': self.phone,
            'hours': self.hours,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id,
            'user': {
                'id': self.user.id,
                'name': self.user.name,
                'email': self.user.email
            } if self.user else None,
            'reviews': [r.to_dict() for r in self.reviews],
            'average_rating': sum(r.rating for r in self.reviews) / len(self.reviews) if self.reviews else 0
        }
    
    def __repr__(self):
        return f'<ServiceProvider {self.id}: {self.name}>'


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='reviews')
    service_provider = db.relationship('ServiceProvider', back_populates='reviews')
    
    # Serialization rules - prevent infinite recursion
    serialize_only = ('id', 'rating', 'comment', 'created_at', 'user_id', 'service_provider_id')
    
    # Validations
    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    @validates('comment')
    def validate_comment(self, key, comment):
        if not comment or len(comment.strip()) < 5:
            raise ValueError("Comment must be at least 5 characters long")
        if len(comment) > 500:
            raise ValueError("Comment must be less than 500 characters")
        return comment.strip()
    
    def to_dict_with_relations(self):
        """Custom serialization with user and service info"""
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id,
            'service_provider_id': self.service_provider_id,
            'user': {
                'id': self.user.id,
                'name': self.user.name
            } if self.user else None,
            'service_provider': {
                'id': self.service_provider.id,
                'name': self.service_provider.name
            } if self.service_provider else None
        }
    
    def __repr__(self):
        return f'<Review {self.id}: {self.rating} stars>'