import pandas as pd

print("\n======================================")
print("01 - KDD ÖN İŞLEME BAŞLADI")
print("======================================\n")

# NSL-KDD sütun isimleri (standart)
sutun_isimleri = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes",
    "land","wrong_fragment","urgent","hot","num_failed_logins","logged_in",
    "num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count",
    "dst_host_srv_count","dst_host_same_srv_rate",
    "dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate",
    "dst_host_srv_rerror_rate","label","difficulty"
]

# Veri setlerini oku
print("[1] Veri setleri yükleniyor...")
train_veri = pd.read_csv("KDDTrain+.txt", names=sutun_isimleri)
test_veri  = pd.read_csv("KDDTest+.txt",  names=sutun_isimleri)

print(f"    -> Eğitim verisi satır sayısı : {train_veri.shape[0]}")
print(f"    -> Test verisi satır sayısı   : {test_veri.shape[0]}")
print(f"    -> Toplam sütun sayısı        : {train_veri.shape[1]}\n")

# Hoca için seçilen özellikler
secilen_sutunlar = [
    "protocol_type",   # port/protokol davranışı
    "service",         # hedef port karşılığı
    "flag",            # bağlantı durumu
    "src_bytes",       # paket uzunluğu (giden)
    "dst_bytes"        # paket uzunluğu (gelen)
]

print("[2] Özellik seçimi yapılıyor...")
print("    -> Seçilen özellikler:")
for s in secilen_sutunlar:
    print("       -", s)
print()

# Özellik ve etiket ayır
print("[3] Özellikler ve etiketler ayrılıyor...")
X_train = train_veri[secilen_sutunlar]
X_test  = test_veri[secilen_sutunlar]

y_train = train_veri["label"].apply(lambda x: 0 if x == "normal" else 1)
y_test  = test_veri["label"].apply(lambda x: 0 if x == "normal" else 1)

print(f"    -> X_train boyutu: {X_train.shape}")
print(f"    -> X_test  boyutu: {X_test.shape}")
print(f"    -> y_train boyutu: {y_train.shape}")
print(f"    -> y_test  boyutu: {y_test.shape}\n")

# Kategorik değişkenleri sayısala çevir
print("[4] Kategorik değişkenler sayısal formata dönüştürülüyor (One-Hot Encoding)...")
X_train = pd.get_dummies(X_train)
X_test  = pd.get_dummies(X_test)

print(f"    -> One-Hot sonrası X_train sütun sayısı: {X_train.shape[1]}")
print(f"    -> One-Hot sonrası X_test  sütun sayısı: {X_test.shape[1]}\n")

# Train-Test sütun eşitleme
print("[5] Eğitim ve test verileri sütunları eşitleniyor...")
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

print(f"    -> Eşitleme sonrası X_test sütun sayısı: {X_test.shape[1]}\n")

# Kaydet
print("[6] Ön işleme çıktıları kaydediliyor...")
X_train.to_csv("X_train_islenmis.csv", index=False)
X_test.to_csv("X_test_islenmis.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_test.to_csv("y_test.csv", index=False)

print("    -> X_train_islenmis.csv")
print("    -> X_test_islenmis.csv")
print("    -> y_train.csv")
print("    -> y_test.csv\n")

print("======================================")
print("01 - ÖN İŞLEME TAMAMLANDI ✅")
print("======================================\n")
