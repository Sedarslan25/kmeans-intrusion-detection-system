import pandas as pd
from sklearn.cluster import KMeans
import joblib
import numpy as np

print("\n==============================")
print("03 - K-MEANS MODEL EĞİTİMİ BAŞLADI")
print("==============================\n")

# Normalize edilmiş verileri oku
print("[1] Normalize edilmiş eğitim verisi yükleniyor...")
X_train = pd.read_csv("X_train_normalize.csv")
print("    -> Veri boyutu:", X_train.shape)

# K-Means modeli oluştur
print("\n[2] K-Means modeli oluşturuluyor...")
kmeans_modeli = KMeans(
    n_clusters=2,
    random_state=42,
    n_init=10
)

# Modeli eğit
print("\n[3] Model eğitiliyor...")
kmeans_modeli.fit(X_train)

print("    -> Model eğitimi tamamlandı ✅")

# Küme merkezleri
print("\n[4] Küme merkezleri hesaplandı:")
print(kmeans_modeli.cluster_centers_)

# Her noktanın merkeze uzaklığı
print("\n[5] Anomali eşiği hesaplanıyor...")
mesafeler = np.min(
    kmeans_modeli.transform(X_train),
    axis=1
)

esik = mesafeler.mean() + 2 * mesafeler.std()

print("    -> Anomali eşik değeri:", esik)

# Modeli kaydet
joblib.dump(kmeans_modeli, "kmeans_modeli.pkl")
joblib.dump(esik, "anomali_esigi.pkl")

print("\n[6] Model ve eşik değeri kaydedildi")
print("    -> kmeans_modeli.pkl")
print("    -> anomali_esigi.pkl")

print("\n==============================")
print("03 - K-MEANS EĞİTİMİ TAMAMLANDI ✅")
print("==============================\n")
