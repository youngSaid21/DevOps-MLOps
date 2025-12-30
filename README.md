# Projet de Scoring de Crédit

Projet complet de machine learning pour la prédiction du remboursement de crédit, incluant l'entraînement d'un modèle XGBoost, une API REST Flask, la containerisation Docker, et le déploiement automatique sur AWS EC2 avec CI/CD.

## 📋 Description

Ce projet vise à prédire la probabilité de remboursement d'un prêt en utilisant des techniques de machine learning. Il comprend :

- **Analyse et préparation des données** : Exploration et preprocessing des données de crédit
- **Entraînement du modèle** : Développement d'un modèle XGBoost pour la classification
- **API REST** : Service web Flask pour exposer le modèle en production
- **Containerisation** : Déploiement avec Docker
- **Tests** : Suite de tests unitaires pour l'API
- **CI/CD** : Intégration continue avec GitHub Actions
- **Déploiement automatique** : Déploiement automatique sur AWS EC2 à chaque push

## 🏗️ Structure du projet

```
DevOps-MLOps/
├── api/                          # Application Flask
│   ├── app.py                    # Application Flask principale
│   └── model_loader.py           # Chargement du modèle XGBoost
├── data/                         # Données brutes
│   └── data.csv                  # Dataset de crédit
├── model/                        # Modèles entraînés
│   └── xgboost_credit_scoring_final.json
├── notebooks/                    # Notebooks d'analyse et d'entraînement
│   └── model_train.ipynb         # Notebook d'entraînement du modèle
├── docker/                       # Configuration Docker
│   └── Dockerfile
├── tests/                        # Tests unitaires
│   └── test_api.py
├── .github/                      # Configuration GitHub Actions
│   └── workflows/
│       ├── ci.yml                # Workflow CI (tests)
│       └── deploy.yml             # Workflow CD (déploiement)
├── docs/                         # Documentation et captures d'écran
├── deploy.sh                     # Script de déploiement pour EC2
├── requirements.txt              # Dépendances Python
└── README.md
```

## 🔧 Prérequis

- Python 3.11+
- Jupyter Notebook (pour l'exploration et l'entraînement)
- Docker (pour la containerisation)
- Compte AWS avec instance EC2 (pour le déploiement)
- Compte GitHub (pour CI/CD)

## 🚀 Installation

1. **Cloner le projet**

2. **Créer un environnement virtuel** :
```bash
python -m venv env
source env/bin/activate  # Sur Windows: env\Scripts\activate
```

3. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

## 📊 Données

Le dataset contient des informations sur les prêts avec les variables suivantes :

- **Variables numériques** : `annual_income`, `debt_to_income_ratio`, `credit_score`, `loan_amount`, `interest_rate`
- **Variables catégorielles** : `gender`, `marital_status`, `education_level`, `employment_status`, `loan_purpose`, `grade_subgrade`
- **Variable cible** : `loan_paid_back` (1 = remboursé, 0 = non remboursé)

Les données sont stockées dans `data/data.csv`.

## 🎓 Entraînement du modèle

### Préprocessing

Le notebook `notebooks/model_train.ipynb` contient :

1. **Exploration des données** : Analyse descriptive et visualisations
2. **Encodage des variables catégorielles** :
   - Encodage ordinal pour `education_level` et `grade_subgrade`
   - Encodage one-hot pour `gender`, `marital_status`, `employment_status`, `loan_purpose`
3. **Normalisation** : Standardisation des variables numériques avec `StandardScaler`
4. **Division train/test** : Séparation des données (90% train, 10% test)

### Modèle

- **Algorithme** : XGBoost Classifier
- **Features** : 23 features après preprocessing
- **Format de sauvegarde** : JSON

### Exécuter l'entraînement

```bash
# Ouvrir le notebook Jupyter
jupyter notebook notebooks/model_train.ipynb
```

Le modèle entraîné est sauvegardé dans `model/xgboost_credit_scoring_final.json`.

## 💻 Utilisation de l'API

### Lancer l'API localement

```bash
cd api
python app.py
```

L'API sera accessible sur `http://localhost:5000`

### Utilisation avec Docker

1. **Construire l'image** :
```bash
docker build -f docker/Dockerfile -t credit-scoring-api .
```

2. **Lancer le conteneur** :
```bash
docker run -p 5000:5000 credit-scoring-api
```

3. **Lancer en arrière-plan** :
```bash
docker run -d -p 5000:5000 --name credit-api credit-scoring-api
```

## 📡 Endpoints API

### `GET /health`
Vérifie le statut de l'API et du modèle.

**Réponse :**
```json
{
  "status": "online",
  "model": "XGBoost_v1"
}
```

### `POST /predict`
Effectue une prédiction de remboursement.

**Corps de la requête (JSON)** - 23 features requises :
```json
{
  "annual_income": 0.5,
  "debt_to_income_ratio": -0.3,
  "credit_score": 0.8,
  "loan_amount": -0.2,
  "interest_rate": 0.1,
  "education_level_ord": 1,
  "grade_subgrade_le": 10,
  "gender_Male": 0.0,
  "gender_Other": 0.0,
  "marital_status_Married": 1.0,
  "marital_status_Single": 0.0,
  "marital_status_Widowed": 0.0,
  "employment_status_Retired": 0.0,
  "employment_status_Self-employed": 0.0,
  "employment_status_Student": 0.0,
  "employment_status_Unemployed": 0.0,
  "loan_purpose_Car": 0.0,
  "loan_purpose_Debt consolidation": 0.0,
  "loan_purpose_Education": 0.0,
  "loan_purpose_Home": 1.0,
  "loan_purpose_Medical": 0.0,
  "loan_purpose_Other": 0.0,
  "loan_purpose_Vacation": 0.0
}
```

**Réponse :**
```json
{
  "status": "success",
  "probability_of_repayment": 0.8542,
  "decision": "Approved",
  "class_id": 1
}
```

**Exemple avec curl (local)** :
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "annual_income": 0.5,
    "debt_to_income_ratio": -0.3,
    "credit_score": 0.8,
    "loan_amount": -0.2,
    "interest_rate": 0.1,
    "education_level_ord": 1,
    "grade_subgrade_le": 10,
    "gender_Male": 0.0,
    "gender_Other": 0.0,
    "marital_status_Married": 1.0,
    "marital_status_Single": 0.0,
    "marital_status_Widowed": 0.0,
    "employment_status_Retired": 0.0,
    "employment_status_Self-employed": 0.0,
    "employment_status_Student": 0.0,
    "employment_status_Unemployed": 0.0,
    "loan_purpose_Car": 0.0,
    "loan_purpose_Debt consolidation": 0.0,
    "loan_purpose_Education": 0.0,
    "loan_purpose_Home": 1.0,
    "loan_purpose_Medical": 0.0,
    "loan_purpose_Other": 0.0,
    "loan_purpose_Vacation": 0.0
  }'
```

**Exemple avec curl (API déployée sur EC2)** :
```bash
curl -X POST http://[VOTRE_IP_EC2]:5000/predict \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## 🧪 Tests

Exécuter les tests unitaires de l'API :

```bash
python -m unittest tests.test_api -v
```

Les tests couvrent :
- Endpoint `/health`
- Endpoint `/predict` avec données valides
- Gestion des erreurs (données manquantes, JSON invalide)
- Validation des méthodes HTTP

## 📦 Dépendances principales

- **Flask 3.1.2** : Framework web
- **XGBoost 3.1.2** : Modèle de machine learning
- **pandas 2.3.3** : Manipulation de données
- **scikit-learn 1.8.0** : Preprocessing et outils ML
- **numpy 2.4.0** : Calculs numériques
- **scipy 1.16.3** : Outils scientifiques

## 🚀 CI/CD et Déploiement Automatique

### GitHub Actions Workflows

Le projet utilise GitHub Actions pour l'intégration et le déploiement continus :

#### Workflow CI (`.github/workflows/ci.yml`)
- **Déclenchement** : À chaque push/PR sur `main`, `master`, ou `develop`
- **Tests** : Exécution des tests unitaires sur Python 3.11
- **Build Docker** : Vérification que l'image Docker se construit correctement
- **Linting** : Vérification du style de code (Black, isort, flake8)

#### Workflow CD (`.github/workflows/deploy.yml`)
- **Déclenchement** : Après succès du workflow CI sur `main` ou `master`
- **Déploiement** : Connexion SSH à EC2 et déploiement automatique
- **Processus** :
  1. Pull du code depuis GitHub
  2. Rebuild de l'image Docker
  3. Redémarrage du conteneur
  4. Vérification que l'API fonctionne

### Configuration du Déploiement Automatique

Pour activer le déploiement automatique, configurez les secrets GitHub :

1. **Allez dans** : Repository → Settings → Secrets and variables → Actions
2. **Ajoutez ces secrets** :
   - `EC2_HOST` : L'IP publique de votre instance EC2
   - `EC2_USER` : L'utilisateur SSH (généralement `ubuntu`)
   - `EC2_SSH_KEY` : Le contenu complet de votre clé SSH `.pem`

### Déploiement Manuel sur EC2

Si vous préférez déployer manuellement :

```bash
# 1. Se connecter à EC2
ssh -i my_key.pem ubuntu@[VOTRE_IP_EC2]

# 2. Aller dans le projet
cd ~/DevOps-MLOps

# 3. Pull le code
git pull origin main

# 4. Exécuter le script de déploiement
chmod +x deploy.sh
./deploy.sh
```

### Déploiement avec Docker sur EC2

```bash
# Sur l'instance EC2
cd ~/DevOps-MLOps

# Construire l'image
docker build -f docker/Dockerfile -t credit-scoring-api .

# Lancer le conteneur
docker run -d -p 5000:5000 --name credit-api --restart unless-stopped credit-scoring-api

# Vérifier les logs
docker logs credit-api

# Tester l'API
curl http://localhost:5000/health
```

### Accès à l'API Déployée

Une fois déployée, l'API est accessible sur :
```
http://[VOTRE_IP_EC2]:5000
```

**Important** : Assurez-vous que le Security Group EC2 autorise le trafic sur le port 5000.

## 🔍 Workflow complet

1. **Exploration** : Analyser les données dans `notebooks/model_train.ipynb`
2. **Preprocessing** : Préparer les données (encodage, normalisation)
3. **Entraînement** : Entraîner le modèle XGBoost
4. **Sauvegarde** : Sauvegarder le modèle dans `model/`
5. **API** : Exposer le modèle via l'API Flask
6. **Tests** : Valider le fonctionnement avec les tests unitaires
7. **CI/CD** : Tests automatiques avec GitHub Actions
8. **Déploiement** : Déploiement automatique sur EC2 à chaque push

## 📝 Notes importantes

- Le modèle attend **23 features pré-traitées** (normalisées et encodées)
- Les données doivent être au format JSON avec **toutes les colonnes requises**
- Le modèle est chargé au démarrage de l'API
- Les variables numériques doivent être normalisées (StandardScaler)
- Les variables catégorielles doivent être encodées (one-hot avec drop='first')

## 📚 Documentation

Des captures d'écran et de la documentation supplémentaire sont disponibles dans le dossier `docs/`.

## 🔐 Sécurité

- Les clés SSH et les informations sensibles sont stockées dans les secrets GitHub
- Le fichier `.gitignore` exclut les fichiers sensibles (`my_key.pem`, `.env`, etc.)
- Les adresses IP publiques doivent être masquées dans les captures d'écran et la documentation

## 📊 Architecture de Déploiement

```
┌─────────────┐
│   GitHub    │
│  Repository │
└──────┬──────┘
       │ Push
       ▼
┌─────────────┐
│ GitHub      │
│ Actions CI  │ ──► Tests, Build Docker
└──────┬──────┘
       │ Success
       ▼
┌─────────────┐
│ GitHub      │
│ Actions CD  │ ──► SSH to EC2
└──────┬──────┘
       │ Deploy
       ▼
┌─────────────┐
│   AWS EC2   │
│  Instance   │
│  ┌────────┐ │
│  │ Docker │ │ ──► API Flask
│  │Container│ │
│  └────────┘ │
└─────────────┘
       │
       ▼
  http://[IP]:5000
```

## 🛠️ Technologies Utilisées

- **Machine Learning** : XGBoost, scikit-learn, pandas
- **API** : Flask
- **Containerisation** : Docker
- **CI/CD** : GitHub Actions
- **Cloud** : AWS EC2
- **Version Control** : Git, GitHub