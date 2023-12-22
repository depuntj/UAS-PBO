# Project UAS inventory Manager dengan DB postgres

---

Program Manajemen Inventaris dibuat menggunakan python, pyqt untuk user interface dan postgresql untuk database

### Instalasi dan Setup

Untuk dapat menjalankan projek Manajemen Inventoris, pengguna perlu melakukan beberapa langkah penginstalan dan konfigurasi, agar aplikasi ini bisa berjalan dengan baik. berikut langkah-langkah yang perlu dilakukan.

1. **Klon repositori ke mesin lokal**

   Untuk melakukan klon repository program Manajemen Inventaris, pengguna bisa menjalankan command berikut di terminal komputer sesuai sistem operasi yang digunakan.

   ```
   git clone https://github.com/depuntj/UAS-PBO.git
   ```

2. **Masuk ke folder projek**

   Setelah repository berhasil dikloning, pengguna bisa masuk ke folder tersebut, dengan mengetikkan command berikut.

   ```
   cd .\UAS-PBO\
   ```

3. **Install paket yang diperlukan**

   Sebelum paket-paket yang diperlukan belum terinstal, maka aplikasi Manajemen Inventaris tidak akan bisa dijalankan di komputer pengguna, sehingga pengguna perlu menginstal beberapa paket yang diperlukan. Untuk itu pengguna bisa mengetikkan command berikut.

   ```
   pip install -r requirements.txt
   ```

4. **Jalankan server database postgresql**

   Setelah paket-paket yang diperlukan berhasil diinstal, pengguna masih perlu melakukan beberapa langkah agar aplikasi terkoneksi ke database. Pengguna bisa menjalankan server database postgresql secara lokal dengan konfigurasi database seperti yang telah tertera pada file .env.local. server bisa dijalankan melalui terminal ataupun software seperti laragon.

5. **Jalankan file main.py**

   Kemudian pengguna bisa menuju file main.py dan menjalankan file tersebut dengan command

   ```
   python main.py
   ```

   atau jika pengguna menggunakan visual studio code, pengguna bisa menginstall extension code runner dan menjalankan kode main.py dengan mengklik tombol run pada kanan atas jendela visual studio code.
