import xgboost as xgb
import os

class ModelLoader:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = self.load_model()

    def load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Le fichier {self.model_path} est introuvable.")
        
        # Initialisation et chargement du format JSON
        # Create XGBClassifier instance
        model = xgb.XGBClassifier()
        
        # Set _estimator_type BEFORE calling load_model() 
        # because load_model() internally calls _get_type() which requires this attribute
        # We set it unconditionally to ensure it exists before load_model() checks for it
        model._estimator_type = "classifier"
        
        # Load the model from file
        model.load_model(self.model_path)
        
        print(f"Modèle chargé avec succès depuis {self.model_path}")
        return model

    def predict(self, data_df):
        """Prend un DataFrame en entrée et retourne la probabilité et la classe."""
        # Calcul de la probabilité de remboursement (classe 1)
        probability = self.model.predict_proba(data_df)[:, 1]
        prediction = self.model.predict(data_df)
        return probability[0], int(prediction[0])