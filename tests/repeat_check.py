"""R-Q20 반복 점검: 화면에 보이는 설명 문장(층위 문장·흐름 연결 문구)이 여러 곳에 그대로 반복되는지 센다.
같은 근거 문장(claim)을 여러 이야기가 인용하는 것은 정상 — 여기서는 '사이트가 쓴 설명 문장'의 복붙만 본다."""
import json, sys, collections

s = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'data/seed.json'))
places = collections.defaultdict(set)


def walk(x, where):
    if isinstance(x, dict):
        if 'layer' in x and 'text' in x and isinstance(x['text'], str):
            places[x['text'].strip()].add(where)
        for v in x.values():
            walk(v, where)
    elif isinstance(x, list):
        for v in x:
            walk(v, where)


for t in s['topics']['topics']:
    walk(t, 'topic:' + t['id'])
for f in s['flows']['flows']:
    walk(f, 'flow:' + f['id'])
    for b in f['bridges']:
        places[b['note'].strip()].add('flow:' + f['id'])
for f in s['tastes']['flows']:
    walk(f, 'taste:' + f['id'])
for i in s['industries']['industries']:
    walk(i, 'industry:' + i['id'])
for k, v in s['stories']['stories'].items():
    walk(v, 'story:' + k)

dups = {t: w for t, w in places.items() if len(w) >= 2 and len(t) >= 25}
print(f'설명 문장 {len(places)}개 중 두 곳 이상에 그대로 나오는 문장 {len(dups)}개')
for t, w in sorted(dups.items(), key=lambda x: -len(x[1]))[:30]:
    print(f'  [{len(w)}곳] {t[:70]} … {sorted(w)}')
sys.exit(0)
