# Utiliser une image Python officielle
FROM python:3.9-slim

# Définir les variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    VIRTUAL_ENV=/app/.venv

# Ajouter Poetry et l'environnement virtuel au PATH
ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

# Installer les dépendances système nécessaires
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        python3-dev \
        libffi-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

# Installer Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement les fichiers de dépendances
COPY pyproject.toml ./

# Installer les dépendances et créer l'environnement virtuel
RUN python -m venv $VIRTUAL_ENV && \
    . $VIRTUAL_ENV/bin/activate && \
    poetry install --only main --no-root

# Copier le reste du code
COPY . .

# Exposer le port
EXPOSE 8007

# Commande par défaut
CMD ["python", "manage.py", "runserver", "0.0.0.0:8007"]
