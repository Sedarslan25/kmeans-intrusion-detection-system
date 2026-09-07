# -*- coding: utf-8 -*-
"""
08 - SALDIRI SENARYOLARI SİMÜLASYONU (DRY-RUN)
Bu dosya AĞA PAKET GÖNDERMEZ.
Sadece rapor/sunum için senaryo test akışını ve beklenen IDS davranışını çıktılar.

Amaç: Hocanın raporda istediği 7. adımı hızlıca tamamlamak.
"""

import time
from datetime import datetime

# IDS tarafındaki eşiklerle aynı mantıkta olsun diye buraya yazıyoruz
PENCERE_SANIYE = 10
FLOOD_ESIK_PAKET = 120
PORT_TARAMA_ESIK = 25

def baslik(metin: str):
    print("\n" + "=" * 55)
    print(metin)
    print("=" * 55)

def zaman():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def bekle(saniye=1):
    time.sleep(saniye)

def syn_flood_simulasyon():
    baslik("A) SYN FLOOD SALDIRISI - SİMÜLASYON")
    print(f"[{zaman()}] Simülasyon amacı: Yoğun SYN benzeri trafik oluştuğunda IDS uyarı verir mi?")
    hedef_ip = input("Hedef IP (sunum/rapor için, sadece yazı): ").strip() or "127.0.0.1"
    paket_sayisi = int(input("Simüle edilecek SYN paket sayısı: ").strip() or "150")

    print("\n[Simülasyon] Trafik yoğunluğu hesaplanıyor...")
    bekle(1)

    print(f"-> Pencere: {PENCERE_SANIYE} sn | Paket: {paket_sayisi} | Eşik: {FLOOD_ESIK_PAKET}")
    if paket_sayisi >= FLOOD_ESIK_PAKET:
        print(f"[!] BEKLENEN IDS UYARISI: FLOOD ŞÜPHESİ (SYN Flood benzeri)")
        print(f"    Kaynak: (simülasyon) 127.0.0.1  -> Hedef: {hedef_ip}")
        print(f"    Gerekçe: {PENCERE_SANIYE} sn içinde {paket_sayisi} paket >= {FLOOD_ESIK_PAKET}")
    else:
        print("[i] Beklenen sonuç: Uyarı çıkmayabilir (eşik aşılmadı).")

    print("\n[Değerlendirme]")
    print("-> IDS mantığı: Kısa zaman penceresinde aşırı paket artışı flood şüphesidir.")
    print("-> Rapora eklenecek kanıt: Bu terminal çıktısı + IDS çalışma ekran görüntüsü.")
    print("\n✅ SYN Flood simülasyonu tamamlandı.")

def port_tarama_simulasyon():
    baslik("B) PORT TARAMA SALDIRISI - SİMÜLASYON")
    print(f"[{zaman()}] Simülasyon amacı: Çok sayıda farklı porta kısa sürede erişim olursa IDS uyarı verir mi?")
    hedef_ip = input("Hedef IP (sunum/rapor için, sadece yazı): ").strip() or "127.0.0.1"

    bas_port = int(input("Başlangıç portu: ").strip() or "8000")
    bit_port = int(input("Bitiş portu: ").strip() or "8030")

    farkli_port = max(0, bit_port - bas_port + 1)

    print("\n[Simülasyon] Port çeşitliliği hesaplanıyor...")
    bekle(1)

    print(f"-> Pencere: {PENCERE_SANIYE} sn | Farklı port: {farkli_port} | Eşik: {PORT_TARAMA_ESIK}")
    if farkli_port >= PORT_TARAMA_ESIK:
        print(f"[!] BEKLENEN IDS UYARISI: PORT TARAMA ŞÜPHESİ")
        print(f"    Kaynak: (simülasyon) 127.0.0.1  -> Hedef: {hedef_ip}")
        print(f"    Gerekçe: {PENCERE_SANIYE} sn içinde {farkli_port} farklı port >= {PORT_TARAMA_ESIK}")
    else:
        print("[i] Beklenen sonuç: Uyarı çıkmayabilir (eşik aşılmadı).")

    print("\n[Değerlendirme]")
    print("-> IDS mantığı: Kısa sürede çok sayıda farklı porta istek = port taraması şüphesi.")
    print("-> Rapora eklenecek kanıt: Bu terminal çıktısı + IDS 'PORT TARAMA ŞÜPHESİ' ekranı.")
    print("\n✅ Port tarama simülasyonu tamamlandı.")

def icmp_flood_simulasyon():
    baslik("C) ICMP FLOOD (PING FLOOD) - SİMÜLASYON")
    print(f"[{zaman()}] Simülasyon amacı: ICMP yoğunluğu artarsa IDS flood şüphesi verir mi?")
    hedef_ip = input("Hedef IP (sunum/rapor için, sadece yazı): ").strip() or "8.8.8.8"
    paket_sayisi = int(input("Simüle edilecek ICMP paket sayısı: ").strip() or "200")

    print("\n[Simülasyon] ICMP yoğunluğu hesaplanıyor...")
    bekle(1)

    print(f"-> Pencere: {PENCERE_SANIYE} sn | Paket: {paket_sayisi} | Eşik: {FLOOD_ESIK_PAKET}")
    if paket_sayisi >= FLOOD_ESIK_PAKET:
        print(f"[!] BEKLENEN IDS UYARISI: FLOOD ŞÜPHESİ (ICMP Flood benzeri)")
        print(f"    Kaynak: (simülasyon) 127.0.0.1  -> Hedef: {hedef_ip}")
        print(f"    Gerekçe: {PENCERE_SANIYE} sn içinde {paket_sayisi} paket >= {FLOOD_ESIK_PAKET}")
    else:
        print("[i] Beklenen sonuç: Uyarı çıkmayabilir (eşik aşılmadı).")

    print("\n[Değerlendirme]")
    print("-> IDS mantığı: ICMP paket sayısı kısa sürede aşırı artarsa flood şüphesidir.")
    print("-> Rapora eklenecek kanıt: Bu terminal çıktısı + IDS çalışma ekran görüntüsü.")
    print("\n✅ ICMP Flood simülasyonu tamamlandı.")

def menu():
    baslik("08 - SALDIRI SENARYOLARI SİMÜLASYONU (DRY-RUN)")
    print("Bu araç AĞA PAKET GÖNDERMEZ. Sadece rapor/sunum çıktısı üretir.\n")
    print(f"Kullanılan eşikler: Pencere={PENCERE_SANIYE}s | Flood={FLOOD_ESIK_PAKET} | PortTarama={PORT_TARAMA_ESIK}\n")

    while True:
        print("\n1) SYN Flood Simülasyonu")
        print("2) Port Tarama Simülasyonu")
        print("3) ICMP Flood Simülasyonu")
        print("0) Çıkış")
        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            syn_flood_simulasyon()
        elif secim == "2":
            port_tarama_simulasyon()
        elif secim == "3":
            icmp_flood_simulasyon()
        elif secim == "0":
            print("Çıkış ✅")
            break
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    menu()
