# SAFE ROUTE Backend

A comprehensive Flask-based backend system for road safety awareness and accident reporting.

## Features

- 🔐 **JWT Authentication** - Secure user registration and login
- 📍 **Accident Reporting** - Real-time accident reporting with geolocation
- 🚨 **Alert System** - Automatic alerts for high-severity accidents
- 🏥 **Emergency Services** - Find nearby hospitals, police, and ambulance services
- 📊 **Analytics Dashboard** - Comprehensive statistics and insights
- 📚 **Awareness Content** - Road safety information management
- 🔒 **Role-Based Access** - Citizen, Admin, and Authority roles

## Tech Stack

- **Framework**: Flask 3.0
- **Database**: MySQL 8.0+
- **Authentication**: JWT (Flask-JWT-Extended)
- **Security**: bcrypt, input validation, rate limiting
- **File Upload**: Pillow for image processing
- **Geolocation**: Custom Haversine distance calculations

## Installation

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip

### Setup Steps

1. **Clone the repository** (if applicable)

2. **Install dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
cp .env.example .env
```

Edit `.env` and update the following:
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- `JWT_SECRET_KEY` (use a strong random key)
- `SECRET_KEY` (use a strong random key)

4. **Create database and tables**:
```bash
mysql -u root -p < schema.sql
```

5. **Run the application**:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/profile` - Get current user profile (requires auth)

### Accidents
- `POST /api/accidents/report` - Report accident (requires auth)
- `GET /api/accidents/live` - Get live accidents with filters
- `GET /api/accidents/<id>` - Get accident details
- `PUT /api/accidents/<id>/status` - Update status (admin/authority)
- `DELETE /api/accidents/<id>` - Delete accident (admin)

### Alerts
- `GET /api/alerts` - Get active alerts
- `GET /api/alerts/nearby` - Get nearby alerts
- `POST /api/alerts/create` - Create alert (admin/authority)
- `PUT /api/alerts/<id>/dismiss` - Dismiss alert (admin/authority)

### Emergency Services
- `GET /api/emergency/nearby` - Get all nearby services
- `GET /api/emergency/hospitals` - Get nearby hospitals
- `GET /api/emergency/police` - Get nearby police stations
- `GET /api/emergency/ambulance` - Get ambulance services
- `POST /api/emergency/add` - Add service (admin)

### Awareness Content
- `GET /api/awareness` - Get all content
- `GET /api/awareness/<id>` - Get specific content
- `GET /api/awareness/categories` - Get categories
- `POST /api/awareness` - Create content (admin/authority)
- `PUT /api/awareness/<id>` - Update content (admin/authority)
- `DELETE /api/awareness/<id>` - Delete content (admin)

### Admin & Analytics
- `GET /api/admin/dashboard` - Dashboard statistics (admin/authority)
- `GET /api/admin/analytics/timeline` - Accident timeline (admin/authority)
- `GET /api/admin/analytics/zones` - Accident-prone zones (admin/authority)
- `GET /api/admin/analytics/severity-by-type` - Severity distribution (admin/authority)
- `GET /api/admin/analytics/monthly` - Monthly statistics (admin/authority)
- `GET /api/admin/analytics/peak-hours` - Peak accident hours (admin/authority)

### Utility
- `GET /health` - Health check
- `GET /uploads/<path>` - Serve uploaded files

## Default Admin Account

- **Email**: admin@saferoute.com
- **Password**: admin123
- **Role**: admin

**⚠️ Change this password immediately in production!**

## API Usage Examples

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "role": "citizen"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Report Accident
```bash
curl -X POST http://localhost:5000/api/accidents/report \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "latitude=28.6139" \
  -F "longitude=77.2090" \
  -F "accident_type=collision" \
  -F "severity=high" \
  -F "description=Two vehicle collision" \
  -F "image=@accident.jpg"
```

### Get Live Accidents
```bash
curl "http://localhost:5000/api/accidents/live?severity=high&page=1&page_size=20"
```

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── database.py            # Database connection and utilities
├── schema.sql             # Database schema
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── models/                # Data models
│   ├── user.py
│   ├── accident.py
│   ├── alert.py
│   ├── emergency_service.py
│   └── awareness.py
├── routes/                # API routes
│   ├── auth.py
│   ├── accidents.py
│   ├── alerts.py
│   ├── emergency.py
│   ├── awareness.py
│   └── admin.py
├── services/              # Business logic services
│   └── analytics_service.py
├── middleware/            # Middleware functions
│   └── auth.py
├── utils/                 # Utility functions
│   ├── geolocation.py
│   ├── validators.py
│   ├── security.py
│   ├── file_handler.py
│   ├── response.py
│   └── logger.py
└── uploads/               # Uploaded files directory
    └── accidents/
```

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control (RBAC)
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Rate limiting
- Secure file uploads

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Running in Production Mode
```bash
export FLASK_ENV=production
python app.py
```

## License

This project is part of the SAFE ROUTE initiative for road safety awareness.
