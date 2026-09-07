from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import joblib
import time

print("\n==============================")
print("05 - IDS GERÇEK ZAMANLI İZLEME")
print("==============================\n")

# Model ve ölçekleyici yükle
print("[1] Model ve ölçekleyici yükleniyor...")
kmeans_modeli = joblib.load("kmeans_modeli.pkl")
olcekleyici = joblib.load("olcekleyici.pkl")
anomali_esigi = joblib.load("anomali_esigi.pkl")

print("    -> Model hazır")
print("    -> Anomali eşiği:", anomali_esigi)

# Canlı trafik dataframe
sutunlar = ["kaynak_ip", "hedef_ip", "kaynak_port", "hedef_port", "paket_uzunlugu"]
canli_trafik = []

def paket_yakala(paket):
    if IP in paket:
        kaynak_ip = paket[IP].src
        hedef_ip = paket[IP].dst
        paket_uzunlugu = len(paket)

        kaynak_port = 0
        hedef_port = 0

        if TCP in paket:
            kaynak_port = paket[TCP].sport
            hedef_port = paket[TCP].dport
        elif UDP in paket:
            kaynak_port = paket[UDP].sport
            hedef_port = paket[UDP].dport

        canli_trafik.append([
            kaynak_ip, hedef_ip, kaynak_port, hedef_port, paket_uzunlugu
        ])

        print(f"[+] Paket alındı | {kaynak_ip}:{kaynak_port} -> {hedef_ip}:{hedef_port} | Uzunluk: {paket_uzunlugu}")

# Trafik dinleme
print("\n[2] Ağ trafiği dinleniyor (10 saniye)...")
sniff(prn=paket_yakala, timeout=10)

# DataFrame oluştur
df_canli = pd.DataFrame(canli_trafik, columns=sutunlar)
df_canli.to_csv("canli_trafik.csv", index=False)

print("\n[3] Canlı trafik CSV olarak kaydedildi")
print("    -> canli_trafik.csv")

# Model için sadece sayısal özellikler
if not df_canli.empty:
    print("\n[4] IDS BİLGİLENDİRME")
    print("    -> Canlı trafik başarıyla yakalandı ve kaydedildi.")
    print("    -> Model eğitimi NSL-KDD veri seti ile yapılmıştır.")
    print("    -> Canlı trafik verisi raporlama ve gözlem amaçlı kullanılmıştır.")

else:
    print("\n[!] Hiç paket yakalanamadı")

print("\n==============================")
print("IDS ÇALIŞMASI TAMAMLANDI ✅")
print("==============================\n")
