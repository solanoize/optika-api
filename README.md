# Optika API

Optika API adalah backend REST API yang dibangun menggunakan Django dan Django REST Framework. Proyek ini menyediakan fungsionalitas untuk mengelola inventaris, pelanggan, pesanan, dan pembelian untuk toko ritel, khususnya toko kacamata atau optik.

API ini sudah terotentikasi menggunakan JSON Web Tokens (JWT) dan menyertakan endpoint untuk mengelola produk, pelanggan, pesanan penjualan, pesanan pembelian, dan pergerakan stok.

## Fitur Utama

- **Manajemen Produk**: Membuat, melihat, memperbarui, dan menghapus produk.
- **Manajemen Pelanggan**: Mengelola data pelanggan.
- **Manajemen Pesanan**: Membuat pesanan penjualan dan melihat detailnya, termasuk item pesanan.
- **Manajemen Pembelian**: Melacak pesanan pembelian dari pemasok.
- **Manajemen Stok**: Secara otomatis melacak pergerakan stok (masuk, keluar, penyesuaian) yang terkait dengan pesanan dan pembelian.
- **Otentikasi**: Sistem otentikasi aman menggunakan JWT.

---

## Teknologi yang Digunakan

- Python
- Django
- Django REST Framework
- Simple JWT for Django REST Framework
- MySQL (via `mysqlclient`)
- `python-dotenv` untuk manajemen environment

---

## Pengaturan dan Instalasi

Ikuti langkah-langkah ini untuk menjalankan proyek ini di lingkungan lokal Anda.

### 1. Prasyarat

- Python 3.9+
- Pip (manajer paket Python)
- Git
- Server Database MySQL

### 2. Clone Repositori

```bash
git clone <URL_REPOSITORI_ANDA>
cd glaser-api
```

### 3. Buat dan Aktifkan Virtual Environment

Sangat disarankan untuk menggunakan lingkungan virtual (virtual environment) untuk mengisolasi dependensi proyek.

**Di Windows:**
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

**Di macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instal Dependensi

Gunakan `pip` untuk menginstal semua paket yang diperlukan dari file `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 5. Konfigurasi Environment (.env)

Proyek ini menggunakan file `.env` untuk mengelola variabel lingkungan yang sensitif dan spesifik untuk setiap environment. Anda perlu membuat file ini secara manual.

a. Buat file bernama `.env` di direktori root proyek.

b. Salin dan tempel konten berikut ke dalam file `.env` Anda dan isi nilainya sesuai dengan pengaturan lokal Anda.

```env
# === CORE ===
SECRET_KEY=<yourkey>
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# === DATABASE (MySQL) ===
DB_NAME=<yourdb>
DB_USER=root
DB_PASSWORD=<yourpassword>
DB_HOST=127.0.0.1
DB_PORT=3306

# === CORS ===
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5500,http://localhost:3000

# === TOKEN LIFE TIME ===
TOKEN_IN_DAYS=90
```
**Penting:** Pastikan file `.env` ditambahkan ke `.gitignore` Anda agar tidak terekspos di repositori Git Anda.

### 6. Jalankan Migrasi Database

Setelah database Anda dikonfigurasi di file `.env`, jalankan migrasi Django untuk membuat skema tabel.

```bash
python manage.py migrate
```

### 7. Buat Superuser (Opsional)

Untuk mengakses antarmuka admin Django, Anda perlu membuat superuser.

```bash
python manage.py createsuperuser
```

### 8. Jalankan Server Pengembangan

Sekarang Anda siap untuk menjalankan server.

```bash
python manage.py runserver
```

Server akan berjalan di `http://127.0.0.1:8000`.

---

## Endpoint API

Berikut adalah endpoint utama yang tersedia. Semua endpoint berada di bawah prefix `/api/optika/`.

- **Otentikasi**
  - `POST /api/token/`: Dapatkan token JWT (berikan `username` dan `password`).
  - `POST /api/token/refresh/`: Refresh token JWT yang sudah ada.

- **Produk**
  - `GET /api/optika/products/`
  - `POST /api/optika/products/`
  - `GET /api/optika/products/<int:pk>/`
  - `PUT /api/optika/products/<int:pk>/`
  - `DELETE /api/optika/products/<int:pk>/`

- **Pelanggan**
  - `GET /api/optika/customers/`
  - `POST /api/optika/customers/`
  - `GET /api/optika/customers/<int:pk>/`
  - `PUT /api/optika/customers/<int:pk>/`
  - `DELETE /api/optika/customers/<int:pk>/`

- **Pesanan**
  - `GET /api/optika/orders/`
  - `POST /api/optika/orders/`
  - `GET /api/optika/orders/<str:order_number>/`

- **Pembelian**
  - `GET /api/optika/purchases/`
  - `POST /api/optika/purchases/`
  - `GET /api/optika/purchases/<str:purchase_number>/`

- **Pergerakan Stok**
  - `GET /api/optika/stock-movements/`

---

## Insomnia Collection

Proyek ini menyertakan file ekspor Insomnia (`Insomnia_Optika_API_2025-11-23.json`) yang berisi koleksi semua endpoint API yang telah dikonfigurasi sebelumnya untuk pengujian yang mudah.

Untuk menggunakannya:
1. Buka Insomnia.
2. Buka `Preferences` > `Data`.
3. Klik `Import Data` > `From File`.
4. Pilih file `Insomnia_Optika_API_2025-11-23.json` dari direktori proyek.

Ini akan mengimpor semua request API, termasuk otentikasi.

**Konfigurasi Lingkungan (Environment) Insomnia:**
Setelah mengimpor koleksi, Anda perlu mengkonfigurasi environment di Insomnia. Buat environment baru atau edit environment yang sudah ada dan tambahkan variabel berikut:

- `BASE_URL`: URL dasar API Anda. Contoh: `http://localhost:8000`
- `TOKEN`: Token autentikasi JWT Anda (akan diisi setelah login).
- `PREFIX_TOKEN`: Prefiks untuk token (biasanya `Bearer`).
- `APPLICATION_NAMESPACE`: Namespace aplikasi (sesuai dengan konfigurasi URL Anda, misalnya `api/optika`).

---

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT.

```
MIT License

Copyright (c) 2025 Alasware

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```