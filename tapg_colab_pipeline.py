# Run this in Google Colab!
# 1. Install dependencies
# !pip install gspread yfinance pytz

import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

from google.colab import auth
import gspread
from google.auth import default

# 2. Authenticate and open the Google Sheet
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# !!! REPLACE THIS URL WITH YOUR NEW GOOGLE SHEET URL !!!
SHEET_URL = "https://docs.google.com/spreadsheets/d/1THtNx9WrDlhR2C3mQOrXXYdqW3bMpBowf2iQoWFi62M/edit"
worksheet = gc.open_by_url(SHEET_URL).worksheet("Data")

def fetch_data(ticker_symbol, period="3mo"):
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period=period)
    return df

print("Fetching data...")
tapg = fetch_data("TAPG.JK")
eido = fetch_data("EIDO")
shanghai = fetch_data("000001.SS")
nifty = fetch_data("^NSEI")
soybean = fetch_data("ZS=F")

print("Calculating technical indicators & specific deltas...")

# --- TAPG Technicals ---
tapg_close = float(tapg['Close'].iloc[-1])
tapg_open = float(tapg['Open'].iloc[-1])
tapg_vol = float(tapg['Volume'].iloc[-1])
vol_ma20 = float(tapg['Volume'].rolling(window=20).mean().iloc[-1])
ma20_val = float(tapg['Close'].rolling(window=20).mean().iloc[-1])

# VWAP Approximation
tapg_typical = (tapg['High'] + tapg['Low'] + tapg['Close']) / 3
tapg['vwap'] = (tapg_typical * tapg['Volume']).cumsum() / tapg['Volume'].cumsum()
vwap_cur = float(tapg['vwap'].iloc[-1])
vwap_prev = float(tapg['vwap'].iloc[-2])

# --- EIDO Macros (Original Logic) ---
eido_reg_close = float(eido['Close'].iloc[-1])
eido_open = float(eido['Open'].iloc[-1])
try:
    eido_ah_data = yf.Ticker("EIDO").history(period="2d", interval="15m", prepost=True)
    eido_ah = float(eido_ah_data['Close'].iloc[-1])
except:
    eido_ah = eido_reg_close

# --- Shanghai Logic (Gap: Open Today - Close Yesterday) ---
sh_open_today = float(shanghai['Open'].iloc[-1])
sh_close_yesterday = float(shanghai['Close'].iloc[-2])
sh_delta = sh_open_today - sh_close_yesterday
sh_delta_str = f"{((sh_delta / sh_close_yesterday) * 100):.2f}%"

# --- Nifty Logic (Session: Close Yesterday - Open Yesterday) ---
ni_close_prev = float(nifty['Close'].iloc[-1])
ni_open_prev = float(nifty['Open'].iloc[-1])
ni_delta = ni_close_prev - ni_open_prev
ni_delta_str = f"{((ni_delta / ni_open_prev) * 100):.2f}%"

# --- Soybean Logic (Session: Close Yesterday - Open Yesterday) ---
sb_close_prev = float(soybean['Close'].iloc[-1])
sb_open_prev = float(soybean['Open'].iloc[-1])
sb_delta = sb_close_prev - sb_open_prev
sb_delta_str = f"{((sb_delta / sb_open_prev) * 100):.2f}%"

# --- Prepare Payload ---
timestamp = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d %H:%M:%S")

payload = [
    timestamp,
    eido_ah, eido_reg_close, eido_open,
    sh_delta_str, sh_open_today, sh_close_yesterday,
    ni_delta_str, ni_open_prev, ni_close_prev,
    sb_delta_str, sb_open_prev, sb_close_prev,
    tapg_close, tapg_open, ma20_val, vwap_cur, vwap_prev, tapg_vol, vol_ma20
]

# --- Update Sheet Headers & Data ---
expected_headers = [
    "timestamp", "eido_ah", "eido_reg_close", "eido_open",
    "shanghai_delta", "shanghai_open", "shanghai_close",
    "nifty_delta", "nifty_open", "nifty_close",
    "soybean_delta", "soybean_open", "soybean_close",
    "tapg_close", "tapg_open", "ma20_val", "vwap_cur", "vwap_prev", "tapg_vol", "vol_ma20"
]

print("Checking headers in Row 1...")
try:
    current_headers = worksheet.row_values(1)
except Exception:
    current_headers = []

# If Row 1 is empty or headers mismatch, write headers
if not current_headers or current_headers != expected_headers:
    print("Writing headers to Row 1...")
    worksheet.update('A1:T1', [expected_headers])
else:
    print("Headers already correct. Skipping header update.")

print("Pushing latest data to Row 2...")
worksheet.update('A2:T2', [payload])

print(f"✅ Successfully updated TAPG Sheet at {timestamp}!")
