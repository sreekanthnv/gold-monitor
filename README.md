# Gold Monitor

A lightweight web app that tracks daily gold rates in India from multiple sources,
with a clean mobile- and web-friendly UI. Deployed on Vercel.

🔗 **Live demo:** [gold-monitor-omega.vercel.app](https://gold-monitor-omega.vercel.app)

## What it does

Fetches and compares 22K and 24K gold rates from several sources in real time, so you
can see jeweller quotes alongside an international spot-price cross-check:

- **Malabar Gold** — live retail rates (server-side fetch)
- **Kalyan Jewellers** — live retail rates, Bangalore (server-side fetch)
- **International Spot** — calculated from the live USD spot price and USD→INR rate,
  with ~15% import duty applied (cross-check, not a jeweller quote)

The app shows per-gram and per-10g prices for both 22K and 24K, with GST (3%) calculated
separately, plus a live status indicator and auto-refresh.

## How it works

- **Backend** (`api/`): a serverless Python handler calls three public rate endpoints on
  each request, normalises messy rate strings into clean values, falls back to a
  calculated 24K→22K conversion when a source omits a value, and returns one JSON payload
  (CORS enabled). Each source is fetched independently, so one failing never breaks the response.
- **Frontend** (`index.html`): single-file HTML/CSS/JS — averages the live quotes, renders
  per-source cards with live/calculated/failed states, and auto-refreshes every 15 minutes.

## Tech stack

`Python` (http.server, requests) · Serverless functions on `Vercel` · vanilla `HTML`/`CSS`/`JS`

## Project structure
gold-monitor/

├── api/              # serverless Python handler — fetches & aggregates rates

├── index.html        # single-file front-end UI

├── requirements.txt  # Python dependencies (requests)

└── vercel.json       # Vercel deployment config

## Running locally

```bash
git clone https://github.com/sreekanthnv/gold-monitor.git
cd gold-monitor
pip install -r requirements.txt
vercel dev        # run the serverless function + static site locally
```

No API keys required — all data sources are public endpoints.

## Notes

- Prices shown are **base metal rates**; jewellers add making charges (₹150–₹1,500/g) on top.
- The International Spot figure is an estimate (spot + import duty), not a retail quote.
- Third-party rate endpoints may change without notice.

## Author

**Sreekanth Nagar Vasudev** — AI Quality & Validation Engineer · [GitHub](https://github.com/sreekanthnv)
