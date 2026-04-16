import urllib.request
import urllib.error
import sys

BASE_URL = "http://127.0.0.1:5000"

urls_to_check = [
    "/",
    "/battalions",
    "/contacts",
    "/about",
    "/sdrf",
    "/sdrf/operations",
    "/sdrf/training",
    "/events",
    "/services",
    "/announcements",
    "/gallery",
    "/admin/login",
]

# Add battalion pages
for i in range(1, 20):
    urls_to_check.append(f"/battalion/{i}")

print("Starting crawl...")
for path in urls_to_check:
    url = f"{BASE_URL}{path}"
    try:
        with urllib.request.urlopen(url) as response:
            print(f"[200] {path}")
    except urllib.error.HTTPError as e:
        print(f"[{e.code}] {path}")
    except urllib.error.URLError as e:
        print(f"[ERROR] {path}: {e.reason}")
    except Exception as e:
        print(f"[ERROR] {path}: {e}")

print("Crawl complete.")
