#!/usr/bin/env python3
"""
Online Persian word lookup. Use when the model is unsure whether a word
is real Persian, or to fetch a definition / part of speech to disambiguate.

Sources, in order:
  1. fa.wiktionary.org   — Persian Wiktionary (definitions in Persian)
  2. en.wiktionary.org   — English Wiktionary (definitions in English)
  3. MyMemory translation API — fallback for translation only

Caches successful results to ~/.cache/persian-skill/lookup.json so repeat
lookups during a session are free. Cache TTL: 30 days.

Usage:
    python3 lookup.py کتاب
    python3 lookup.py --json کتاب
    python3 lookup.py --translate "good morning"   # en -> fa
    python3 lookup.py --translate-from-fa صبح بخیر # fa -> en

Exits 0 on found, 1 on not-found, 2 on network error.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

CACHE_DIR = Path(os.path.expanduser("~/.cache/persian-skill"))
CACHE_FILE = CACHE_DIR / "lookup.json"
CACHE_TTL_SEC = 30 * 24 * 3600
TIMEOUT = 6  # seconds — agents shouldn't block long on a lookup
USER_AGENT = "persian-language-skill/1.0 (educational; +github)"


# ---- Cache ------------------------------------------------------------------

def _load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_cache(cache: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _cache_get(key: str) -> dict | None:
    cache = _load_cache()
    entry = cache.get(key)
    if not entry:
        return None
    if time.time() - entry.get("_ts", 0) > CACHE_TTL_SEC:
        return None
    return entry


def _cache_put(key: str, value: dict) -> None:
    cache = _load_cache()
    cache[key] = {**value, "_ts": time.time()}
    _save_cache(cache)


# ---- HTTP -------------------------------------------------------------------

def _http_get_json(url: str) -> dict | None:
    """GET a URL and parse the JSON body. Treats 404 as a normal response
    (Wiktionary returns 404 with a JSON body for missing pages)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            try:
                return json.loads(e.read().decode("utf-8"))
            except Exception:
                return None
        return None
    except Exception:
        return None


# ---- Sources ----------------------------------------------------------------

def lookup_wiktionary(word: str, lang: str = "fa") -> dict | None:
    """Query Wiktionary's REST page summary endpoint.
    Returns {source, word, exists, extract, url} or None on error."""
    title = urllib.parse.quote(word)
    url = f"https://{lang}.wiktionary.org/api/rest_v1/page/summary/{title}"
    data = _http_get_json(url)
    if data is None:
        return None
    if data.get("type") == "https://mediawiki.org/wiki/HyperSwitch/errors/not_found":
        return {"source": f"{lang}.wiktionary", "word": word,
                "exists": False, "extract": None,
                "url": f"https://{lang}.wiktionary.org/wiki/{title}"}
    return {
        "source": f"{lang}.wiktionary",
        "word": word,
        "exists": True,
        "extract": data.get("extract"),
        "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
    }


def translate_mymemory(text: str, src: str, tgt: str) -> dict | None:
    """Free MyMemory translation. No key needed for low-volume use."""
    q = urllib.parse.quote(text)
    url = (f"https://api.mymemory.translated.net/get"
           f"?q={q}&langpair={src}|{tgt}")
    data = _http_get_json(url)
    if data is None:
        return None
    translation = (data.get("responseData") or {}).get("translatedText")
    if not translation:
        return None
    return {"source": "mymemory", "src": src, "tgt": tgt,
            "input": text, "translation": translation}


# ---- Driver -----------------------------------------------------------------

def lookup_word(word: str) -> dict:
    cache_key = f"word:{word}"
    cached = _cache_get(cache_key)
    if cached:
        return {**cached, "cached": True}

    # Try Persian Wiktionary first; fall back to English.
    for lang in ("fa", "en"):
        result = lookup_wiktionary(word, lang)
        if result and result.get("exists"):
            _cache_put(cache_key, result)
            return {**result, "cached": False}

    return {"source": None, "word": word, "exists": False,
            "extract": None, "url": None, "cached": False}


def translate(text: str, src: str, tgt: str) -> dict | None:
    cache_key = f"trans:{src}:{tgt}:{text}"
    cached = _cache_get(cache_key)
    if cached:
        return {**cached, "cached": True}
    result = translate_mymemory(text, src, tgt)
    if result:
        _cache_put(cache_key, result)
        return {**result, "cached": False}
    return None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("query", nargs="+", help="Word or phrase to look up")
    p.add_argument("--translate", action="store_true",
                   help="Translate from English to Persian")
    p.add_argument("--translate-from-fa", action="store_true",
                   help="Translate from Persian to English")
    p.add_argument("--json", action="store_true",
                   help="Emit raw JSON (default: human-readable)")
    args = p.parse_args()

    text = " ".join(args.query)

    if args.translate or args.translate_from_fa:
        src, tgt = ("en", "fa") if args.translate else ("fa", "en")
        result = translate(text, src, tgt)
        if result is None:
            print(json.dumps({"error": "network or no result"},
                             ensure_ascii=False))
            return 2
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(f"{src}→{tgt}: {result['translation']}")
            print(f"(source: {result['source']}"
                  f"{', cached' if result.get('cached') else ''})")
        return 0

    result = lookup_word(text)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        if result["exists"]:
            print(f"✓ '{text}' found in {result['source']}"
                  f"{' (cached)' if result.get('cached') else ''}")
            if result.get("extract"):
                print()
                print(result["extract"])
            if result.get("url"):
                print(f"\n{result['url']}")
        else:
            print(f"✗ '{text}' not found in fa.wiktionary or en.wiktionary")
            print("This does not prove the word is wrong — Wiktionary is "
                  "incomplete. Cross-check manually if uncertain.")
    return 0 if result.get("exists") else 1


if __name__ == "__main__":
    sys.exit(main())
