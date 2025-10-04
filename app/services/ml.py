import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import asyncio
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
MODELS_DIR = os.path.join(BASE_DIR, "..", "models") 



def train_and_save_models(latitude, longitude, date):
    url = "https://power.larc.nasa.gov/api/temporal/hourly/point"


    params = {
        "parameters": "T2M,PRECTOTCORR,WS2M",
        "start": "20140101",    
        "end": "20241231",       
        "latitude": latitude,
        "longitude": longitude,
        "community": "AG",
        "time-standard": "UTC",  
        "format": "JSON"
    }


    response = requests.get(url, params=params)
    data = response.json()


    t2m = data["properties"]["parameter"]["T2M"] 
    prectot = data["properties"]["parameter"]["PRECTOTCORR"]
    ws2m = data["properties"]["parameter"]["WS2M"]

    Keys = pd.Series(t2m.keys())

    df = pd.DataFrame({
        "date": pd.to_datetime(Keys.str[:8], format="%Y%m%d"),
        "hora": pd.to_datetime(Keys.str[8:], format="%H").dt.hour,
        "temperature_C": list(t2m.values()),
        "precipitation_mm": list(prectot.values()),
        "wind_speed_m/s": list(ws2m.values()),
        "lat": latitude,
        "lon": longitude
    })


    df["dia_ano"] = df["date"].dt.dayofyear


    X = df[["lat", "lon", "hora", "dia_ano"]]
    y_temp = df["temperature_C"]
    y_prec = df["precipitation_mm"]
    y_vento = df["wind_speed_m/s"]

    X_train, X_test, y_train_temp, y_test_temp = train_test_split(X, y_temp, test_size=0.2, random_state=42)
    _, _, y_train_prec, y_test_prec = train_test_split(X, y_prec, test_size=0.2, random_state=42)
    _, _, y_train_vento, y_test_vento = train_test_split(X, y_vento, test_size=0.2, random_state=42)

    
    modelo_temp = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_temp.fit(X_train, y_train_temp)

    modelo_prec = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_prec.fit(X_train, y_train_prec)

    modelo_vento = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_vento.fit(X_train, y_train_vento)


    joblib.dump(modelo_temp, os.path.join(MODELS_DIR, "modelo_temp.pkl"))
    joblib.dump(modelo_prec, os.path.join(MODELS_DIR, "modelo_prec.pkl"))
    joblib.dump(modelo_vento, os.path.join(MODELS_DIR, "modelo_vento.pkl"))

    print("Modelos treinados e salvos!")



async def predict_weather(latitude, longitude, day, month, year):
    
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)


    modelos = [
        os.path.join(MODELS_DIR, "modelo_temp.pkl"),
        os.path.join(MODELS_DIR, "modelo_prec.pkl"),
        os.path.join(MODELS_DIR, "modelo_vento.pkl"),
    ]
    if not all(os.path.exists(m) for m in modelos):
        train_and_save_models(latitude, longitude, f"{year}-{month:02d}-{day:02d}")

    modelo_temp = joblib.load(modelos[0])
    modelo_prec = joblib.load(modelos[1])
    modelo_vento = joblib.load(modelos[2])


    data = {}
    pred = []
    sumTemp = 0
    sumPrec = 0
    sumVento = 0

    for i in range(24):
        X_novo = pd.DataFrame([{
            "lat": latitude,
            "lon": longitude,
            "hora": i,
            "dia_ano": pd.to_datetime(f"{year}-{month}-{day}").day_of_year,
        }])

        y_pred_temp = modelo_temp.predict(X_novo)[0]
        sumTemp += y_pred_temp
        y_pred_prec = modelo_prec.predict(X_novo)[0]
        sumPrec += y_pred_prec
        y_pred_vento = modelo_vento.predict(X_novo)[0]
        sumVento += y_pred_vento
        pred.append({"hora": i, "temp": float(y_pred_temp), "prec": float(y_pred_prec), "vento": float(y_pred_vento), "timestamp": f"{year}-{month}-{day}T{i if i >= 10 else f'0{i}'}:00:00Z"})
    
    data["inputs"] =({"lat": latitude, "lon": longitude, "dia": day, "mes": month, "ano": year})
    data["previsoes"] =(pred)
    data["medias"] = ( {"temp": float(sumTemp/24), "prec": float(sumPrec/24), "vento": float(sumVento/24) })


    return data   




