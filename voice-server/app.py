"""JARVIS ElevenLabs voice proxy. Never place credentials in public HTML."""
import os
import hmac
import time
import threading
from collections import defaultdict, deque
from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "IRHApOXLvnW57QJPQH2P")
ALLOWED_ORIGIN = "https://jerebekki-dot.github.io"
RATE_LIMIT = 10
hits = defaultdict(deque)
lock = threading.Lock()

@app.after_request
def cors(response):
    if request.headers.get("Origin") == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
        response.headers["Vary"] = "Origin"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/health")
def health():
    return jsonify(status="ok",voice_configured=bool(os.getenv("ELEVENLABS_API_KEY")))

@app.route("/speak", methods=["OPTIONS"])
def options():
    if request.headers.get("Origin") != ALLOWED_ORIGIN:
        return jsonify(error="origin not allowed"), 403
    resp = Response(status=204)
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Jarvis-Token"
    resp.headers["Access-Control-Max-Age"] = "600"
    return resp

@app.route("/speak", methods=["POST"])
def speak():
    if request.headers.get("Origin") != ALLOWED_ORIGIN:
        return jsonify(error="origin not allowed"), 403
    expected = os.getenv("JARVIS_ACCESS_TOKEN", "")
    received = request.headers.get("X-Jarvis-Token", "")
    if len(expected) < 24 or not hmac.compare_digest(expected, received):
        return jsonify(error="not authorized"), 401
    key = os.getenv("ELEVENLABS_API_KEY")
    if not key:
        return jsonify(error="voice not configured"), 503
    if not request.is_json:
        return jsonify(error="json expected"), 415
    data = request.get_json(silent=True) or {}
    message = data.get("text")
    if not isinstance(message, str) or not 1 <= len(message.strip()) <= 280:
        return jsonify(error="text length must be 1-280"), 400
    # Browser origin is not authentication; also restrict usage in production.
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "").split(",")[0].strip()
    now = time.monotonic()
    with lock:
        q = hits[ip]
        while q and now-q[0] > 3600:
            q.popleft()
        if len(q) >= RATE_LIMIT:
            return jsonify(error="hourly voice limit"), 429
        q.append(now)
    try:
        result = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            headers={"xi-api-key":key,"Accept":"audio/mpeg","Content-Type":"application/json"},
            json={"text":message.strip(),"model_id":"eleven_multilingual_v2",
                  "voice_settings":{"stability":0.65,"similarity_boost":0.8,"style":0}},
            timeout=30)
        if result.status_code != 200:
            app.logger.warning("voice service failed: %s",result.status_code)
            return jsonify(error="voice service unavailable"), 502
        return Response(result.content, mimetype="audio/mpeg")
    except requests.RequestException:
        return jsonify(error="voice network error"), 502

if __name__=="__main__":
    app.run(port=int(os.getenv("PORT","10000")))
