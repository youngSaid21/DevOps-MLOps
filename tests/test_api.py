"""
Tests pour l'API de scoring de crédit.
"""
import sys
import os
import unittest
import json

# Ajouter le dossier api au path pour pouvoir importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from flask import Flask
from app import app


class TestAPI(unittest.TestCase):
    """Classe de tests pour l'API Flask."""
    
    def setUp(self):
        """Configuration avant chaque test."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_endpoint(self):
        """Test de l'endpoint /health."""
        response = self.client.get('/health')
        
        # Vérifier le code de statut
        self.assertEqual(response.status_code, 200)
        
        # Vérifier le format JSON
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('model', data)
        self.assertEqual(data['status'], 'online')
        self.assertEqual(data['model'], 'XGBoost_v1')
    
    def test_predict_endpoint_success(self):
        """Test de l'endpoint /predict avec des données valides."""
        # Données de test avec les 23 features attendues par le modèle
        # (après preprocessing: normalisation et encodage one-hot)
        # Note: avec drop='first', la première catégorie est supprimée
        test_data = {
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
        
        response = self.client.post(
            '/predict',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        # Vérifier le code de statut
        self.assertEqual(response.status_code, 200)
        
        # Vérifier le format JSON
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('probability_of_repayment', data)
        self.assertIn('decision', data)
        self.assertIn('class_id', data)
        
        # Vérifier les types de données
        self.assertIsInstance(data['probability_of_repayment'], (int, float))
        self.assertIn(data['decision'], ['Approved', 'Rejected'])
        self.assertIn(data['class_id'], [0, 1])
        
        # Vérifier que la probabilité est entre 0 et 1
        self.assertGreaterEqual(data['probability_of_repayment'], 0.0)
        self.assertLessEqual(data['probability_of_repayment'], 1.0)
    
    def test_predict_endpoint_missing_data(self):
        """Test de l'endpoint /predict avec des données manquantes."""
        # Données incomplètes
        test_data = {
            "annual_income": 0.5,
            "credit_score": 0.8
        }
        
        response = self.client.post(
            '/predict',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        # Devrait retourner une erreur
        self.assertEqual(response.status_code, 400)
        
        # Vérifier le format JSON d'erreur
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)
    
    def test_predict_endpoint_invalid_json(self):
        """Test de l'endpoint /predict avec un JSON invalide."""
        response = self.client.post(
            '/predict',
            data='invalid json',
            content_type='application/json'
        )
        
        # Devrait retourner une erreur
        self.assertEqual(response.status_code, 400)
    
    def test_predict_endpoint_wrong_method(self):
        """Test de l'endpoint /predict avec une méthode HTTP incorrecte."""
        response = self.client.get('/predict')
        
        # Devrait retourner 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)
    
    def test_health_endpoint_wrong_method(self):
        """Test de l'endpoint /health avec une méthode HTTP incorrecte."""
        response = self.client.post('/health')
        
        # Devrait retourner 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)
    
    def test_predict_response_structure(self):
        """Test que la structure de la réponse de /predict est correcte."""
        test_data = {
            "annual_income": 0.0,
            "debt_to_income_ratio": 0.0,
            "credit_score": 0.0,
            "loan_amount": 0.0,
            "interest_rate": 0.0,
            "education_level_ord": 0,
            "grade_subgrade_le": 0,
            "gender_Male": 0.0,
            "gender_Other": 0.0,
            "marital_status_Married": 0.0,
            "marital_status_Single": 0.0,
            "marital_status_Widowed": 0.0,
            "employment_status_Retired": 0.0,
            "employment_status_Self-employed": 0.0,
            "employment_status_Student": 0.0,
            "employment_status_Unemployed": 0.0,
            "loan_purpose_Car": 0.0,
            "loan_purpose_Debt consolidation": 0.0,
            "loan_purpose_Education": 0.0,
            "loan_purpose_Home": 0.0,
            "loan_purpose_Medical": 0.0,
            "loan_purpose_Other": 0.0,
            "loan_purpose_Vacation": 0.0
        }
        
        response = self.client.post(
            '/predict',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.data)
            
            # Vérifier toutes les clés requises
            required_keys = ['status', 'probability_of_repayment', 'decision', 'class_id']
            for key in required_keys:
                self.assertIn(key, data, f"La clé '{key}' est manquante dans la réponse")
            
            # Vérifier la cohérence entre decision et class_id
            if data['class_id'] == 1:
                self.assertEqual(data['decision'], 'Approved')
            else:
                self.assertEqual(data['decision'], 'Rejected')


if __name__ == '__main__':
    # Lancer les tests
    unittest.main(verbosity=2)

