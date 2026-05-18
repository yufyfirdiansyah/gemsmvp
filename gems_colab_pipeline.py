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

def get_delta(df):
    if df.empty: return 0, "0.00%"
    last = float(df['Close'].iloc[-1])
    prev = float(df['Close'].iloc[-2])
    delta = ((last - prev) / prev) * 100
    return last, f"{delta:+.2f}%"

print("Fetching GEMS and Macro data...")
gems = fetch_data("GEMS.JK")

# Clean GEMS data by removing trailing rows with 0 volume (incomplete/pre-market days)
original_len = len(gems)
while not gems.empty and (gems['Volume'].iloc[-1] == 0 or pd.isna(gems['Volume'].iloc[-1])):
    gems = gems.iloc[:-1]
if len(gems) < original_len:
    print(f"⚠️ Dropped {original_len - len(gems)} trailing row(s) with 0 volume. Using last active trading day's data.")

fxi = fetch_data("FXI")
ng = fetch_data("NG=F")
usdidr = fetch_data("USDIDR=X")
btu = fetch_data("BTU")
whc = fetch_data("WHC.AX")

print("Calculating GEMS Technicals...")
# --- GEMS Technicals ---
gems_close = float(gems['Close'].iloc[-1])
gems_open = float(gems['Open'].iloc[-1])
gems_vol = float(gems['Volume'].iloc[-1])
gems_ma20 = float(gems['Close'].rolling(window=20).mean().iloc[-1])
gems_vol_ma20 = float(gems['Volume'].rolling(window=20).mean().iloc[-1])

# VWAP Approximation
gems_typical = (gems['High'] + gems['Low'] + gems['Close']) / 3
gems['vwap'] = (gems_typical * gems['Volume']).cumsum() / gems['Volume'].cumsum()
vwap_cur = float(gems['vwap'].iloc[-1])
vwap_prev = float(gems['vwap'].iloc[-2])

print("Calculating Macro Deltas...")
fxi_last, fxi_delta = get_delta(fxi)
ng_last, ng_delta = get_delta(ng)
usdidr_last, usdidr_delta = get_delta(usdidr)
btu_last, btu_delta = get_delta(btu)
whc_last, whc_delta = get_delta(whc)

# --- Prepare Payload ---
timestamp = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d %H:%M:%S")

payload = [
    timestamp,
    fxi_delta, fxi_last,
    ng_delta, ng_last,
    usdidr_delta, usdidr_last,
    btu_delta, btu_last,
    whc_delta, whc_last,
    gems_close, gems_open, gems_ma20, vwap_cur, vwap_prev, gems_vol, gems_vol_ma20
]

# --- Update Sheet Headers & Data ---
expected_headers = [
    "timestamp", "fxi_delta", "fxi_last",
    "ng_delta", "ng_last",
    "usdidr_delta", "usdidr_last",
    "btu_delta", "btu_last",
    "whc_delta", "whc_last",
    "gems_close", "gems_open", "gems_ma20", "gems_vwap_cur", "gems_vwap_prev", "gems_vol", "gems_vol_ma20"
]

print("Checking headers in Row 1...")
try:
    current_headers = worksheet.row_values(1)
except Exception:
    current_headers = []

if not current_headers or current_headers != expected_headers:
    print("Writing headers to Row 1...")
    worksheet.update('A1:R1', [expected_headers])
else:
    print("Headers already correct.")

print("Pushing latest data to Row 2...")
worksheet.update('A2:R2', [payload])

print(f"✅ GEMS Pipeline Sync Success at {timestamp}!")
