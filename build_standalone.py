import base64, sys, os

SRC = "oxygen-island-prototype.html"
OUT = "oxygen-island-standalone.html"

vids = {
    "videos/plage-artificielle.mp4": "videos/plage-artificielle.mp4",
    "videos/dj.mp4": "videos/dj.mp4",
    "videos/restauration.mp4": "videos/restauration.mp4",
    "videos/news.mp4": "videos/news.mp4",
}

with open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

count = 0
for path in vids:
    if not os.path.exists(path):
        print("MISSING:", path); sys.exit(1)
    with open(path, "rb") as vf:
        b64 = base64.b64encode(vf.read()).decode("ascii")
    needle = 'src="%s" type="video/mp4"' % path
    replacement = 'src="data:video/mp4;base64,%s" type="video/mp4"' % b64
    if needle not in html:
        print("NEEDLE NOT FOUND:", needle); sys.exit(1)
    html = html.replace(needle, replacement, 1)
    count += 1
    print("embedded", path, "->", len(b64), "b64 chars")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("DONE:", count, "videos embedded ->", OUT, "size:", os.path.getsize(OUT), "bytes")
