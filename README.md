# TirnBot - Bot Auto Bridge Multi-Chain (Arbitrum Sepolia, OP Sepolia, Base Sepolia)

TirnBot adalah bot otomatis yang melakukan bridging token di antara beberapa jaringan, termasuk 
Arbitrum Sepolia, OP Sepolia, dan Base Sepolia. Bot ini dirancang untuk memudahkan 
transfer token antarjaringan dengan cepat dan efisien.

## Fitur
- **Auto Bridging Multi-Chain:** Mengotomatisasi proses bridging dari Arbitrum Sepolia, OP Sepolia, dan Base Sepolia.
- **Notifikasi Transaksi Real-Time:** Menampilkan hasil transaksi yang berhasil secara real-time dengan detail seperti hash transaksi, jumlah ETH yang dikirim, dan total transaksi yang sukses.
- **Penandaan Jaringan dengan Warna:** Output menampilkan warna berbeda untuk setiap jaringan (Arbitrum, OP, Base) agar mudah diidentifikasi.
- **Pengecekan Koneksi Jaringan:** Bot akan memeriksa apakah terhubung ke setiap jaringan sebelum  memulai proses bridging.
- **Retry Transaksi:** Jika ada kegagalan dalam perkiraan gas atau pengiriman transaksi, bot akan menampilkan pesan kesalahan.

## Persyaratan
- Python 3.7 atau lebih tinggi
- `web3.py`
- `eth_account`
  
## Instalasi

1. Clone repository ini ke lokal Anda:

   ```bash
   git clone https://github.com/fadhilahmadd/t3rnTx-bot.git
   ```

2. Masuk ke direktori proyek:
   ```bash
   cd t3rnTx-bot
   ```

3. Install dependencies yang diperlukan:
   ```bash
   pip install web3 colorama
   ```

## Konfigurasi

1. Ganti `pripatkey`, `addrss`, dan `labels` dengan kunci pribadi dan alamat Anda di file 
   `keys_and_addresses.py`.

2. Atur konfigurasi jaringan dan alamat kontrak di file `network_config.py` sesuai dengan jaringan 
   yang ingin Anda gunakan.
   
3. Ubah data `data_bridge.py` dengan cara lakukan swap manual pada jaringan yang ingin diambil data HEX nya lalu ketika sukses, cek data pada txhash, lihat contoh screenshot
 ![TirnBot Screenshot](https://github.com/AI-EXC/t3rnTx-bot/blob/main/tirn2.PNG?raw=true)

## Cara Penggunaan

1. Jalankan bot dengan perintah berikut:
   
   ```bash
   python app.py
   ```

2. Bot akan secara otomatis melakukan bridging antarjaringan sesuai dengan konfigurasi yang telah 
   diatur.

## Catatan
- Bot ini dapat dihentikan kapan saja dengan menggunakan kombinasi **Ctrl + C** di terminal.
- Bot ini saya set min sepolia balance di OP, Base, Arb min 1.0 ETH. (untuk sisa di executor)

## Kontribusi
Silahkan pull request untuk kontribusi atau menambah fitur. PULL REQ JIKA BISA JARINGAN BLAST GAES

## TENJIN🚀
