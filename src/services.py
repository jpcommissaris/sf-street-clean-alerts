import requests
from flask import current_app
from utils import formatted_zone
import time
from shapely.geometry import LineString, Point
import json
import os
from datetime import datetime

API_URL = "https://data.sfgov.org/resource/yhqp-riqs.json?$select=cnn,corridor,blockside,fromhour,tohour,week1,week2,week3,week4,week5,weekday,line"

BATCH_SIZE = 5000
CACHE_TTL = 7 * 24 * 60 * 60  # 1 week in seconds

YARD_TO_DEGREES = 0.00000914399  # shapely deg per yard

type ApiData = dict[str, dict]
type StoredData = tuple[float, ApiData]

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data-gignore")
os.makedirs(DATA_DIR, exist_ok=True)
DATA_PATH = f"{DATA_DIR}/sfmta_street_cleaning.json"

KEEP_FIELDS = [
    "cnn",
    "corridor",
    "blockside",
    "line",
]


# makes an assumption that this is unique
# makes assumption that per weekday only one instance: (the dataset sometimes has more than one per weekday (IDK WHY), but hours are always the same so its mergeable.)
def getKey(cnn: str, blockside: str):
    return f"{cnn}-{blockside}"


def fetch_all_records():
    all_data = []
    offset = 0
    while True:
        params = {"$limit": BATCH_SIZE, "$offset": offset}
        resp = requests.get(API_URL, params=params, timeout=60)
        resp.raise_for_status()
        chunk = resp.json()
        print("Chunk received")
        if not chunk:
            break
        all_data.extend(chunk)
        offset += BATCH_SIZE

    data_map = {}
    for row in all_data:
        cnn: str = row.get("cnn", None)
        blockside: str = row.get("blockside", None)
        weekday: str = row.get("weekday", None)
        fromHour: str = row.get("fromhour", None)
        toHour: str = row.get("tohour", None)
        if cnn and blockside and weekday and weekday != "Holiday":
            key = getKey(cnn, blockside)
            # Add key to map if DNE
            if key not in data_map:
                filtered_row = {k: v for k, v in row.items() if k in KEEP_FIELDS}
                data_map[key] = filtered_row

            # Add weekday to map if DNE
            if weekday not in data_map[key]:
                data_map[key][weekday] = []

            # Add data point
            data_map[key][weekday].append(
                {
                    "weeks": [
                        int(row["week1"]),
                        int(row["week2"]),
                        int(row["week3"]),
                        int(row["week4"]),
                        int(row["week5"]),
                    ],
                    "fromHour": fromHour,
                    "toHour": toHour,
                }
            )
            print(data_map[key][weekday])

    return data_map


def sync_data():
    data = {}
    last_fetched = 0
    now = time.time()
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            fromLoad: StoredData = json.load(f)
            (last_fetched, data) = fromLoad

    if len(data) == 0 or (now - last_fetched) > CACHE_TTL:
        print("Refreshing SFMTA dataset from source...")
        data: ApiData = fetch_all_records()
        print("Done with refresh")
        with open(DATA_PATH, "w") as f:
            json.dump((now, data), f, indent=2)
    return data


def find_nearest_blocks(blocks, user_lat, user_lon, n=3, max_yards=100):
    pt = Point(user_lon, user_lat)
    dists = []
    for key, block in blocks.items():
        if "line" not in block:
            continue
        line = LineString(block["line"]["coordinates"])
        dist = pt.distance(line)
        dists.append((dist, key, block))
    dists.sort()  # sort by distance
    # Convert yards to degrees (approx.)
    max_degrees = YARD_TO_DEGREES * max_yards
    # Filter to within max_degrees, return up to n
    return [x for x in dists if x[0] <= max_degrees][:n]


def safe_get(lst, idx, default=None):
    return lst[idx] if 0 <= idx < len(lst) else default


def get_street_cleaning_info(lat: float, lon: float):
    # try:
    # -- Make request & parse output
    data = sync_data()
    zones_data = find_nearest_blocks(data, lat, lon)

    print(zones_data)

    all_cleanings_string = ""  # todo

    next_cleaning = []
    now = datetime.now()
    for zone_data in zones_data:
        dis, id, zone = zone_data
        next_cleaning.append(formatted_zone(zone, now))

    return {
        # return 4 closest cleaning points
        "r": "Hello - Closets cleans in order based on location input",
        "all_cleanings_string": all_cleanings_string,
        "clean1": safe_get(next_cleaning, 0),  # isoDate + formatted string
        "clean2": safe_get(next_cleaning, 1),
        "clean3": safe_get(next_cleaning, 2),
        "clean4": safe_get(next_cleaning, 3),
        # "raw": zones_data,
    }


# except Exception as e:
#     print("Request failed: ", e)
#     return None
