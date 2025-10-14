#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, jsonify
from flask_restful import Resource

# Local imports
from config import app, db, api
from models import User, ServiceProvider, Review

# Views go here!

@app.route('/')
def index():
    return '<h1>Konekte - Community Resource Hub API</h1>'


# User Routes
class Users(Resource):
    def get(self):
        users = User.query.all()
        return make_response(
            jsonify([user.to_dict() for user in users]),
            200
        )
    
    def post(self):
        try:
            data = request.get_json()
            new_user = User(
                name=data.get('name'),
                email=data.get('email')
            )
            db.session.add(new_user)
            db.session.commit()
            return make_response(
                jsonify(new_user.to_dict(rules=('-service_providers', '-reviews'))),
                201
            )
        except ValueError as e:
            return make_response(jsonify({"error": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"error": "Failed to create user"}), 400)


class UserByID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
        return make_response(jsonify(user.to_dict()), 200)


# ServiceProvider Routes
class ServiceProviders(Resource):
    def get(self):
        # Get query parameters for filtering
        category = request.args.get('category')
        search = request.args.get('search')
        
        # Start with base query
        query = ServiceProvider.query
        
        # Apply filters if provided
        if category:
            query = query.filter_by(category=category)
        
        if search:
            # Search in name, description, or location
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    ServiceProvider.name.ilike(search_term),
                    ServiceProvider.description.ilike(search_term),
                    ServiceProvider.location.ilike(search_term)
                )
            )
        
        services = query.all()
        
        return make_response(
            jsonify([service.to_dict(rules=('-user.service_providers', '-reviews.service_provider')) for service in services]),
            200
        )
    
    def post(self):
        try:
            data = request.get_json()
            new_service = ServiceProvider(
                name=data.get('name'),
                category=data.get('category'),
                description=data.get('description'),
                location=data.get('location'),
                phone=data.get('phone'),
                hours=data.get('hours'),
                user_id=data.get('user_id')
            )
            db.session.add(new_service)
            db.session.commit()
            return make_response(
                jsonify(new_service.to_dict(rules=('-user.service_providers', '-reviews'))),
                201
            )
        except ValueError as e:
            return make_response(jsonify({"error": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"error": "Failed to create service provider"}), 400)


class ServiceProviderByID(Resource):
    def get(self, id):
        service = ServiceProvider.query.filter_by(id=id).first()
        if not service:
            return make_response(jsonify({"error": "Service provider not found"}), 404)
        return make_response(
            jsonify(service.to_dict(rules=('-user.service_providers', '-reviews.service_provider'))),
            200
        )
    
    def patch(self, id):
        service = ServiceProvider.query.filter_by(id=id).first()
        if not service:
            return make_response(jsonify({"error": "Service provider not found"}), 404)
        
        try:
            data = request.get_json()
            
            # Update only provided fields
            if 'name' in data:
                service.name = data['name']
            if 'category' in data:
                service.category = data['category']
            if 'description' in data:
                service.description = data['description']
            if 'location' in data:
                service.location = data['location']
            if 'phone' in data:
                service.phone = data['phone']
            if 'hours' in data:
                service.hours = data['hours']
            
            db.session.commit()
            return make_response(
                jsonify(service.to_dict(rules=('-user.service_providers', '-reviews.service_provider'))),
                200
            )
        except ValueError as e:
            return make_response(jsonify({"error": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"error": "Failed to update service provider"}), 400)
    
    def delete(self, id):
        service = ServiceProvider.query.filter_by(id=id).first()
        if not service:
            return make_response(jsonify({"error": "Service provider not found"}), 404)
        
        try:
            db.session.delete(service)
            db.session.commit()
            return make_response(jsonify({"message": "Service provider deleted successfully"}), 200)
        except Exception as e:
            return make_response(jsonify({"error": "Failed to delete service provider"}), 400)


# Review Routes
class Reviews(Resource):
    def get(self):
        # Optional: filter by service_provider_id
        service_id = request.args.get('service_provider_id')
        
        if service_id:
            reviews = Review.query.filter_by(service_provider_id=service_id).all()
        else:
            reviews = Review.query.all()
        
        return make_response(
            jsonify([review.to_dict(rules=('-user.reviews', '-service_provider.reviews')) for review in reviews]),
            200
        )
    
    def post(self):
        try:
            data = request.get_json()
            new_review = Review(
                rating=data.get('rating'),
                comment=data.get('comment'),
                user_id=data.get('user_id'),
                service_provider_id=data.get('service_provider_id')
            )
            db.session.add(new_review)
            db.session.commit()
            return make_response(
                jsonify(new_review.to_dict(rules=('-user.reviews', '-service_provider.reviews'))),
                201
            )
        except ValueError as e:
            return make_response(jsonify({"error": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"error": "Failed to create review"}), 400)


class ReviewByID(Resource):
    def get(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            return make_response(jsonify({"error": "Review not found"}), 404)
        return make_response(
            jsonify(review.to_dict(rules=('-user.reviews', '-service_provider.reviews'))),
            200
        )
    
    def patch(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            return make_response(jsonify({"error": "Review not found"}), 404)
        
        try:
            data = request.get_json()
            
            # Update only provided fields
            if 'rating' in data:
                review.rating = data['rating']
            if 'comment' in data:
                review.comment = data['comment']
            
            db.session.commit()
            return make_response(
                jsonify(review.to_dict(rules=('-user.reviews', '-service_provider.reviews'))),
                200
            )
        except ValueError as e:
            return make_response(jsonify({"error": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"error": "Failed to update review"}), 400)
    
    def delete(self, id):
        review = Review.query.filter_by(id=id).first()
        if not review:
            return make_response(jsonify({"error": "Review not found"}), 404)
        
        try:
            db.session.delete(review)
            db.session.commit()
            return make_response(jsonify({"message": "Review deleted successfully"}), 200)
        except Exception as e:
            return make_response(jsonify({"error": "Failed to delete review"}), 400)


# Register API Resources
api.add_resource(Users, '/api/users')
api.add_resource(UserByID, '/api/users/<int:id>')
api.add_resource(ServiceProviders, '/api/service-providers')
api.add_resource(ServiceProviderByID, '/api/service-providers/<int:id>')
api.add_resource(Reviews, '/api/reviews')
api.add_resource(ReviewByID, '/api/reviews/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)