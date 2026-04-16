"""Test battalion content API endpoints"""
import requests
from requests.auth import HTTPBasicAuth

# Test configuration
BASE_URL = 'http://localhost:5000'
USERNAME = 'battalion1_admin'  # Battalion 1 admin
PASSWORD = 'apsp2024'  # Default password
BATTALION_ID = 1

print("\n=== Testing Battalion Content API Endpoints ===\n")

# Create a session to maintain cookies
session = requests.Session()

# Step 1: Login
print("1. Testing Login...")
login_response = session.post(
    f'{BASE_URL}/battalion-admin-login',
    data={'username': USERNAME, 'password': PASSWORD},
    allow_redirects=False
)
if login_response.status_code in [200, 302]:
    print("   ✓ Login successful")
else:
    print(f"   ✗ Login failed with status {login_response.status_code}")
    print(f"   Response: {login_response.text[:200]}")
    exit(1)

# Step 2: Test Events List
print("\n2. Testing Events List API...")
events_response = session.get(f'{BASE_URL}/api/battalion/events/list?battalion_id={BATTALION_ID}')
print(f"   Status Code: {events_response.status_code}")
if events_response.status_code == 200:
    events_data = events_response.json()
    print(f"   ✓ Events API working")
    print(f"   Found {len(events_data.get('events', []))} events")
    if events_data.get('events'):
        for event in events_data['events'][:2]:
            print(f"     - {event['title']} ({event['date']})")
else:
    print(f"   ✗ Events API failed")
    print(f"   Response: {events_response.text[:200]}")

# Step 3: Test Announcements List
print("\n3. Testing Announcements List API...")
announcements_response = session.get(f'{BASE_URL}/api/battalion/announcements/list?battalion_id={BATTALION_ID}')
print(f"   Status Code: {announcements_response.status_code}")
if announcements_response.status_code == 200:
    announcements_data = announcements_response.json()
    print(f"   ✓ Announcements API working")
    print(f"   Found {len(announcements_data.get('announcements', []))} announcements")
    if announcements_data.get('announcements'):
        for ann in announcements_data['announcements'][:2]:
            print(f"     - {ann['title']} ({ann['date']})")
else:
    print(f"   ✗ Announcements API failed")
    print(f"   Response: {announcements_response.text[:200]}")

# Step 4: Test Gallery List
print("\n4. Testing Gallery List API...")
gallery_response = session.get(f'{BASE_URL}/api/battalion/gallery/list?battalion_id={BATTALION_ID}')
print(f"   Status Code: {gallery_response.status_code}")
if gallery_response.status_code == 200:
    gallery_data = gallery_response.json()
    print(f"   ✓ Gallery API working")
    print(f"   Found {len(gallery_data.get('gallery', []))} images")
    if gallery_data.get('gallery'):
        for img in gallery_data['gallery'][:2]:
            print(f"     - {img.get('caption', 'No caption')}")
else:
    print(f"   ✗ Gallery API failed")
    print(f"   Response: {gallery_response.text[:200]}")

# Step 5: Test Edit Page Access
print("\n5. Testing Edit Battalion Page Access...")
edit_page_response = session.get(f'{BASE_URL}/battalion-admin-dashboard/{BATTALION_ID}')
print(f"   Status Code: {edit_page_response.status_code}")
if edit_page_response.status_code == 200:
    print("   ✓ Edit page accessible")
    # Check if the page contains our new sections
    page_content = edit_page_response.text
    if 'Battalion History' in page_content:
        print("   ✓ Battalion History section found")
    if 'Events Management' in page_content:
        print("   ✓ Events Management section found")
    if 'Announcements Management' in page_content:
        print("   ✓ Announcements Management section found")
    if 'Gallery Management' in page_content:
        print("   ✓ Gallery Management section found")
else:
    print(f"   ✗ Edit page not accessible")

print("\n=== Test Complete ===\n")
print("Summary:")
print("- Login to battalion admin: http://localhost:5000/battalion-admin-login")
print("- Username: battalion1_admin")
print("- Password: apsp2024")
print("- Edit page with all content management sections should be visible")
print("\nOpen browser and check the JavaScript console for any errors!")
print("The page should load events, announcements, and gallery automatically.")
