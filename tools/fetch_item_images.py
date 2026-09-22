import json, pathlib, urllib.request, time, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / 'items.json'
OUT = ROOT / 'assets' / 'items'
OUT.mkdir(parents=True, exist_ok=True)
data=json.loads(DATA.read_text(encoding='utf-8'))
items=data.get('items',data if isinstance(data,list) else [])
failed=[]
for i,item in enumerate(items,1):
    url=item.get('image_url'); local=item.get('image_local')
    if not url or not local:
        failed.append((item.get('name_en'),'missing url/path')); continue
    path=ROOT/local; path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and path.stat().st_size>100:
        print(f'[{i}/{len(items)}] exists {item.get("name_en")}'); continue
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 Batomon-Site-Asset-Fetcher'})
    ok=False
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=20) as r: blob=r.read()
            if not blob.startswith(b'\x89PNG'): raise ValueError('not PNG')
            path.write_bytes(blob); print(f'[{i}/{len(items)}] fetched {item.get("name_en")} ({len(blob)} bytes)'); ok=True; break
        except Exception as e:
            print(f' retry {attempt+1}: {e}'); time.sleep(1)
    if not ok: failed.append((item.get('name_en'),url))
if failed:
    print('\nFAILED:')
    for name,detail in failed: print('-',name,detail)
    sys.exit(1)
print(f'\nAll {len(items)} item images are present.')
