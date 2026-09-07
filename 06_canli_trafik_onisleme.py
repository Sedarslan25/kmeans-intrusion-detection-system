import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

print("\n==============================")
print("06 - CANLI TRAFİK ÖN İŞLEME")
print("==============================\n")

# 1) Veriyi oku
dosya_girdi = "canli_trafik.csv"
print(f"[1] Girdi dosyası okunuyor: {dosya_girdi}")
veri = pd.read_csv(dosya_girdi)
print("    -> İlk boyut:", veri.shape)

# 2) Temel temizlik: boşlar / NaN
print("\n[2] Eksik veriler temizleniyor...")
veri = veri.dropna()
print("    -> Boyut (NaN silindi):", veri.shape)

# 3) Tip dönüşümü (port ve uzunluk sayısal olmalı)
print("\n[3] Sayısal dönüşümler yapılıyor...")
for kolon in ["kaynak_port", "hedef_port", "paket_uzunlugu"]:
    veri[kolon] = pd.to_numeric(veri[kolon], errors="coerce")

veri = veri.dropna()
print("    -> Boyut (sayısal olmayanlar temizlendi):", veri.shape)

# 4) Mantıksız kayıtları filtrele
print("\n[4] Mantıksız değerler filtreleniyor...")
# Port 0 olabilir (ICMP gibi), ama negatif olamaz; paket uzunluğu 0/negatif olamaz
veri = veri[(veri["kaynak_port"] >= 0) & (veri["hedef_port"] >= 0) & (veri["paket_uzunlugu"] > 0)]
print("    -> Boyut (filtre sonrası):", veri.shape)

# 5) Normalizasyon (sadece sayısal alanlar)
print("\n[5] Normalizasyon uygulanıyor (portlar + paket uzunluğu)...")
ozellikler = veri[["kaynak_port", "hedef_port", "paket_uzunlugu"]].copy()

olcekleyici_canli = StandardScaler()
ozellikler_norm = olcekleyici_canli.fit_transform(ozellikler)

ozellikler_norm = pd.DataFrame(
    ozellikler_norm,
    columns=["kaynak_port_norm", "hedef_port_norm", "paket_uzunlugu_norm"]
)

# 6) Çıktıyı birleştir ve kaydet
cikti = pd.concat([veri.reset_index(drop=True), ozellikler_norm], axis=1)

dosya_cikti = "canli_trafik_islenmis.csv"
cikti.to_csv(dosya_cikti, index=False)
joblib.dump(olcekleyici_canli, "olcekleyici_canli.pkl")

print("\n[6] Çıktılar kaydedildi ✅")
print("    ->", dosya_cikti)
print("    -> olcekleyici_canli.pkl")

print("\n==============================")
print("06 - CANLI TRAFİK ÖN İŞLEME TAMAMLANDI ✅")
print("==============================\n")

