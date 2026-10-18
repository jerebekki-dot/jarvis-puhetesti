# JARVIS voice service

Separate Render **free** Python web service, root directory `voice-server`, build command `pip install -r requirements.txt`, start command `gunicorn --bind 0.0.0.0:$PORT app:app`.

Environment secret: `ELEVENLABS_API_KEY` from your own ElevenLabs account. Never commit it to GitHub. Voice ID default is Adam `IRHApOXLvnW57QJPQH2P`.

When Render issues URL, set `JARVIS_VOICE_ENDPOINT` in `index.html` to `https://<render-service>.onrender.com/speak` and commit. Until then JARVIS uses browser speech and clearly labels it as a fallback.

**Important:** This is a limited personal prototype, not a secure publicly exposed paid API. CORS is not authentication; someone can imitate the Origin header and consume your ElevenLabs quota. For real deployment add server-side authentication, quotas, monitoring and billing safeguards. Render free service may sleep. Do not enable paid plans without explicit consent.
