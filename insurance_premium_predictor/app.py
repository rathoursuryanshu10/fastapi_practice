from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import userInput
from schema.prediction_response import PredictionResponse
from model.predict import model,MODEL_VERSION,predict_output

app = FastAPI()

@app.get('/')
def home():
    return {'message':'This is an Insurance premium category prediction API.'}

@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

@app.post('/predict',response_model=PredictionResponse)
def predict(data:userInput):
    user_input = {
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'occupation':data.occupation,
        'city_tier':data.city_tier,
        'bmi' : data.bmi,
        'income_lpa' :data.income_lpa
    }
    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200,content={'response':prediction})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))