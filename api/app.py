from flask import Flask, request, jsonify
import pandas as pd
from model_loader import ModelLoader

app = Flask(__name__)

# Initialisation globale du modèle au démarrage de l'API
# On suppose que le fichier est dans le même répertoire
predictor = ModelLoader("model/xgboost_credit_scoring_final.json")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Récupération des données JSON envoyées par l'utilisateur
        data = request.get_json()
        
        # 2. Conversion en DataFrame (XGBoost a besoin du nom des colonnes)
        # On s'attend à recevoir les 23 features scalées
        df_input = pd.DataFrame([data])
        
        # 3. Prédiction via notre loader
        prob, class_pred = predictor.predict(df_input)
        
        # 4. Retourner le résultat
        return jsonify({
            "status": "success",
            "probability_of_repayment": round(float(prob), 4),
            "decision": "Approved" if class_pred == 1 else "Rejected",
            "class_id": class_pred
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "online", "model": "XGBoost_v1"})

if __name__ == '__main__':
    # On lance l'API sur le port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)