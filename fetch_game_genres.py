"""
Fetches Steam genres for the 1584 filtered games and saves game_genres.json.

Strategy:
  1. Steam Store Search API  →  finds appid by title
  2. Steam appdetails API    →  fetches genres for that appid
  3. SteamSpy tags API       →  fallback if genres list is empty

Output: game_genres.json
  { "Dota 2": ["Free to Play", "Strategy"], ... }

Empty list [] means the game was not found or had no genre data.
Resume-safe: skips games already present in game_genres.json.

Usage:
    python3 fetch_game_genres.py
"""

import json
import time
import urllib.parse
import requests
import pandas as pd
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
DATA_PATH          = "steam-200k.csv"
OUTPUT_PATH        = "game_genres.json"
DELAY_SEC          = 1.5        # polite rate limiting
MIN_GAMES_PER_USER = 3
MIN_USERS_PER_GAME = 5

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0 (compatible; genre-fetcher/1.0)"})

# ── Step 1: replicate notebook filtering → exact same 1584 titles ─────────────
print("Loading dataset...")
df = pd.read_csv(DATA_PATH, header=None,
                 names=["user_id", "game_title", "behavior", "value", "empty"])
df = df[df["behavior"] == "play"].dropna()

user_counts = df.groupby("user_id")["game_title"].count()
game_counts = df.groupby("game_title")["user_id"].count()

df = df[df["user_id"].isin(user_counts[user_counts >= MIN_GAMES_PER_USER].index)]
df = df[df["game_title"].isin(game_counts[game_counts >= MIN_USERS_PER_GAME].index)]

game_titles = sorted(df["game_title"].unique().tolist())
print(f"Unique games after filtering: {len(game_titles)}")

# ── Step 2: resume support ────────────────────────────────────────────────────
if Path(OUTPUT_PATH).exists():
    with open(OUTPUT_PATH) as f:
        genres_map = json.load(f)
    print(f"Resuming — {len(genres_map)} games already saved")
else:
    genres_map = {}

remaining = [t for t in game_titles if t not in genres_map]
print(f"Games to fetch: {len(remaining)}")

if not remaining:
    print("All games already fetched.")
    raise SystemExit(0)

# ── Helpers ───────────────────────────────────────────────────────────────────

def search_appid(title: str) -> int | None:
    """Search Steam store for a game title, return appid if exact match found."""
    url = ("https://store.steampowered.com/api/storesearch/"
           f"?term={urllib.parse.quote(title)}&l=english&cc=US")
    try:
        r = SESSION.get(url, timeout=15)
        r.raise_for_status()
        items = r.json().get("items", [])
        for item in items:
            if item.get("name", "").strip().lower() == title.strip().lower():
                return item["id"]
        # If no exact match, take first result only if name is very close
        if items:
            first_name = items[0].get("name", "").strip().lower()
            if first_name == title.strip().lower():
                return items[0]["id"]
        return None
    except Exception:
        return None


def fetch_steam_genres(appid: int) -> list:
    """Fetch official Steam genres for an appid."""
    url = (f"https://store.steampowered.com/api/appdetails"
           f"?appids={appid}&filters=genres")
    try:
        r = SESSION.get(url, timeout=15)
        r.raise_for_status()
        data = r.json().get(str(appid), {})
        if not data.get("success"):
            return []
        return [g["description"]
                for g in data.get("data", {}).get("genres", [])]
    except Exception:
        return []


def fetch_steamspy_tags(appid: int) -> list:
    """Fetch SteamSpy community tags as fallback."""
    url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
    try:
        r = SESSION.get(url, timeout=15)
        r.raise_for_status()
        tags = r.json().get("tags", {})
        # tags is {tag_name: vote_count}, return top 5 by votes
        return [t for t, _ in sorted(tags.items(),
                                     key=lambda x: x[1], reverse=True)[:5]]
    except Exception:
        return []

# ── Step 3: fetch ─────────────────────────────────────────────────────────────
ok = no_match = api_fail = 0

for i, title in enumerate(remaining, 1):
    appid = search_appid(title)
    time.sleep(DELAY_SEC)

    if appid is None:
        genres_map[title] = []
        no_match += 1
    else:
        genres = fetch_steam_genres(appid)
        time.sleep(DELAY_SEC)

        if not genres:
            genres = fetch_steamspy_tags(appid)
            time.sleep(DELAY_SEC)

        genres_map[title] = genres
        if genres:
            ok += 1
        else:
            api_fail += 1

    if i % 25 == 0 or i == len(remaining):
        pct = i / len(remaining) * 100
        print(f"  [{i:4d}/{len(remaining)}] {pct:.0f}%  "
              f"ok={ok}  no_match={no_match}  api_fail={api_fail}")
        with open(OUTPUT_PATH, "w") as f:
            json.dump(genres_map, f, ensure_ascii=False, indent=2)

# ── Step 4: final save + summary ──────────────────────────────────────────────
with open(OUTPUT_PATH, "w") as f:
    json.dump(genres_map, f, ensure_ascii=False, indent=2)

with_genre = sum(1 for g in genres_map.values() if g)
total      = len(game_titles)
print(f"\nSaved → {OUTPUT_PATH}")
print(f"  Total       : {total}")
print(f"  With genres : {with_genre} ({with_genre/total*100:.0f}%)")
print(f"  Without     : {total - with_genre}")
