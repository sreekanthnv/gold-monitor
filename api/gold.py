from http.server import BaseHTTPRequestHandler
import json, re, sys

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

HDR = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

def num(s):
    v = re.sub(r"[^\d.]", "", str(s))
    return round(float(v)) if v else None

def malabar():
    r = requests.post(
        "https://www.malabargoldanddiamonds.com/malabarprice/index/getrates/?country=IN&state=Kerala",
        headers={**HDR, "Referer": "https://www.malabargoldanddiamonds.com/goldprice"},
        timeout=10,
    )
    d = r.json()
    k22, k24 = num(d["22kt"]), num(d["24kt"])
    return {"name": "Malabar Gold", "domain": "malabargoldanddiamonds.com",
            "k22": k22, "k24": k24, "note": d.get("updated_time", ""), "status": "ok"}

def kalyan():
    r = requests.post(
        "https://www.kalyanjewellers.net/kalyan_gold_rates/ajax/get_rate",
        data={"countryId": "1", "stateId": "8", "cityId": "40"},
        headers={**HDR, "Referer": "https://www.kalyanjewellers.net/gold-rate/Gold-Rate-Today"},
        timeout=10,
    )
    d = r.json()
    k22 = num(d.get("today_22k", ""))
    raw24 = d.get("today_24k", "N/A")
    k24 = num(raw24) if raw24 not in ("N/A", None, "") else (round(k22 * 24 / 22) if k22 else None)
    return {"name": "Kalyan Jewellers", "domain": "kalyanjewellers.net · Bangalore",
            "k22": k22, "k24": k24, "note": d.get("updated_time", ""), "status": "ok"}

def spot():
    sr = requests.get("https://api.metals.live/v1/spot/gold", timeout=10)
    fr = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
    sd = sr.json()
    price = sd[0]["gold"] if isinstance(sd, list) else (sd.get("price") or sd.get("gold"))
    fx = fr.json()["rates"]["INR"]
    base24 = (price / 31.1035) * fx * 1.15 * 1.0075
    k24 = round(base24)
    k22 = round(k24 * 22 / 24)
    return {"name": "International Spot", "domain": f"${price:.0f}/oz · ₹{fx:.1f}/USD · +15% import duty",
            "k22": k22, "k24": k24, "note": "Calculated — not a jeweller quote", "status": "calc"}

SOURCES = [malabar, kalyan, spot]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        results = []
        for fn in SOURCES:
            try:
                results.append(fn())
            except Exception as e:
                results.append({"name": fn.__name__.title(), "domain": "",
                                "status": "error", "error": str(e)})

        body = json.dumps(results, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass
