# Rubik's Cube 3D - Interactive

## Deskripsi Proyek
Proyek ini adalah simulasi interaktif Rubik's Cube 3D yang dibangun menggunakan Python dan OpenGL (PyOpenGL). Aplikasi ini memungkinkan pengguna untuk memutar kubus, memilih sisi, melakukan rotasi sisi (searah atau berlawanan jarum jam), dan menyelesaikan kubus secara otomatis dengan membalikkan langkah-langkah sebelumnya. Proyek ini dirancang dengan struktur modular untuk memisahkan logika rendering, animasi, input pengguna, pengelolaan warna, dan variabel global.

### Fitur
- **Rendering 3D**: Menampilkan Rubik's Cube dengan warna standar (Oranye, Merah, Biru, Kuning, Hijau, Putih).
- **Interaksi Pengguna**:
  - Klik kiri untuk memilih sisi.
  - Tombol 'a' untuk rotasi berlawanan jarum jam, 'd' untuk searah jarum jam.
  - Tombol 'r' untuk menyelesaikan kubus dengan membalikkan langkah-langkah.
  - Drag Rotation menggunakan mouse untuk memutar tampilan kubus.
  - Roda mouse untuk zoom in/out.
- **Animasi Rotasi**: Animasi halus saat sisi diputar.
- **Validasi Kubus**: Memastikan setiap warna muncul tepat 9 kali setelah rotasi.

### Struktur File
- `rubik.py`: File utama untuk inisialisasi OpenGL dan pengaturan callback.
- `rubik_utils.py`: Mengelola animasi rotasi dan langkah penyelesaian.
- `rubik_globals.py`: Menyimpan variabel global seperti sudut, zoom, dan status kubus.
- `rubik_color_holder.py`: Mengelola warna kubus dan logika rotasi sisi.
- `rubik_input_handler.py`: Menangani input pengguna (mouse dan keyboard).
- `rubik_renderer.py`: Menangani rendering kubus dan deteksi sisi.

## Instalasi
 **Instal Dependensi**:
   Jalankan perintah berikut untuk menginstal dependensi:
   ```bash
   pip install PyOpenGL PyOpenGL_accelerate numpy
   ```

## Cara Menjalankan
1. **Navigasi ke Direktori Proyek**:
   Buka terminal atau command prompt, lalu masuk ke direktori proyek:
   ```bash
   cd path/to/rubiks-cube-project
   ```

2. **Jalankan Aplikasi**:
   Jalankan file utama `rubik.py`:
   ```bash
   python rubik.py
   ```

3. **Interaksi dengan Aplikasi**:
   - **Memilih Sisi**: Klik kiri pada sisi kubus yang ingin diputar.
   - **Rotasi Sisi**:
     - Tekan 'd' untuk memutar sisi searah jarum jam.
     - Tekan 'a' untuk memutar sisi berlawanan jarum jam.
   - **Menyelesaikan Kubus**: Tekan 'r' untuk membalikkan semua langkah sebelumnya secara otomatis.
   - **Memutar Tampilan**:
     - Tahan klik kiri dan gerakkan mouse untuk memutar kubus.
     - Gunakan roda mouse untuk zoom in/out.
