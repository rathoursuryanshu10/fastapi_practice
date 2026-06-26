import joblib
import pandas as pd

# Load the model
model = joblib.load("model/model.joblib")
#Ml Flow
MODEL_VERSION = '1.0.0'

class_labels = model.classes_.tolist()

def predict_output(user_input:dict):
    df = pd.DataFrame([user_input])
    predicted_class = model.predict(df)[0]

    #get the probabalities of all classes 
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    #creating the mapping: {class_name: probabilities}
    class_prob = dict(zip(class_labels,map(lambda p:round(p,4),probabilities)))

    
    return {
        "predicted_category" : predicted_class,
        "confidence": round(confidence,4),
        "class_probabilities" : class_prob
    }