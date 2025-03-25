# Valorant Stats Dashboard

Personal Valorant statistics dashboard with MongoDB and Django. Features Google SSO authentication and HenrikDev API integration.

## 🚀 Features

- Personal statistics dashboard for Valorant
- Google SSO authentication (restricted to specific email)
- Match history tracking
- Performance statistics
- API caching system
- Dockerized deployment

## 🛠️ Tech Stack

- **Backend**: Django + Django Ninja Extra
- **Database**: MongoDB
- **Authentication**: Google OAuth via django-allauth
- **Package Management**: Poetry
- **Containerization**: Docker & Docker Compose
- **API Integration**: HenrikDev Valorant API

## 📋 Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Poetry for dependency management
- Google OAuth credentials
- HenrikDev API key

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

1. **Google OAuth Setup**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Add authorized redirect URIs:
     - `http://localhost:8000/accounts/google/login/callback/`
   - Copy Client ID and Secret to `.env`

2. **HenrikDev API**
   - Get your API key from [HenrikDev](https://henrikdev.xyz)
   - Add it to `.env`

3. **Environment Variables**
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   MONGODB_URL=mongodb://mongodb:27017/
   DB_NAME=valorant_stats
   
   HENRIK_API_KEY=your-henrik-api-key
   
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   GOOGLE_ALLOWED_EMAIL=your.email@gmail.com
   ```

## 🚀 Development

1. **Run migrations**
   ```bash
   poetry run python manage.py migrate
   ```

2. **Create superuser**
   ```bash
   poetry run python manage.py createsuperuser
   ```

3. **Run development server**
   ```bash
   poetry run python manage.py runserver
   ```

## 🐳 Docker

The application is fully dockerized with two services:
- `web`: Django application
- `mongodb`: MongoDB database

To run with Docker:
```bash
docker-compose up --build
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
