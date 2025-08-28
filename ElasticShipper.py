import argparse
import json
import random
import re
import time
from datetime import datetime, timezone
from typing import Dict, Any, List

import requests

FIXED_FIELDS: Dict[str, str] = {
    "Customer Name": "full_name",
    "Customer Phone (Int)": "phone_number_int",
    "Customer Address": "full_address",
    "Country": "alpha2",
    "Is Subscribed": "boolean",
    "Date Of Birth": "date_iso",
    "Music Genre": "music_genre",
    "Music Instrument": "music_instrument",
    "Music Genre Object": "music_genre",
    "Music Instrument Object": "music_instrument",
    "Artist Name": "artist_name",
    "Song Title": "song_title",
    "Album Title": "album_title",
}

def parse_interval(text: str) -> int:
    m = re.fullmatch(r"\s*(\d+)\s*([smSM]?)\s*", text)
    if not m:
        raise argparse.ArgumentTypeError("Use formats like 15s or 2m")
    v = int(m.group(1))
    return v * 60 if m.group(2).lower() == "m" else v

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    # Default to K8s Service DNS names so this works inside the cluster
    p.add_argument("--api-base", default="http://random-data-generator.elastic.svc.cluster.local:5000")
    p.add_argument("--interval", type=parse_interval, default=parse_interval("15s"))
    p.add_argument("--schema-name", default="elasticshipper")
    p.add_argument("--min-count", type=int, default=80)
    p.add_argument("--max-count", type=int, default=150)
    p.add_argument("--timeout", type=int, default=10)
    p.add_argument("--es-url", default="http://elasticsearch.elastic.svc.cluster.local:9200")
    p.add_argument("--es-index", default="elasticshipper")
    p.add_argument("--es-bulk-size", type=int, default=1000)
    p.add_argument("--es-api-key", default="X1ZpVzY1Z0JETXhrZXBLODRpU2c6eDRQRzNiRjNBWlVkaVZwVXNQV3l2dw==")
    return p

def post_schema(api_base: str, schema: Dict[str, Any], timeout: int) -> None:
    try:
        r = requests.post(f"{api_base}/schemas", json=schema, timeout=timeout)
        if r.status_code >= 400:
            print(f"[schema] {r.status_code}: {r.text[:200]}")
        else:
            print(f"[schema] {schema['name']} count={schema['count']}")
    except Exception as e:
        print(f"[schema] {e}")

def fetch_data(api_base: str, schema_name: str, timeout: int):
    try:
        r = requests.get(f"{api_base}/schemas/{schema_name}/data", timeout=timeout)
        return r.json() if r.status_code < 400 else f"[data] {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return f"[data] {e}"

def ensure_index(es_url: str, index: str, timeout: int, headers: Dict[str, str]) -> None:
    try:
        h = requests.head(f"{es_url}/{index}", timeout=timeout, headers=headers)
        if h.status_code == 200:
            return
        if h.status_code == 404:
            r = requests.put(f"{es_url}/{index}", json={}, timeout=timeout, headers=headers)
            if r.status_code < 400:
                print(f"[es] created index {index}")
            else:
                print(f"[es] create {r.status_code}: {r.text[:200]}")
        else:
            print(f"[es] HEAD /{index} -> {h.status_code}")
    except Exception as e:
        print(f"[es] ensure_index {e}")

def _ndjson(actions: List[Dict[str, Any]], docs: List[Dict[str, Any]]) -> str:
    lines = []
    for a, d in zip(actions, docs):
        lines.append(json.dumps(a))
        lines.append(json.dumps(d))
    return "\n".join(lines) + "\n"

def bulk_index(es_url: str, index: str, docs: List[Dict[str, Any]], timeout: int, bulk_size: int, headers: Dict[str, str]) -> None:
    if not docs:
        return
    url = f"{es_url}/_bulk"
    hdrs = {"Content-Type": "application/x-ndjson", **headers}
    i = 0
    total = 0
    while i < len(docs):
        chunk = docs[i:i+bulk_size]
        actions = [{"index": {"_index": index}} for _ in chunk]
        body = _ndjson(actions, chunk)
        try:
            r = requests.post(url, data=body, headers=hdrs, timeout=max(timeout, 10))
            if r.status_code == 401:
                print("[es] 401 Unauthorized")
                return
            if r.status_code >= 400:
                print(f"[es] bulk {r.status_code}: {r.text[:200]}")
                return
            resp = r.json()
            total += len(resp.get("items", []))
        except Exception as e:
            print(f"[es] bulk {e}")
            return
        i += bulk_size
    print(f"[es] indexed {total}")

def main():
    args = build_parser().parse_args()
    min_c = max(1, args.min_count)
    max_c = max(min_c, args.max_count)
    headers = {"Authorization": f"ApiKey {args.es_api_key}"} if args.es_api_key else {}

    print("Starting. Ctrl+C to stop.")
    print(f"API: {args.api_base} | interval: {args.interval}s | count: {min_c}-{max_c} | ES: {args.es_url}/{args.es_index}")

    ensure_index(args.es_url, args.es_index, args.timeout, headers)

    try:
        while True:
            count = random.randint(min_c, max_c)
            schema = {"name": args.schema_name, "count": count, "fields": FIXED_FIELDS}
            post_schema(args.api_base, schema, args.timeout)

            data = fetch_data(args.api_base, args.schema_name, args.timeout)
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                preview = data[:2] if isinstance(data, list) else data
                print(f"[{ts}] {json.dumps(preview, ensure_ascii=False)}")
            except Exception:
                print(f"[{ts}] {data}")

            if isinstance(data, list):
                now = datetime.now(timezone.utc).isoformat()
                docs = []
                for d in data:
                    if isinstance(d, dict):
                        x = dict(d)
                        # no @timestamp per your request—just ship it
                        x["@ingested_at"] = now
                        docs.append(x)
                bulk_index(args.es_url, args.es_index, docs, args.timeout, args.es_bulk_size, headers)
            else:
                print("[es] skipped: not a list")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()