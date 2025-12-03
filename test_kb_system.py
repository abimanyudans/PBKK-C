"""
Test Script untuk Knowledge Base System
========================================
Demonstrasi cara menggunakan KB System untuk deteksi fraud
"""

import sys
import os

# Tambahkan path parent directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from knowledge_base import create_fraud_detection_system

def print_separator():
    print("\n" + "="*70 + "\n")

def test_case_1_suspicious():
    """
    Test Case 1: Transaksi Mencurigakan
    - Waktu: 2 AM (tengah malam)
    - Nominal: Rp 3500 (tinggi)
    - Beberapa fitur ekstrim
    """
    print("🧪 TEST CASE 1: TRANSAKSI MENCURIGAKAN")
    print_separator()
    
    kb_system = create_fraud_detection_system()
    
    # Simulasi transaksi mencurigakan
    features = {
        'Time': 7200,  # 2 AM (7200 detik = 2 jam)
        'Amount': 3500,
        'V1': -2.5, 'V2': 4.5, 'V3': -1.2, 'V4': 3.8,
        'V5': 0.5, 'V6': -0.8, 'V7': 1.2, 'V8': -2.1,
        'V9': 0.5, 'V10': 0.3, 'V11': -0.4, 'V12': 0.7,
        'V13': 0.2, 'V14': -0.9, 'V15': 0.4, 'V16': 0.6,
        'V17': -0.3, 'V18': 0.1, 'V19': 0.8, 'V20': -0.5,
        'V21': 0.2, 'V22': 0.4, 'V23': -0.6, 'V24': 0.3,
        'V25': 0.1, 'V26': -0.2, 'V27': 0.5, 'V28': 0.3
    }
    
    ml_prediction = {
        'prediction': 1,
        'probability': 0.65,
        'accuracy': 0.99
    }
    
    # Inferensi
    result = kb_system.infer(features, ml_prediction)
    
    # Tampilkan penjelasan
    explanation = kb_system.explain(result)
    print(explanation)
    
    return result

def test_case_2_legitimate():
    """
    Test Case 2: Transaksi Sah
    - Waktu: 12 PM (siang hari)
    - Nominal: Rp 50 (rendah)
    - Semua fitur normal
    """
    print("🧪 TEST CASE 2: TRANSAKSI SAH (LEGITIMATE)")
    print_separator()
    
    kb_system = create_fraud_detection_system()
    
    # Simulasi transaksi sah
    features = {
        'Time': 43200,  # 12 PM (43200 detik = 12 jam)
        'Amount': 50,
        'V1': 0.1, 'V2': -0.2, 'V3': 0.3, 'V4': -0.1,
        'V5': 0.2, 'V6': 0.1, 'V7': -0.15, 'V8': 0.05,
        'V9': 0.1, 'V10': -0.1, 'V11': 0.2, 'V12': -0.05,
        'V13': 0.1, 'V14': 0.15, 'V15': -0.1, 'V16': 0.2,
        'V17': 0.05, 'V18': -0.1, 'V19': 0.1, 'V20': 0.15,
        'V21': -0.05, 'V22': 0.1, 'V23': 0.2, 'V24': -0.1,
        'V25': 0.05, 'V26': 0.1, 'V27': -0.15, 'V28': 0.05
    }
    
    ml_prediction = {
        'prediction': 0,
        'probability': 0.15,
        'accuracy': 0.99
    }
    
    # Inferensi
    result = kb_system.infer(features, ml_prediction)
    
    # Tampilkan penjelasan
    explanation = kb_system.explain(result)
    print(explanation)
    
    return result

def test_case_3_micro_transaction():
    """
    Test Case 3: Micro Transaction (Test Kartu Curian)
    - Waktu: 3 AM
    - Nominal: Rp 0.5 (sangat kecil)
    - Probabilitas ML sedang
    """
    print("🧪 TEST CASE 3: MICRO TRANSACTION")
    print_separator()
    
    kb_system = create_fraud_detection_system()
    
    # Simulasi micro transaction
    features = {
        'Time': 10800,  # 3 AM
        'Amount': 0.5,
        'V1': -1.5, 'V2': 2.0, 'V3': -0.8, 'V4': 1.5,
        'V5': 0.3, 'V6': -0.5, 'V7': 0.8, 'V8': -1.2,
        'V9': 0.4, 'V10': 0.2, 'V11': -0.3, 'V12': 0.5,
        'V13': 0.1, 'V14': -0.6, 'V15': 0.3, 'V16': 0.4,
        'V17': -0.2, 'V18': 0.1, 'V19': 0.6, 'V20': -0.3,
        'V21': 0.1, 'V22': 0.3, 'V23': -0.4, 'V24': 0.2,
        'V25': 0.1, 'V26': -0.1, 'V27': 0.3, 'V28': 0.2
    }
    
    ml_prediction = {
        'prediction': 0,
        'probability': 0.45,
        'accuracy': 0.99
    }
    
    # Inferensi
    result = kb_system.infer(features, ml_prediction)
    
    # Tampilkan penjelasan
    explanation = kb_system.explain(result)
    print(explanation)
    
    return result

def test_case_4_extreme_amount():
    """
    Test Case 4: Nominal Ekstrim
    - Waktu: 10 AM (normal)
    - Nominal: Rp 8000 (sangat tinggi)
    - Probabilitas ML tinggi
    """
    print("🧪 TEST CASE 4: NOMINAL EKSTRIM")
    print_separator()
    
    kb_system = create_fraud_detection_system()
    
    # Simulasi nominal ekstrim
    features = {
        'Time': 36000,  # 10 AM
        'Amount': 8000,
        'V1': -3.0, 'V2': 5.5, 'V3': -2.0, 'V4': 4.0,
        'V5': 1.0, 'V6': -1.5, 'V7': 2.0, 'V8': -3.5,
        'V9': 1.0, 'V10': 0.5, 'V11': -0.8, 'V12': 1.2,
        'V13': 0.4, 'V14': -1.5, 'V15': 0.8, 'V16': 1.0,
        'V17': -0.5, 'V18': 0.3, 'V19': 1.5, 'V20': -0.8,
        'V21': 0.4, 'V22': 0.8, 'V23': -1.0, 'V24': 0.5,
        'V25': 0.2, 'V26': -0.4, 'V27': 0.8, 'V28': 0.4
    }
    
    ml_prediction = {
        'prediction': 1,
        'probability': 0.88,
        'accuracy': 0.99
    }
    
    # Inferensi
    result = kb_system.infer(features, ml_prediction)
    
    # Tampilkan penjelasan
    explanation = kb_system.explain(result)
    print(explanation)
    
    return result

def compare_results(results):
    """
    Bandingkan hasil semua test case
    """
    print_separator()
    print("📊 PERBANDINGAN HASIL TEST CASES")
    print_separator()
    
    print(f"{'Test Case':<25} {'ML Prob':<12} {'Final Score':<15} {'Adjustment':<12} {'Decision':<10}")
    print("-" * 80)
    
    for i, result in enumerate(results, 1):
        test_name = f"Test Case {i}"
        ml_prob = f"{result['ml_probability']:.2%}"
        final_score = f"{result['final_risk_score']:.2%}"
        adjustment = f"{result['risk_adjustment']:+.2%}"
        decision = "FRAUD" if result['final_prediction'] == 1 else "LEGIT"
        
        print(f"{test_name:<25} {ml_prob:<12} {final_score:<15} {adjustment:<12} {decision:<10}")
    
    print("-" * 80)
    print("\n📈 INSIGHT:")
    print("- KB System menyesuaikan risk score berdasarkan konteks")
    print("- Aturan bisnis membantu mendeteksi pola yang mungkin terlewat ML")
    print("- Kombinasi ML + KB menghasilkan keputusan yang lebih robust")

def main():
    """
    Jalankan semua test cases
    """
    print("\n" + "🧠 KNOWLEDGE BASE SYSTEM - TEST SUITE ".center(70, "="))
    print("Demonstrasi sistem deteksi fraud dengan rule-based reasoning")
    print("=" * 70)
    
    results = []
    
    # Run all test cases
    results.append(test_case_1_suspicious())
    results.append(test_case_2_legitimate())
    results.append(test_case_3_micro_transaction())
    results.append(test_case_4_extreme_amount())
    
    # Compare results
    compare_results(results)
    
    print("\n" + "✅ SEMUA TEST SELESAI ".center(70, "="))
    print("\nUntuk penggunaan interaktif, jalankan aplikasi Flask:")
    print("  python app.py")
    print("  Kemudian buka: http://localhost:5000/knowledge-base.html")
    print()

if __name__ == "__main__":
    main()
