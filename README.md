# Tip Predictor (Django + XGBoost)

## Run
    pip install -r requirements.txt
    python manage.py runserver
Open http://127.0.0.1:8000/

## Test
    python manage.py test

## How it works
- `ml_app/predictor.py` loads `ml_models/xgb_model.joblib` once and encodes inputs
  the same way the notebook's LabelEncoder did (alphabetical order).
- `POST /predict/` validates with `PredictionForm` and returns JSON.
- `static/ml_app/app.js` calls it live as the user changes inputs.