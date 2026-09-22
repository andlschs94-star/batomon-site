import json, pathlib, urllib.request, time, sys, re
ROOT=pathlib.Path(__file__).resolve().parents[1]
data=json.loads((ROOT/"characters.json").read_text(encoding="utf-8"))
chars=data["characters"]
out=ROOT/"assets"/"batomon"; out.mkdir(parents=True,exist_ok=True)
failed=[]
def slug(s): return re.sub(r'[^a-z0-9]+','-',str(s).lower()).strip('-')
for n,c in enumerate(chars,1):
    en=c.get("officialName") or c.get("name_en") or c.get("name") or ""
    s=slug(en)
    url=f"https://batomon.com/game/25377295/monster/{s}.png"
    path=out/f"{s}.png"
    if path.exists() and path.stat().st_size>100:
        print(f"[{n}/{len(chars)}] exists {en}"); continue
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 Batomon-Site-Asset-Fetcher"})
    ok=False
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=20) as r: blob=r.read()
            if len(blob)<100: raise ValueError("empty image")
            path.write_bytes(blob); print(f"[{n}/{len(chars)}] fetched {en} ({len(blob)} bytes)"); ok=True; break
        except Exception as ex:
            print(" retry",attempt+1,ex); time.sleep(1)
    if not ok: failed.append((en,url))
if failed:
    print("FAILED")
    for x in failed: print("-",x)
    sys.exit(1)
print(f"All {len(chars)} official Batomon images are present.")
