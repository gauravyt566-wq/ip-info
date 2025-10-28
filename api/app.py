from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def lookup_ip(ip_or_me: str):
    """IP ya 'me' ke hisaab se IP lookup kare."""
    if not ip_or_me or ip_or_me.strip().lower() in ("", "me", "my"):
        url = "http://ip-api.com/json/"
    else:
        url = f"http://ip-api.com/json/{ip_or_me.strip()}"

    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

@app.route("/")
def home():
    """Home endpoint with usage info."""
    return jsonify({
        "message": "Welcome to IP Lookup API 🌍",
        "usage": "Use /lookup?ip=8.8.8.8 or /lookup?ip=me",
        "author": "@ITZ_GAURAVYT"
    })

@app.route("/lookup", methods=["GET"])
def lookup():
    """Main lookup endpoint."""
    ip = request.args.get("ip", "").strip()
    try:
        data = lookup_ip(ip)

        # Agar IP invalid ho ya result fail aaye
        if data.get("status") != "success":
            return jsonify({
                "status": "fail",
                "message": f"Invalid IP address: '{ip}' or lookup failed.",
                "query": ip
            }), 400

        # Agar valid response mila
        return jsonify(data), 200

    except requests.RequestException as e:
        return jsonify({
            "status": "error",
            "message": "Network error while connecting to IP-API.",
            "details": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Unexpected server error occurred.",
            "details": str(e)
        }), 500
