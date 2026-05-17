# Google Sheet Schema - TAPG Trading Dashboard

Create a new Google Sheet and rename the first tab to **"Data"**.

## Column Headers (Row 1)
| Column | Header Name | Description |
| :--- | :--- | :--- |
| A | `timestamp` | Last update time (WIB) |
| B | `eido_ah` | EIDO After Hours / Last Price |
| C | `eido_reg_close` | EIDO Regular Market Close |
| D | `eido_open` | EIDO Market Open |
| E | `shanghai_delta` | Shanghai Gap: (Open Today - Close Yesterday) |
| F | `shanghai_open` | Shanghai Open (Today) |
| G | `shanghai_close` | Shanghai Close (Yesterday) |
| H | `nifty_delta` | Nifty Performance: (Close - Open) Prev Session |
| I | `nifty_open` | Nifty Open (Yesterday) |
| J | `nifty_close` | Nifty Close (Yesterday) |
| K | `soybean_delta` | Soybean Performance: (Close - Open) Prev Session |
| L | `soybean_open` | Soybean Open (Yesterday) |
| M | `soybean_close` | Soybean Close (Yesterday) |
| N | `tapg_close` | TAPG.JK Current Price |
| O | `tapg_open` | TAPG.JK Open Price |
| P | `ma20_val` | TAPG 20-Day Moving Average |
| Q | `vwap_cur` | TAPG Current VWAP (Daily) |
| R | `vwap_prev` | TAPG Previous VWAP |
| S | `tapg_vol` | TAPG Current Volume |
| T | `vol_ma20` | TAPG 20-Day Average Volume |

## Setup Instructions
1. Create the sheet.
2. Put these headers in Row 1.
3. Use the **tapg_colab_pipeline.py** to populate Row 2.
4. Deploy **tapg_appscript.js** as a Web App to serve this data.
