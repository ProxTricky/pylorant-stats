# Valorant Stats Dashboard

Personal Valorant statistics dashboard with MongoDB and Django. Features Auth0 authentication and HenrikDev API integration.

## 🚀 Features

- Personal statistics dashboard for Valorant
- Secure Auth0 authentication (email-restricted access)
- Match history tracking
- Performance statistics
- API caching system
- Dockerized deployment

## 🛠️ Tech Stack

- **Backend**: Django + Django Ninja Extra
- **Database**: MongoDB (external)
- **Authentication**: Auth0
- **Package Management**: Poetry
- **Containerization**: Docker
- **API Integration**: HenrikDev Valorant API

## 📋 Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Poetry for dependency management
- Auth0 account and credentials
- HenrikDev API key
- External MongoDB instance

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/valorant-stats.git
   cd valorant-stats
   ```

2. **Install Poetry**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run with Docker**
   ```bash
   docker-compose up --build
   ```

## ⚙️ Configuration

1. **Auth0 Setup**
   - Create an account on [Auth0](https://auth0.com)
   - Create a new Regular Web Application
   - Configure your application settings
   - Add your allowed email in the settings
   - Copy credentials to `.env`

2. **HenrikDev API**
   - Get your API key from [HenrikDev](https://henrikdev.xyz)
   - Add it to `.env`

3. **MongoDB Configuration**
   - Configure your external MongoDB connection
   - Update MongoDB credentials in `.env`

4. **Environment Variables**
   ```env
   # Django
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # MongoDB External
   MONGODB_URL=mongodb://user:password@your-mongo-host:27017/
   MONGODB_DB_NAME=valorant_stats
   MONGODB_USER=your-mongo-user
   MONGODB_PASSWORD=your-mongo-password
   MONGODB_HOST=your-mongo-host
   MONGODB_PORT=27017

   # Valorant API
   HENRIK_API_KEY=your-henrik-api-key

   # Auth0 Configuration
   AUTH0_DOMAIN=your-tenant.auth0.com
   AUTH0_CLIENT_ID=your-client-id
   AUTH0_CLIENT_SECRET=your-client-secret
   AUTH0_AUDIENCE=your-api-identifier
   AUTH0_ALLOWED_EMAIL=your.email@example.com
   ```

## 🚀 Development

1. **Run migrations**
   ```bash
   poetry run python manage.py migrate
   ```

2. **Run development server**
   ```bash
   poetry run python manage.py runserver
   ```

## 🐳 Docker

The application is dockerized with:
- Django web application
- External MongoDB connection
- Environment configuration via .env

To run with Docker:
```bash
docker-compose up --build
```

## 🔒 Security

- Auth0 authentication with JWT tokens
- Email restriction for access control
- Secure API endpoints with token verification
- MongoDB authentication
- Environment variable protection

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
