#!/bin/bash
# Script de déploiement pour EC2
# Ce script sera utilisé par GitHub Actions

set -e

echo "Début du déploiement..."

# Aller dans le répertoire du projet
cd ~/DevOps-MLOps || { echo "Répertoire non trouvé"; exit 1; }

# Pull les dernières modifications
echo "Récupération du code..."
git fetch origin
git reset --hard origin/main || git reset --hard origin/master

# Arrêter et supprimer l'ancien conteneur
echo "Arrêt de l'ancien conteneur..."
docker stop credit-api 2>/dev/null || true
docker rm credit-api 2>/dev/null || true

# Nettoyer les anciennes images (optionnel, pour économiser l'espace)
echo "Nettoyage des anciennes images..."
docker image prune -f || true

# Construire la nouvelle image Docker
echo "Construction de l'image Docker..."
docker build -f docker/Dockerfile -t credit-scoring-api .

# Lancer le nouveau conteneur
echo "Lancement du nouveau conteneur..."
docker run -d -p 5000:5000 --name credit-api --restart unless-stopped credit-scoring-api

# Attendre le démarrage
echo "Attente du démarrage..."
sleep 5

# Vérifier que l'API fonctionne
echo "Vérification de l'API..."
MAX_RETRIES=5
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "API démarrée avec succès!"
    docker logs --tail 20 credit-api
    exit 0
  fi
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "Tentative $RETRY_COUNT/$MAX_RETRIES..."
  sleep 3
done

echo "Erreur: L'API ne répond pas après $MAX_RETRIES tentatives"
docker logs credit-api
exit 1

