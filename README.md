# K-Means Intrusion Detection System

An educational intrusion-detection workflow built with Python and the NSL-KDD dataset. The project preprocesses network-traffic features, normalizes them, trains a K-Means anomaly model, evaluates results, and includes scripts for live-traffic monitoring and simulation.

> **Türkçe özet:** NSL-KDD veri kümesi üzerinde ağ trafiğini ön işleyen, normalize eden, K-Means ile anomali tespiti yapan ve canlı trafik izleme/saldırı simülasyonu adımları içeren eğitim amaçlı IDS projesi.

## Workflow

1. `01_kdd_onisleme.py` — selects network features and one-hot encodes categorical values.
2. `02_normalizasyon.py` — applies `StandardScaler` without train/test leakage.
3. `03_kmeans_egitim.py` — trains a two-cluster K-Means model and derives an anomaly threshold.
4. `04_kmeans_test.py` — evaluates the model on the test split.
5. `05_ids_canli_izleme.py` to `07_ids_gercek_zamanli.py` — live traffic processing and monitoring helpers.
6. `08_saldirilar.py` and `09_simülasyon.py` — controlled simulation utilities.

> **Türkçe:** İş akışı; ön işleme, normalizasyon, eğitim, test, canlı izleme ve kontrollü simülasyon aşamalarından oluşur.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python 01_kdd_onisleme.py
python 02_normalizasyon.py
python 03_kmeans_egitim.py
python 04_kmeans_test.py
```

> **Türkçe:** Komutları proje kök klasöründe ve sırayla çalıştırın. Ön işleme ve eğitim sırasında oluşturulan CSV/model çıktıları `.gitignore` ile depodan hariç tutulur; istenildiğinde komutlarla yeniden üretilir.

## Dataset and repository size

The raw NSL-KDD training and test files are included for reproducibility. Generated normalized datasets, evaluation exports, and serialized models are intentionally excluded because they can be recreated and would add hundreds of megabytes to the repository.

> **Türkçe:** Ham NSL-KDD verileri tekrarlanabilirlik için korunur; yüzlerce MB tutan üretilmiş çıktı dosyaları yeniden üretilebildiği için GitHub'a yüklenmez.

## Tech stack

- Python
- pandas and NumPy
- scikit-learn (`StandardScaler`, `KMeans`)
- joblib
- Scapy (live capture scripts)

## Scope and safety note

This is an educational anomaly-detection project, not a production security control. Live-capture features may require administrator privileges and should only be used on networks and systems where you have authorization.

> **Türkçe:** Bu proje eğitim amaçlıdır; canlı ağ izleme işlevleri yalnızca izinli ağlarda kullanılmalıdır.
