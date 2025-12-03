"""
Knowledge Base System untuk Deteksi Penipuan Kartu Kredit
==========================================================
Sistem ini menggunakan pendekatan rule-based reasoning untuk meningkatkan
akurasi deteksi fraud dengan menggabungkan prediksi ML dan aturan bisnis.

Komponen:
- Rule Engine: Evaluasi aturan bisnis
- Knowledge Base: Fakta dan pola penipuan
- Inference Engine: Forward chaining untuk reasoning
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Any
from datetime import datetime, time


class FraudKnowledgeBase:
    """
    Knowledge Base untuk menyimpan fakta dan pola penipuan kartu kredit
    """
    
    def __init__(self):
        self.facts = {
            # Pola waktu transaksi penipuan
            'high_risk_hours': [0, 1, 2, 3, 4, 5, 23],  # Tengah malam - subuh
            
            # Threshold nominal transaksi
            'suspicious_amount_threshold': 2500,
            'very_high_amount_threshold': 7500,
            'micro_transaction_threshold': 0.5,
            
            # Pola V features (hasil PCA) - nilai ekstrim
            'v_feature_thresholds': {
                'extreme_low': -3,
                'extreme_high': 3,
                'very_extreme': 5
            },
            
            # Pola kombinasi yang mencurigakan
            'fraud_patterns': [
                {
                    'name': 'Transaksi Malam Nominal Besar',
                    'description': 'Transaksi dengan nominal tinggi di jam tidak biasa',
                    'risk_level': 'HIGH'
                },
                {
                    'name': 'Multiple Micro Transactions',
                    'description': 'Transaksi mikro yang sering digunakan untuk testing kartu curian',
                    'risk_level': 'MEDIUM'
                },
                {
                    'name': 'Anomali Fitur Ekstrim',
                    'description': 'Fitur PCA menunjukkan nilai sangat tidak normal',
                    'risk_level': 'HIGH'
                }
            ],
            
            # Statistik dari dataset training
            'dataset_stats': {
                'fraud_rate': 0.00172,  # ~0.172% transaksi adalah fraud
                'avg_fraud_amount': 122.21,
                'avg_legitimate_amount': 88.29
            }
        }
        
        # Load rules dari file jika ada
        self.rules = self._load_rules()
    
    def _load_rules(self) -> List[Dict]:
        """Load aturan dari file JSON"""
        try:
            with open('fraud_rules.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_rules()
    
    def _get_default_rules(self) -> List[Dict]:
        """Aturan default jika file tidak ditemukan"""
        return [
            {
                'id': 'R1',
                'name': 'Nominal Sangat Tinggi',
                'condition': 'amount > 7500',
                'action': 'increase_risk',
                'weight': 0.2,
                'description': 'Transaksi dengan nominal sangat tinggi',
                'priority': 3
            },
            {
                'id': 'R2',
                'name': 'Waktu Tidak Biasa',
                'condition': 'hour in [0,1,2,3,4] and amount > 2000',
                'action': 'increase_risk',
                'weight': 0.15,
                'description': 'Transaksi di jam berisiko tinggi dengan nominal besar',
                'priority': 2
            },
            {
                'id': 'R3',
                'name': 'Micro Transaction',
                'condition': 'amount < 0.5 and prob > 0.5',
                'action': 'increase_risk',
                'weight': 0.1,
                'description': 'Transaksi mikro dengan probabilitas mencurigakan',
                'priority': 1
            },
            {
                'id': 'R4',
                'name': 'Anomali Fitur Ekstrim',
                'condition': 'extreme_features > 5',
                'action': 'increase_risk',
                'weight': 0.2,
                'description': 'Banyak fitur menunjukkan nilai ekstrim',
                'priority': 3
            },
            {
                'id': 'R5',
                'name': 'Kombinasi Waktu dan Nominal',
                'condition': 'hour in [0,1,2,3,4] and amount > 5000 and prob > 0.4',
                'action': 'increase_risk',
                'weight': 0.25,
                'description': 'Kombinasi berbahaya: waktu malam + nominal tinggi + ML prob tinggi',
                'priority': 4
            }
        ]
    
    def get_fact(self, key: str) -> Any:
        """Ambil fakta dari knowledge base"""
        return self.facts.get(key)
    
    def get_rules(self) -> List[Dict]:
        """Ambil semua aturan"""
        return self.rules
    
    def add_rule(self, rule: Dict):
        """Tambah aturan baru"""
        self.rules.append(rule)
    
    def get_fraud_patterns(self) -> List[Dict]:
        """Ambil pola-pola penipuan yang diketahui"""
        return self.facts['fraud_patterns']


class RuleEngine:
    """
    Rule Engine untuk mengevaluasi aturan bisnis fraud detection
    """
    
    def __init__(self, knowledge_base: FraudKnowledgeBase):
        self.kb = knowledge_base
        self.fired_rules = []
        self.reasoning_trace = []
    
    def evaluate(self, features: Dict, ml_prediction: Dict) -> Dict:
        """
        Evaluasi aturan berdasarkan fitur transaksi dan prediksi ML
        
        Args:
            features: Dictionary berisi fitur transaksi (Time, V1-V28, Amount)
            ml_prediction: Dictionary berisi hasil prediksi ML (prediction, probability, accuracy)
        
        Returns:
            Dictionary berisi hasil evaluasi lengkap dengan reasoning
        """
        self.fired_rules = []
        self.reasoning_trace = []
        
        # Ekstrak informasi dari features
        context = self._prepare_context(features, ml_prediction)
        
        # Evaluasi setiap aturan
        risk_score = ml_prediction['probability']
        rules_applied = []
        
        for rule in self.kb.get_rules():
            if self._evaluate_rule(rule, context):
                self.fired_rules.append(rule['id'])
                rules_applied.append({
                    'rule_id': rule['id'],
                    'rule_name': rule['name'],
                    'description': rule['description'],
                    'weight': rule['weight'],
                    'action': rule['action']
                })
                
                # Apply rule action
                if rule['action'] == 'increase_risk':
                    risk_score = min(1.0, risk_score + (rule['weight'] * (1 - risk_score)))
                elif rule['action'] == 'flag_high_risk':
                    risk_score = max(risk_score, 0.7)
                
                self.reasoning_trace.append(
                    f"✓ Aturan {rule['id']} terpicu: {rule['description']}"
                )
        
        # Tentukan klasifikasi final
        final_prediction = 1 if risk_score > 0.5 else 0
        confidence = 'TINGGI' if risk_score > 0.75 or risk_score < 0.25 else \
                    'SEDANG' if risk_score > 0.6 or risk_score < 0.4 else 'RENDAH'
        
        # Deteksi pola penipuan yang diketahui
        detected_patterns = self._detect_patterns(context)
        
        return {
            'final_prediction': final_prediction,
            'final_risk_score': float(risk_score),
            'ml_probability': ml_prediction['probability'],
            'risk_adjustment': float(risk_score - ml_prediction['probability']),
            'confidence_level': confidence,
            'rules_fired': rules_applied,
            'detected_patterns': detected_patterns,
            'reasoning_trace': self.reasoning_trace,
            'recommendation': self._get_recommendation(final_prediction, risk_score, context),
            'context_summary': self._summarize_context(context)
        }
    
    def _prepare_context(self, features: Dict, ml_prediction: Dict) -> Dict:
        """Siapkan konteks untuk evaluasi aturan"""
        # Ekstrak waktu dari Time (asumsi dalam detik)
        time_seconds = features.get('Time', 0)
        hour = int((time_seconds / 3600) % 24)
        
        # Hitung jumlah fitur dengan nilai ekstrim
        v_features = [features.get(f'V{i}', 0) for i in range(1, 29)]
        extreme_features = sum(1 for v in v_features if abs(v) > 3)
        very_extreme_features = sum(1 for v in v_features if abs(v) > 5)
        
        amount = features.get('Amount', 0)
        prob = ml_prediction['probability']
        
        return {
            'hour': hour,
            'amount': amount,
            'prob': prob,
            'extreme_features': extreme_features,
            'very_extreme_features': very_extreme_features,
            'v_features': v_features,
            'time_seconds': time_seconds,
            'ml_prediction': ml_prediction['prediction']
        }
    
    def _evaluate_rule(self, rule: Dict, context: Dict) -> bool:
        """Evaluasi apakah sebuah aturan terpenuhi"""
        try:
            condition = rule['condition']
            # Evaluasi kondisi dengan context
            return eval(condition, {"__builtins__": {}}, context)
        except Exception as e:
            self.reasoning_trace.append(f"⚠ Error evaluasi aturan {rule['id']}: {str(e)}")
            return False
    
    def _detect_patterns(self, context: Dict) -> List[Dict]:
        """Deteksi pola penipuan yang diketahui"""
        detected = []
        
        # Pattern 1: Transaksi Malam Nominal Besar
        if context['hour'] in [0, 1, 2, 3, 4] and \
           context['amount'] > 5000:
            detected.append({
                'pattern': 'Transaksi Malam Nominal Besar',
                'risk_level': 'HIGH',
                'description': f"Transaksi $ {context['amount']:.2f} pada jam {context['hour']}:00"
            })
        
        # Pattern 2: Multiple characteristics (micro transaction)
        if context['amount'] < self.kb.get_fact('micro_transaction_threshold') and \
           context['prob'] > 0.5:
            detected.append({
                'pattern': 'Micro Transaction Mencurigakan',
                'risk_level': 'MEDIUM',
                'description': f"Transaksi mikro $ {context['amount']:.2f} dengan prob {context['prob']:.2%}"
            })
        
        # Pattern 3: Anomali Fitur Ekstrim
        if context['extreme_features'] > 5:
            detected.append({
                'pattern': 'Anomali Fitur Ekstrim',
                'risk_level': 'HIGH',
                'description': f"{context['extreme_features']} fitur menunjukkan nilai abnormal"
            })
        
        return detected
    
    def _get_recommendation(self, prediction: int, risk_score: float, context: Dict) -> str:
        """Berikan rekomendasi tindakan"""
        if prediction == 1:
            if risk_score > 0.85:
                return "TOLAK transaksi dan blokir kartu sementara. Hubungi pemegang kartu segera."
            elif risk_score > 0.65:
                return "TAHAN transaksi untuk verifikasi manual. Minta konfirmasi OTP/PIN."
            else:
                return "TANDAI transaksi untuk monitoring lebih lanjut."
        else:
            if risk_score > 0.4:
                return "LANJUTKAN transaksi dengan monitoring tambahan."
            else:
                return "SETUJUI transaksi - teridentifikasi sebagai transaksi sah."
    
    def _summarize_context(self, context: Dict) -> Dict:
        """Ringkasan konteks untuk debugging/logging"""
        return {
            'waktu_transaksi': f"{context['hour']}:00",
            'nominal': f"$ {context['amount']:.2f}",
            'probabilitas_ml': f"{context['prob']:.2%}",
            'fitur_ekstrim': context['extreme_features'],
            'kategori_waktu': 'Berisiko Tinggi' if context['hour'] in [0,1,2,3,4] else 'Normal',
            'kategori_nominal': 'Sangat Tinggi' if context['amount'] > 7500 else 'Tinggi' if context['amount'] > 2500 else 'Normal'
        }


class InferenceEngine:
    """
    Inference Engine untuk forward chaining reasoning
    """
    
    def __init__(self, knowledge_base: FraudKnowledgeBase):
        self.kb = knowledge_base
        self.rule_engine = RuleEngine(knowledge_base)
    
    def infer(self, features: Dict, ml_prediction: Dict) -> Dict:
        """
        Lakukan inferensi menggunakan forward chaining
        Gabungkan hasil ML dengan knowledge base reasoning
        """
        # Evaluasi menggunakan rule engine
        kb_result = self.rule_engine.evaluate(features, ml_prediction)
        
        # Tambahkan metadata
        kb_result['inference_method'] = 'Forward Chaining dengan Rule-Based Reasoning'
        kb_result['knowledge_base_version'] = '1.0'
        kb_result['timestamp'] = datetime.now().isoformat()
        
        return kb_result
    
    def explain(self, result: Dict) -> str:
        """
        Generate penjelasan lengkap dalam bahasa Indonesia
        """
        explanation = []
        explanation.append("=" * 70)
        explanation.append("PENJELASAN HASIL DETEKSI PENIPUAN")
        explanation.append("=" * 70)
        
        # Hasil Prediksi
        prediction_text = "FRAUD (PENIPUAN)" if result['final_prediction'] == 1 else "LEGITIMATE (SAH)"
        explanation.append(f"\n🎯 HASIL PREDIKSI: {prediction_text}")
        explanation.append(f"   Skor Risiko: {result['final_risk_score']:.2%}")
        explanation.append(f"   Tingkat Kepercayaan: {result['confidence_level']}")
        
        # Konteks Transaksi
        explanation.append(f"\n📊 KONTEKS TRANSAKSI:")
        for key, value in result['context_summary'].items():
            explanation.append(f"   • {key.replace('_', ' ').title()}: {value}")
        
        # Analisis ML
        explanation.append(f"\n🤖 ANALISIS MACHINE LEARNING:")
        explanation.append(f"   • Probabilitas ML: {result['ml_probability']:.2%}")
        explanation.append(f"   • Penyesuaian Risiko: {result['risk_adjustment']:+.2%}")
        
        # Aturan yang Terpicu
        if result['rules_fired']:
            explanation.append(f"\n📋 ATURAN YANG TERPICU ({len(result['rules_fired'])} aturan):")
            for rule in result['rules_fired']:
                explanation.append(f"   • [{rule['rule_id']}] {rule['rule_name']}")
                explanation.append(f"     → {rule['description']}")
                explanation.append(f"     → Bobot: {rule['weight']}, Aksi: {rule['action']}")
        else:
            explanation.append(f"\n📋 ATURAN YANG TERPICU: Tidak ada")
        
        # Pola yang Terdeteksi
        if result['detected_patterns']:
            explanation.append(f"\n⚠️  POLA PENIPUAN TERDETEKSI:")
            for pattern in result['detected_patterns']:
                explanation.append(f"   • {pattern['pattern']} [{pattern['risk_level']}]")
                explanation.append(f"     → {pattern['description']}")
        else:
            explanation.append(f"\n✓ Tidak ada pola penipuan yang terdeteksi")
        
        # Reasoning Trace
        if result['reasoning_trace']:
            explanation.append(f"\n🔍 JEJAK REASONING:")
            for trace in result['reasoning_trace']:
                explanation.append(f"   {trace}")
        
        # Rekomendasi
        explanation.append(f"\n💡 REKOMENDASI:")
        explanation.append(f"   {result['recommendation']}")
        
        explanation.append("\n" + "=" * 70)
        
        return "\n".join(explanation)


# Fungsi helper untuk integrasi mudah
def create_fraud_detection_system():
    """Factory function untuk membuat sistem deteksi fraud lengkap"""
    kb = FraudKnowledgeBase()
    inference_engine = InferenceEngine(kb)
    return inference_engine


# Testing
if __name__ == "__main__":
    # Contoh penggunaan
    system = create_fraud_detection_system()
    
    # Simulasi transaksi mencurigakan
    test_features = {
        'Time': 7200,  # 2 AM
        'Amount': 3500,
        'V1': -2.5, 'V2': 4.5, 'V3': -1.2, 'V4': 3.8,
        'V5': 0.5, 'V6': -0.8, 'V7': 1.2, 'V8': -2.1,
        **{f'V{i}': 0.0 for i in range(9, 29)}
    }
    
    test_ml_prediction = {
        'prediction': 1,
        'probability': 0.65,
        'accuracy': 0.99
    }
    
    result = system.infer(test_features, test_ml_prediction)
    print(system.explain(result))
