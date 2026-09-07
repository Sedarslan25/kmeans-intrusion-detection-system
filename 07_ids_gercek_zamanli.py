from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import time
from collections import defaultdict, deque

print("\n======================================")
print("07 - IDS GERÇEK ZAMANLI ANOMALİ TESPİTİ")
print("======================================\n")

# -----------------------------
# AYARLAR (hocaya göstermek için net)
# -----------------------------
PENCERE_SANIYE = 10           # analiz penceresi
FLOOD_ESIK_PAKET = 120        # 10 sn içinde aynı kaynaktan gelen paket sayısı (flood şüphesi)
PORT_TARAMA_ESIK = 25         # 10 sn içinde aynı kaynaktan farklı hedef port sayısı
DINLEME_SURESI = 30           # toplam dinleme (sn)

print("[A] IDS Ayarları")
print(f"    -> Pencere süresi: {PENCERE_SANIYE} sn")
print(f"    -> Flood eşiği: {FLOOD_ESIK_PAKET} paket / pencere")
print(f"    -> Port tarama eşiği: {PORT_TARAMA_ESIK} farklı port / pencere")
print(f"    -> Toplam dinleme: {DINLEME_SURESI} sn\n")

# -----------------------------
# VERİ YAPILARI (pencere tutmak için)
# -----------------------------
# Her kaynak IP için: son N saniyedeki paket zamanları
paket_zamanlari = defaultdict(deque)

# Her kaynak IP için: son N saniyedeki hedef port seti
hedef_portlar = defaultdict(lambda: defaultdict(deque))
# hedef_portlar[src_ip][dst_port] -> o porta giden paket zamanları listesi

# Uyarı logları
uyarilar = []

def temizle_eski_kayitlar(simdi):
    """Pencere dışına çıkan (eski) kayıtları temizler."""
    sinir = simdi - PENCERE_SANIYE

    # Paket zamanları temizliği
    for src_ip in list(paket_zamanlari.keys()):
        dq = paket_zamanlari[src_ip]
        while dq and dq[0] < sinir:
            dq.popleft()
        if not dq:
            del paket_zamanlari[src_ip]

    # Hedef port kayıtları temizliği
    for src_ip in list(hedef_portlar.keys()):
        port_dict = hedef_portlar[src_ip]
        for port in list(port_dict.keys()):
            dq = port_dict[port]
            while dq and dq[0] < sinir:
                dq.popleft()
            if not dq:
                del port_dict[port]
        if not port_dict:
            del hedef_portlar[src_ip]

def ids_kontrol(src_ip, dst_ip):
    """Kurallara göre kontrol edip anomali uyarısı üretir."""
    simdi = time.time()
    temizle_eski_kayitlar(simdi)

    paket_sayisi = len(paket_zamanlari.get(src_ip, []))
    farkli_port_sayisi = len(hedef_portlar.get(src_ip, {}).keys())

    # 1) Flood kontrolü
    if paket_sayisi >= FLOOD_ESIK_PAKET:
        uyarilar.append({
            "zaman": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tur": "FLOOD_SUPHESI",
            "kaynak_ip": src_ip,
            "hedef_ip": dst_ip,
            "detay": f"{PENCERE_SANIYE} sn içinde {paket_sayisi} paket"
        })
        print(f"[!] UYARI: FLOOD ŞÜPHESİ | Kaynak: {src_ip} | {PENCERE_SANIYE} sn içinde {paket_sayisi} paket")

    # 2) Port taraması kontrolü
    if farkli_port_sayisi >= PORT_TARAMA_ESIK:
        uyarilar.append({
            "zaman": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tur": "PORT_TARAMA_SUPHESI",
            "kaynak_ip": src_ip,
            "hedef_ip": dst_ip,
            "detay": f"{PENCERE_SANIYE} sn içinde {farkli_port_sayisi} farklı hedef port"
        })
        print(f"[!] UYARI: PORT TARAMA ŞÜPHESİ | Kaynak: {src_ip} | {PENCERE_SANIYE} sn içinde {farkli_port_sayisi} farklı port")

def paket_yakala(p):
    if IP not in p:
        return

    simdi = time.time()
    src_ip = p[IP].src
    dst_ip = p[IP].dst
    paket_uzunlugu = len(p)

    src_port = 0
    dst_port = 0

    if TCP in p:
        src_port = p[TCP].sport
        dst_port = p[TCP].dport
    elif UDP in p:
        src_port = p[UDP].sport
        dst_port = p[UDP].dport

    # Pencere kayıtları ekle
    paket_zamanlari[src_ip].append(simdi)
    if dst_port != 0:  # 0 ise port yok (ICMP vb.)
        hedef_portlar[src_ip][dst_port].append(simdi)

    # Hocaya gösterilecek net log satırı
    print(f"[+] Paket | {src_ip}:{src_port} -> {dst_ip}:{dst_port} | Uzunluk: {paket_uzunlugu}")

    # IDS kontrol (kurallarla)
    ids_kontrol(src_ip, dst_ip)

# -----------------------------
# IDS ÇALIŞTIRMA
# -----------------------------
print("[B] IDS başlatıldı ✅")
print("    -> Trafik dinleniyor... (Ctrl + C ile durdurabilirsin)\n")

sniff(prn=paket_yakala, timeout=DINLEME_SURESI)

# -----------------------------
# UYARI LOG KAYDI
# -----------------------------
print("\n[C] Dinleme bitti. Uyarılar kaydediliyor...")

df_uyari = pd.DataFrame(uyarilar)
if df_uyari.empty:
    print("    -> UYARI yok. (Bu da normal olabilir)")
else:
    df_uyari.to_csv("ids_uyari_log.csv", index=False)
    print("    -> ids_uyari_log.csv kaydedildi ✅")
    print(df_uyari.head(10))

print("\n======================================")
print("07 - IDS TAMAMLANDI ✅")
print("======================================\n")
