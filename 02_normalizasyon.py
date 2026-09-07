import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

print("\n======================================")
print("02 - NORMALİZASYON BAŞLADI")
print("======================================\n")

# Ön işlenmiş verileri oku
print("[1] Ön işlenmiş veriler yükleniyor...")
X_train = pd.read_csv("X_train_islenmis.csv")
X_test  = pd.read_csv("X_test_islenmis.csv")

print(f"    -> X_train boyutu: {X_train.shape}")
print(f"    -> X_test  boyutu: {X_test.shape}")
print(f"    -> Özellik sayısı: {X_train.shape[1]}\n")

# Normalizasyon
print("[2] StandardScaler oluşturuluyor ve eğitiliyor (fit)...")
olcekleyici = StandardScaler()
X_train_norm = olcekleyici.fit_transform(X_train)

print("    -> Scaler yalnızca eğitim verisi üzerinde fit edildi\n")

print("[3] Test verisi aynı scaler ile dönüştürülüyor (transform)...")
X_test_norm  = olcekleyici.transform(X_test)
print("    -> Veri sızıntısı (data leakage) önlendi\n")

# DataFrame'e geri çevir
print("[4] Normalize edilmiş veriler DataFrame formatına dönüştürülüyor...")
X_train_norm = pd.DataFrame(X_train_norm, columns=X_train.columns)
X_test_norm  = pd.DataFrame(X_test_norm, columns=X_train.columns)

# Kaydet
print("[5] Normalize edilmiş veriler kaydediliyor...")
X_train_norm.to_csv("X_train_normalize.csv", index=False)
X_test_norm.to_csv("X_test_normalize.csv", index=False)

print("    -> X_train_normalize.csv")
print("    -> X_test_normalize.csv\n")

# Ölçekleyiciyi kaydet (IDS için lazım)
print("[6] Ölçekleyici (StandardScaler) kaydediliyor...")
joblib.dump(olcekleyici, "olcekleyici.pkl")
print("    -> olcekleyici.pkl\n")

print("======================================")
print("02 - NORMALİZASYON TAMAMLANDI ✅")
print("======================================\n")
