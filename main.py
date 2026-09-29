from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from features import extract_features_59

import numpy as np
import pickle
from pydantic import BaseModel
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from urllib.parse import urlparse

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# STATIC FILES
app.mount("/static", StaticFiles(directory="."), name="static")

# LOAD MODEL
model = load_model("models/malicious_cnn_model_v2.keras")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

max_len = 100
feature_size = 59


class URLRequest(BaseModel):
    url: str


#  Extract domain properly
def extract_domain(url):
    domain = urlparse(url).netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


#  Trusted domains
trusted_domains = {
    "google.com",
    "facebook.com",
    "youtube.com",
    "amazon.com",
    "github.com",
    "chatgpt.com"
}


#  Final decision logic (SAFE + WORKING)
def final_prediction(url, model_prob):
    domain = extract_domain(url)

    is_trusted = any(domain == d or domain.endswith("." + d) for d in trusted_domains)

    #  TRUSTED DOMAIN FIRST (absolute priority)
    if is_trusted:
        return "Safe"

    #  High confidence malicious
    if model_prob > 0.98:
        return "Malicious"

    # Normal threshold
    if model_prob > 0.3:
        return "Malicious"
    else:
        return "Safe"

@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/predict")
def predict(request: URLRequest):
    url = request.url

    try:
        #  Text processing
        seq = tokenizer.texts_to_sequences([url])
        seq = pad_sequences(seq, maxlen=max_len, padding='post')
        seq = seq.astype(np.int32)

       #  Engineered features (REAL 59 features)
        raw_features = extract_features_59(url)

        features = np.array(raw_features, dtype=np.float32).reshape(1, -1)

        print("Feature vector length:", len(raw_features))
        #  Model prediction
        pred = model.predict([seq, features])[0][0]

        print("Model probability:", pred)

        #  Final calibrated decision
        result = final_prediction(url, pred)

        return {
            "url": url,
            "malicious_probability": float(pred),
            "prediction": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }