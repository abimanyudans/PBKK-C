# 🚀 Quick Start - Knowledge Base System

## Instalasi Cepat

```bash
cd Credit-Card-Fraud-Detection-System
pip install flask numpy pandas scikit-learn xgboost
```

## Jalankan Aplikasi

```bash
python app.py
```

Buka browser: **http://localhost:5000/knowledge-base.html**

## Test dari Python

```bash
python test_kb_system.py
```

## File Penting

| File                            | Deskripsi                                                           |
| ------------------------------- | ------------------------------------------------------------------- |
| `knowledge_base.py`             | Engine KB (3 class: KB, RuleEngine, InferenceEngine)                |
| `fraud_rules.json`              | 10 aturan deteksi fraud                                             |
| `app.py`                        | Flask endpoints: `/predict_with_kb`, `/explain_kb`, `/get_kb_rules` |
| `templates/knowledge-base.html` | UI interaktif untuk testing                                         |
| `README_KB.md`                  | Dokumentasi lengkap                                                 |
| `test_kb_system.py`             | Test script 4 skenario                                              |

## Endpoint API

### 1. Prediksi dengan KB

```bash
POST /predict_with_kb
Body: {
  "features": [7200, -2.5, 4.5, ..., 3500],  # 30 nilai
  "model": "xgb"
}
```

### 2. Penjelasan Reasoning

```bash
POST /explain_kb
Body: {
  "kb_result": { ... }
}
```

### 3. Lihat Semua Aturan

```bash
GET /get_kb_rules
```

## Contoh Cepat

```python
from knowledge_base import create_fraud_detection_system

kb = create_fraud_detection_system()

features = {
    'Time': 7200,  # 2 AM
    'Amount': 3500,
    'V1': -2.5, 'V2': 4.5,
    # ... V3-V28
}

ml_pred = {
    'prediction': 1,
    'probability': 0.65,
    'accuracy': 0.99
}

result = kb.infer(features, ml_pred)
print(kb.explain(result))
```

## Fitur Utama

✅ **10 Aturan Bisnis** - Deteksi pola fraud spesifik  
✅ **Forward Chaining** - Inference engine untuk reasoning  
✅ **Explainability** - Setiap keputusan dapat dijelaskan  
✅ **Hybrid ML + KB** - Gabungan pattern recognition + logic  
✅ **Interactive UI** - Test langsung dari browser

## Dokumentasi Lengkap

Baca: `README_KB.md` untuk detail arsitektur, API, dan customization.

## Support

📧 hossain.stu2018@juniv.edu  
🌐 www.frauddetection.site

---

**Dibuat untuk Final Project Rekayasa Sistem Berbasis Pengetahuan**  
_Semester 5 - December 2025_
