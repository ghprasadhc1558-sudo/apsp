
import urllib.request
import urllib.parse
import json
import http.cookiejar

BASE_URL = "http://127.0.0.1:5000"
USERNAME = "battalion14_admin"
OLD_PASSWORD = "apsp@2024"
NEW_PASSWORD = "NewPass123!"

# Setup cookie jar
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def login(username, password):
    print(f"Attempting login with {username}...")
    login_url = f"{BASE_URL}/battalion/14/login"
    data = urllib.parse.urlencode({"username": username, "password": password}).encode()
    try:
        req = urllib.request.Request(login_url, data=data)
        res = opener.open(req)
        content = res.read().decode('utf-8')
        
        # Check for success indicators
        if "Logout" in content or "Edit Battalion Information" in content:
            print("Login success confirmed by content.")
            return True
        elif "/battalion/14" in res.geturl():
            # If redirected back to battalion page, we need to check if we are logged in
            # usually flash messages or logout link
            if "Logout" in content:
                 print("Login success confirmed by redirect and content.")
                 return True
            else:
                 print("Redirected but Logout link not found. Login might have failed.")
                 # Check for error flash
                 if "Invalid username or password" in content:
                     print("Login failed: Invalid credentials.")
                 return False
        else:
            print("Login failed.")
            return False
    except Exception as e:
        print(f"Login error: {e}")
        return False

def change_password(current, new):
    print(f"Changing password...")
    api_url = f"{BASE_URL}/api/battalion-admin/change-password"
    data = json.dumps({
        "current_password": current,
        "new_password": new
    }).encode('utf-8')
    
    req = urllib.request.Request(api_url, data=data, headers={'Content-Type': 'application/json'})
    try:
        res = opener.open(req)
        response_data = json.loads(res.read().decode('utf-8'))
        print(f"Response: {response_data}")
        return response_data.get('success', False)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"Error changing password: {e}")
        return False

def verify_fix():
    print("--- START VERIFICATION ---")
    
    # 1. Login with old password
    if not login(USERNAME, OLD_PASSWORD):
        print("Initial login failed. Aborting.")
        return

    # 2. Change Password
    if change_password(OLD_PASSWORD, NEW_PASSWORD):
        print("Password change reported success.")
    else:
        print("Password change failed.")
        return

    # 3. Verify old password fails (requires clearing sessions or logging out)
    # To properly test, we should logout first
    print("Logging out...")
    try:
        opener.open(f"{BASE_URL}/logout")
    except:
        pass
    
    print("Verifying old password fails...")
    if login(USERNAME, OLD_PASSWORD):
        print("ERROR: Old password still works!")
        return
    else:
        print("Old password rejected as expected.")

    # 4. Verify new password works
    print(f"Verifying new password...")
    if login(USERNAME, NEW_PASSWORD):
        print("New password login successful.")
    else:
        print("New password login FAILED.")
        return

    # 5. Revert Password
    print("Reverting password...")
    if change_password(NEW_PASSWORD, OLD_PASSWORD):
        print("Password reverted successfully.")
    else:
        print("Failed to revert password!")

if __name__ == "__main__":
    verify_fix()
