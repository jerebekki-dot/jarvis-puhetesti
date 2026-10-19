#!/usr/bin/env python3
"""Extract inline script from JARVIS HTML for Node syntax verification."""
from html.parser import HTMLParser
from pathlib import Path
import sys

class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.blocks = []
    def handle_starttag(self, tag, attrs):
        if tag == "script" and not dict(attrs).get("src"):
            self.capture = True
            self.blocks.append("")
    def handle_endtag(self, tag):
        if tag == "script":
            self.capture = False
    def handle_data(self, data):
        if self.capture:
            self.blocks[-1] += data

def main():
    page = Path("index.html").read_text(encoding="utf-8")
    parser = Scripts()
    parser.feed(page)
    assert parser.blocks, "Inline JavaScript missing"
    joined = "\n;\n".join(parser.blocks)
    Path("/tmp/jarvis_inline_check.js").write_text(joined, encoding="utf-8")
    for needle in ("SpeechRecognition", "currentVersion='3.0-dev.1'", "function scheduleListen", "logDiagnostic", "setVisualState"):
        assert needle in joined, f"Missing expected feature: {needle}"
    print("JARVIS static feature assertions OK")

if __name__ == "__main__":
    main()
