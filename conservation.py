import joblib
import pandas as pd

mlb = joblib.load('models/mlb.pkl')
rf = joblib.load('models/rf_model.pkl')
scaler = joblib.load('models/scaler.pkl')

def checkConservation(Height, Weight, Lifespan, Speed, Gestation, Diet):
    features = ['Height', 'Weight', 'Lifespan', 'Average Speed', 'Gestation Period']
    numeric_data_point = pd.DataFrame([[Height, Weight, Lifespan, Speed, Gestation]], columns=features)
    diet_data_point = mlb.transform([Diet])
    diet_data_point = pd.DataFrame(diet_data_point, columns=mlb.classes_)
    new_data_point = pd.concat([numeric_data_point.reset_index(drop=True), diet_data_point.reset_index(drop=True)], axis=1)
    new_data_point = scaler.transform(new_data_point)
    status = rf.predict(new_data_point)
    return status
