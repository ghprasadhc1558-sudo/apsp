import urllib.request
import urllib.parse
import json
import http.cookiejar
import os

BASE_URL = "http://127.0.0.1:5000"
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def login():
    print("Logging in...")
    url = f"{BASE_URL}/admin/login"
    data = urllib.parse.urlencode({"username": "admin", "password": "admin123"}).encode()
    try:
        with opener.open(url, data=data) as response:
            if response.getcode() == 200:
                print("Login OK")
                return True
            else:
                print(f"Login Failed: {response.getcode()}")
                return False
    except Exception as e:
        print(f"Login Error: {e}")
        return False

def test_services():
    print("\n--- Services Test ---")
    url = f"{BASE_URL}/admin/api/services"
    
    # Add Service
    data = json.dumps({"title": "Test Svc Lib", "url": "http://lib.com", "description": "Desc"}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with opener.open(req) as response:
            res_json = json.loads(response.read().decode())
            print("Add Service: OK")
            svc_id = res_json['service']['id']
    except Exception as e:
        print(f"Add Service Error: {e}")
        return

    # List Services
    try:
        with opener.open(url) as response:
            res_json = json.loads(response.read().decode())
            found = any(s['title'] == 'Test Svc Lib' for s in res_json.get('services', []))
            if found:
                print("List Services: OK")
            else:
                print("List Services: FAIL")
    except Exception as e:
        print(f"List Services Error: {e}")

    # Delete Service
    if svc_id:
        del_url = f"{url}/{svc_id}"
        req = urllib.request.Request(del_url, method='DELETE')
        try:
            with opener.open(req) as response:
                print("Delete Service: OK")
        except Exception as e:
            print(f"Delete Service Error: {e}")

def test_events_multipart():
    print("\n--- Events Test ---")
    url = f"{BASE_URL}/admin/api/events"
    
    # Create dummy PDF
    filename = "test_urllib.pdf"
    with open(filename, "wb") as f:
        f.write(b"dummy pdf content")

    boundary = '---BOUNDARY---'
    lines = []
    
    # Title
    lines.append(f'--{boundary}')
    lines.append('Content-Disposition: form-data; name="title"')
    lines.append('')
    lines.append('Test Event Urllib')
    
    # Description
    lines.append(f'--{boundary}')
    lines.append('Content-Disposition: form-data; name="description"')
    lines.append('')
    lines.append('Description Lib')

    # File
    lines.append(f'--{boundary}')
    lines.append(f'Content-Disposition: form-data; name="pdf"; filename="{filename}"')
    lines.append('Content-Type: application/pdf')
    lines.append('')
    lines.append('dummy pdf content')
    
    lines.append(f'--{boundary}--')
    lines.append('')
    
    body = '\r\n'.join(lines).encode()
    
    req = urllib.request.Request(url, data=body, headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}, method='POST')
    
    try:
        with opener.open(req) as response:
            res_json = json.loads(response.read().decode())
            print("Add Event: OK")
            evt_id = res_json['event']['id'] # Assuming API returns {event: {id: ...}}
            # If API returns success message but not event object, we might need to fetch list to find ID. 
            # In routes.py: return jsonify({'success': True, 'message': 'Event added successfully', 'event': event.to_dict()})
            # So it should return event.
    except Exception as e:
        print(f"Add Event Error: {e}")
        os.remove(filename)
        return

    os.remove(filename)
    
    # List Events
    try:
        with opener.open(url) as response:
            res_json = json.loads(response.read().decode())
            events = res_json.get('events', [])
            target = next((e for e in events if e['title'] == 'Test Event Urllib'), None)
            if target:
                print("List Events: OK")
                if target.get('pdf_file'):
                     print("Event PDF: OK")
                else:
                     print("Event PDF: MISSING")
            else:
                print("List Events: FAIL")
    except Exception as e:
        print(f"List Events Error: {e}")

    # Delete Event
    if evt_id:
        del_url = f"{url}/{evt_id}"
        req = urllib.request.Request(del_url, method='DELETE')
        try:
            with opener.open(req) as response:
                print("Delete Event: OK")
        except Exception as e:
             print(f"Delete Event Error: {e}")

if __name__ == "__main__":
    if login():
        test_services()
        test_events_multipart()
