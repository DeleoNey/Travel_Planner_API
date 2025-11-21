# 🌍 Travel Planner API

A powerful RESTful API for planning and managing trips with route points, weather forecasts, and nearby places discovery. Built with Django REST Framework and PostgreSQL.

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

## ✨ Features

- 🔐 **User Authentication**: JWT-based authentication with registration and login
- 🗺️ **Trip Management**: Create, update, and manage trips with detailed information
- 📍 **Route Points**: Add multiple destinations to trips with geolocation
- 🌤️ **Weather Forecast**: Get weather information for trip destinations
- 🏨 **Nearby Places**: Discover points of interest near your destinations
- 💰 **Budget Tracking**: Plan and track expenses in different currencies
- 📱 **RESTful API**: Well-structured endpoints following REST principles
- 📚 **API Documentation**: Interactive Swagger/ReDoc documentation
- 🐳 **Docker Support**: Easy deployment with Docker Compose

## 🛠️ Tech Stack

- **Backend Framework**: Django 5.2.8
- **API Framework**: Django REST Framework 3.16.1
- **Authentication**: JWT (Simple JWT 5.5.1)
- **Database**: PostgreSQL 16
- **API Documentation**: drf-yasg 1.21.11
- **Containerization**: Docker & Docker Compose
- **Admin Panel**: pgAdmin 4

## 📋 Prerequisites

- Docker & Docker Compose
- Git

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/DeleoNey/Travel_Planner_API.git
cd Travel_Planner_API
```

### 2. Create environment file

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=travel_planner
POSTGRES_USER=traveler
POSTGRES_PASSWORD=traveler
POSTGRES_HOST=db
POSTGRES_PORT=5432

WEATHER_API_KEY=your_api_key(openweathermap)
PLACES_API_KEY=your_api_key(OpenTripMap API)
```

### 3. Build and run with Docker

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### 4. Create superuser (Admin access)

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to create an admin account:
```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
```

### 5. Access the services

- **API**: http://localhost:8000/api/
- **Swagger Documentation**: http://localhost:8000/swagger/
- **ReDoc Documentation**: http://localhost:8000/redoc/
- **Admin Panel**: http://localhost:8000/admin/ (use superuser credentials)
- **pgAdmin**: http://localhost:5050
  - Email: `admin@admin.com`
  - Password: `admin`

## 📡 API Endpoints

### 🔐 Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/users/register/` | Register new user | ❌ |
| POST | `/api/users/login/` | Login and get JWT tokens | ❌ |
| POST | `/api/users/token/refresh/` | Refresh access token | ❌ |
| GET | `/api/users/profile/` | Get user profile | ✅ |

### 🗺️ Trips

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/trips/` | List all user trips | ✅ |
| POST | `/api/trips/` | Create new trip | ✅ |
| GET | `/api/trips/{id}/` | Get trip details | ✅ |
| PUT | `/api/trips/{id}/` | Update trip | ✅ |
| PATCH | `/api/trips/{id}/` | Partial update trip | ✅ |
| DELETE | `/api/trips/{id}/` | Delete trip | ✅ |

### 📍 Trip Points (Route Points)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/trips/{trip_id}/points/` | List all points in trip | ✅ |
| POST | `/api/trips/{trip_id}/points/` | Add point to trip | ✅ |
| GET | `/api/trips/{trip_id}/points/{id}/` | Get point details | ✅ |
| PUT | `/api/trips/{trip_id}/points/{id}/` | Update point | ✅ |
| PATCH | `/api/trips/{trip_id}/points/{id}/` | Partial update point | ✅ |
| DELETE | `/api/trips/{trip_id}/points/{id}/` | Delete point | ✅ |
| GET | `/api/trips/{trip_id}/points/{id}/places-nearby/` | Get nearby places | ✅ |
| GET | `/api/trips/{trip_id}/points/{id}/weather/` | Get weather forecast | ✅ |

## 📝 API Usage Examples

### Register a new user

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "traveler",
    "email": "traveler@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "traveler",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Create a trip

```bash
curl -X POST http://localhost:8000/api/trips/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "European Adventure",
    "description": "Two weeks exploring Europe",
    "start_date": "2025-06-01",
    "end_date": "2025-06-14",
    "base_currency": "EUR"
  }'
```

### Add a trip point

```bash
curl -X POST http://localhost:8000/api/trips/1/points/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Paris",
    "country": "France",
    "date": "2025-06-01",
    "planned_budget": 500.00,
    "latitude": 48.8566,
    "longitude": 2.3522
  }'
```

### Get weather forecast

```bash
curl -X GET http://localhost:8000/api/trips/1/points/1/weather/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Discover nearby places

```bash
curl -X GET http://localhost:8000/api/trips/1/points/1/places-nearby/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🗄️ Database Schema

### User Model
- `username` (unique)
- `email` (unique)
- `first_name`
- `last_name`
- `is_active`
- `is_staff`

### Trip Model
- `user` (FK to User)
- `title`
- `description`
- `start_date`
- `end_date`
- `base_currency`
- `created_at`
- `updated_at`

### TripPoint Model
- `trip` (FK to Trip)
- `city`
- `country`
- `date`
- `planned_budget`
- `latitude`
- `longitude`
- `created_at`

## 🔒 Authentication

This API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. Register or login to get access and refresh tokens
2. Include the access token in the Authorization header:
   ```
   Authorization: Bearer YOUR_ACCESS_TOKEN
   ```
3. Refresh tokens when they expire using `/api/users/token/refresh/`

**Token Lifetimes:**
- Access Token: 60 minutes (default)
- Refresh Token: 1 day (default)

## 📦 Project Structure

```
Travel_Planner_API/
├── travel_planner_api/      # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                   # User authentication app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── trips/                   # Trips management app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── route_points/            # Trip points app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── core/                    # Core utilities
│   └── permissions.py       # Custom permission classes
├── integrations/            # External API integrations
│   └── services/
│       ├── currency.py      # Currency conversion service
│       ├── places.py        # Places discovery service
│       └── weather.py       # Weather forecast service
├── docker-compose.yml       # Docker services configuration
├── Dockerfile               # Docker image definition
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```

## 🐳 Docker Services

The application consists of three services:

- **web**: Django application (port 8000)
- **db**: PostgreSQL database (port 5432)
- **pgadmin**: Database administration tool (port 5050)

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | - |
| `DEBUG` | Debug mode | True |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts | localhost,127.0.0.1 |
| `POSTGRES_DB` | Database name | travel_planner |
| `POSTGRES_USER` | Database user | traveler |
| `POSTGRES_PASSWORD` | Database password | traveler |
| `POSTGRES_HOST` | Database host | db |
| `POSTGRES_PORT` | Database port | 5432 |

## 👤 Author

**DeleoNey**

- GitHub: [@DeleoNey](https://github.com/DeleoNey)
