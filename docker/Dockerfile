# Utiliser une image Python officielle comme image de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour XGBoost et autres bibliothèques
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt depuis la racine du projet
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le dossier model avec le modèle XGBoost
COPY model /app/model

# Copier les fichiers de l'application API
COPY api/app.py .
COPY api/model_loader.py .

# Exposer le port 5000
EXPOSE 5000

# Définir la variable d'environnement pour Flask
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Commande pour lancer l'application
CMD ["python", "app.py"]

