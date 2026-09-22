import json, pathlib, urllib.request, time, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
data=json.loads((ROOT/"events.json").read_text(encoding="utf-8"))
events=data["events"]
out=ROOT/"assets"/"events"; out.mkdir(parents=True,exist_ok=True)
failed=[]
for n,e in enumerate(events,1):
    slug=e["id"]; url=e.get("image_url") or f"https://batomon.com/game/25377295/event/{slug}.png"
    path=out/f"{slug}.png"
    if path.exists() and path.stat().st_size>100:
        print(f"[{n}/{len(events)}] exists {e['name_en']}"); continue
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 Batomon-Site-Asset-Fetcher"})
    ok=False
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=20) as r: blob=r.read()
            if len(blob)<100: raise ValueError("empty image")
            path.write_bytes(blob); print(f"[{n}/{len(events)}] fetched {e['name_en']} ({len(blob)} bytes)"); ok=True; break
        except Exception as ex:
            print(" retry",attempt+1,ex); time.sleep(1)
    if not ok: failed.append((e["name_en"],url))
if failed:
    print("FAILED")
    for x in failed: print("-",x)
    sys.exit(1)
print(f"All {len(events)} event images are present.")
