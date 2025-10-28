from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def lookup_ip(ip_or_me: str):
    # agar user ne 'me' ya blank diya to apna IP fetch kare
    if not ip_or_me or ip_or_me.strip().lower() in ("", "me", "my"):
        url = "http://ip-api.com/json/"
    else:
        url = f"http://ip-api.com/json/{ip_or_me.strip()}"

    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Public IP Lookup API 🌍",
        "usage": "/lookup?ip=8.8.8.8 or /lookup?ip=me",
        "author": "@ITZ_GAURAVYT"
    })

@app.route("/lookup", methods=["GET"])
def lookup():
    ip = request.args.get("ip", "").strip()
    try:
        data = lookup_ip(ip)
        if data.get("status") != "success":
            return jsonify({"error": "Lookup failed", "info": data}), 400
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": "Network error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

if __name__ == "__main__":
    # For local / termux testing
    app.run(host="0.0.0.0", port=8080)
