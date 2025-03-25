# Utiliser une image Python officielle
FROM python:3.9-slim

# Définir les variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Ajouter Poetry au PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Installer les dépendances système
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installer Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de configuration
COPY pyproject.toml poetry.lock* ./

# Installer les dépendances
RUN poetry install --no-root --no-dev

# Copier le reste du code
COPY . .

# Exposer le port
EXPOSE 8000

# Commande par défaut
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
