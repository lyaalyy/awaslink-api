import os
import re
import numpy as np
import joblib
import tensorflow as tf
import scipy.sparse as sp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from urllib.parse import urlparse
import ipaddress

app = FastAPI(title="AwasLink AI Inference Server")

# Load model dan komponen pendukung
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = tf.keras.models.load_model(os.path.join(BASE_DIR, "model_phishing.keras"))
tfidf = joblib.load(os.path.join(BASE_DIR, "tfidf_vectorizer.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler_manual_features.pkl"))

class MessageInput(BaseModel):
    message: str

def extract_features(text):
    text = str(text) if text else ""
    url_pattern = r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.(?:com|net|org|id|co\.id|my\.id|ac\.id|go\.id|info|biz)\b'
    urls = re.findall(url_pattern, text, re.IGNORECASE)
    
    # --- PERBAIKAN: Memastikan url benar-benar berbentuk String tunggal ---
    url = str(urls) if urls else ""
            
    # Text Features
    pjg_pesan = len(text)
    jml_kata = len(text.split())
    ada_url = 1 if url else 0
    jml_url = len(urls)
    angka_telp = 1 if re.search(r'(\+62|08)\d{8,13}', text) else 0
    mendesak = 1 if re.search(r'\b(segera|sekarang|expired|kadaluarsa|urgent|darurat|deadline|hari ini|terakhir|berakhir)\b', text, re.IGNORECASE) else 0
    hadiah = 1 if re.search(r'\b(menang|pemenang|hadiah|reward|bonus|gratis|cashback|voucher|promo|diskon|free|lucky)\b', text, re.IGNORECASE) else 0
    sensitif = 1 if re.search(r'\b(otp|pin|password|kata sandi|verifikasi|rekening|cvv|username|login|akun|account)\b', text, re.IGNORECASE) else 0
    brand = 1 if re.search(r'\b(bca|bri|bni|mandiri|cimb|dana|ovo|gopay|shopee|tokopedia|lazada|grab|gojek|pln|bpjs|telkom|indosat)\b', text, re.IGNORECASE) else 0
    jml_seru = text.count('!')
    jml_angka = sum(c.isdigit() for c in text)
    jml_kapital = sum(c.isupper() for c in text)
    
    huruf_saja = [c for c in text if c.isalpha()]
    rasio_kapital = jml_kapital / len(huruf_saja) if len(huruf_saja) > 0 else 0
    simbol = 1 if re.search(r'[\U0001F300-\U0001F9FF★✓✔☎]', text) else 0
    
    # URL Features
    pjg_url = len(url)
    url_https = 1 if url.startswith('https://') else 0
    jml_titik = url.count('.')
    jml_strip = url.count('-')
    
    jml_subdomain = 0
    if url:
        try:
            domain = urlparse('http://' + url if not url.startswith('http') else url).netloc.lower().replace('www.', '')
            jml_subdomain = max(0, domain.count('.') - 1)
        except: pass
        
    url_singkat = 1 if any(s in url for s in ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 's.id', 'rb.gy']) else 0
    domain_indo = 1 if any(tld in url for tld in ['.co.id', '.my.id', '.ac.id', '.go.id', '.or.id', '.sch.id', '.web.id']) else 0
    
    ip_di_url = 0
    if url:
        try:
            # Perbaikan: mengambil elemen pertama setelah split agar tidak error list
            domain_ip = url.split('//')[-1].split('/').split(':')
            ipaddress.ip_address(domain_ip)
            ip_di_url = 1
        except: pass

    return np.array([[pjg_pesan, jml_kata, ada_url, jml_url, angka_telp, mendesak, hadiah, sensitif, brand, jml_seru, jml_angka, jml_kapital, rasio_kapital, simbol, pjg_url, url_https, jml_titik, jml_strip, jml_subdomain, url_singkat, domain_indo, ip_di_url]])
   

@app.get("/")
async def root():
    return {
        "message": "AwasLink API is Running! ", 
        "instruction": "Silakan tambahkan /docs pada URL di atas untuk membuka halaman pengujian (Swagger UI)."
    }

@app.post("/predict")
async def predict(input_data: MessageInput):
    teks_asli = input_data.message
    teks_lower = teks_asli.lower()

    # Jika pesan kurang dari 25 karakter dan tidak mengandung link/domain
    if len(teks_asli) < 25 and "http" not in teks_lower and "www" not in teks_lower and ".com" not in teks_lower and ".id" not in teks_lower:
        return {
            "verdict": "Aman",
            "confidence": 0.0,
            "message": teks_asli
        }
    # ================================================================

    # 1. Ekstrak dan Scale 22 Fitur Manual
    manual_feats = extract_features(teks_asli)
    manual_feats_scaled = scaler.transform(manual_feats)
    
    # 2. Ekstrak 1.000 Fitur TF-IDF
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', teks_lower)
    tfidf_feats = tfidf.transform([clean_text])
    
    # 3. Gabungkan Fitur (Total 1.022 fitur)
    full_features = sp.hstack([manual_feats_scaled, tfidf_feats]).toarray()
    
    # 4. Prediksi AI
    prediction_array = model.predict(full_features)
    prediction_value = float(prediction_array.item())
    
    verdict = "Phishing/Scam" if prediction_value > 0.5 else "Aman"
    
    return {
        "verdict": verdict,
        "confidence": round(prediction_value * 100, 2),
        "message": teks_asli
    }