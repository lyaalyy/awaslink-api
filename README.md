# AwasLink AI Inference API 

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15+-FF6F00.svg?logo=tensorflow)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**AwasLink AI** adalah "otak" kecerdasan buatan di balik ekosistem AwasLink. Server API ini dirancang khusus untuk mendeteksi ancaman *phishing*, *scam*, dan URL berbahaya pada pesan teks (SMS/WhatsApp) berbahasa Indonesia. 

Sistem ini tidak hanya mengandalkan *Machine Learning* biasa, tetapi menggunakan pendekatan **Hybrid** yang menggabungkan ekstraksi fitur manual (pola teks) dengan *Deep Learning* tingkat lanjut untuk memberikan hasil prediksi yang akurat, cepat, dan andal.

## Fitur Unggulan

- **Hybrid Feature Engineering:** Menggabungkan 22 fitur ekstraksi manual (seperti deteksi panjang URL, penggunaan simbol, dan kata kunci desakan) dengan 1.000 fitur teks hasil vektorisasi TF-IDF.
- **Zero-Latency Heuristics (Logika Cerdas):** Memiliki aturan logika darurat (*Quick Patch*) yang mampu mengenali obrolan santai sehari-hari secara instan, menghemat beban komputasi AI dengan mengembalikan status aman dalam hitungan milidetik.
- **Sistem Keputusan Biner:** Mengklasifikasikan pesan secara tegas ke dalam kategori `Aman` atau `Phishing/Scam`, sehingga sangat mudah diintegrasikan oleh tim *Frontend* ke dalam UI/UX aplikasi.
- **RESTful API Modern:** Dibangun menggunakan FastAPI untuk menangani *request* secara asinkron dengan performa tinggi.
- **Dokumentasi Otomatis:** Dilengkapi dengan Swagger UI untuk pengujian API secara langsung dari *browser*.

## Teknologi yang Digunakan

- **Framework:** FastAPI, Uvicorn
- **Machine Learning:** TensorFlow / Keras, Scikit-Learn
- **Pemrosesan Data:** NumPy, SciPy, Pandas
- **Deployment:** Hugging Face Spaces / Docker

---

## Dokumentasi API

### 1. Endpoint Utama: Deteksi Pesan
Endpoint ini menerima teks dari pengguna dan mengembalikan nilai probabilitas ancaman siber.

- **URL:** `/predict`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`

**Contoh Request (JSON):**
```json
{
  "message": "Selamat nomor anda memenangkan hadiah 100jt, klik link ini bit.ly/penipuan"
}

Logika Ambang Batas (Threshold)
API ini menggunakan aturan ambang batas biner berikut untuk menentukan status pesan berdasarkan persentase confidence (probabilitas bahaya):
-> 0.00 - 0.50 (0% - 50%): Aman (Teks bersih dari ancaman)
-> 0.51 - 1.00 (51% - 100%): Phishing/Scam (Teks terindikasi berbahaya)

Tim Pengembang
Dikembangkan dengan penuh dedikasi oleh Tim Proyek AwasLink Capstone Project CC26-PSU004
1. Project Manager & AI Engineer: Alya Yuliandhita P.M
2. Frontend Developer   : Gilang Dafa A.
3. Backend Developer    : Mahesa Rahmat R.
4. AI Engineer          : Anatasya Putri Amalia N.
5. Data Sciencentist    : Ashma Nisa S. A., Hana Talitha s.
