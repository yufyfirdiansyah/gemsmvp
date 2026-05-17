# Google Sheet Schema - GEMS Trading Dashboard

Buat Google Sheet baru dan ubah nama tab pertama menjadi **"Data"**.

## Column Headers (Row 1)
| Column | Header Name | Description |
| :--- | :--- | :--- |
| A | `timestamp` | Waktu update terakhir (WIB) |
| B | `fxi_delta` | Perubahan FXI (%) - Sinyal Demand China |
| C | `fxi_last` | Harga terakhir FXI |
| D | `ng_delta` | Perubahan Natural Gas (%) - Sinyal Substitusi |
| E | `ng_last` | Harga terakhir Natural Gas (NG=F) |
| F | `usdidr_delta` | Perubahan Kurs USD/IDR (%) |
| G | `usdidr_last` | Kurs terakhir USD/IDR |
| H | `btu_delta` | Perubahan BTU (NYSE) - Sinyal Sentimen Coal Global |
| I | `btu_last` | Harga close BTU (Jam 04:00 WIB) |
| J | `whc_delta` | Perubahan WHC.AX (ASX) - Proxy Harga Coal Newcastle |
| K | `whc_last` | Harga WHC.AX (Jam 08:00 WIB) |
| L | `gems_close` | Harga Terakhir GEMS.JK |
| M | `gems_open` | Harga Open GEMS.JK |
| N | `gems_ma20` | Moving Average 20 Hari GEMS |
| O | `gems_vwap_cur` | VWAP GEMS Hari Ini |
| P | `gems_vwap_prev` | VWAP GEMS Kemarin |
| Q | `gems_vol` | Volume GEMS Hari Ini |
| R | `gems_vol_ma20` | Rata-rata Volume 20 Hari GEMS |

## Instruksi Setup
1. Buat sheet baru.
2. Masukkan header di atas pada Baris 1.
3. Gunakan **gems_colab_pipeline.py** untuk mengisi Baris 2.
4. Deploy **gems_appscript.js** sebagai Web App.
