"""출처 링크 전수 점검 (GitHub Actions에서 실행). 결과: link_report.json
분류: ok(2xx·3xx) / blocked(401·403·429 — 사이트가 자동 접속을 막음, 사람이 열면 보통 열림) / broken(404·410·DNS 실패) / error(시간 초과 등)
"""
import json, sys, concurrent.futures as cf, datetime
import requests

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8"}


def check(src):
    url = src.get("url")
    r = {"id": src["id"], "url": url, "publisher": src.get("publisher")}
    if not url or not url.startswith("http"):
        r.update(status=None, kind="no-url")
        return r
    try:
        resp = requests.get(url, headers=UA, timeout=25, allow_redirects=True, stream=True)
        code = resp.status_code
        resp.close()
        r.update(status=code, final=resp.url)
        r["kind"] = "ok" if code < 400 else "blocked" if code in (401, 403, 405, 406, 429, 451, 503) else "broken" if code in (404, 410) else "error"
    except requests.exceptions.ConnectionError as e:
        r.update(status=None, kind="broken" if "Name or service" in str(e) or "NameResolution" in str(e) else "error", err=str(e)[:160])
    except Exception as e:  # noqa: BLE001
        r.update(status=None, kind="error", err=str(e)[:160])
    return r


def main(seed_path, out_path):
    seed = json.load(open(seed_path))
    srcs = seed["sources"]
    with cf.ThreadPoolExecutor(16) as ex:
        res = list(ex.map(check, srcs))
    summary = {}
    for x in res:
        summary[x["kind"]] = summary.get(x["kind"], 0) + 1
    json.dump({"checkedAt": datetime.datetime.utcnow().isoformat() + "Z", "total": len(res), "summary": summary,
               "results": sorted(res, key=lambda x: (x["kind"] != "broken", x["kind"] != "error", x["kind"] != "blocked", x["id"]))},
              open(out_path, "w"), ensure_ascii=False, indent=1)
    print(summary)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
