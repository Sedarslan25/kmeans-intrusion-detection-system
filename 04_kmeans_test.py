# -*- coding: utf-8 -*-
"""
04 - KMEANS MODEL TESTİ (NSL-KDD Test Verisi)
- X_test_normalize.csv + y_test.csv ile değerlendirme
- KMeans + mesafe eşiği (anomali_esigi.pkl) kullanır
"""

import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

print("\n======================================")
print("04 - KMEANS MODEL TESTİ BAŞLADI")
print("======================================\n")

# 1) Dosyaları yükle
print("[1] Test verileri yükleniyor...")
X_test = pd.read_csv("X_test_normalize.csv")
y_test = pd.read_csv("y_test.csv").squeeze()  # Series'e çevir
print(f"    -> X_test boyutu: {X_test.shape}")
print(f"    -> y_test boyutu: {y_test.shape}")

# 2) Model ve eşik yükle
print("\n[2] Model ve eşik değeri yükleniyor...")
kmeans_modeli = joblib.load("kmeans_modeli.pkl")
anomali_esigi = joblib.load("anomali_esigi.pkl")
print("    -> Model yüklendi ✅")
print(f"    -> Anomali eşiği: {anomali_esigi}")

# 3) Mesafeleri hesapla ve anomali tahmini üret
print("\n[3] Test verisi üzerinde anomali tahmini yapılıyor...")
mesafe_matrisi = kmeans_modeli.transform(X_test)         # her kümeye uzaklık
min_mesafe = np.min(mesafe_matrisi, axis=1)              # en yakın kümeye uzaklık
y_tahmin = (min_mesafe > anomali_esigi).astype(int)      # 1=anomali, 0=normal

anomali_sayisi = int((y_tahmin == 1).sum())
normal_sayisi = int((y_tahmin == 0).sum())
print(f"    -> Tahmin edilen NORMAL: {normal_sayisi}")
print(f"    -> Tahmin edilen ANOMALİ: {anomali_sayisi}")

# 4) Değerlendirme metrikleri
print("\n[4] Performans metrikleri hesaplanıyor...")
cm = confusion_matrix(y_test, y_tahmin, labels=[0, 1])
acc = accuracy_score(y_test, y_tahmin)
prec = precision_score(y_test, y_tahmin, zero_division=0)
rec = recall_score(y_test, y_tahmin, zero_division=0)
f1 = f1_score(y_test, y_tahmin, zero_division=0)

tn, fp, fn, tp = cm.ravel()

print("\n---------- CONFUSION MATRIX ----------")
print("Satır=Gerçek, Sütun=Tahmin")
print("            Tahmin Normal   Tahmin Anomali")
print(f"Gerçek Normal      {tn:>6}          {fp:>6}")
print(f"Gerçek Anomali     {fn:>6}          {tp:>6}")
print("--------------------------------------\n")

print("---------- METRİKLER ----------")
print(f"Accuracy  : {acc:.4f}")
print(f"Precision : {prec:.4f}")
print(f"Recall    : {rec:.4f}")
print(f"F1-Score  : {f1:.4f}")
print("--------------------------------\n")

# 5) Sonuçları dosyaya kaydet (rapor için iyi olur)
print("[5] Test çıktıları kaydediliyor...")
sonuc_df = pd.DataFrame({
    "min_mesafe": min_mesafe,
    "gercek_etiket": y_test.astype(int),
    "tahmin": y_tahmin.astype(int)
})
sonuc_df.to_csv("kmeans_test_sonuclari.csv", index=False)
print("    -> kmeans_test_sonuclari.csv ✅")

print("\n======================================")
print("04 - KMEANS MODEL TESTİ TAMAMLANDI ✅")
print("======================================\n")
