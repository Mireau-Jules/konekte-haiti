# Konekte - Community Resource Hub for Haiti

## Project Overview

**Konekte** is a full-stack web application that connects Haitian communities with essential services and resources. The platform allows users to discover, review, and contribute information about healthcare facilities, educational institutions, water services, community centers, and emergency services across Haiti.

### Purpose

This application was built to address real community needs in Haiti by creating a centralized platform where citizens can:
- Find essential services (medical, educational, water, community centers, emergency)
- Share reviews and ratings based on their experiences
- Add new service providers to help their community
- Search and filter services by category and location

### Technology Stack

- **Frontend**: React with React Router DOM for client-side routing
- **Backend**: Flask with Flask-RESTful for API endpoints
- **Database**: SQLite with Flask-SQLAlchemy ORM
- **Form Validation**: Formik for client-side validation
- **Database Migrations**: Flask-Migrate (Alembic)

---

## Project Structure

```
konekte-haiti/
├── server/
│   ├── app.py                 # Flask application with API routes
│   ├── config.py              # Flask configuration and database setup
│   ├── models.py              # SQLAlchemy models (User, ServiceProvider, Review)
│   ├── seed.py                # Database seed script with sample data
│   ├── instance/
│   │   └── app.db            # SQLite database file
│   ├── migrations/            # Alembic migration files
│   └── Pipfile                # Python dependencies
└── client/
    ├── src/
    │   ├── App.js            # Main React component with routing
    │   ├── App.css           # Main styles
    │   ├── index.js          # React entry point
    │   └── components/
    │       ├── NavBar.js      # Navigation bar component
    │       ├── ServiceList.js # Service listings with search/filter
    │       ├── ServiceDetail.js # Individual service details and reviews
    │       ├── AddServiceForm.js # Form to add new services
    │       └── AddReviewForm.js # Form to add reviews
    ├── package.json           # JavaScript dependencies
    └── public/                # Static files
```

---

## Data Models

### User
- `id`: Primary key
- `name`: User's full name
- `email`: User's email address
- `created_at`: Timestamp

### ServiceProvider
- `id`: Primary key
- `name`: Service name
- `category`: One of (Medical/Health, Education, Water & Sanitation, Community Centers, Emergency Services)
- `description`: Detailed description of services
- `location`: Service location/address
- `phone`: Contact phone number
- `hours`: Operating hours
- `user_id`: Foreign key (User who added the service)
- `created_at`: Timestamp

### Review (Many-to-Many Association)
- `id`: Primary key
- `rating`: 1-5 stars (integer)
- `comment`: User's text review
- `user_id`: Foreign key (User who wrote review)
- `service_provider_id`: Foreign key (Service being reviewed)
- `created_at`: Timestamp

**Relationships**:
- User has many ServiceProviders
- User has many Reviews
- ServiceProvider has many Reviews
- User ↔ ServiceProvider through Review (many-to-many)

---

## API Endpoints

### ServiceProviders
- `GET /api/service-providers` - List all services (supports ?category= and ?search= filters)
- `GET /api/service-providers/:id` - Get single service with reviews
- `POST /api/service-providers` - Create new service
- `PATCH /api/service-providers/:id` - Update service
- `DELETE /api/service-providers/:id` - Delete service

### Reviews
- `GET /api/reviews` - List all reviews (supports ?service_provider_id= filter)
- `POST /api/reviews` - Create new review
- `PATCH /api/reviews/:id` - Update review
- `DELETE /api/reviews/:id` - Delete review

### Users
- `GET /api/users` - List all users
- `POST /api/users` - Create new user

---

## Setup and Installation

### Prerequisites
- Python 3.9+
- Node.js 14+
- npm or yarn
- Git

### Backend Setup

1. **Navigate to server directory:**
```bash
cd server
```

2. **Create virtual environment and install dependencies:**
```bash
pipenv install
pipenv shell
```

3. **Initialize database:**
```bash
flask db init
flask db revision -m'Create DB'
flask db upgrade head
flask db revision --autogenerate -m'Create User, ServiceProvider, and Review models'
flask db upgrade head
```

4. **Seed sample data:**
```bash
python seed.py
```

5. **Start Flask server:**
```bash
python app.py
```

The backend will run on `http://localhost:5555`

### Frontend Setup

1. **Open new terminal and navigate to client directory:**
```bash
cd client
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start React development server:**
```bash
npm start
```

The frontend will open at `http://localhost:3000`

---

## Running the Application

### For Teachers/Evaluators:

1. **Start both servers** (in separate terminal windows):

**Terminal 1 - Backend:**
```bash
cd server
pipenv shell
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd client
npm start
```

2. **Access the application:**
- Open browser to `http://localhost:3000`
- Backend API available at `http://localhost:5555`

3. **Test the application:**
- View services on home page
- Click on any service to see details and reviews
- Add a new service via "Ajouter un Service" link
- Add reviews to services
- Search and filter services by category

### Sample Data

The application comes pre-loaded with:
- 6 users
- 12 service providers across 5 categories
- 15 sample reviews with ratings

---

## Features Implemented

### Frontend Features
✅ Home page with service listing  
✅ Search services by name, description, or location  
✅ Filter services by category  
✅ Service detail pages with reviews  
✅ Add new service form with validation  
✅ Add review form with rating and comment  
✅ Navigation between pages using React Router  
✅ Responsive design with CSS styling  

### Backend Features
✅ Full CRUD operations for services  
✅ Create and read operations for all resources  
✅ Data validation (string length, number format, data types)  
✅ RESTful API endpoints  
✅ Database seeding with realistic Haitian data  
✅ CORS enabled for frontend-backend communication  

### Validation

**Formik Form Validation:**
- Service Name: 3-150 characters (string length validation)
- Category: Must be valid category (data type validation)
- Description: 10-1000 characters (string length validation)
- Location: 5-200 characters (string length validation)
- Phone: 8-15 digits (number format validation)
- Rating: 1-5 integer (data type validation)
- Comment: 5-500 characters (string length validation)

---

## Technical Requirements Met

### Phase 4 Requirements
✅ Flask API backend with React frontend  
✅ 3 models with defined relationships  
✅ 2 one-to-many relationships (User→ServiceProvider, User→Review, ServiceProvider→Review)  
✅ 1 many-to-many relationship (User ↔ ServiceProvider through Review)  
✅ User-submittable attributes in association model (rating, comment)  
✅ Full CRUD for ServiceProvider resource  
✅ Create and read actions for all resources  
✅ Formik forms with validation on all inputs  
✅ Data type validation (rating 1-5 integer)  
✅ String/number format validation (phone 8-15 digits)  
✅ 3+ client-side routes (/, /services/:id, /add-service)  
✅ Navigation bar for route switching  
✅ Fetch calls connecting frontend to backend  

---

## Common Issues and Solutions

### Database Issues
**Problem**: "no such table: users" error
- **Solution**: Run `python seed.py` to create tables and seed data

### Port Already in Use
**Problem**: "Address already in use" error
- **Solution**: 
  - Backend: Change port in app.py (line: `app.run(port=5555)`)
  - Frontend: Kill process using port 3000 or change port in package.json

### Component Not Loading
**Problem**: 404 errors when fetching from backend
- **Solution**: Ensure both servers are running (backend on 5555, frontend on 3000)

### Form Validation Not Working
**Problem**: Forms submit without validation
- **Solution**: Ensure Formik is installed (`npm list formik`)

---

## Future Enhancements

- User authentication and login system
- Email notifications for new reviews
- Map integration to display services geographically
- Photo uploads for service providers
- Admin dashboard for moderation
- Multi-language support
- Mobile app version

---

## Commit History

This project contains 30+ commits showing the development process:
- Initial project setup
- Database models and migrations
- Backend API routes
- Frontend component development
- Form validation implementation
- Styling and UI improvements

Each commit follows best practices:
- Clear, descriptive messages in present tense
- 50 characters or less per message
- Frequent commits showing incremental progress

---

## License

This project is open source and available for educational purposes.

---

## Author

Built for Phase 4 project assessment  
Demonstrating full-stack development skills with Flask and React  
Focused on solving real community problems in Haiti