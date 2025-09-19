# 🌴 SawitPro FFB Management

**Modul Odoo untuk pengelolaan pengiriman, penimbangan, dan penjualan TBS (Tandan Buah Segar) kelapa sawit.**  
Mendukung integrasi penuh dengan *fleet*, *mill*, dan penjualan, serta menyediakan wizard untuk *bulk import* dan pembuatan **Sales Order** otomatis.

---

## 📝 Deskripsi
Modul **SawitPro FFB Management** membantu perusahaan kelapa sawit dalam:
- Mencatat pengiriman TBS secara detail.
- Mengelola harga TBS per *mill* dan per tanggal.
- Mengotomatisasi rekap harian dan konversinya menjadi **Sale Order**.

---

## 📂 Struktur Direktori

sawitpro_ffb_management/
├─ models/
│ ├─ daily_summary.py # Rekap harian pengiriman
│ ├─ delivery_order.py # Data pengiriman TBS
│ ├─ ffb_price.py # Harga TBS per mill
│ ├─ sale_enhanced.py # Fitur tambahan sale order
│ ├─ sale_integration.py # Integrasi rekap ke sale order
│ ├─ trip.py # Data perjalanan pengiriman
│ └─ weighbridge_receipt.py # Bukti penimbangan
│
├─ wizard/
│ ├─ bulk_import_wizard.py # Import data pengiriman CSV
│ └─ create_sales_from_summary_wizard.py # Buat sale order otomatis
│
├─ views/ # Form, tree, dashboard XML
├─ data/ # Sequence & cron job
├─ security/ # Hak akses & grup keamanan
└─ demo/ # Data demo untuk testing


---

## 🚀 Fitur Utama

- **Pengelolaan Delivery Order**  
  Input, update, dan rekap pengiriman TBS.

- **Rekap Harian Otomatis**  
  Rekap otomatis berdasarkan pengiriman yang sudah dikonfirmasi/delivered.

- **Integrasi Penjualan**  
  Rekap harian dapat langsung diubah menjadi *Sale Order* lengkap dengan harga sesuai *mill* dan tanggal.

- **Import Data Massal**  
  Wizard untuk import pengiriman dan penimbangan dari file CSV.

- **Manajemen Harga TBS**  
  Penentuan harga TBS per *mill* dan per tanggal.

- **Dashboard & Reporting**  
  Tampilan ringkas untuk memantau pengiriman dan penjualan.

---

## ⚙️ Instalasi

1. Salin folder `sawitpro_ffb_management` ke direktori `custom_addons` Odoo Anda.
2. Masuk ke **Apps** di Odoo, klik *Update Apps List*.
3. Cari **SawitPro FFB Management** dan klik **Install**.

---

## 💡 Cara Penggunaan

- **Pengiriman TBS**  
  Input data melalui menu **Delivery Order**.

- **Rekap Harian**  
  Jalankan fungsi rekap harian melalui menu atau otomatis via *cron job*.

- **Import CSV**  
  Gunakan wizard **Bulk Import** untuk memasukkan data pengiriman secara massal.

- **Penjualan Otomatis**  
  Gunakan wizard **Create Sales From Summary** untuk membuat *Sale Order* dari rekap harian.

---

## 🔐 Hak Akses
Pengaturan akses model terdapat di:
- `security/ir.model.access.csv`
- `security/security.xml`

---

