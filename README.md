# Projet de Scoring de Crédit

Projet complet de machine learning pour la prédiction du remboursement de crédit, incluant l'entraînement d'un modèle XGBoost, une API REST Flask, et la containerisation Docker.

## 📋 Description

Ce projet vise à prédire la probabilité de remboursement d'un prêt en utilisant des techniques de machine learning. Il comprend :

- **Analyse et préparation des données** : Exploration et preprocessing des données de crédit
- **Entraînement du modèle** : Développement d'un modèle XGBoost pour la classification
- **API REST** : Service web Flask pour exposer le modèle en production
- **Containerisation** : Déploiement avec Docker
- **Tests** : Suite de tests unitaires pour l'API

## 🏗️ Structure du projet

```
DevOps/
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
├── docs/                         # Documentation et captures d'écran
├── requirements.txt              # Dépendances Python
└── README.md
```

## 🔧 Prérequis

- Python 3.11+
- Jupyter Notebook (pour l'exploration et l'entraînement)
- Docker (optionnel, pour la containerisation)

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

**Exemple avec curl** :
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

## 🔍 Workflow complet

1. **Exploration** : Analyser les données dans `notebooks/model_train.ipynb`
2. **Preprocessing** : Préparer les données (encodage, normalisation)
3. **Entraînement** : Entraîner le modèle XGBoost
4. **Sauvegarde** : Sauvegarder le modèle dans `model/`
5. **API** : Exposer le modèle via l'API Flask
6. **Déploiement** : Containeriser avec Docker
7. **Tests** : Valider le fonctionnement avec les tests unitaires

## 📝 Notes importantes

- Le modèle attend **23 features pré-traitées** (normalisées et encodées)
- Les données doivent être au format JSON avec **toutes les colonnes requises**
- Le modèle est chargé au démarrage de l'API
- Les variables numériques doivent être normalisées (StandardScaler)
- Les variables catégorielles doivent être encodées (one-hot avec drop='first')

## 📚 Documentation

Des captures d'écran et de la documentation supplémentaire sont disponibles dans le dossier `docs/`.