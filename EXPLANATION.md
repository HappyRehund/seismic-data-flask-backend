# 📖 EXPLANATION — Seismic Viewer Backend

> Dokumen ini menjelaskan keseluruhan arsitektur, alur development, interaksi dengan data CSV, dan rencana integrasi dengan **Dataiku** secara naratif (storytelling).

---

## 🧭 Daftar Isi

1. [Gambaran Umum Aplikasi](#-gambaran-umum-aplikasi)
2. [Cerita Development: Dari Nol Hingga Jadi](#-cerita-development-dari-nol-hingga-jadi)
3. [Penjelasan Layer-by-Layer](#-penjelasan-layer-by-layer)
   - [Routes — Pintu Gerbang API](#1-routes--pintu-gerbang-api)
   - [Controllers — Si Pengatur Lalu Lintas](#2-controllers--si-pengatur-lalu-lintas)
   - [Services — Otak Bisnis](#3-services--otak-bisnis)
   - [Repositories — Tukang Ambil Data](#4-repositories--tukang-ambil-data)
   - [Models — Cetak Biru Data](#5-models--cetak-biru-data)
   - [DTOs — Kontrak Data](#6-dtos--kontrak-data)
   - [Common — Peralatan Bersama](#7-common--peralatan-bersama)
4. [Bagaimana Aplikasi Berinteraksi dengan CSV](#-bagaimana-aplikasi-berinteraksi-dengan-csv)
5. [Integrasi dengan Dataiku](#-integrasi-dengan-dataiku)
6. [Ringkasan Arsitektur](#-ringkasan-arsitektur)

---

## 🌍 Gambaran Umum Aplikasi

**Seismic Viewer Backend** adalah sebuah REST API yang dibangun menggunakan **Flask** (Python) untuk melayani data seismik kepada frontend. Aplikasi ini menyediakan data berupa:

| Domain | Deskripsi | Sumber Data |
|--------|-----------|-------------|
| **Well** | Koordinat sumur minyak/gas (posisi inline, crossline, X, Y, basement, surface) | `csv_data/well/well_coordinates.csv` |
| **Well Log** | Data logging sumur (GR, RT, RHOB, NPHI, DT, dll — 27 parameter per kedalaman) | `csv_data/well_log/gnk_well_log.csv` |
| **Horizon** | Data horizon seismik (inline, crossline, top, bottom) | `csv_data/horizon/horizon.csv` |
| **Seismic Section** | Gambar penampang seismik (inline & crossline) berupa file PNG | `csv_data/inline_crossline/inline/*.png` & `csv_data/inline_crossline/crossline/*.png` |

Arsitektur yang digunakan adalah **Clean Architecture** dengan pemisahan layer yang jelas: **Routes → Controllers → Services → Repositories → Models**, ditambah **DTOs** dan **Common utilities** sebagai pendukung.

---

## 📝 Cerita Development: Dari Nol Hingga Jadi

### Bab 1: "Mulai dari Mana Ya?"

Bayangkan kamu sedang duduk di depan layar, baru saja membuat folder `backend/` dan file `main.py`. Di tangan kamu ada tumpukan file CSV berisi data seismik — koordinat sumur, well log, horizon, dan gambar-gambar penampang seismik. Tugasmu: **buatkan API agar frontend bisa mengakses semua data ini.**

Pertanyaan pertama yang muncul: *"Mulai dari mana?"*

Jawabannya: **mulai dari dua arah sekaligus.**

---

### Bab 2: "Fondasi — Model Dulu, Biar Tahu Bentuk Datanya"

Sebelum membuat endpoint apapun, hal pertama yang dilakukan adalah **membuka file CSV** dan mempelajari strukturnya. Kolom apa saja yang ada? Tipenya apa? Mana yang wajib, mana yang opsional?

Dari situlah lahir folder `models/`:

- **`well_model.py`** — mendefinisikan `WellCoordinate` dengan 14 field: `inline`, `crossline`, `x`, `y`, `basement`, `surface`, `well_name`, dan lainnya. Di sini juga ada logika parsing khusus untuk koordinat yang formatnya "407.890.049" (titik ganda yang perlu dihandle).

- **`well_log_model.py`** — mendefinisikan `WellLog` dengan 27 field parameter logging: `GR` (Gamma Ray), `RT` (Resistivity), `RHOB` (Density), `NPHI` (Neutron Porosity), dan lainnya. Setiap field menggunakan fungsi helper `_f()` untuk menangani nilai kosong atau non-numerik.

- **`horizon_model.py`** — mendefinisikan `Horizon` dengan field `X`, `Y`, `Inline`, `Crossline`, `TraceNumber`, `bottom`, `top`, dan referensinya.

- **`seismic_section_model.py`** — mendefinisikan `SeismicSection` dengan `SectionType` (INLINE atau CROSSLINE), nomor section, dan `image_data` berupa bytes (data gambar PNG mentah).

Setiap model dilengkapi dengan:
- Method `from_dict()` → untuk parsing data dari CSV/dictionary menjadi object
- Method `to_dict()` → untuk serialisasi object kembali menjadi dictionary (agar bisa dijadikan JSON)
- Method `validate()` → untuk validasi data

> 💡 **Analogi:** Model itu seperti **cetakan kue**. Sebelum membuat kue (data), kamu harus tahu bentuk cetakannya dulu.

---

### Bab 3: "Lalu, Siapa yang Mengambil Data dari CSV?"

Setelah tahu bentuk datanya, langkah berikutnya adalah membuat **Repository** — layer yang bertanggung jawab **membaca data dari sumbernya** (dalam hal ini file CSV).

Lahirlah folder `repositories/`:

- **`well_repository.py`** — membuka `csv_data/well/well_coordinates.csv` menggunakan `csv.DictReader` dengan delimiter `;` (semicolon). Menyediakan method: `find_all()`, `find_by_name()`, `count()`, `exists()`.

- **`well_log_repository.py`** — membuka `csv_data/well_log/gnk_well_log.csv` menggunakan `csv.DictReader` dengan delimiter `,` (comma). Menyediakan method: `find_all()`, `find_all_page()` (pagination), `find_by_well()` (filter berdasarkan nama sumur), `count()`.

- **`horizon_repository.py`** — membuka `csv_data/horizon/horizon.csv`. Menyediakan method: `find_all()`, `find_all_page()` (pagination).

- **`seismic_section_repository.py`** — **berbeda dari yang lain**, repository ini tidak membaca CSV, melainkan **membaca file gambar PNG** dari folder `csv_data/inline_crossline/inline/` dan `csv_data/inline_crossline/crossline/`. Menyediakan method: `find_by_number()` yang membangun path file berdasarkan tipe section dan nomor.

Setiap repository CSV mengikuti pola yang sama:
```
1. __init__  → simpan path CSV, cek file ada atau tidak
2. _ensure_file_exists() → raise error kalau file CSV tidak ditemukan
3. Buka file → baca dengan csv.DictReader → parsing setiap row dengan Model.from_dict()
```

> 💡 **Analogi:** Repository itu seperti **tukang gudang**. Dia tahu persis di mana barang disimpan dan cara mengambilnya, tapi dia tidak peduli barang itu mau diapakan.

---

### Bab 4: "Saatnya Logika Bisnis — Service Layer"

Data mentah dari repository belum tentu langsung bisa dikirim ke frontend. Kadang perlu diolah dulu — dihitung statistiknya, divalidasi, atau ditransformasi.

Di sinilah peran folder `services/`:

- **`well_service.py`** — selain meneruskan data dari repository, service ini juga **menghitung summary** (statistik min/max/range untuk inline dan crossline, daftar nama sumur, total wells). Juga memvalidasi bahwa `well_name` tidak kosong sebelum query.

- **`well_log_service.py`** — meneruskan operasi CRUD dari repository, termasuk pagination (`get_all_well_logs_page`) dan filter by well name.

- **`horizon_service.py`** — meneruskan data horizon dengan dukungan pagination.

- **`seismic_section_service.py`** — meneruskan request gambar inline/crossline ke repository.

> 💡 **Analogi:** Service itu seperti **koki di dapur**. Bahan mentah (data) datang dari gudang (repository), lalu koki mengolahnya menjadi hidangan yang siap disajikan.

---

### Bab 5: "Siapa yang Menerima Pesanan? — Controller"

Sekarang data sudah bisa diambil dan diolah. Tapi siapa yang menerima request HTTP dari frontend, memanggil service yang tepat, dan mengembalikan response dalam format JSON?

Itulah tugas folder `controllers/`:

- **`well_controller.py`** — menerima request, memanggil `WellService`, dan membungkus hasilnya dalam `success_response()` atau `error_response()`. Menangani 4 operasi: get all wells, get by name, get summary, check exists.

- **`well_log_controller.py`** — menangani 3 operasi: get all, get paginated (membaca query params `page` dan `page_size`), get by well name.

- **`horizon_controller.py`** — menangani 2 operasi: get all, get paginated.

- **`seismic_section_controller.py`** — menangani 2 operasi: get inline image, get crossline image. **Berbeda dengan controller lain**, ini mengembalikan `file_response()` (binary PNG) bukan JSON.

Setiap controller mengikuti pola:
```python
try:
    result = self.service.do_something()
    return success_response(result)  # → {"success": true, "data": {...}}
except Exception as e:
    return error_response(str(e), 500)  # → {"success": false, "error": "..."}
```

> 💡 **Analogi:** Controller itu seperti **pelayan restoran**. Dia menerima pesanan (HTTP request), menyampaikan ke dapur (service), dan mengantar hidangan jadi (HTTP response) ke meja tamu.

---

### Bab 6: "Terakhir, Pasang Papan Nama — Routes"

Setelah semua layer di belakang layar siap, langkah terakhir adalah **mendaftarkan endpoint URL** agar dunia luar bisa mengaksesnya.

Lahirlah folder `routes/`:

- **`well_routes.py`** — mendaftarkan 4 endpoint:
  - `GET /api/well` → semua sumur
  - `GET /api/well/summary` → ringkasan statistik
  - `GET /api/well/<well_name>` → detail satu sumur
  - `GET /api/well/<well_name>/exists` → cek keberadaan sumur

- **`well_log_routes.py`** — mendaftarkan 3 endpoint:
  - `GET /api/well-log` → semua well log
  - `GET /api/well-log-page?page=1&page_size=500` → well log berpaginasi
  - `GET /api/well-log/<well_name>` → well log per sumur

- **`horizon_routes.py`** — mendaftarkan 2 endpoint:
  - `GET /api/horizon` → semua data horizon
  - `GET /api/horizon-page?page=1&page_size=500` → horizon berpaginasi

- **`seismic_section_routes.py`** — mendaftarkan 2 endpoint:
  - `GET /api/inline/<number>/image` → gambar penampang inline
  - `GET /api/crossline/<number>/image` → gambar penampang crossline

Semua routes menggunakan Flask **Blueprint** dan didaftarkan di `main.py` dengan prefix `/api`.

> 💡 **Analogi:** Routes itu seperti **papan menu di depan restoran**. Pelanggan (frontend) melihat menu ini untuk tahu apa saja yang tersedia dan cara memesannya.

---

### Bab 7: "Pendukung di Balik Layar"

Selain 5 layer utama, ada dua folder pendukung:

#### **DTOs (Data Transfer Objects)**

Folder `dto/` berisi definisi tipe data yang mengalir masuk dan keluar API:

- **`dto/base.py`** — mendefinisikan `DtoResponse` protocol dan `ListResponse` (wrapper generik untuk response berisi list + count).
- **`dto/data/`** — berisi `TypedDict` untuk validasi tipe statis:
  - `well_data.py` → `WellData`, `RangeStatisticsData`, `StatisticsData`, `WellsSummaryData`, `WellExistsData`
  - `well_log_data.py` → `WellLogData`, `WellLogsData`
  - `horizon_data.py` → `HorizonPointData`, `HorizonData`
- **`dto/response/`** — berisi response DTO khusus:
  - `well_response.py` → `WellsSummaryResponse`, `WellExistsResponse` (dataclass dengan `to_dict()` dan `from_dict()`)

#### **Common Utilities**

Folder `common/` berisi helper yang dipakai lintas layer:

- **`response_utils.py`** — 3 fungsi standar:
  - `success_response(data)` → `{"success": true, "data": {...}}`
  - `error_response(message, status_code)` → `{"success": false, "error": "..."}`
  - `file_response(data, mime_type, filename)` → response binary dengan header Content-Type, Content-Length, Content-Disposition, Cache-Control

- **`well_name_utils.py`** — `normalize_well_name()` untuk menstandarkan format nama sumur. Contoh: `"gnk-1"` → `"GNK-001"`, `"GNK-12A"` → `"GNK-012A"`. Ini penting karena data di CSV mungkin menggunakan format yang tidak konsisten.

---

## 📂 Bagaimana Aplikasi Berinteraksi dengan CSV

Berikut diagram alur bagaimana satu request `GET /api/well` mengalir melalui seluruh arsitektur:

```
Frontend (Browser/React)
    │
    │  HTTP GET /api/well
    ▼
┌──────────────────────────────┐
│  main.py                     │
│  Flask app + CORS + Blueprint│
│  url_prefix = '/api'         │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  routes/well_routes.py       │
│  @well_routes.route('/well') │
│  → controller.get_all_wells()│
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  controllers/well_controller │
│  try:                        │
│    wells = service.get_all() │
│    return success_response() │
│  except:                     │
│    return error_response()   │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  services/well_service.py    │
│  return repo.find_all()      │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  repositories/well_repository.py         │
│                                          │
│  with open('csv_data/well/...csv') as f: │
│    reader = csv.DictReader(f, ';')       │
│    for row in reader:                    │
│      well = WellCoordinate.from_dict(row)│
│      wells.append(well)                  │
│  return wells                            │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  csv_data/well/              │
│  well_coordinates.csv        │
│  (file CSV di disk)          │
└──────────────────────────────┘
```

### Pola Interaksi CSV di Setiap Repository:

| Repository | File CSV | Delimiter | Metode Baca |
|-----------|----------|-----------|-------------|
| `WellRepository` | `csv_data/well/well_coordinates.csv` | `;` (semicolon) | `csv.DictReader` |
| `WellLogRepository` | `csv_data/well_log/gnk_well_log.csv` | `,` (comma) | `csv.DictReader` |
| `HorizonRepository` | `csv_data/horizon/horizon.csv` | `,` (comma) | `csv.DictReader` |
| `SeismicSectionRepository` | `csv_data/inline_crossline/**/*.png` | — | `open(path, 'rb').read()` |

**Catatan penting:**
- Setiap kali request masuk, repository **membaca ulang file CSV dari awal** (tidak ada caching). Ini sederhana dan cocok untuk prototype, tapi tidak efisien untuk production.
- Data CSV dibaca row-by-row dan dikonversi menjadi object Python (dataclass) melalui `Model.from_dict()`.
- Untuk well log dan horizon yang datanya besar, tersedia **pagination** (`find_all_page`) yang melewati baris di luar range halaman.

---

## 🔄 Integrasi dengan Dataiku

### Kenapa Arsitektur Ini Mudah Dipindah ke Dataiku?

Arsitektur Clean Architecture yang digunakan **sengaja dirancang** agar sumber data bisa diganti tanpa mengubah layer lain. Perubahan **hanya terjadi di Repository layer**. Routes, Controllers, Services, Models, DTOs — semuanya **tetap sama persis**.

### Apa yang Berubah?

Saat ini, repository membaca data seperti ini:

```python
# Sekarang (CSV lokal)
import csv

class WellRepository:
    def __init__(self, csv_path='csv_data/well/well_coordinates.csv'):
        self.csv_path = csv_path

    def find_all(self):
        with open(self.csv_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                well = WellCoordinate.from_dict(row)
                wells.append(well)
        return wells
```

Di Dataiku, kamu akan menggantinya menjadi:

```python
# Nanti di Dataiku
import dataiku

class WellRepository:
    def __init__(self, dataset_name='well_coordinates'):
        self.dataset_name = dataset_name

    def find_all(self):
        dataset = dataiku.Dataset(self.dataset_name)
        df = dataset.get_dataframe(infer_with_pandas=False)
        wells = []
        for _, row in df.iterrows():
            well = WellCoordinate.from_dict(row.to_dict())
            wells.append(well)
        return wells
```

**Perhatikan:** method `from_dict()` di Model **tidak perlu berubah** karena Dataiku DataFrame juga menghasilkan dictionary saat di-convert per-row. Yang berubah hanya **cara membuka dan membaca sumber data**.

### Pemetaan CSV → Dataiku Dataset

| Saat Ini (CSV Lokal) | Nanti di Dataiku | Tipe |
|----------------------|-----------------|------|
| `csv_data/well/well_coordinates.csv` | Dataset: `well_coordinates` | Tabular (CSV/Database) |
| `csv_data/well_log/gnk_well_log.csv` | Dataset: `gnk_well_log` | Tabular (CSV/Database) |
| `csv_data/horizon/horizon.csv` | Dataset: `horizon` | Tabular (CSV/Database) |
| `csv_data/inline_crossline/**/*.png` | Managed Folder: `seismic_images` | Binary (PNG) |
| `csv_data/fault/*.csv` | Dataset: `fault_data` | Tabular (CSV/Database) |

### Langkah-Langkah Migrasi ke Dataiku

#### Langkah 1: Upload Data CSV ke Dataiku Dataset

1. Buka Dataiku DSS → Project
2. Buat Dataset baru → pilih "Upload your files"
3. Upload file CSV (`well_coordinates.csv`, `gnk_well_log.csv`, `horizon.csv`)
4. Dataiku akan otomatis mendeteksi kolom dan tipe data
5. Pastikan nama dataset sesuai pemetaan di atas

#### Langkah 2: Upload File Gambar ke Managed Folder

1. Buat **Managed Folder** baru bernama `seismic_images`
2. Upload semua file PNG ke dalam folder tersebut dengan struktur:
   ```
   seismic_images/
   ├── inline/
   │   ├── inline_100.png
   │   ├── inline_101.png
   │   └── ...
   └── crossline/
       ├── crossline_200.png
       ├── crossline_201.png
       └── ...
   ```
3. Akses menggunakan Dataiku API:
   ```python
   import dataiku

   folder = dataiku.Folder("seismic_images")
   image_data = folder.get_download_stream("inline/inline_100.png").read()
   ```

#### Langkah 3: Modifikasi Repository Layer

Buat versi Dataiku dari setiap repository. Contoh untuk `SeismicSectionRepository`:

```python
# Sekarang (file lokal)
class SeismicSectionRepository:
    def find_by_number(self, section_type, number):
        path = f"csv_data/inline_crossline/{section_type.value}/{section_type.value}_{number}.png"
        with open(path, 'rb') as f:
            image_data = f.read()
        return SeismicSection(section_type, number, image_data)

# Nanti di Dataiku
class SeismicSectionRepository:
    def __init__(self, folder_name='seismic_images'):
        self.folder = dataiku.Folder(folder_name)

    def find_by_number(self, section_type, number):
        path = f"{section_type.value}/{section_type.value}_{number}.png"
        stream = self.folder.get_download_stream(path)
        image_data = stream.read()
        return SeismicSection(section_type, number, image_data)
```

#### Langkah 4: Opsional — Ganti ke Database

Dataiku juga mendukung koneksi ke database (PostgreSQL, MySQL, dll). Jika data CSV sudah dimasukkan ke database melalui Dataiku:

```python
import dataiku

class WellRepository:
    def __init__(self, dataset_name='well_coordinates'):
        self.dataset_name = dataset_name

    def find_all(self):
        # Dataiku secara transparan membaca dari database
        # sama seperti membaca CSV — API-nya identik!
        dataset = dataiku.Dataset(self.dataset_name)
        df = dataset.get_dataframe(infer_with_pandas=False)
        return [WellCoordinate.from_dict(row.to_dict()) for _, row in df.iterrows()]
```

> 💡 **Keindahan Dataiku:** Baik sumber datanya CSV yang di-upload, file di S3, tabel PostgreSQL, atau dataset Snowflake — API `dataiku.Dataset().get_dataframe()` **sama saja**. Kamu tidak perlu tahu di balik layar data disimpan di mana.

### Yang TIDAK Berubah Saat Migrasi

| Layer | Berubah? | Alasan |
|-------|----------|--------|
| `routes/` | ❌ Tidak | Endpoint URL tetap sama |
| `controllers/` | ❌ Tidak | Logika HTTP handling tetap sama |
| `services/` | ❌ Tidak | Logika bisnis tetap sama |
| `repositories/` | ✅ **Ya** | Cara baca data berubah (CSV → Dataiku API) |
| `models/` | ❌ Tidak | Struktur data tetap sama |
| `dto/` | ❌ Tidak | Kontrak request/response tetap sama |
| `common/` | ❌ Tidak | Utility response tetap sama |
| `main.py` | ❌ Tidak | Entry point tetap sama |

> **Inilah kekuatan Clean Architecture:** hanya 4 file repository yang perlu dimodifikasi, dan seluruh API tetap berjalan seperti biasa.

---

## 🏗 Ringkasan Arsitektur

```
┌──────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                  (Flask App Factory)                          │
│           Membuat app, pasang CORS, daftarkan routes         │
└──────────────────────┬───────────────────────────────────────┘
                       │ register_blueprint()
          ┌────────────┼────────────┬──────────────┐
          ▼            ▼            ▼              ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
    │  well    │ │ well_log │ │ horizon  │ │seismic_section│
    │ routes   │ │ routes   │ │ routes   │ │   routes      │
    │ (4 URL)  │ │ (3 URL)  │ │ (2 URL)  │ │   (2 URL)     │
    └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────┬────────┘
         │            │            │               │
         ▼            ▼            ▼               ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
    │  well    │ │ well_log │ │ horizon  │ │seismic_section│
    │controller│ │controller│ │controller│ │  controller   │
    └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────┬────────┘
         │            │            │               │
         ▼            ▼            ▼               ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
    │  well    │ │ well_log │ │ horizon  │ │seismic_section│
    │ service  │ │ service  │ │ service  │ │   service     │
    └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────┬────────┘
         │            │            │               │
         ▼            ▼            ▼               ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
    │  well    │ │ well_log │ │ horizon  │ │seismic_section│
    │  repo    │ │  repo    │ │  repo    │ │    repo       │
    └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────┬────────┘
         │            │            │               │
         ▼            ▼            ▼               ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
    │ CSV file │ │ CSV file │ │ CSV file │ │  PNG files    │
    │ (well)   │ │(well_log)│ │(horizon) │ │(inline/xline)│
    └──────────┘ └──────────┘ └──────────┘ └──────────────┘
```

### Alur Development (Urutan Pembuatan)

```
1. 📐 Models        → "Bentuk datanya seperti apa?"
2. 📦 Repositories  → "Bagaimana cara baca dari CSV?"
3. 🧠 Services      → "Ada logika bisnis yang perlu diolah?"
4. 🎮 Controllers   → "Bagaimana menangani HTTP request/response?"
5. 🚪 Routes        → "URL endpoint-nya apa saja?"
6. 📋 DTOs          → "Kontrak tipe data untuk type safety"
7. 🔧 Common        → "Utility yang dipakai bersama-sama"
8. 🚀 main.py       → "Rangkai semuanya jadi satu aplikasi Flask!"
```

### Total Endpoint: **11 endpoint + 1 health check**

| # | Method | Endpoint | Fungsi |
|---|--------|----------|--------|
| 1 | GET | `/health` | Health check |
| 2 | GET | `/api/well` | Semua sumur |
| 3 | GET | `/api/well/summary` | Statistik sumur |
| 4 | GET | `/api/well/<name>` | Detail satu sumur |
| 5 | GET | `/api/well/<name>/exists` | Cek keberadaan sumur |
| 6 | GET | `/api/well-log` | Semua well log |
| 7 | GET | `/api/well-log-page` | Well log berpaginasi |
| 8 | GET | `/api/well-log/<name>` | Well log per sumur |
| 9 | GET | `/api/horizon` | Semua horizon |
| 10 | GET | `/api/horizon-page` | Horizon berpaginasi |
| 11 | GET | `/api/inline/<num>/image` | Gambar inline seismik |
| 12 | GET | `/api/crossline/<num>/image` | Gambar crossline seismik |

---

> **Kesimpulan:** Aplikasi ini dirancang dengan prinsip *separation of concerns* yang ketat. Setiap layer punya tanggung jawab tunggal, dan pergantian sumber data (dari CSV lokal ke Dataiku Dataset/Managed Folder/Database) hanya memerlukan perubahan di satu tempat: **Repository layer**. Ini membuat aplikasi mudah diuji, mudah dimaintain, dan siap untuk scale-up ke production di platform Dataiku.
