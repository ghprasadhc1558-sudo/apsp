import requests
import os

BASE_URL = "http://127.0.0.1:5000"
SESSION = requests.Session()

def login():
    try:
        print("Logging in...")
        data = {
            "username": "admin", 
            "password": "admin123"
        }
        res = requests.post(f"{BASE_URL}/admin/login", data=data)
        if res.status_code == 200:
            print("Login successful")
            return True
        else:
            print(f"Login failed: {res.status_code}")
            return False
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def test_services():
    try:
        print("\nTesting Services...")
        data = {
            "title": "Test Service Script",
            "url": "https://script-test.com",
            "description": "Created by validation script"
        }
        res = requests.post(f"{BASE_URL}/admin/api/services", json=data)
        if res.status_code == 200:
            print("Service added successfully")
            service_id = res.json().get("service", {}).get("id")
        else:
            print(f"Failed to add service: {res.text}")
            return

        res = requests.get(f"{BASE_URL}/admin/api/services")
        if res.status_code == 200:
            services = res.json().get("services", [])
            found = False
            for s in services:
                if s["title"] == "Test Service Script":
                    found = True
                    print("Service found in list")
                    break
            if not found:
                print("Service NOT found in list")
        
        if service_id:
            res = requests.delete(f"{BASE_URL}/admin/api/services/{service_id}")
            if res.status_code == 200:
                print("Service deleted successfully")
            else:
                print(f"Failed to delete service: {res.text}")
    except Exception as e:
        print(f"Service test failed: {e}")

def test_events():
    try:
        print("\nTesting Events...")
        with open("test.pdf", "wb") as f:
            f.write(b"%PDF-1.4 dummy content")

        data = {"title": "Test Event Script", "description": "Event with PDF"}
        files = {"pdf": open("test.pdf", "rb")}
        
        res = requests.post(f"{BASE_URL}/admin/api/events", data=data, files=files)
        if res.status_code == 200:
            print("Event added successfully")
            event_id = res.json().get("event", {}).get("id")
        else:
            print(f"Failed to add event: {res.text}")
            files["pdf"].close()
            os.remove("test.pdf")
            return

        files["pdf"].close()
        os.remove("test.pdf")

        res = requests.get(f"{BASE_URL}/admin/api/events")
        if res.status_code == 200:
            events = res.json().get("events", [])
            found = False
            for e in events:
                if e["title"] == "Test Event Script":
                    found = True
                    print("Event found in list")
                    if e.get("pdf_file"):
                        print("Event has PDF file attached")
                    else:
                        print("Event MISSING PDF file")
                    break
            if not found:
                print("Event NOT found in list")

        if event_id:
            res = requests.delete(f"{BASE_URL}/admin/api/events/{event_id}")
            if res.status_code == 200:
                print("Event deleted successfully")
            else:
                print(f"Failed to delete event: {res.text}")

    except Exception as e:
        print(f"Event test failed: {e}")

if __name__ == "__main__":
    if login(): # Login is not actually sessions based unless cookies are preserved, but for this simple app it might not matter if API routes are open or if session cookie is handled.
        # Wait, the login sets a session cookie. requests.Session() handles cookies.
        pass

    # Re-writing verify script to use session properly.
    s = requests.Session()
    
    print("Logging in with Session...")
    res = s.post(f"{BASE_URL}/admin/login", data={"username": "admin", "password": "admin123"})
    if res.status_code == 200:
        print("Login OK")
    else:
        print("Login FAIL")
        exit()

    # Services Test
    print("\n--- Services Test ---")
    res = s.post(f"{BASE_URL}/admin/api/services", json={"title": "Test Svc", "url": "http://test.com", "description": "Desc"})
    if res.status_code == 200:
        print("Add Service: OK")
        svc_id = res.json()['service']['id']
        
        res = s.get(f"{BASE_URL}/admin/api/services")
        if "Test Svc" in res.text:
            print("List Services: OK")
        else:
            print("List Services: FAIL")
            
        res = s.delete(f"{BASE_URL}/admin/api/services/{svc_id}")
        if res.status_code == 200:
            print("Delete Service: OK")
        else:
            print("Delete Service: FAIL")
    else:
        print(f"Add Service: FAIL {res.text}")

    # Events Test
    print("\n--- Events Test ---")
    with open("test_dummy.pdf", "wb") as f:
        f.write(b"dummy pdf content")
    
    files = {'pdf': ('test_dummy.pdf', open('test_dummy.pdf', 'rb'), 'application/pdf')}
    data = {'title': 'Test Event PDF', 'description': 'Testing upload'}
    
    res = s.post(f"{BASE_URL}/admin/api/events", data=data, files=files)
    if res.status_code == 200:
        print("Add Event: OK")
        evt_id = res.json()['event']['id']
        
        res = s.get(f"{BASE_URL}/admin/api/events")
        if "Test Event PDF" in res.text:
            print("List Events: OK")
        else:
            print("List Events: FAIL")

        res = s.delete(f"{BASE_URL}/admin/api/events/{evt_id}")
        if res.status_code == 200:
            print("Delete Event: OK")
        else:
            print("Delete Event: FAIL")
            
    else:
        print(f"Add Event: FAIL {res.text}")
    
    files['pdf'][1].close()
    os.remove("test_dummy.pdf")
